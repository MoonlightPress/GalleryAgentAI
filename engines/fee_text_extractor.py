import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import re
from pathlib import Path

COMPACT_PATH = Path("deploy_data/compact_opportunities.json")

# Patterns applied in order; first match wins
FEE_PATTERNS = [
    # Yen range or single yen amount
    (re.compile(r'¥[\d,]+(?:\s*[–\-~]\s*¥?[\d,]+)?'), "amount"),
    # Japanese yen expressed with kanji/romaji
    (re.compile(r'[\d,]+\s*(?:円|yen)', re.IGNORECASE), "amount"),
    # USD
    (re.compile(r'\$[\d]+(?:\.\d{2})?\s*(?:USD)?', re.IGNORECASE), "amount"),
    # Euro
    (re.compile(r'€[\d]+(?:\.\d{2})?'), "amount"),
]

FREE_PATTERN = re.compile(
    r'\bfree\b'
    r'|no\s+(?:entry\s+)?fee'
    r'|no\s+charge'
    r'|free\s+(?:to\s+)?(?:submit|enter|apply)'
    r'|無料',
    re.IGNORECASE
)

EMPTY_FEE_VALUES = {None, "", "unknown", "not listed", "not publicly listed", "unverified"}


def build_text_blob(opp: dict) -> str:
    bullets = opp.get("three_bullets") or []
    if isinstance(bullets, list):
        bullets_text = " ".join(str(b) for b in bullets)
    else:
        bullets_text = str(bullets)

    parts = [
        opp.get("one_sentence") or "",
        opp.get("quick_action") or "",
        opp.get("why_this_fits_short") or "",
        bullets_text,
        opp.get("category_label") or "",
        opp.get("title") or "",
    ]
    return " ".join(p for p in parts if p)


def fee_is_missing(opp: dict) -> bool:
    raw = opp.get("fees")
    if raw is None:
        return True
    if isinstance(raw, str) and raw.strip().lower() in EMPTY_FEE_VALUES:
        return True
    return False


def extract_fee(text: str):
    """Return (fee_string, matched) or (None, False)."""
    # Check free first (common and unambiguous)
    if FREE_PATTERN.search(text):
        return "Free", True

    for pattern, _ in FEE_PATTERNS:
        m = pattern.search(text)
        if m:
            return m.group(0).strip(), True

    return None, False


def main():
    if not COMPACT_PATH.exists():
        print(f"ERROR: {COMPACT_PATH} not found — nothing to process.")
        return

    with COMPACT_PATH.open(encoding="utf-8") as f:
        opportunities = json.load(f)

    if not isinstance(opportunities, list):
        print("ERROR: compact_opportunities.json is not a list.")
        return

    count_extracted = 0
    count_already_had = 0
    count_still_missing = 0

    for opp in opportunities:
        if not isinstance(opp, dict):
            continue

        if not fee_is_missing(opp):
            count_already_had += 1
            continue

        blob = build_text_blob(opp)
        fee, matched = extract_fee(blob)

        if matched:
            opp["fees"] = fee
            opp["fees_verified"] = True
            opp["fees_source"] = "extracted_from_text"
            count_extracted += 1
        else:
            count_still_missing += 1

    # Write back
    COMPACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with COMPACT_PATH.open("w", encoding="utf-8") as f:
        json.dump(opportunities, f, ensure_ascii=False, indent=2)

    print(f"Fee extraction complete.")
    print(f"  Fees extracted from text : {count_extracted}")
    print(f"  Already had fees         : {count_already_had}")
    print(f"  Still missing after run  : {count_still_missing}")
    print(f"  Total opportunities      : {len(opportunities)}")


if __name__ == "__main__":
    main()
