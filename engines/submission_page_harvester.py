"""
Submission Page Harvester

For opportunities that have a submission_page URL but are missing fees,
contact, or deadline info, fetch the page and extract what's there.

Reads/Writes: deploy_data/compact_opportunities.json
"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import os
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
COMPACT_PATH = ROOT / "deploy_data" / "compact_opportunities.json"

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
TIMEOUT = 10
LIMIT = 60
PAUSE = 0.8


def extract_emails(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)


def extract_fees(text: str) -> list[str]:
    yen_ranges = re.findall(
        r"¥[\d,]+(?:\s*[–\-~]\s*¥?[\d,]+)?", text
    )
    yen_words = re.findall(r"[\d,]+\s*(?:円|yen)", text, flags=re.IGNORECASE)
    usd = re.findall(r"\$[\d]+(?:\.\d{2})?", text)
    return yen_ranges + yen_words + usd


def is_free(text: str) -> bool:
    lower = text.lower()
    return "free" in lower or "no fee" in lower or "無料" in text


def extract_dates(text: str) -> list[str]:
    english = re.findall(
        r"\b(?:January|February|March|April|May|June|July|August|September|"
        r"October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}",
        text,
    )
    japanese = re.findall(r"\d{4}年\d{1,2}月\d{1,2}日", text)
    return english + japanese


def needs_harvest(opp: dict) -> bool:
    if not opp.get("submission_page"):
        return False
    missing_fees = not opp.get("fees_verified", False)
    missing_contact = not opp.get("contact_verified", False)
    missing_deadline = not opp.get("deadline_verified", False)
    return missing_fees or missing_contact or missing_deadline


def harvest_opportunity(opp: dict) -> dict:
    url = opp["submission_page"]
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    except Exception as e:
        print(f"  [skip] {url[:60]} — request error: {e}")
        return opp

    if resp.status_code != 200:
        print(f"  [skip] {url[:60]} — HTTP {resp.status_code}")
        return opp

    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)

    changes = []

    # Contact / email
    if not opp.get("contact_verified", False):
        emails = extract_emails(text)
        if emails:
            opp["contact"] = emails[0]
            opp["contact_verified"] = True
            opp["contact_source"] = "harvested_from_submission_page"
            changes.append(f"contact={emails[0]}")

    # Fees
    if not opp.get("fees_verified", False):
        if is_free(text):
            opp["fees"] = "Free"
            opp["fees_verified"] = True
            opp["fees_source"] = "harvested_from_submission_page"
            changes.append("fees=Free")
        else:
            fee_hits = extract_fees(text)
            if fee_hits:
                opp["fees"] = fee_hits[0]
                opp["fees_verified"] = True
                opp["fees_source"] = "harvested_from_submission_page"
                changes.append(f"fees={fee_hits[0]}")

    # Deadline
    if not opp.get("deadline_verified", False):
        dates = extract_dates(text)
        if dates:
            opp["deadline"] = dates[0]
            opp["deadline_verified"] = True
            opp["deadline_source"] = "harvested_from_submission_page"
            changes.append(f"deadline={dates[0]}")

    title_short = opp.get("title", "")[:50]
    if changes:
        print(f"  [found] {title_short} — {', '.join(changes)}")
    else:
        print(f"  [empty] {title_short}")

    return opp


def main():
    if not COMPACT_PATH.exists():
        print(f"[error] compact_opportunities.json not found at {COMPACT_PATH}")
        return

    with open(COMPACT_PATH, "r", encoding="utf-8") as f:
        opps = json.load(f)

    candidates = [o for o in opps if needs_harvest(o)]
    batch = candidates[:LIMIT]

    print(f"[submission_page_harvester] {len(opps)} total | {len(candidates)} need harvest | processing {len(batch)}")

    contacts_found = 0
    fees_found = 0
    deadlines_found = 0

    for opp in batch:
        before_contact = opp.get("contact_verified", False)
        before_fees = opp.get("fees_verified", False)
        before_deadline = opp.get("deadline_verified", False)

        harvest_opportunity(opp)

        if opp.get("contact_verified") and not before_contact:
            contacts_found += 1
        if opp.get("fees_verified") and not before_fees:
            fees_found += 1
        if opp.get("deadline_verified") and not before_deadline:
            deadlines_found += 1

        time.sleep(PAUSE)

    with open(COMPACT_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, ensure_ascii=False, indent=2)

    print()
    print(f"[done] processed={len(batch)}  contacts_found={contacts_found}  fees_found={fees_found}  deadlines_found={deadlines_found}")
    print(f"[saved] {COMPACT_PATH}")


if __name__ == "__main__":
    main()
