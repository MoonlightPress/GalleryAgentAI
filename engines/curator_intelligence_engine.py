
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/curator_intelligence_report.md"


CURATOR_PATTERNS = {
    "photobook": [
        "printed matter",
        "artist book",
        "small press",
        "book fair",
    ],

    "quiet_photography": [
        "memory",
        "daily life",
        "architecture",
        "urban",
        "poetic",
    ],

    "community_space": [
        "community",
        "artist-run",
        "independent",
        "collective",
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

    for tag in opp.get("tags", []):
        parts.append(str(tag))

    return " ".join(parts).lower()


def detect_patterns(opp):

    b = blob(opp)

    found = []

    for pattern, words in (
        CURATOR_PATTERNS.items()
    ):

        hits = sum(
            1 for w in words
            if w in b
        )

        if hits >= 2:
            found.append(pattern)

    return found


def main():

    opps = load_json(OPP_PATH, [])

    lines = [
        "# Curator Intelligence Report",
        "",
        "This report identifies recurring curatorial and institutional patterns.",
        "",
    ]

    counts = {}

    for opp in opps:

        patterns = detect_patterns(opp)

        opp["curator_patterns"] = patterns

        for p in patterns:
            counts[p] = (
                counts.get(p, 0)
                + 1
            )

    lines.append("## Pattern Frequency")
    lines.append("")

    for k, v in sorted(
        counts.items(),
        key=lambda x: x[1],
        reverse=True,
    ):
        lines.append(f"- {k}: {v}")

    Path(OUT_PATH).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    Path(OUT_PATH).write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    with open(
        OPP_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            opps,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Wrote {OUT_PATH}"
    )


if __name__ == "__main__":
    main()
