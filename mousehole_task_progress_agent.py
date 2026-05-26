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
        json.dump(data, f, indent=2, ensure_ascii=False)


tasks = load_json("mousehole_task_seed.json", {"tasks": []})["tasks"]
materials = load_json("memory/materials_memory.json", {})
accomplishments = load_json("memory/accomplishments_memory.json", {"items": []})
artist_memory = load_json("memory/artist_memory.json", {})


def complete(task):
    key = task.get("material_key")

    if key in materials:
        return bool(materials.get(key))

    if key in artist_memory:
        return bool(artist_memory.get(key))

    text = json.dumps(accomplishments, ensure_ascii=False).lower()

    if key:
        return key.replace("_", " ") in text

    return False


out = []

for task in tasks:
    is_done = complete(task)

    out.append({
        **task,
        "complete": is_done,
        "status": "complete" if is_done else "open"
    })

save_json(
    "memory/mousehole_tasks.json",
    {
        "tasks": out
    }
)

print("Saved memory/mousehole_tasks.json")