import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import re
import calendar
from datetime import date
from pathlib import Path

COMPACT_PATH = Path("deploy_data/compact_opportunities.json")

# Pattern sets (all case-insensitive unless noted)
ROLLING_TERMS = [
    'rolling', 'ongoing', 'open year-round', 'year round',
    'no fixed deadline', '随時', 'anytime', 'open submissions', 'continuous',
]

CLOSED_TERMS = [
    'deadline passed', 'deadline was', 'submissions closed',
    'cycle closed', 'registration closed',
]

CHECK_SCHEDULE_TERMS = [
    'check current schedule', 'check schedule', 'check website',
    'tbd', 'to be announced', 'お問い合わせ',
]

# Matches things like "June 2025", "March 15, 2025", "2025-06", "06/2025", etc.
MONTH_NAMES = (
    'january|february|march|april|may|june|july|august|september|'
    'october|november|december|'
    'jan|feb|mar|apr|jun|jul|aug|sep|oct|nov|dec'
)
CONFIRMED_DATE_RE = re.compile(
    r'(?:' + MONTH_NAMES + r')\s+\d{1,2}[,\s]+20\d{2}'   # "March 15, 2026"
    r'|20\d{2}[\-/]\d{2}'                                   # "2026-06"
    r'|\d{1,2}[\-/]\d{1,2}[\-/]20\d{2}'                    # "06/15/2026"
    r'|(?:' + MONTH_NAMES + r')[,\s]+20\d{2}',              # "June 2026"
    re.IGNORECASE,
)

YEAR_ONLY_RE = re.compile(r'20\d{2}')

# ── Past-deadline detection ────────────────────────────────────────────────
# A deadline that has already passed must NOT be treated as a verified, open
# call. We parse the deadline field into its last valid day and compare to today.
_MONTH_NUM = {m: i + 1 for i, m in enumerate(
    'january february march april may june july august september october november december'.split())}
for _m, _n in list(_MONTH_NUM.items()):
    _MONTH_NUM[_m[:3]] = _n

_ISO_FULL_RE      = re.compile(r'(20\d{2})[-/](\d{1,2})[-/](\d{1,2})')
_NUM_MDY_RE       = re.compile(r'\b(\d{1,2})[-/](\d{1,2})[-/](20\d{2})\b')
_MONTH_DAY_YEAR_RE = re.compile(r'(' + MONTH_NAMES + r')[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?[,\s]+(20\d{2})', re.IGNORECASE)
_DAY_MONTH_YEAR_RE = re.compile(r'\b(\d{1,2})(?:st|nd|rd|th)?\s+(' + MONTH_NAMES + r')[a-z]*\.?[,\s]+(20\d{2})', re.IGNORECASE)
_ISO_YM_RE        = re.compile(r'(20\d{2})[-/](\d{1,2})(?![-/\d])')
_MONTH_YEAR_RE    = re.compile(r'(' + MONTH_NAMES + r')[a-z]*\.?[,\s]+(20\d{2})', re.IGNORECASE)


def _safe_date(y: int, mo: int, d: int):
    try:
        return date(y, mo, d)
    except ValueError:
        return None


def parse_deadline_date(deadline_field: str):
    """Parse a deadline string into the LAST valid day it denotes, or None if
    undatable. Month/year-only deadlines resolve to the last day of that month —
    a month-year deadline is not 'past' until the whole month is over."""
    s = str(deadline_field or "")
    m = _ISO_FULL_RE.search(s)
    if m:
        return _safe_date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = _NUM_MDY_RE.search(s)
    if m:
        return _safe_date(int(m.group(3)), int(m.group(1)), int(m.group(2)))
    m = _MONTH_DAY_YEAR_RE.search(s)
    if m:
        return _safe_date(int(m.group(3)), _MONTH_NUM[m.group(1).lower()[:3]], int(m.group(2)))
    m = _DAY_MONTH_YEAR_RE.search(s)
    if m:
        return _safe_date(int(m.group(3)), _MONTH_NUM[m.group(2).lower()[:3]], int(m.group(1)))
    m = _ISO_YM_RE.search(s)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12:
            return _safe_date(y, mo, calendar.monthrange(y, mo)[1])
        return None
    m = _MONTH_YEAR_RE.search(s)
    if m:
        y, mo = int(m.group(2)), _MONTH_NUM[m.group(1).lower()[:3]]
        return _safe_date(y, mo, calendar.monthrange(y, mo)[1])
    return None


