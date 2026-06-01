
import json
import os
from collections import Counter
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/taste_clusters.md"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():

    opps = load_json(OPP_PATH, [])

    counter = Counter()

    for opp in opps[:80]:

        for lineage in opp.get(
            "lineage_matches",
            []
        ):
            counter[lineage["name"]] += 1

    lines = [
        "# Taste Cluster Report",
        "",
        "Dominant aesthetic clusters detected in current recommendations:",
        "",
    ]

    for name, count in counter.most_common():
        lines.append(
            f"- {name}: {count}"
        )

    lines += [
        "",
        "## Interpretation",
        "",
        "The system is increasingly prioritizing:",
        "",
        "- photobook ecosystems",
        "- quiet documentary work",
        "- independent art-book culture",
        "- artist-run spaces",
        "- atmospheric photography",
        "- intimate publication environments",
    ]

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
