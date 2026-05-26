import json
import os


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

    total = 0

    traj = opp.get("trajectory_analysis", {})
    eco = opp.get("ecosystem_bridge_analysis", {})

    total += float(
        traj.get("career_compounding_score", 0)
    )

    total += float(
        eco.get("ecosystem_value", 0)
    )

    total += float(
        eco.get("entry_point_strength", 0)
    )

    total += float(
        eco.get("peer_visibility_gain", 0)
    ) * 0.5

    total += float(
        eco.get("institutional_visibility_gain", 0)
    ) * 0.5

    opp["compound_career_score"] = round(total, 2)

ranked = sorted(
    opps,
    key=lambda x: -float(
        x.get("compound_career_score", 0)
    )
)

save_json(
    "memory/opportunities_master.json",
    ranked
)

print("Saved compound career scoring.")