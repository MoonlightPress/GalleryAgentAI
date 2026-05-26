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
        json.dump(data, f, indent=2, ensure_ascii=False)


ENTRY_PATH = "artist_memory_entry.json"

entry = load_json(ENTRY_PATH, {})

if not entry:
    raise Exception("artist_memory_entry.json is missing or empty.")

memory = load_json(
    "memory/artist_memory.json",
    {
        "favorite_artists": [],
        "desired_peers": [],
        "publication_history": [],
        "sales_history": [],
        "career_goals": [],
        "avoid_preferences": [],
        "notes": [],
        "last_updated": ""
    }
)

for key, value in entry.items():
    if key == "last_updated":
        continue

    if key not in memory:
        memory[key] = []

    if isinstance(value, list):
        for item in value:
            if item and item not in memory[key]:
                memory[key].append(item)
    else:
        if value and value not in memory[key]:
            memory[key].append(value)

memory["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

save_json("memory/artist_memory.json", memory)

print("Saved memory/artist_memory.json")