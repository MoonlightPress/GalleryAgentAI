
import json
import os
from pathlib import Path
from random import shuffle

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/momentum_wave.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def score(opp):

    base = float(
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
        base
        + (lineage * 0.6)
        + (prestige * 0.2)
    )

def main():

    opps = load_json(
        OPP_PATH,
        []
    )

    ranked = sorted(
        opps,
        key=score,
        reverse=True,
    )

    wave = {
        "immediate_push": ranked[:8],
        "midterm_wave": ranked[8:20],
        "exploration_layer": ranked[20:40],
    }

    for key in wave:
        shuffle(wave[key])

    Path(OUT_PATH).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            wave,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Generated momentum wave."
    )

if __name__ == "__main__":
    main()
