
import json
import os
from pathlib import Path

EXPANDED_PATH = "expanded_source_registry.json"
SOURCE_TARGETS_PATH = "source_targets.json"
ADVANCED_REGISTRY_PATH = "advanced_source_registry.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def flatten_groups(data):
    out = []
    for group_name, items in data.get("source_groups", {}).items():
        for item in items:
            x = dict(item)
            x["source_group"] = group_name
            x["priority"] = "high" if group_name in {"photobook_publishers", "artist_book_fairs"} else "medium"
            out.append(x)
    return out

def main():
    expanded = load_json(EXPANDED_PATH, {})
    new_sources = flatten_groups(expanded)

    targets = load_json(SOURCE_TARGETS_PATH, {"seed_sources": [], "fit_keywords": [], "reject_keywords": []})
    advanced = load_json(ADVANCED_REGISTRY_PATH, {"priority_sources": []})

    existing_urls = {s.get("url") for s in targets.get("seed_sources", [])}
    added_targets = 0

    for src in new_sources:
        if src.get("url") not in existing_urls:
            targets.setdefault("seed_sources", []).append({
                "name": src["name"],
                "url": src["url"],
                "source_type": src["type"],
                "region": src["region"],
                "priority": src["priority"],
                "source_group": src["source_group"],
            })
            existing_urls.add(src.get("url"))
            added_targets += 1

    existing_advanced = {s.get("url") for s in advanced.get("priority_sources", [])}
    added_advanced = 0

    for src in new_sources:
        if src.get("url") not in existing_advanced:
            advanced.setdefault("priority_sources", []).append({
                "name": src["name"],
                "url": src["url"],
                "type": src["type"],
                "region": src["region"],
                "crawl_depth": 2,
                "priority": src["priority"],
                "source_group": src["source_group"],
            })
            existing_advanced.add(src.get("url"))
            added_advanced += 1

    save_json(SOURCE_TARGETS_PATH, targets)
    save_json(ADVANCED_REGISTRY_PATH, advanced)

    print(f"Added {added_targets} sources to {SOURCE_TARGETS_PATH}")
    print(f"Added {added_advanced} sources to {ADVANCED_REGISTRY_PATH}")

if __name__ == "__main__":
    main()
