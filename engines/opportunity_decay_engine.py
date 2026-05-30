
import json
import os
from pathlib import Path
from datetime import datetime

OPP_PATH = "deploy_data/compact_opportunities.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def stale_penalty(opp):

    verification = str(
        opp.get(
            "verification_status",
            ""
        )
    )

    evidence = str(
        opp.get(
            "evidence_quality",
            ""
        )
    )

    penalty = 0

    if verification in [
        "weak",
        "candidate",
    ]:
        penalty += 0.6

    if evidence in [
        "none",
        "weak",
    ]:
        penalty += 0.5

    return penalty

def main():

    opps = load_json(
        OPP_PATH,
        []
    )

    changed = 0

    for opp in opps:

        penalty = stale_penalty(
            opp
        )

        if penalty > 0:

            old = float(
                opp.get(
                    "overall_score",
                    0
                ) or 0
            )

            opp["pre_decay_score"] = old

            opp["overall_score"] = max(
                0,
                round(old - penalty, 2)
            )

            changed += 1

    opps.sort(
        key=lambda x: float(
            x.get(
                "overall_score",
                0
            ) or 0
        ),
        reverse=True
    )

    with open(
        OPP_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            opps,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Decayed {changed} stale opportunities."
    )

if __name__ == "__main__":
    main()
