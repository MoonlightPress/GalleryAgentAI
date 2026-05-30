
import json
import os
from pathlib import Path

REL_PATH = "memory/relationship_memory.json"
OPP_PATH = "deploy_data/compact_opportunities.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def title_of(opp):
    return (
        opp.get("title")
        or opp.get("organisation")
        or "Unknown"
    )

def build_memory_entry(opp):
    return {
        "title": title_of(opp),
        "state": "unseen",
        "interest_level": 0,
        "relationship_strength": 0,
        "last_action": "",
        "next_action": "",
        "follow_up_date": "",
        "contact_history": [],
        "notes": [],
        "submission_history": [],
        "custom_tags": [],
        "curator_names": [],
        "seen_by_artist": False,
        "favorite": False,
        "hidden": False,
    }

def main():
    opps = load_json(OPP_PATH, [])
    existing = load_json(REL_PATH, {})
    created = 0

    for opp in opps:
        title = title_of(opp)

        if title not in existing:
            existing[title] = build_memory_entry(opp)
            created += 1

    save_json(REL_PATH, existing)

    print(f"Added {created} relationship records.")

if __name__ == "__main__":
    main()
