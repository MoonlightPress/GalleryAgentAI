
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/score_sanity_report.md"

# Aggregator markers — same set used in source_type_weight_engine
AGGREGATOR_TITLE_MARKERS = [
    "一覧", "アートイベント一覧", "公募展の展覧会",
    "list of", "best of", "top 10", "all events", "event calendar",
]

JUNK_VALUES = {"unknown", "n/a", "none", "null", "not publicly listed", "unverified", ""}


def is_real(value):
    return bool(value) and str(value).strip().lower() not in JUNK_VALUES


def source_strength(opp):
    if opp.get("url_verification_status") == "ok":
        return 2
    if opp.get("source_url") or opp.get("official_website") or opp.get("source_link"):
        return 1
    return 0


def has_distinct_submission_page(opp):
    raw_sub = opp.get("submission_page") or ""
    sub     = (raw_sub[0] if isinstance(raw_sub, list) else raw_sub).strip().rstrip("/")
    src     = (opp.get("source_url") or "").strip().rstrip("/")
    official = (opp.get("official_website") or "").strip().rstrip("/")
    return is_real(sub) and sub != src and sub != official


def verification_strength(opp):
    points = 0
    if has_distinct_submission_page(opp):
        points += 1
    for key in ["deadline", "fees", "contact", "email", "contact_url"]:
        if is_real(opp.get(key)):
            points += 1
    return points


def is_aggregator_title(opp):
    title = (opp.get("title") or "").lower()
    return any(m.lower() in title for m in AGGREGATOR_TITLE_MARKERS)


def compute_cap(opp):
    """
    Return (cap, reason) — the strictest applicable cap and a short explanation.

    Cap hierarchy (lowest cap wins):
      1. Aggregator title                          → 5.5
      2. Low source_purity_score (<6)              → 7.0
      3. Missing official website AND submission   → 5.0
      4. verification_status == research_needed    → 6.5
      5. Open call type with no deadline           → score - 0.5  (floor 3.0)
      6. Legacy source/verification strength caps  (original logic)
    """
    source = source_strength(opp)
    verify = verification_strength(opp)

    # ── New hard caps ─────────────────────────────────────────────────────────

    if is_aggregator_title(opp):
        return 5.5, "aggregator/listicle title detected"

    purity = float(opp.get("source_purity_score", 10) or 10)
    if purity < 6:
        return 7.0, f"source_purity_score={purity:.1f} < 6"

    has_website = is_real(opp.get("official_website"))
    has_sub_page = is_real(
        (opp.get("submission_page") or "")[0]
        if isinstance(opp.get("submission_page"), list)
        else (opp.get("submission_page") or "")
    )
    if not has_website and not has_sub_page:
        return 5.0, "no official_website and no submission_page"

    if opp.get("verification_status") == "research_needed":
        return 6.5, "verification_status=research_needed"

    # ── Deadline penalty (not a hard cap — reduction) ─────────────────────────
    # Applied inside main() after this function returns, flagged via special sentinel.
    # Return None cap to signal "apply deadline deduction instead".
    category = (opp.get("category") or "").lower()
    deadline_missing = not is_real(opp.get("deadline"))
    if "open_call" in category and deadline_missing:
        return None, "open_call with no deadline: -0.5"

    # ── Legacy source/verification strength caps ──────────────────────────────
    if source == 0:
        return 6.5, "no source URL or official website"
    if source == 1 and verify <= 1:
        return 8.0, "single source, weak verification"
    if source == 2 and verify <= 1:
        return 8.6, "verified URL, but weak supporting evidence"
    if source == 2 and verify >= 3:
        return 9.4, "strong source and strong verification"
    return 8.8, "moderate source/verification"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def main():
    opps = load_json(OPP_PATH, [])

    lines = [
        "# Score Sanity Report",
        "",
        "Caps inflated scores when source purity, verification, or evidence is weak.",
        "",
        "| Title | Before | After | Reason |",
        "|-------|--------|-------|--------|",
    ]

    changed = 0

    for opp in opps:
        old = float(opp.get("overall_score", 0) or 0)
        cap, reason = compute_cap(opp)

        if cap is None:
            # Deadline deduction: reduce by 0.5, floor at 3.0
            new = max(3.0, round(old - 0.5, 2))
            if new < old:
                opp["uncapped_score"]   = old
                opp["overall_score"]    = new
                opp["score_sanity_note"] = f"Score reduced by 0.5 ({reason})."
                lines.append(
                    f"| {opp.get('title','')[:50]} | {old} | {new} | {reason} |"
                )
                changed += 1
        elif old > cap:
            opp["uncapped_score"]    = old
            opp["overall_score"]     = cap
            opp["score_sanity_note"] = f"Score capped at {cap}: {reason}."
            lines.append(
                f"| {opp.get('title','')[:50]} | {old} | {cap} | {reason} |"
            )
            changed += 1

    opps.sort(key=lambda x: float(x.get("overall_score", 0) or 0), reverse=True)

    with open(OPP_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, indent=2, ensure_ascii=False)

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Capped/adjusted {changed} scores.")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
