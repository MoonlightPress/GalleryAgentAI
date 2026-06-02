
import json
import re
import sys
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SRC = "memory/verified_opportunities.json"
TARGETS_OUT = "memory/submission_targets.json"
REPORT = "reports/submission_link_report.md"

MAX_LINKS_PER_OPP = 3

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
    "Connection": "keep-alive",
}

SUBMISSION_KEYWORDS = [
    "submit", "submission", "apply", "application", "entry",
    "open call", "artist call", "contest", "award",
    "応募", "公募", "募集", "出展", "申し込み", "申込",
]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

DATE_PATTERNS = [
    re.compile(r"20[2-9][0-9][-/\.][0-9]{1,2}[-/\.][0-9]{1,2}"),
    re.compile(r"[0-9]{1,2}[-/\.][0-9]{1,2}[-/\.]20[2-9][0-9]"),
    re.compile(
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+[0-9]{1,2},?\s+20[2-9][0-9]",
        re.I,
    ),
    re.compile(r"20[2-9][0-9]年\s*[0-9]{1,2}月\s*[0-9]{1,2}日"),
]

_DATE_PAT = re.compile(
    r"\b(?:20\d{2}[-/\.]\d{1,2}[-/\.]\d{1,2}"
    r"|\d{1,2}[-/\.]\d{1,2}[-/\.]20\d{2}"
    r"|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\w*\.?\s+\d{1,2},?\s+20\d{2}"
    r"|20\d{2}年\s*\d{1,2}月\s*\d{1,2}日)\b",
    re.I,
)

# Phrases that indicate an application deadline (when to submit by)
_DEADLINE_SIGNALS = [
    "deadline", "apply by", "apply before", "application deadline",
    "submit by", "submission deadline", "applications close", "applications due",
    "entry deadline", "entry closes", "last day to apply", "application due",
    "応募締切", "締切", "申込締切", "受付締切",
]

# Phrases that indicate event/exhibition dates (when the show happens)
_EVENT_DATE_SIGNALS = [
    "exhibition date", "exhibition period", "exhibition runs", "on view",
    "event date", "event dates", "fair date", "fair dates", "show dates",
    "opening night", "opening reception", "runs from", "runs through",
    "会期", "開催期間", "開催日", "展示期間",
]


def _classify_date_hit(text, start, end):
    """Return 'deadline', 'event_date', or 'unknown' based on surrounding text."""
    window = text[max(0, start - 200): end + 200].lower()
    for sig in _DEADLINE_SIGNALS:
        if sig in window:
            return "deadline"
    for sig in _EVENT_DATE_SIGNALS:
        if sig in window:
            return "event_date"
    return "unknown"


def extract_classified_dates(text):
    """
    Scan page text for dates and classify as deadline vs event_date by context.
    Returns lists of classified date strings.
    """
    deadlines = []
    event_dates = []
    seen = set()
    for m in _DATE_PAT.finditer(text):
        val = m.group(0)
        if val in seen:
            continue
        seen.add(val)
        kind = _classify_date_hit(text, m.start(), m.end())
        if kind == "deadline":
            deadlines.append(val)
        elif kind == "event_date":
            event_dates.append(val)
    return {"deadlines": deadlines[:5], "event_dates": event_dates[:5]}

# Matches currency amounts near fee-related words, or explicit free-entry phrases
FEE_CONTEXT_RE = re.compile(
    r"(?:fee|entry|submission|cost|charge)[^.]{0,80}?(?:£|€|\$|¥|USD|GBP|EUR|JPY)\s*[\d,]+"
    r"|(?:£|€|\$|¥|USD|GBP|EUR|JPY)\s*[\d,]+[^.]{0,60}?(?:fee|entry|submission)"
    r"|(?:no\s+fee|free\s+(?:to\s+)?(?:submit|enter)|free\s+entry|no\s+charge)",
    re.I,
)

REQUIREMENTS_TRIGGERS = re.compile(
    r"\b(?:eligib\w+|requirement\w*|must\s+(?:be|submit|have)|"
    r"size\s+limit|maximum\s+(?:of\s+)?\d|submit\s+up\s+to|"
    r"open\s+to\s+(?:all|artist)|accepted\s+(?:medium|format|work))\b",
    re.I,
)


def score_link(link):
    kind = link.get("kind", "")
    same_domain = link.get("same_domain", False)
    blob = f"{link.get('label', '')} {link.get('url', '')}".lower()
    keyword_hit = any(k in blob for k in SUBMISSION_KEYWORDS)

    if kind == "submission_candidate" and same_domain:
        return 3
    if kind == "submission_candidate":
        return 2
    if keyword_hit:
        return 1
    return 0


