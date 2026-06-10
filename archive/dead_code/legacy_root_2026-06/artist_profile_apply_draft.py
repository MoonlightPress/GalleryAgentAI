
import json
import os
from pathlib import Path

DRAFT_PATH = "memory/artist_visual_profile_draft.json"
MASTER_PATH = "memory/artist_master_profile.json"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    draft = load_json(DRAFT_PATH, {})
    master = load_json(MASTER_PATH, {})

    if not draft:
        raise SystemExit("No draft found. Generate memory/artist_visual_profile_draft.json first.")

    master["visual_profile"] = draft
    save_json(MASTER_PATH, master)

    print(f"Applied visual profile draft to {MASTER_PATH}")


if __name__ == "__main__":
    main()
