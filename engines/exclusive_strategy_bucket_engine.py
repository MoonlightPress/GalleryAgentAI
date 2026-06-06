
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/exclusive_strategy_buckets.json"
SUPPRESSION_PATH = "memory/ibm_suppression.json"

BUCKET_ORDER = [
    "immediate_best_moves",
    "publication_targets",
    "japan_book_ecosystem",
    "stretch_targets",
    "relationship_builders",
    "research_needed",
    "low_priority",
    "reject",
]

LABELS = {
    "immediate_best_moves": "Immediate Best Moves",
    "publication_targets": "Publication Targets",
    "japan_book_ecosystem": "Japan Book / Zine Ecosystem",
    "stretch_targets": "Stretch Targets",
    "relationship_builders": "Relationship Builders",
    "research_needed": "Needs Research",
    "low_priority": "Low Priority",
    "reject": "Reject / Hide",
}


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def text_blob(opp):
    parts = []
    for key in [
        "title",
        "name",
        "organization",
        "category",
        "category_label",
        "one_sentence",
        "why_this_fits_short",
    ]:
        if opp.get(key):
            parts.append(str(opp[key]))

    for key in ["tags", "visual_fit_hits", "fit_keyword_hits"]:
        for item in opp.get(key, []) or []:
            parts.append(str(item))

    return " ".join(parts).lower()


def num(value):
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def has(text, terms):
    return any(t in text for t in terms)


_PASSED_MARKERS = ("passed", "closed", "cycle closed", "deadline was", "deadline passed")
_RECURRING_MARKERS = ("annual", "recurring", "watch", "2027", "2028", "next cycle")


def _deadline_confirmed_passed(opp):
    deadline = str(opp.get("deadline") or "").lower()
    cycle_note = str(opp.get("cycle_note") or "").lower()
    return any(m in deadline or m in cycle_note for m in _PASSED_MARKERS)


def _is_recurring(opp):
    deadline = str(opp.get("deadline") or "").lower()
    cycle_note = str(opp.get("cycle_note") or "").lower()
    return any(m in deadline or m in cycle_note for m in _RECURRING_MARKERS)


def choose_bucket(opp):
    text = text_blob(opp)
    title = str(opp.get("title") or opp.get("name") or "").lower()

    score = num(opp.get("overall_score"))
    dscore = num(opp.get("differentiated_score"))
    visual = num(opp.get("visual_fit_score"))

    if opp.get("recommendation_visibility") == "hidden":
        return "reject"

    if opp.get("verification_bucket") == "reject":
        return "reject"

    # Data-level bucket override — lets individual records pin to a bucket
    # without requiring engine changes (e.g. invitation-only publishers → stretch_targets)
    if opp.get("verification_bucket") == "stretch_targets":
        return "stretch_targets"

    # Confirmed passed deadline: recurring → watch (stretch_targets), one-off → reject
    if _deadline_confirmed_passed(opp):
        return "stretch_targets" if _is_recurring(opp) else "reject"

    # Only use dscore for low_priority check when it is actually set (>0)
    if score <= 4 or (dscore > 0 and dscore <= 4):
        return "low_priority"

    if has(title, ["facebook", "instagram", "pinterest", "tiktok", "continue reading"]):
        return "reject"

    # Tier 4 — Prestige Targets: always stretch_targets, never immediate_best_moves.
    # These are future goals for the deep-work year at ~30, not current actions.
    tier_4_terms = [
        "royal watercolour society",
        "american watercolor society",
        "cité internationale des arts",
        "cite internationale des arts",
        "asian cultural council",
        "printed matter art book fairs",
        "center for book arts",
        "offprint",
        "aperture",
        "mack",
        # torch press: invitation-only label; no submissions; Tier 4 aspirational target
        "torch press",
    ]

    # Tier 1 — Ambient Visibility: zine/bookshop ecosystem, art book fairs.
    # Also includes currently-open watercolor open calls (NWWS etc.) that are
    # actionable right now. Route to immediate or japan_book_ecosystem.
    tier_1_terms = [
        "tokyo art book fair",
        "mount zine",
        "utrecht",
        "book and sons",
        "flotsam",
        "b&b shimokitazawa",
        "bookandbeer",
        "shashasha",
        "zine fest",
        "zine fair",
        "fugensha",
        "akaaka",
        # New Tokyo relationship targets
        "sunny boy books",
        "clouds art",
        "shimokitazawa arts",
        # Recurring Tokyo zine fairs
        "zinefes",
        "zineフェス",
        "zine fest tokyo",
        # Currently-open international watercolor calls
        "northwest watercolor society",
        "cspwc",
        "canadian society of painters",
    ]

    # Tier 1-2 publication / artist-book terms
    publication_terms = [
        "artist book",
        "printed matter",
        "publication",
        "small press",
        "self publish",
        "zine",
    ]

    # Tier 2 — Networking: artist-run spaces and relationship venues
    relationship_terms = [
        "cafe",
        "bookstore",
        "shimokitazawa",
        "bonus track",
        "gallery wall",
        "community",
        "artist-run",
    ]

    # Tier 4 check is first — prestige targets never reach immediate_best_moves
    if has(text, tier_4_terms):
        return "stretch_targets"

    # Tier 1 ambient visibility — immediate or japan book ecosystem
    if has(text, tier_1_terms):
        if visual >= 3 or score >= 7.5:
            return "immediate_best_moves"
        return "japan_book_ecosystem"

    # High visual fit + publication angle → immediate
    if visual >= 5 and has(text, publication_terms):
        return "immediate_best_moves"

    # Tier 1-2 publication targets
    if has(text, publication_terms):
        return "publication_targets"

    # Tier 2 relationship / networking venues
    if has(text, relationship_terms):
        return "relationship_builders"

    if opp.get("verification_bucket") in {"research_needed", None}:
        return "research_needed"

    if score >= 8 and visual >= 1:
        return "immediate_best_moves"

    return "research_needed"


