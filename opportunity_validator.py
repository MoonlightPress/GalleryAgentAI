import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import requests
import os
from datetime import datetime


REQUIRED_FIELDS = [
    "name",
    "type",
    "city",
    "country",
    "official_website",
    "why_fit",
    "next_action"
]


VALID_STATUSES = [
    "active",
    "research_needed",
    "closed",
    "sent",
    "rejected",
    "archived"
]


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def is_valid_url(url):

    if not url:
        return False

    if not url.startswith("http"):
        return False

    try:
        r = requests.head(
            url,
            allow_redirects=True,
            timeout=10
        )

        return r.status_code < 400

    except Exception:
        return False


def validate_opportunity(opp):

    issues = []

    for field in REQUIRED_FIELDS:

        value = opp.get(field, "")

        if not isinstance(value, str):
            issues.append(f"{field}_not_string")
            continue

        if len(value.strip()) < 3:
            issues.append(f"{field}_too_short")

    if opp.get("status") not in VALID_STATUSES:
        issues.append("invalid_status")

    fit_score = opp.get("fit_score", 0)

    if not isinstance(fit_score, int):
        issues.append("fit_score_not_int")

    if fit_score < 1 or fit_score > 10:
        issues.append("fit_score_out_of_range")

    website = opp.get("official_website", "")

    if website and not is_valid_url(website):
        issues.append("website_invalid")

    confidence = opp.get("confidence_score", 0)

    if confidence and confidence < 0.4:
        issues.append("low_confidence")

    return issues


def main():

    memory = load_json(
        "memory/opportunities.json",
        []
    )

    cleaned = []
    rejected = []

    print(f"Loaded {len(memory)} opportunities")

    for opp in memory:

        issues = validate_opportunity(opp)

        opp["validation_checked_at"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        opp["validation_issues"] = issues

        if issues:
            rejected.append(opp)
            print(
                f"REJECTED: {opp.get('name', 'UNKNOWN')} -> {issues}"
            )

        else:
            cleaned.append(opp)
            print(
                f"VALID: {opp.get('name', 'UNKNOWN')}"
            )

    save_json(
        "memory/opportunities.json",
        cleaned
    )

    save_json(
        "memory/rejected_opportunities.json",
        rejected
    )

    print()
    print(f"Valid opportunities: {len(cleaned)}")
    print(f"Rejected opportunities: {len(rejected)}")

    print()
    print("Saved cleaned opportunities")
    print("Saved rejected opportunities")


if __name__ == "__main__":
    main()