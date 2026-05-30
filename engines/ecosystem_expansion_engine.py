
import json
import os
from collections import Counter

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/ecosystem_patterns.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():

    opps = load_json(OPP_PATH, [])

    country_counter = Counter()
    category_counter = Counter()
    tag_counter = Counter()

    for opp in opps[:120]:

        country = str(
            opp.get("country", "")
        )

        if country:
            country_counter[country] += 1

        category = str(
            opp.get("category", "")
        )

        if category:
            category_counter[category] += 1

        for tag in opp.get(
            "tags",
            []
        ):
            tag_counter[str(tag)] += 1

    data = {
        "dominant_countries":
            country_counter.most_common(20),

        "dominant_categories":
            category_counter.most_common(20),

        "dominant_tags":
            tag_counter.most_common(40),
    }

    with open(
        OUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Wrote {OUT_PATH}"
    )

if __name__ == "__main__":
    main()
