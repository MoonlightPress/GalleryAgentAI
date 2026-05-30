
import json
import os
from pathlib import Path
from collections import defaultdict

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/institution_reputation_graph.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def title_of(opp):
    return (
        opp.get("title")
        or opp.get("name")
        or "Unknown"
    )

def main():

    opps = load_json(
        OPP_PATH,
        []
    )

    graph = defaultdict(list)

    for opp in opps:

        source = str(
            opp.get(
                "organization",
                ""
            )
        )

        category = str(
            opp.get(
                "category",
                ""
            )
        )

        prestige = float(
            opp.get(
                "prestige_score",
                0
            ) or 0
        )

        graph[source].append({
            "title": title_of(opp),
            "category": category,
            "prestige": prestige,
            "score": opp.get(
                "overall_score",
                0
            ),
        })

    for source in graph:

        graph[source].sort(
            key=lambda x: (
                x["prestige"],
                x["score"]
            ),
            reverse=True
        )

    Path(OUT_PATH).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            graph,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Wrote {OUT_PATH}"
    )

if __name__ == "__main__":
    main()
