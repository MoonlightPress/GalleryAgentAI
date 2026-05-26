import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import os
from datetime import datetime


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


materials_path = "memory/materials_memory.json"

materials = load_json(
    materials_path,
    {
        "artist_bios": [],
        "artist_statements": [],
        "cv_versions": [],
        "portfolio_sets": [],
        "image_specs": [],
        "translations": [],
        "last_updated": ""
    }
)

materials["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

save_json(materials_path, materials)

print("Saved memory/materials_memory.json")