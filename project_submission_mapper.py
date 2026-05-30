
import json
import os
from pathlib import Path

CONCEPT_PATH = "memory/artist_project_concepts.json"
OUT_PATH = "reports/project_submission_map.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def main():
    concepts = load_json(CONCEPT_PATH, [])

    lines = [
        "# Project Submission Map",
        "",
        "This turns project concepts into concrete submission paths.",
        "",
    ]

    for concept in concepts:
        lines.append(f"## {concept.get('title')}")
        lines.append("")

        lines.append("### Best First Version")
        lines.append(f"- Format: {concept.get('format')}")
        lines.append("- Length: 12–20 images")
        lines.append("- Statement: 80–120 words")
        lines.append("- Delivery: PDF + Instagram/website link")
        lines.append("")

        lines.append("### Best First Targets")
        targets = concept.get("opportunity_targets", [])[:5]
        if not targets:
            lines.append("_No targets yet._")
        else:
            for target in targets:
                lines.append(f"- {target.get('title')}")
        lines.append("")

        lines.append("### What To Prepare")
        lines.append("- 12–20 image edit")
        lines.append("- 1 short title")
        lines.append("- 1 sentence project description")
        lines.append("- 80–120 word statement")
        lines.append("- 3-line email")
        lines.append("")

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