def select_links(relevant_links):
    scored = [(score_link(l), l) for l in relevant_links]
    scored = [(s, l) for s, l in scored if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    # Deduplicate by URL
    seen = set()
    result = []
    for _, l in scored:
        url = l.get("url", "")
        if url and url not in seen:
            seen.add(url)
            result.append(l)
        if len(result) >= MAX_LINKS_PER_OPP:
            break
    return result


def fetch(url):
    try:
        r = requests.get(url, timeout=15, headers=BROWSER_HEADERS)
        if r.status_code >= 400:
            return None, f"http_{r.status_code}"
        return r.text, "ok"
    except Exception as e:
        return None, str(e)[:80]


def parse_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return " ".join(soup.get_text(" ", strip=True).split())


def extract_emails(html):
    found = list(dict.fromkeys(EMAIL_RE.findall(html)))
    # Drop image filenames that match the email pattern
    return [e for e in found if not re.search(r"\.(png|jpg|gif|svg|webp)$", e, re.I)][:10]


def extract_dates(text):
    found = []
    for pat in DATE_PATTERNS:
        found.extend(pat.findall(text))
    return list(dict.fromkeys(found))[:10]


def extract_fees(text):
    return list(dict.fromkeys(m.group(0).strip() for m in FEE_CONTEXT_RE.finditer(text)))[:5]


def extract_requirements(text):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    hits = [s.strip() for s in sentences if REQUIREMENTS_TRIGGERS.search(s)]
    return [h[:300] for h in hits[:3]]


def crawl_opportunity(item):
    selected = select_links(item.get("relevant_links", []))
    item["submission_links"] = selected

    pages = []
    for link in selected:
        url = link.get("url", "")
        if not url:
            continue
        print(f"  Fetching: {url}")
        html, status = fetch(url)

        page = {
            "url": url,
            "label": link.get("label", ""),
            "status": status,
            "emails": [],
            "date_candidates": [],
            "deadline_candidates": [],
            "event_date_candidates": [],
            "fee_candidates": [],
            "requirements_excerpt": [],
        }

        if html:
            text = parse_text(html)
            page["emails"] = extract_emails(html)
            page["date_candidates"] = extract_dates(text)
            classified = extract_classified_dates(text)
            page["deadline_candidates"] = classified["deadlines"]
            page["event_date_candidates"] = classified["event_dates"]
            page["fee_candidates"] = extract_fees(text)
            page["requirements_excerpt"] = extract_requirements(text)

        pages.append(page)

    item["submission_page_data"] = {
        "fetched_at": date.today().isoformat(),
        "pages": pages,
        "all_emails": list(dict.fromkeys(e for p in pages for e in p["emails"])),
        "all_dates": list(dict.fromkeys(d for p in pages for d in p["date_candidates"])),
        "all_deadline_candidates": list(dict.fromkeys(d for p in pages for d in p["deadline_candidates"])),
        "all_event_date_candidates": list(dict.fromkeys(d for p in pages for d in p["event_date_candidates"])),
        "all_fees": list(dict.fromkeys(f for p in pages for f in p["fee_candidates"])),
    }

    return item


def main():
    data = json.loads(Path(SRC).read_text(encoding="utf-8"))
    report_lines = ["# Submission Link Report", ""]

    for item in data:
        title = item.get("title", "Unknown")
        print(f"\n{title}")

        existing = item.get("submission_page_data", {})
        if existing.get("pages"):
            print(f"  Skipping — already fetched {len(existing['pages'])} page(s) on {existing.get('fetched_at', '?')}")
            report_lines.append(f"## {title} [cached]")
            report_lines.append(f"- Pages already fetched: {len(existing['pages'])}")
            report_lines.append("")
            continue

        item = crawl_opportunity(item)
        spd = item["submission_page_data"]

        report_lines.append(f"## {title}")
        report_lines.append(f"- Links fetched: {len(spd['pages'])}")
        for p in spd["pages"]:
            report_lines.append(f"  - [{p['status']}] {p['label'] or p['url']}")
            if p["date_candidates"]:
                report_lines.append(f"    Dates: {', '.join(p['date_candidates'][:3])}")
            if p["fee_candidates"]:
                report_lines.append(f"    Fees: {'; '.join(p['fee_candidates'][:2])}")
            if p["emails"]:
                report_lines.append(f"    Emails: {', '.join(p['emails'][:2])}")
            if p["requirements_excerpt"]:
                report_lines.append(f"    Requirements: {p['requirements_excerpt'][0][:120]}…")
        if spd["all_dates"]:
            report_lines.append(f"- All dates found: {', '.join(spd['all_dates'][:5])}")
        report_lines.append("")

    Path(SRC).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {SRC}")

    Path(TARGETS_OUT).parent.mkdir(parents=True, exist_ok=True)
    Path(TARGETS_OUT).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {TARGETS_OUT}")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
