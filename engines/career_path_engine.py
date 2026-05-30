
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/career_paths.md"

CAREER_PATHS = {
    "Photobook Artist": [
        "photobook",
        "artist book",
        "printed matter",
        "publication",
    ],

    "Independent Documentary Photographer": [
        "documentary",
        "quiet",
        "daily life",
        "urban",
    ],

    "Artist-Run Community Builder": [
        "community",
        "artist-run",
        "collective",
        "alternative",
    ],

    "International Small Press Artist": [
        "small press",
        "zine",
        "book fair",
        "publication",
    ],
}

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def blob(opp):

    parts = []

    for key in [
        "title",
        "one_sentence",
        "why_this_fits_short",
        "category",
    ]:
        val = opp.get(key)

        if val:
            parts.append(str(val))

    for tag in opp.get(
        "tags",
        []
    ):
        parts.append(str(tag))

    return " ".join(parts).lower()

def score_path(text, words):

    return sum(
        1 for w in words
        if w in text
    )

def main():

    opps = load_json(
        OPP_PATH,
        []
    )

    lines = [
        "# Career Path Analysis",
        "",
        "Potential long-term artistic trajectories suggested by current recommendation patterns.",
        "",
    ]

    for path, words in (
        CAREER_PATHS.items()
    ):

        scored = []

        for opp in opps:

            s = score_path(
                blob(opp),
                words,
            )

            if s >= 2:
                scored.append(
                    (
                        s,
                        opp.get(
                            "title",
                            ""
                        )
                    )
                )

        scored.sort(
            reverse=True
        )

        lines.append(
            f"## {path}"
        )

        lines.append("")

        for score, title in scored[:12]:

            lines.append(
                f"- {title} "
                f"(signal {score})"
            )

        lines.append("")

    Path(OUT_PATH).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    Path(OUT_PATH).write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print(
        f"Wrote {OUT_PATH}"
    )

if __name__ == "__main__":
    main()
