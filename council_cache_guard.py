import json
import os


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


opportunities = load_json(
    "memory/opportunities.json",
    []
)

needs_review = []
cached = []

for opp in opportunities:

    review = opp.get("council_review")

    if review and review.get("overall_score") is not None:
        cached.append(opp)
    else:
        needs_review.append(opp)

save_json(
    "memory/opportunities_needing_council.json",
    needs_review
)

save_json(
    "memory/opportunities_cached.json",
    cached
)

print(f"Cached: {len(cached)}")
print(f"Needs review: {len(needs_review)}")