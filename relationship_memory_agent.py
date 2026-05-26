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


ENTRY = "relationship_entry.json"

entry = load_json(
    ENTRY,
    {}
)

if not entry:
    raise Exception(
        "relationship_entry.json missing."
    )

memory = load_json(
    "memory/relationship_memory.json",
    {
        "relationships": []
    }
)

entry["logged_at"] = datetime.now().strftime(
    "%Y-%m-%d %H:%M"
)

memory["relationships"].append(
    entry
)

save_json(
    "memory/relationship_memory.json",
    memory
)

print("Saved relationship memory.")