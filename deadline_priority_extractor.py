
import re

DATE_PATTERNS = [
    r"\b20[2-9][0-9][-/\.][0-9]{1,2}[-/\.][0-9]{1,2}\b",
    r"\b[0-9]{1,2}[-/\.][0-9]{1,2}[-/\.]20[2-9][0-9]\b",
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+[0-9]{1,2},?\s+20[2-9][0-9]\b",
    r"\b20[2-9][0-9]年\s*[0-9]{1,2}月\s*[0-9]{1,2}日\b",
    r"\b[0-9]{1,2}月\s*[0-9]{1,2}日\b",
]

DEADLINE_TERMS = [
    "deadline", "due", "application deadline", "submission deadline",
    "締切", "締め切り", "応募締切", "申込締切", "応募期間", "受付期間",
]

BAD_DATE_CONTEXT = [
    "event date", "会期", "開催", "venue", "open hours", "hours",
    "exhibition period", "展示期間"
]

def sentence_split(text):
    chunks = re.split(r"(?<=[.!?。])\s+|\n", text or "")
    return [" ".join(c.split()) for c in chunks if c and c.strip()]

def extract_deadline_candidates(text):
    candidates = []
    for sent in sentence_split(text):
        dates = []
        for pat in DATE_PATTERNS:
            dates.extend(re.findall(pat, sent, flags=re.I))
        if not dates:
            continue

        low = sent.lower()
        score = 0
        if any(t.lower() in low for t in DEADLINE_TERMS):
            score += 100
        if any(t.lower() in low for t in BAD_DATE_CONTEXT):
            score -= 50
        if len(sent) < 240:
            score += 10

        for d in dates:
            candidates.append({
                "date": d,
                "sentence": sent,
                "deadline_score": score,
            })

    candidates.sort(key=lambda x: x["deadline_score"], reverse=True)
    return candidates

def best_deadline(text):
    candidates = extract_deadline_candidates(text)
    if not candidates:
        return "unknown", "", []
    best = candidates[0]
    if best["deadline_score"] <= 0:
        return "unknown", "", candidates
    return best["date"], best["sentence"], candidates
