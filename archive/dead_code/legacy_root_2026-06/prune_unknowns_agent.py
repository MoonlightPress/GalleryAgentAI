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

cleaned = []
removed = []

for opp in opportunities:

    score = opp.get("overall_score", 0)

    text = json.dumps(
        opp,
        ensure_ascii=False
    ).lower()

    is_empty = (
        opp.get("name") == "Unknown"
        and (
            "no opportunity information" in text
            or "nothing to evaluate" in text
            or "insufficient data" in text
        )
    )

    if is_empty:
        removed.append(opp)
        continue

    cleaned.append(opp)

save_json(
    "memory/opportunities.json",
    cleaned
)

save_json(
    "memory/pruned_opportunities.json",
    removed
)

print(f"Kept: {len(cleaned)}")
print(f"Removed: {len(removed)}")