import json
import os
import hashlib
from datetime import datetime


MASTER_PATH = "memory/opportunities_master.json"
WORKING_PATH = "memory/opportunities.json"
ARCHIVE_PATH = "memory/opportunities_archive.json"


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def make_id(opp):
    source = (
        opp.get("source_url")
        or opp.get("official_website")
        or opp.get("submission_page")
        or opp.get("name", "")
    )

    raw = f"{opp.get('name', '')}|{source}"

    return hashlib.md5(
        raw.encode("utf-8")
    ).hexdigest()[:12]


def normalize(opp):
    opp["name"] = (
        opp.get("name")
        or opp.get("title")
        or opp.get("opportunity_name")
        or "Unknown"
    )

    opp["organization"] = (
        opp.get("organization")
        or opp.get("org")
        or opp.get("name")
        or "Unknown"
    )

    opp["type"] = (
        opp.get("type")
        or opp.get("category")
        or "unknown"
    )

    opp["category"] = (
        opp.get("category")
        or opp.get("type")
        or "unknown"
    )

    opp["city"] = opp.get("city") or ""
    opp["country"] = opp.get("country") or "Japan"

    opp["official_website"] = opp.get("official_website") or ""
    opp["submission_page"] = opp.get("submission_page") or opp.get("official_website") or ""
    opp["source_url"] = opp.get("source_url") or opp.get("submission_page") or opp.get("official_website") or ""
    opp["source_link"] = opp.get("source_link") or opp.get("source_url") or ""

    opp["source_status"] = (
        "verified_link_present"
        if opp["source_link"].startswith("http")
        else "missing_source_link"
    )

    opp["deadline"] = opp.get("deadline") or "Check source"
    opp["fees"] = opp.get("fees") or "Check source"
    opp["status"] = opp.get("status") or "needs_review"
    opp["visibility"] = opp.get("visibility") or "secondary"
    opp["priority"] = opp.get("priority") or "C"
    opp["friction_level"] = opp.get("friction_level") or "unknown"

    opp["id"] = opp.get("id") or make_id(opp)

    opp["last_seen"] = datetime.now().strftime("%Y-%m-%d")
    opp["needs_council_review"] = not bool(opp.get("council_review"))

    return opp


def merge_records(existing, incoming):
    merged = dict(existing)

    for key, value in incoming.items():
        if value not in [None, "", [], {}]:
            merged[key] = value

    merged["id"] = existing.get("id") or incoming.get("id") or make_id(merged)
    merged["last_seen"] = datetime.now().strftime("%Y-%m-%d")

    return merged


def main():
    master = load_json(MASTER_PATH, [])
    working = load_json(WORKING_PATH, [])

    by_id = {}

    for opp in master + working:
        normalized = normalize(opp)
        oid = normalized["id"]

        if oid in by_id:
            by_id[oid] = merge_records(by_id[oid], normalized)
        else:
            by_id[oid] = normalized

    merged = list(by_id.values())

    active = [
        opp for opp in merged
        if opp.get("source_status") == "verified_link_present"
    ]

    archive = [
        opp for opp in merged
        if opp.get("source_status") != "verified_link_present"
    ]

    save_json(MASTER_PATH, merged)
    save_json(WORKING_PATH, active)
    save_json(ARCHIVE_PATH, archive)

    print(f"Master records: {len(merged)}")
    print(f"Active sourced records: {len(active)}")
    print(f"Archived missing-source records: {len(archive)}")


if __name__ == "__main__":
    main()