def deadline_is_past(deadline_field: str, today: date = None) -> bool:
    """True only when the deadline parses to a concrete day before today."""
    today = today or date.today()
    parsed = parse_deadline_date(deadline_field)
    return parsed is not None and parsed < today


def build_text_blob(opp: dict) -> str:
    parts = [
        opp.get("deadline") or "",
        opp.get("one_sentence") or "",
        opp.get("quick_action") or "",
        opp.get("why_this_fits_short") or "",
    ]
    return " ".join(p for p in parts if p)


def contains_any(text: str, terms: list) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def classify_deadline(blob: str, deadline_field: str, today: date = None) -> dict:
    """Return a dict of fields to update, or empty dict if no match."""
    today = today or date.today()

    # 1. Rolling
    if contains_any(blob, ROLLING_TERMS):
        return {
            "deadline": "Rolling — check website for current window",
            "deadline_verified": True,
            "deadline_type": "rolling",
        }

    # 2. Closed / passed
    if contains_any(blob, CLOSED_TERMS):
        return {
            "deadline_type": "closed",
            # Do NOT set deadline_verified = True
        }

    # 2b. Dated deadline that has already passed — must never be marked verified.
    if deadline_field and deadline_is_past(deadline_field, today):
        return {
            "deadline_type": "passed",
            "deadline_verified": False,
            "deadline_past": True,
        }

    # 3. Confirmed date — specific month+date already in the deadline field
    if deadline_field and CONFIRMED_DATE_RE.search(deadline_field):
        return {
            "deadline_verified": True,
            "deadline_type": "confirmed_date",
        }

    # 4. Annual inferred — deadline field has a year and a month name but
    #    deadline_verified is still False (covers "June 2025" style entries)
    if deadline_field:
        has_year = YEAR_ONLY_RE.search(deadline_field)
        has_month = re.search(MONTH_NAMES, deadline_field, re.IGNORECASE)
        if has_year and has_month:
            return {
                "deadline_verified": True,
                "deadline_type": "annual_inferred",
            }

    # 5. Check schedule
    if contains_any(blob, CHECK_SCHEDULE_TERMS):
        return {
            "deadline_type": "check_schedule",
            "deadline_verified": False,
        }

    return {}


def main():
    if not COMPACT_PATH.exists():
        print(f"ERROR: {COMPACT_PATH} not found — nothing to process.")
        return

    with COMPACT_PATH.open(encoding="utf-8") as f:
        opportunities = json.load(f)

    if not isinstance(opportunities, list):
        print("ERROR: compact_opportunities.json is not a list.")
        return

    counts = {
        "rolling": 0,
        "confirmed_date": 0,
        "annual_inferred": 0,
        "check_schedule": 0,
        "closed": 0,
        "total_processed": 0,
        "already_verified": 0,
        "downgraded_past": 0,
        "no_match": 0,
    }

    for opp in opportunities:
        if not isinstance(opp, dict):
            continue

        deadline_verified = opp.get("deadline_verified")
        if deadline_verified is True:
            # Self-correct: a previously-verified deadline that is now in the
            # past must be downgraded, not skipped over.
            if deadline_is_past(opp.get("deadline") or ""):
                opp["deadline_verified"] = False
                opp["deadline_type"] = "passed"
                opp["deadline_past"] = True
                counts["downgraded_past"] += 1
            else:
                counts["already_verified"] += 1
            continue

        counts["total_processed"] += 1
        blob = build_text_blob(opp)
        deadline_field = opp.get("deadline") or ""

        updates = classify_deadline(blob, deadline_field)
        if updates:
            dtype = updates.get("deadline_type", "unknown")
            if dtype in counts:
                counts[dtype] += 1
            else:
                counts[dtype] = 1
            opp.update(updates)
        else:
            counts["no_match"] += 1

    # Write back
    COMPACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with COMPACT_PATH.open("w", encoding="utf-8") as f:
        json.dump(opportunities, f, ensure_ascii=False, indent=2)

    print("Deadline normalisation complete.")
    print(f"  Already verified (skipped)  : {counts['already_verified']}")
    print(f"  Downgraded (deadline passed): {counts['downgraded_past']}")
    print(f"  Total processed             : {counts['total_processed']}")
    print(f"  Rolling found               : {counts['rolling']}")
    print(f"  Confirmed date              : {counts['confirmed_date']}")
    print(f"  Annual inferred             : {counts['annual_inferred']}")
    print(f"  Check schedule              : {counts['check_schedule']}")
    print(f"  Closed/passed               : {counts['closed']}")
    print(f"  No pattern match            : {counts['no_match']}")


if __name__ == "__main__":
    main()
