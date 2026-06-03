"""
Rumor Mill Propagation Engine

Merges factual data discovered by rumor_mill_engine (deadline, fee,
submission_url, contact_email) back into deploy_data/compact_opportunities.json.

Matches by title. Only overwrites a field if the existing value is empty/None.
"""
import sys
import json
import os

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

RUMOR_MILL_PATH = "memory/rumor_mill.json"
COMPACT_PATH = "deploy_data/compact_opportunities.json"
FIELDS = ["deadline", "fee", "submission_url", "contact_email"]


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def normalize(s):
    return s.strip().lower() if s else ""


def main():
    rumor = load_json(RUMOR_MILL_PATH, {})
    entries = rumor.get("entries", {})

    opps = load_json(COMPACT_PATH, [])
    if not opps:
        print("No compact_opportunities found.")
        return

    # Build title index: normalized title → list of opp indices
    title_index = {}
    for i, opp in enumerate(opps):
        t = normalize(opp.get("title") or opp.get("name") or "")
        if t:
            title_index.setdefault(t, []).append(i)

    updated = 0
    for rm_title, entry in entries.items():
        if not entry.get("data_found"):
            continue
        found = entry.get("found", {})
        if not found:
            continue

        norm_rm = normalize(rm_title)
        # Try exact match first, then substring
        indices = title_index.get(norm_rm, [])
        if not indices:
            for t, idxs in title_index.items():
                if norm_rm in t or t in norm_rm:
                    indices = idxs
                    break

        for idx in indices:
            opp = opps[idx]
            changed = False
            for field in FIELDS:
                if found.get(field) and not opp.get(field):
                    opp[field] = found[field]
                    changed = True
            if changed:
                updated += 1

    with open(COMPACT_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, ensure_ascii=False, indent=2)

    print(f"Propagated rumor mill data to {updated} opportunities.")
    print(f"Wrote {COMPACT_PATH}")


if __name__ == "__main__":
    main()
