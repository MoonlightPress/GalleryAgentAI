
import json
import os
import sys
from pathlib import Path
from datetime import date

sys.stdout.reconfigure(encoding='utf-8')

OPP_PATH = "deploy_data/compact_opportunities.json"
SEED_PATH = "global_opportunity_seeds.json"
BACKUP_PATH = "deploy_data/compact_opportunities_before_global_expansion.json"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def title_key(item):
    return str(item.get("title") or item.get("name") or "").strip().lower()


def normalize_seed(seed):
    out = dict(seed)
    out["source_type"] = "global_seed"
    out["added_by"] = "global_opportunity_expander"
    out["added_at"] = date.today().isoformat()
    out["verification_status"] = out.get("verification_status", "partial")
    out["manual_review_needed"] = True
    out["research_priority"] = out.get("research_priority", "high")
    out["submission_process_known"] = bool(out.get("submission_page"))
    out["deadline_verified"] = bool(out.get("deadline"))
    out["fees_verified"] = bool(out.get("fees"))
    out["contact_verified"] = bool(out.get("contact") or out.get("email") or out.get("contact_url"))
    out["missing_fields"] = [
        field for field, present in {
            "submission process": out["submission_process_known"],
            "deadline": out["deadline_verified"],
            "fees": out["fees_verified"],
            "contact": out["contact_verified"],
        }.items()
        if not present
    ]
    return out


def main():
    current = load_json(OPP_PATH, [])
    seeds = load_json(SEED_PATH, [])

    if not current:
        raise SystemExit("No existing opportunities found. Expected deploy_data/compact_opportunities.json")

    if not seeds:
        raise SystemExit("No global seeds found. Expected global_opportunity_seeds.json")

    if not os.path.exists(BACKUP_PATH):
        save_json(BACKUP_PATH, current)

    existing = {title_key(item) for item in current}
    added = []

    for seed in seeds:
        key = title_key(seed)
        if key and key not in existing:
            current.append(normalize_seed(seed))
            existing.add(key)
            added.append(seed.get("title"))

    current.sort(key=lambda x: float(x.get("overall_score", 0) or 0), reverse=True)

    save_json(OPP_PATH, current)

    print(f"Added {len(added)} global opportunities.")
    for title in added:
        print(f"- {title}")
    print(f"Total opportunities: {len(current)}")


if __name__ == "__main__":
    main()
