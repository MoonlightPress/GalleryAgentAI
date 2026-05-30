
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
REPORT_PATH = "reports/native_medium_rankings.md"

def load(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():
    opps = load(OPP_PATH, [])

    groups = {
        "painting": [],
        "mixed": [],
        "translation_candidates": [],
        "photography_demoted": [],
        "unknown": [],
    }

    for opp in opps:
        native = opp.get("native_medium", "unknown")
        if native == "photography":
            if opp.get("translation_candidate"):
                groups["translation_candidates"].append(opp)
            else:
                groups["photography_demoted"].append(opp)
        elif native in groups:
            groups[native].append(opp)
        else:
            groups["unknown"].append(opp)

    for k in groups:
        groups[k].sort(key=lambda x: float(x.get("source_purity_score", 0) or 0), reverse=True)

    labels = {
        "painting": "Native Painting / Works on Paper",
        "mixed": "Mixed / Artist Book / Bookstore Ecosystem",
        "translation_candidates": "Translation Candidates",
        "photography_demoted": "Photography-Only Demoted",
        "unknown": "Unknown Medium",
    }

    lines = [
        "# Native Medium Rankings",
        "",
        "This report separates native watercolor/works-on-paper opportunities from photography sources and translation candidates.",
        "",
    ]

    for key, label in labels.items():
        lines.append(f"## {label}")
        lines.append("")
        items = groups[key]
        if not items:
            lines.append("_No items._")
            lines.append("")
            continue
        for opp in items[:20]:
            title = opp.get("title") or opp.get("name") or "Unknown"
            score = opp.get("source_purity_score")
            why = opp.get("why_this_fits_short") or opp.get("one_sentence") or ""
            reason = opp.get("source_purity_reason", "")
            lines.append(f"- **{title}** — {score}. {reason}. {why}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT_PATH}")

if __name__ == "__main__":
    main()
