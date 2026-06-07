"""
feedback_learning_engine.py

Reads memory/feedback.json, adjusts opportunity scores based on artist actions:
- applied  -> +0.5 boost to similar opportunities (same category + city)
- follow   -> +0.3 boost to similar opportunities
- maybe_later -> no change
- not_for_me  -> -1.0 to same category if dismissed 3+ times

"Similar" = matching category + city (effort_tier used as soft context).
Effort tier is bucketed from the messy difficulty field.

Writes learned weights to memory/learned_preferences.json.
Updates deploy_data/compact_opportunities.json in-place.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent.parent
FEEDBACK_PATH = ROOT / "memory" / "feedback.json"
COMPACT_PATH = ROOT / "deploy_data" / "compact_opportunities.json"
PREFS_PATH = ROOT / "memory" / "learned_preferences.json"


# ---------------------------------------------------------------------------
# Effort tier bucketing
# ---------------------------------------------------------------------------
def _effort_tier(difficulty: str) -> str:
    d = str(difficulty).lower()
    if any(x in d for x in ("very_high", "very high", "extremely", "high_friction")):
        return "very_high"
    if any(x in d for x in ("high", "medium-high", "medium_high")):
        return "high"
    if any(x in d for x in ("low", "minimal")):
        return "low"
    return "medium"


# ---------------------------------------------------------------------------
# Token helper — used by preference_rescoring_engine.py
# ---------------------------------------------------------------------------
def tokens_from_opp(opp: dict) -> list:
    """Return a list of tokens representing this opportunity's characteristics."""
    tokens = []
    if opp.get("category"):
        tokens.append(f"cat:{opp['category']}")
    if opp.get("city"):
        tokens.append(f"city:{str(opp['city']).lower()}")
    tier = _effort_tier(str(opp.get("difficulty", "")))
    tokens.append(f"effort:{tier}")
    if opp.get("exclusive_primary_bucket"):
        tokens.append(f"bucket:{opp['exclusive_primary_bucket']}")
    for tag in (opp.get("tags") or []):
        tokens.append(f"tag:{str(tag).lower()}")
    return tokens


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def run():
    # ------------------------------------------------------------------
    # 1. Load feedback
    # ------------------------------------------------------------------
    if not FEEDBACK_PATH.exists():
        print("Feedback: No feedback.json found, skipping.")
        return

    with open(FEEDBACK_PATH, encoding="utf-8") as f:
        feedback = json.load(f)

    if not feedback:
        print("Feedback: No feedback records yet, skipping.")
        return

    print(f"Feedback: Loaded {len(feedback)} feedback record(s).")

    # ------------------------------------------------------------------
    # 2. Load compact opportunities
    # ------------------------------------------------------------------
    if not COMPACT_PATH.exists():
        print("Feedback: compact_opportunities.json not found, skipping.")
        return

    with open(COMPACT_PATH, encoding="utf-8") as f:
        opps = json.load(f)

    # ------------------------------------------------------------------
    # 3. Build lookup: lowercased title/name -> index
    # ------------------------------------------------------------------
    by_id: dict = {}
    for idx, opp in enumerate(opps):
        title = str(opp.get("title", "")).lower().strip()
        name = str(opp.get("name", "")).lower().strip()
        if title:
            by_id[title] = idx
        if name and name != title:
            by_id[name] = idx

    # ------------------------------------------------------------------
    # 4. Analyse feedback records
    # ------------------------------------------------------------------
    # Accumulate deltas per opp index (deduplicated per category signal)
    score_deltas: dict = defaultdict(float)
    boosted_from: dict = defaultdict(set)  # track which categories already boosted this opp

    category_not_for_me: dict = defaultdict(int)   # category -> dismiss count
    category_applied: dict = defaultdict(float)
    category_followed: dict = defaultdict(float)

    for record in feedback:
        opp_id = str(record.get("opp_id", "")).lower().strip()
        action = str(record.get("action", "")).lower().strip()

        # Locate source opp
        src_idx = by_id.get(opp_id)
        if src_idx is None:
            # opp may have been removed or id doesn't match
            continue

        src = opps[src_idx]
        src_category = str(src.get("category", "")).strip()
        src_city = str(src.get("city", "")).strip().lower()

        if action == "not_for_me":
            category_not_for_me[src_category] += 1

        elif action in ("applied", "follow"):
            boost = 0.5 if action == "applied" else 0.3
            if action == "applied":
                category_applied[src_category] = max(category_applied[src_category], boost)
            else:
                category_followed[src_category] = max(category_followed[src_category], boost)

            # Boost all similar opps (same category + city)
            for idx, opp in enumerate(opps):
                if idx == src_idx:
                    continue
                if str(opp.get("category", "")).strip() != src_category:
                    continue
                opp_city = str(opp.get("city", "")).strip().lower()
                if opp_city != src_city:
                    continue
                # Dedup: don't boost same opp twice from same category signal
                signal_key = f"{src_category}:{action}"
                if signal_key in boosted_from[idx]:
                    continue
                boosted_from[idx].add(signal_key)
                score_deltas[idx] += boost

    # ------------------------------------------------------------------
    # 5. Determine penalised categories (3+ not_for_me dismissals)
    # ------------------------------------------------------------------
    penalised_categories: dict = {}
    for cat, count in category_not_for_me.items():
        if count >= 3:
            penalised_categories[cat] = -1.0

    # ------------------------------------------------------------------
    # 6. Write changes to opps
    # ------------------------------------------------------------------
    opps_boosted = 0
    opps_penalised = 0

    for idx, opp in enumerate(opps):
        cat = str(opp.get("category", "")).strip()
        delta = score_deltas.get(idx, 0.0)
        penalty = penalised_categories.get(cat, 0.0)

        if delta > 0:
            old_score = float(opp.get("overall_score", 0) or 0)
            new_score = min(10.0, old_score + delta)
            opp["overall_score"] = round(new_score, 4)
            opp["feedback_score_delta"] = round(delta, 4)
            opp["feedback_boosted"] = True
            opps_boosted += 1

        if penalty < 0:
            old_score = float(opp.get("overall_score", 0) or 0)
            new_score = max(0.0, old_score + penalty)
            opp["overall_score"] = round(new_score, 4)
            opp["feedback_penalty"] = True
            existing_delta = float(opp.get("feedback_score_delta", 0.0) or 0.0)
            opp["feedback_score_delta"] = round(existing_delta + penalty, 4)
            opps_penalised += 1

    # ------------------------------------------------------------------
    # 7. Write compact_opportunities.json
    # ------------------------------------------------------------------
    with open(COMPACT_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # 8. Write learned_preferences.json
    # ------------------------------------------------------------------
    prefs = {
        "last_run": datetime.now(timezone.utc).isoformat(),
        "category_boosts": {k: round(v, 4) for k, v in {**category_applied, **category_followed}.items()},
        "category_penalties": {k: round(v, 4) for k, v in penalised_categories.items()},
        "dismissed_categories": dict(category_not_for_me),
        "total_feedback_records": len(feedback),
        "opps_boosted": opps_boosted,
        "opps_penalized": opps_penalised,
    }

    with open(PREFS_PATH, "w", encoding="utf-8") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)

    print(
        f"Feedback: {len(feedback)} records | "
        f"{opps_boosted} opps boosted | "
        f"{opps_penalised} categories penalised | "
        f"Learned prefs -> {PREFS_PATH.name}"
    )


if __name__ == "__main__":
    run()
