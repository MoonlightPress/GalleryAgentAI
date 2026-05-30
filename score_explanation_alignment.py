
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
REPORT_PATH = "reports/score_explanation_alignment.md"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def score_band(score):
    try:
        score = float(score or 0)
    except Exception:
        return "unknown"

    if score >= 8.5:
        return "strong"
    if score >= 7:
        return "promising"
    if score >= 5.5:
        return "research"
    return "low"

def main():
    opps = load_json(OPP_PATH, [])

    lines = [
        "# Score / Explanation Alignment",
        "",
        "Scores now follow the explanation. A high score should not appear beside a warning that says the opportunity does not fit.",
        "",
        "## Top Truth-Aligned Opportunities",
        "",
    ]

    shown = 0
    for opp in sorted(opps, key=lambda x: float(x.get("truth_aligned_score", 0) or 0), reverse=True):
        if opp.get("recommendation_visibility") == "hidden":
            continue

        title = opp.get("title") or opp.get("name") or "Unknown"
        score = opp.get("truth_aligned_score")
        band = score_band(score)
        why = opp.get("why_this_fits_short") or opp.get("one_sentence") or ""
        reasons = opp.get("truth_alignment_reasons", [])

        lines.append(f"- **{title}** — {score} — {band}. {why}")
        if reasons:
            for reason in reasons[:3]:
                lines.append(f"  - Note: {reason}")

        shown += 1
        if shown >= 25:
            break

    Path(REPORT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {REPORT_PATH}")

if __name__ == "__main__":
    main()