def compact(opp):
    return {
        "title": opp.get("title") or opp.get("name") or "Unknown",
        "score": opp.get("overall_score"),
        "differentiated_score": opp.get("differentiated_score"),
        "visual_fit_score": opp.get("visual_fit_score"),
        "verification_bucket": opp.get("verification_bucket", ""),
        "verification_score": opp.get("verification_score", ""),
        "why": opp.get("why_this_fits_short") or opp.get("one_sentence") or "",
        "source": (
            opp.get("source_url")
            or opp.get("official_website")
            or opp.get("source_link")
            or opp.get("submission_page")
            or ""
        ),
        "visual_hits": opp.get("visual_fit_hits", []) or [],
        "opportunity_type": opp.get("opportunity_type", "open_call"),
        "action_type": opp.get("action_type", "apply"),
        "relationship_note": opp.get("relationship_note", ""),
        "draft_introduction_ja": opp.get("draft_introduction_ja", ""),
    }


def load_suppression():
    data = load_json(SUPPRESSION_PATH, {})
    return set(data.get("suppressed", {}).keys())


def main():
    opps = load_json(OPP_PATH, [])
    suppressed = load_suppression()

    buckets = {key: [] for key in BUCKET_ORDER}

    for opp in opps:
        title = (opp.get("title") or opp.get("name") or "").strip().lower()
        org = str(opp.get("organization") or "").strip().lower()
        key = f"{title}::{org}"
        if key in suppressed:
            opp["exclusive_primary_bucket"] = "reject"
            buckets["reject"].append(compact(opp))
            continue

        bucket = choose_bucket(opp)
        opp["exclusive_primary_bucket"] = bucket
        buckets.setdefault(bucket, []).append(compact(opp))

    for key in buckets:
        buckets[key].sort(
            key=lambda x: float(x.get("differentiated_score", x.get("score", 0)) or 0),
            reverse=True,
        )

    save_json(OPP_PATH, opps)
    save_json(OUT_PATH, buckets)

    print("Built exclusive strategic buckets:")
    for key in BUCKET_ORDER:
        print(f"{LABELS[key]}: {len(buckets.get(key, []))}")


if __name__ == "__main__":
    main()
