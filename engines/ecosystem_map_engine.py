
import json, os
from pathlib import Path
from collections import defaultdict

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/ecosystem_map.md"

def load_json(path,fallback):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():

    opps = load_json(OPP_PATH,[])

    groups = defaultdict(list)

    for opp in opps:
        groups[
            opp.get(
                "category",
                "unknown"
            )
        ].append(
            opp.get(
                "title",
                "Unknown"
            )
        )

    lines = [
        "# Ecosystem Map",
        ""
    ]

    for category, items in sorted(groups.items()):
        lines.append(f"## {category}")
        lines.append("")

        for item in items[:20]:
            lines.append(f"- {item}")

        lines.append("")

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
