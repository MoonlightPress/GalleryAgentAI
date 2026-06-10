import json
import os


REQUIRED_LINK_FIELDS = [
    "official_website",
    "submission_page",
    "source_url",
    "contact_page"
]


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def has_source_link(opp):
    for field in REQUIRED_LINK_FIELDS:
        value = opp.get(field)
        if value and str(value).startswith("http"):
            return True
    return False


def best_source_link(opp):
    for field in [
        "submission_page",
        "official_website",
        "source_url",
        "contact_page"
    ]:
        value = opp.get(field)
        if value and str(value).startswith("http"):
            return value
    return ""


opportunities = load_json(
    "memory/opportunities.json",
    []
)

valid = []
invalid = []

for opp in opportunities:
    opp["source_link"] = best_source_link(opp)

    if has_source_link(opp):
        opp["source_status"] = "verified_link_present"
        valid.append(opp)
    else:
        opp["source_status"] = "missing_source_link"
        invalid.append(opp)

save_json(
    "memory/opportunities.json",
    valid
)

save_json(
    "memory/opportunities_missing_sources.json",
    invalid
)

print(f"Valid sourced opportunities: {len(valid)}")
print(f"Missing source links: {len(invalid)}")