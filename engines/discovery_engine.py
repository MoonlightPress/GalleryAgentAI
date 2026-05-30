
import json
import os
from pathlib import Path

NETWORK_PATH = "memory/institution_network.json"
OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/discovery_paths.md"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def top_opps(opps):
    return sorted(
        opps,
        key=lambda x: float(
            x.get("overall_score", 0)
            or 0
        ),
        reverse=True,
    )[:15]

def main():

    network = load_json(
        NETWORK_PATH,
        {}
    )

    opps = load_json(
        OPP_PATH,
        []
    )

    lines = [
        "# Discovery Paths",
        "",
        "This report suggests adjacent institutions and ecosystems.",
        "",
    ]

    for opp in top_opps(opps):

        title = (
            opp.get("title")
            or "Unknown"
        )

        lines.append(f"## {title}")
        lines.append("")

        related = network.get(
            title,
            []
        )

        for rel in related[:8]:

            lines.append(
                f"- {rel['title']} "
                f"(similarity {rel['score']})"
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
