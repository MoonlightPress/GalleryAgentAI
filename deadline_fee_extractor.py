
import json
import re
from pathlib import Path
from datetime import datetime

SRC = "memory/submission_requirements.json"
OUT = "memory/submission_intelligence.json"

FEE_PATTERNS = [
    r"¥\s?[0-9,]+",
    r"￥\s?[0-9,]+",
    r"\$\s?[0-9,]+",
    r"£\s?[0-9,]+",
    r"€\s?[0-9,]+",
    r"[0-9,]+\s?円",
    r"[0-9,]+\s?yen",
    r"[0-9,]+\s?JPY",
    r"[0-9,]+\s?USD",
    r"[0-9,]+\s?GBP",
]

DEADLINE_WORDS = [
    "deadline", "due", "apply by", "submission deadline", "entry deadline",
    "締切", "締め切り", "応募締切", "募集締切", "申込締切"
]

def extract_fees(text):
    found = []
    for pat in FEE_PATTERNS:
        found.extend(re.findall(pat, text, flags=re.I))
    return list(dict.fromkeys(found))[:10]

def choose_deadline(page):
    text = page.get("full_text", "")
    dates = page.get("date_candidates", [])

    if not dates:
        return "unknown", 0.0

    low = text.lower()
    for d in dates:
        idx = low.find(str(d).lower())
        if idx >= 0:
            window = low[max(0, idx-120):idx+120]
            if any(w.lower() in window for w in DEADLINE_WORDS):
                return d, 0.9

    current_year = datetime.now().year
    for d in dates:
        if str(current_year) in str(d) or str(current_year + 1) in str(d):
            return d, 0.6

    return dates[0], 0.25

def main():
    pages = json.loads(Path(SRC).read_text(encoding="utf-8"))

    for page in pages:
        text = page.get("full_text", "")
        fees = extract_fees(text)
        deadline, confidence = choose_deadline(page)

        page["fee_candidates"] = fees
        page["best_fee"] = fees[0] if fees else "unknown"
        page["best_deadline"] = deadline
        page["deadline_confidence"] = confidence

    Path(OUT).write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
