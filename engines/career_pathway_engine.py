
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/career_pathways.md"

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
        "# Career Pathways",
        "",
        "Suggested sequence:",
        ""
    ]

    for idx, opp in enumerate(opps[:15],1):
        lines.append(
            f"{idx}. {opp.get('title')} ({opp.get('overall_score')}/10)"
        )

    Path(OUT_PATH).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    Path(OUT_PATH).write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print(f"Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
