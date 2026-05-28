
import json
import os

REL_PATH = "memory/relationship_memory.json"
STRATEGY_PATH = "memory/strategy_feed.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def relationship_bonus(entry):
    state = entry.get("state")

    if state == "conversation_started":
        return 2

    if state == "soft_relationship":
        return 3

    if state == "strong_relationship":
        return 5

    if state == "submitted":
        return 1

    return 0

def interest_bonus(entry):
    return (
        float(entry.get("interest_level", 0))
        * 0.4
    )

def momentum_score(item, memory):
    base = float(item.get("score", 0) or 0)

    return round(
        base
        + relationship_bonus(memory)
        + interest_bonus(memory),
        2,
    )

def main():
    feed = load_json(STRATEGY_PATH, {})
    memory = load_json(REL_PATH, {})

    updated = 0

    for section in feed.values():
        for item in section:
            title = item.get("title")
            mem = memory.get(title, {})

            item["momentum_score"] = (
                momentum_score(item, mem)
            )

            updated += 1

    with open(
        STRATEGY_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            feed,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Updated {updated} momentum scores."
    )

if __name__ == "__main__":
    main()
