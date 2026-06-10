import json
import os
from datetime import datetime


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


opps = load_json(
    "memory/opportunities_master.json",
    []
)

for opp in opps:

    score = float(
        opp.get("compound_career_score", 0)
    )

    ignored = int(
        opp.get("times_ignored", 0)
    )

    viewed = int(
        opp.get("times_viewed", 0)
    )

    interacted = int(
        opp.get("times_interacted", 0)
    )

    adjusted = score

    adjusted -= ignored * 0.35
    adjusted += interacted * 0.5
    adjusted += viewed * 0.1

    opp["dynamic_surface_score"] = round(
        adjusted,
        2
    )

save_json(
    "memory/opportunities_master.json",
    sorted(
        opps,
        key=lambda x: -float(
            x.get(
                "dynamic_surface_score",
                0
            )
        )
    )
)

print("Saved opportunity decay model.")