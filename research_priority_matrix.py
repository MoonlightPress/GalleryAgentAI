
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/research_priority_matrix.md"

def load_json(path,fallback):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():

    opps = sorted(
        load_json(OPP_PATH,[]),
        key=lambda x: float(
            x.get("overall_score",0) or 0
        ),
        reverse=True
    )

    lines = [
        "# Research Priority Matrix",
        "",
        "These organizations should receive deep manual research first.",
        ""
    ]

    for opp in opps[:25]:

        lines.append(
            f"## {opp.get('organization','Unknown')}"
        )

        lines.append(
            f"- Opportunity: {opp.get('title')}"
        )

        lines.append(
            f"- Score: {opp.get('overall_score')}"
        )

        lines.append(
            "- Research artist roster"
        )

        lines.append(
            "- Research publications"
        )

        lines.append(
            "- Research curatorial language"
        )

        lines.append("")

    Path("reports").mkdir(exist_ok=True)

    Path(OUT_PATH).write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

if __name__ == "__main__":
    main()
