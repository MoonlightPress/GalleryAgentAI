import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import re
from pathlib import Path

COMPACT_PATH = Path("deploy_data/compact_opportunities.json")

# A number that may carry thousands separators but never a trailing one:
# matches "500", "13,200", "12,000" — but on "¥500, deadline" stops at "500".
_NUM = r'\d{1,3}(?:,\d{3})*|\d+'

# Patterns applied in order; first match wins
FEE_PATTERNS = [
    # Yen range or single yen amount
    (re.compile(rf'¥(?:{_NUM})(?:\s*[–\-~]\s*¥?(?:{_NUM}))?'), "amount"),
    # Japanese yen expressed with kanji/romaji
    (re.compile(rf'(?:{_NUM})\s*(?:円|yen)', re.IGNORECASE), "amount"),
    # USD — grouped digits, else "$12,000" truncated to "$12" (live bug 2026-07-27)
    (re.compile(rf'\$(?:{_NUM})(?:\.\d{{2}})?\s*(?:USD)?', re.IGNORECASE), "amount"),
    # Euro
    (re.compile(rf'€(?:{_NUM})(?:\.\d{{2}})?'), "amount"),
]

# Money named near these words is what she WINS, not what she pays. Reading a
# prize as an entry fee invents a cost the source never stated — worse than
# leaving the fee blank, because she budgets against it.
PRIZE_CONTEXT = re.compile(
    r'prize|award|grant|winner|wins\b|receives?\b|cash|scholarship'
    r'|stipend|honorarium|funding|賞金|助成|奨学金',
    re.IGNORECASE
)

# How far either side of a matched amount to look for that context.
PRIZE_WINDOW = 50

# An explicit fee label immediately before the amount overrides prize context —
# "$12,000 prize. Entry fee: $35" must still yield $35, not nothing.
FEE_LABEL = re.compile(
    r'(?:entry|submission|application|registration|handling)?\s*'
    r'(?:fee|fees|cost|charge|price|参加費|申込料|出品料)\s*'
    r'(?:is|of|:|：|=)?\s*$',
    re.IGNORECASE
)

# How far back to look for that label.
FEE_LABEL_WINDOW = 30

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
        for m in pattern.finditer(text):
            before = text[max(0, m.start() - FEE_LABEL_WINDOW):m.start()]
            if not FEE_LABEL.search(before):
                window = text[max(0, m.start() - PRIZE_WINDOW):m.end() + PRIZE_WINDOW]
                if PRIZE_CONTEXT.search(window):
                    continue  # a prize/grant, not a cost — keep looking for a real fee
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
