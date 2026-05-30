
import json
from pathlib import Path

DRAFT_PATH = Path("memory/artist_visual_profile_draft.json")
MASTER_PATH = Path("memory/artist_master_profile.json")


def load_json(path, fallback):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return fallback


def main():
    draft = load_json(DRAFT_PATH, {})
    master = load_json(MASTER_PATH, {})

    if not draft:
        raise SystemExit("No visual profile draft found.")

    master["visual_profile"] = draft

    MASTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    MASTER_PATH.write_text(
        json.dumps(master, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Applied visual profile draft to {MASTER_PATH}")


if __name__ == "__main__":
    main()
