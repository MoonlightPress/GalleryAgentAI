
import json
import os
from pathlib import Path

REL_PATH = "memory/relationship_memory.json"
OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/reputation_profile.json"

STATE_VALUES = {
    "unseen": 0,
    "researching": 1,
    "interested": 2,
    "submitted": 4,
    "waiting": 5,
    "follow_up": 6,
    "conversation_started": 8,
    "soft_relationship": 12,
    "strong_relationship": 18,
    "rejected": -3,
    "archived": -1,
}

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save_json(path, data):
    Path(path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
        )

def title_of(opp):
    return (
        opp.get("title")
        or opp.get("name")
        or "Unknown"
    )

def lookup(opps):
    return {
        title_of(o): o
        for o in opps
    }

def main():

    rel = load_json(
        REL_PATH,
        {}
    )

    opps = load_json(
        OPP_PATH,
        []
    )

    opp_lookup = lookup(opps)

    total = 0
    category_scores = {}
    country_scores = {}

    for title, entry in rel.items():

        state = entry.get(
            "state",
            "unseen"
        )

        value = STATE_VALUES.get(
            state,
            0
        )

        total += value

        opp = opp_lookup.get(title)

        if not opp:
            continue

        category = str(
            opp.get("category", "")
        )

        country = str(
            opp.get("country", "")
        )

        category_scores[
            category
        ] = (
            category_scores.get(
                category,
                0
            ) + value
        )

        country_scores[
            country
        ] = (
            country_scores.get(
                country,
                0
            ) + value
        )

    reputation = {
        "overall_reputation": total,
        "category_reputation": category_scores,
        "country_reputation": country_scores,
    }

    save_json(
        OUT_PATH,
        reputation
    )

    print(
        f"Calculated reputation score: {total}"
    )

if __name__ == "__main__":
    main()
