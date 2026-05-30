
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
CANDIDATE_PATH = "ingestion/opportunity_candidates.json"
BACKUP_PATH = "deploy_data/compact_opportunities_before_candidate_import.json"


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
        str(item.get("source_url") or item.get("official_website") or "").strip().lower()
    )


def main():
    opps = load_json(OPP_PATH, [])
    candidates = load_json(CANDIDATE_PATH, [])

    if not opps:
        raise SystemExit("No existing opportunity file found.")

    if not os.path.exists(BACKUP_PATH):
        save_json(BACKUP_PATH, opps)

    existing = {key(o) for o in opps}
    added = 0

    # Conservative import: only import top candidates with score >= 5.5.
    for c in candidates:
        if float(c.get("overall_score", 0) or 0) < 5.5:
            continue

        if key(c) in existing:
            continue

        c["import_status"] = "candidate_unverified"
        c["do_not_show_as_verified"] = True
        opps.append(c)
        existing.add(key(c))
        added += 1

    save_json(OPP_PATH, opps)

    print(f"Imported {added} candidates into {OPP_PATH}")


if __name__ == "__main__":
    main()
