
import json, os
from pathlib import Path

PROFILE_PATH = "memory/visual_language_profile.json"
INST_DIR = "institution_profiles"
OUT_PATH = "reports/institution_fit_report.md"

def load_json(path,fallback):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():

    visual = load_json(
        PROFILE_PATH,
        {}
    )

    themes = [
        str(x).lower()
        for x in visual.get(
            "visual_language",
            []
        )
    ]

    lines = [
        "# Institution Fit Report",
        ""
    ]

    if not os.path.exists(INST_DIR):
        return

    for file in Path(INST_DIR).glob("*.json"):

        data = load_json(file,{})

        keywords = [
            str(x).lower()
            for x in data.get(
                "curatorial_keywords",
                []
            )
        ]

        hits = [
            x for x in themes
            if x in keywords
        ]

        lines.append(
            f"## {data.get('name')}"
        )

        lines.append(
            f"- Fit Hits: {len(hits)}"
        )

        lines.append(
            f"- Keywords: {', '.join(hits)}"
        )

        lines.append("")

    Path("reports").mkdir(exist_ok=True)

    Path(OUT_PATH).write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print(f"Wrote {OUT_PATH}")
