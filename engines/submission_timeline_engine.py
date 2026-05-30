
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/submission_timeline.md"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def bucket(opp):

    score = float(
        opp.get(
            "overall_score",
            0
        ) or 0
    )

    difficulty = float(
        opp.get(
            "difficulty_score",
            0
        ) or 0
    )

    if score >= 8 and difficulty <= 6:
        return "Immediate Targets"

    if score >= 7:
        return "Build Toward"

    return "Longer-Term / Experimental"

def main():

    opps = load_json(
        OPP_PATH,
        []
    )

    sections = {
        "Immediate Targets": [],
        "Build Toward": [],
        "Longer-Term / Experimental": [],
    }

    for opp in opps[:100]:

        sections[
            bucket(opp)
        ].append(opp)

    lines = [
        "# Submission Timeline",
        "",
        "Suggested strategic pacing for outreach and applications.",
        "",
    ]

    for section, items in sections.items():

        lines.append(
            f"## {section}"
        )

        lines.append("")

        for opp in items[:20]:

            lines.append(
                f"- {opp.get('title')} "
                f"({opp.get('overall_score')}/10)"
            )

        lines.append("")

    Path(OUT_PATH).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    Path(OUT_PATH).write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        f"Wrote {OUT_PATH}"
    )

if __name__ == "__main__":
    main()
