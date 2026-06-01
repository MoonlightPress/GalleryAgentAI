import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


opps = load_json(
    "memory/opportunities_master.json",
    []
)

updated = []

for opp in opps:

    source = (
        opp.get("source_link")
        or opp.get("source_url")
        or opp.get("official_website")
    )

    verification = {
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "website_alive": False,
        "status_code": None,
        "deadline_confidence": "unknown",
        "submission_open_probability": "unknown",
        "contact_found": False,
        "verification_notes": []
    }

    if not source:
        verification["verification_notes"].append(
            "No source URL found."
        )

        opp["verification"] = verification
        updated.append(opp)
        continue

    try:

        response = requests.get(
            source,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        verification["status_code"] = response.status_code

        if response.status_code == 200:

            verification["website_alive"] = True

            html = response.text.lower()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            if (
                "deadline" in html
                or "submission" in html
                or "apply" in html
                or "open call" in html
            ):
                verification["submission_open_probability"] = "possible"

            if (
                "closed" in html
                or "expired" in html
            ):
                verification["deadline_confidence"] = "possibly_closed"

            emails = soup.find_all(
                string=lambda t:
                t and "@" in t
            )

            if emails:
                verification["contact_found"] = True

        else:
            verification["verification_notes"].append(
                f"Status code {response.status_code}"
            )

    except Exception as e:

        verification["verification_notes"].append(
            str(e)
        )

    opp["verification"] = verification

    updated.append(opp)

    print(
        "Verified:",
        opp.get("title", "Unknown")
    )

save_json(
    "memory/opportunities_master.json",
    updated
)

print("Saved verification layer.")