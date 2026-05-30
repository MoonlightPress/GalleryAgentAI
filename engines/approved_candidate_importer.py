
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
APPROVED_PATH = "ingestion/approved_candidates.json"
BACKUP_PATH = "deploy_data/compact_opportunities_before_approved_candidate_import.json"

MAX_IMPORT = 25

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def key(item):
    return (
        str(item.get("title") or "").strip().lower(),
        str(item.get("source_url") or item.get("official_website") or "").strip().lower(),
    )

def main():
    opps = load_json(OPP_PATH, [])
    approved = load_json(APPROVED_PATH, [])

    if not os.path.exists(BACKUP_PATH):
        save_json(BACKUP_PATH, opps)

    existing = {key(o) for o in opps}
    added = 0

    for candidate in approved[:MAX_IMPORT]:
        if key(candidate) in existing:
            continue

        opps.append(candidate)
        existing.add(key(candidate))
        added += 1

    opps.sort(key=lambda x: float(x.get("overall_score", 0) or 0), reverse=True)

    save_json(OPP_PATH, opps)

    print(f"Imported approved candidates: {added}")
    print(f"Total opportunities: {len(opps)}")

if __name__ == "__main__":
    main()
