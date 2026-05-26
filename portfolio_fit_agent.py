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


profiles = load_json(
    "portfolio_profiles.json",
    {
        "profiles": []
    }
)

opps = load_json(
    "memory/opportunities_master.json",
    []
)

for opp in opps:

    category = opp.get(
        "category",
        ""
    ).lower()

    suggested = []

    for profile in profiles["profiles"]:

        text = json.dumps(
            profile,
            ensure_ascii=False
        ).lower()

        if category in text:
            suggested.append(
                profile["name"]
            )

    opp["recommended_portfolio_profiles"] = suggested

save_json(
    "memory/opportunities_master.json",
    opps
)

print("Saved portfolio profile recommendations.")