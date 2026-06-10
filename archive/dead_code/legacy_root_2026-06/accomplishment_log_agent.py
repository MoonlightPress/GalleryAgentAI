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


memory = load_json(
    "memory/accomplishments_memory.json",
    {
        "items": []
    }
)

entry_path = "accomplishment_entry.txt"

if not os.path.exists(entry_path):
    raise Exception("Create accomplishment_entry.txt first.")

with open(entry_path, "r", encoding="utf-8") as f:
    text = f.read().strip()

if not text:
    raise Exception("accomplishment_entry.txt is empty.")

item = {
    "date_logged": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "raw_text": text,
    "tags": [],
    "used_for_pathways": []
}

lower = text.lower()

if "sold" in lower or "sale" in lower:
    item["tags"].append("sales")

if "gallery" in lower or "exhibition" in lower or "show" in lower:
    item["tags"].append("exhibition")

if "zine" in lower or "book" in lower or "published" in lower:
    item["tags"].append("publishing")

if "cafe" in lower:
    item["tags"].append("local_visibility")

if "commission" in lower:
    item["tags"].append("commission")

memory["items"].append(item)

save_json(
    "memory/accomplishments_memory.json",
    memory
)

print("Saved accomplishment.")