
import json
import os
import re
from pathlib import Path

SCRAPED_PATHS = [
    "ingestion/scraped_pages.json",
    "ingestion/deep_crawl_results.json",
]

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/deadline_evidence.json"
REPORT_PATH = "reports/deadline_evidence_report.md"

DATE_PATTERNS = [
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}\b",
    r"\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\b",
    r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b",
    r"\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b",
]

DEADLINE_WORDS = [
    "deadline",
    "apply by",
    "apply before",
    "application deadline",
    "submit by",
    "applications close",
    "applications due",
    "entry deadline",
    "entry closes",
    "last day to apply",
    "closes",
    "due",
    "until",
    "submission deadline",
    "応募締切", "締切", "申込締切", "受付締切",
]

EVENT_DATE_WORDS = [
    "exhibition date",
    "exhibition period",
    "exhibition runs",
    "event date",
    "event dates",
    "fair date",
    "fair dates",
    "show dates",
    "on view",
    "opening night",
    "opening reception",
    "runs from",
    "runs through",
    "会期", "開催期間", "開催日", "展示期間",
]


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def source_name(record):
    return record.get("source_name") or record.get("source") or record.get("title") or "Unknown"


def text_of(record):
    return record.get("text") or record.get("text_excerpt") or ""


def extract_deadline_snippets(text):
    text = re.sub(r"\s+", " ", text or "")
    lower = text.lower()

    deadline_snippets = []
    event_date_snippets = []

    for word in DEADLINE_WORDS:
        start = lower.find(word)
        if start == -1:
            continue
        snippet = text[max(0, start - 180): min(len(text), start + 360)]
        deadline_snippets.append(snippet)

    for word in EVENT_DATE_WORDS:
        start = lower.find(word)
        if start == -1:
            continue
        snippet = text[max(0, start - 180): min(len(text), start + 360)]
        event_date_snippets.append(snippet)

    date_hits = []

    for pattern in DATE_PATTERNS:
        for match in re.finditer(pattern, text):
            date_hits.append(match.group(0))
            start = match.start()
            snippet = text[max(0, start - 180): min(len(text), start + 260)]
            deadline_snippets.append(snippet)

    def dedupe(lst):
        seen = set()
        out = []
        for s in lst:
            if s not in seen:
                seen.add(s)
                out.append(s)
        return out

    return (
        dedupe(deadline_snippets)[:8],
        list(dict.fromkeys(date_hits))[:12],
        dedupe(event_date_snippets)[:4],
    )


def main():
    records = []

    for path in SCRAPED_PATHS:
        records.extend(load_json(path, []))

    evidence = {}

    for record in records:
        name = source_name(record)
        snippets, dates, event_snippets = extract_deadline_snippets(text_of(record))

        if snippets or dates or event_snippets:
            evidence[name] = {
                "source_name": name,
                "source_url": record.get("final_url") or record.get("source_url") or record.get("url") or "",
                "deadline_snippets": snippets,
                "event_date_snippets": event_snippets,
                "date_hits": dates,
                "confidence": "medium" if dates else "low"
            }

    save_json(OUT_PATH, evidence)

    lines = [
        "# Deadline Evidence Report",
        "",
        "This report extracts deadline-like language and date strings from scraped pages.",
        ""
    ]

    for name, item in evidence.items():
        lines.append(f"## {name}")
        lines.append(f"- Confidence: {item.get('confidence')}")
        lines.append(f"- Dates: {', '.join(item.get('date_hits', [])) or 'none found'}")
        lines.append(f"- Source: {item.get('source_url')}")
        lines.append("")
        for snippet in item.get("deadline_snippets", [])[:3]:
            lines.append(f"> {snippet}")
            lines.append("")

    Path(REPORT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
