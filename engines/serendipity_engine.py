
import json
import os
import random

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/serendipity_picks.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def interesting(opp):

    score = float(
        opp.get(
            "overall_score",
            0
        ) or 0
    )

    lineage = float(
        opp.get(
            "lineage_score",
            0
        ) or 0
    )

    prestige = float(
        opp.get(
            "prestige_score",
            0
        ) or 0
    )

    return (
        lineage >= 1.2
        or prestige >= 8
        or score >= 7
    )

def main():

    opps = load_json(
        OPP_PATH,
        []
    )

    pool = [
        x for x in opps
        if interesting(x)
    ]

    random.shuffle(pool)

    chosen = pool[:12]

    with open(
        OUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            chosen,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Generated {len(chosen)} serendipity picks."
    )

if __name__ == "__main__":
    main()
