
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SRC = "memory/actionable_targets.json"
OUT = "memory/official_page_extractions.json"
REPORT = "reports/official_page_extraction_report.md"
CACHE = Path("verification_cache/official_pages")

HEADERS = {"User-Agent": "Mozilla/5.0 (MochiOfficialExtractor/1.0)"}

EMAIL_RE = r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"

DATE_PATTERNS = [
    r"\b20[2-9][0-9][-/\.][0-9]{1,2}[-/\.][0-9]{1,2}\b",
    r"\b[0-9]{1,2}[-/\.][0-9]{1,2}[-/\.]20[2-9][0-9]\b",
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+[0-9]{1,2},?\s+20[2-9][0-9]\b",
    r"\b20[2-9][0-9]年\s*[0-9]{1,2}月\s*[0-9]{1,2}日\b",
]

FEE_PATTERNS = [
    r"(?:entry fee|application fee|submission fee|fee|応募料|参加費|出展料|料金)[^\n。.:：]{0,80}[.:：]?\s*([$£€¥]\s?[0-9,]+|[0-9,]+\s?(?:yen|円|jpy|usd|gbp|eur|pounds?))",
    r"([$£€¥]\s?[0-9,]+|[0-9,]+\s?(?:yen|円|jpy|usd|gbp|eur|pounds?))[^\n。]{0,80}(?:entry fee|application fee|submission fee|応募料|参加費|出展料|fee)",
]

REQUIREMENT_TERMS = {
    "portfolio": ["portfolio", "ポートフォリオ"],
    "artist_statement": ["artist statement", "statement", "ステートメント"],
    "bio_cv": ["cv", "resume", "bio", "biography", "略歴", "プロフィール"],
    "images": ["images", "jpg", "jpeg", "png", "画像", "作品画像"],
    "work_details": ["title", "medium", "dimensions", "year", "作品名", "サイズ", "技法", "制作年"],
    "pdf": ["pdf", "PDF"],
    "zine_book": ["book", "zine", "publication", "artist book", "冊子", "ZINE"],
}

ELIGIBILITY_TERMS = [
    "eligibility", "eligible", "open to", "artists", "international",
    "応募資格", "対象", "参加資格", "応募条件"
]

DEADLINE_TERMS = ["deadline", "due", "締切", "締め切り", "応募期間", "application period", "受付期間"]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def safe_name(text):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", str(text or "untitled"))[:80].strip("_") or "untitled"

def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
        r.encoding = r.apparent_encoding or r.encoding
        return {
            "status": r.status_code,
            "final_url": r.url,
            "html": r.text,
            "error": None,
        }
    except Exception as e:
        return {
            "status": None,
            "final_url": url,
            "html": "",
            "error": str(e),
        }

def visible_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    return "\n".join([line.strip() for line in soup.get_text("\n").splitlines() if line.strip()])

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        label = " ".join(a.get_text(" ", strip=True).split())
        url = urljoin(base_url, a["href"])
        blob = (label + " " + url).lower()
        if any(k in blob for k in ["contact", "inquiry", "apply", "application", "open call", "submit", "応募", "募集", "お問い合わせ"]):
            links.append({"label": label, "url": url})
    out = []
    seen = set()
    for link in links:
        if link["url"] not in seen:
            seen.add(link["url"])
            out.append(link)
    return out[:20]

def extract_dates(text):
    found = []
    for pat in DATE_PATTERNS:
        found.extend(re.findall(pat, text, flags=re.I))
    return list(dict.fromkeys(found))[:20]

def extract_fees(text):
    found = []
    for pat in FEE_PATTERNS:
        found.extend(re.findall(pat, text, flags=re.I))
    cleaned = []
    for x in found:
        if isinstance(x, tuple):
            x = next((p for p in x if p), "")
        if x and x not in cleaned:
            cleaned.append(x)
    return cleaned[:10]

def extract_requirement_hits(text):
    low = text.lower()
    hits = []
    for key, terms in REQUIREMENT_TERMS.items():
        if any(term.lower() in low for term in terms):
            hits.append(key)
    return hits

def sentence_hits(text, terms, limit=5):
    chunks = re.split(r"(?<=[.!?。])\s+|\n", text)
    hits = []
    for chunk in chunks:
        c = " ".join(chunk.split())
        if len(c) < 20 or len(c) > 350:
            continue
        low = c.lower()
        if any(term.lower() in low for term in terms):
            hits.append(c)
    return hits[:limit]

def choose_urls(target):
    urls = []
    for key in ["official_submission_url", "best_link"]:
        if target.get(key) and target.get(key) != "unknown":
            urls.append(target[key])
    for u in target.get("source_urls", []):
        if u and u not in urls:
            urls.append(u)
    return urls[:4]

def extract_target(target):
    title = target.get("title")
    urls = choose_urls(target)

    pages = []
    all_text = []

    for url in urls:
        result = fetch(url)
        html = result["html"]
        text = visible_text(html) if html else ""
        links = extract_links(html, result["final_url"]) if html else []

        CACHE.mkdir(parents=True, exist_ok=True)
        if html:
            (CACHE / f"{safe_name(title)}_{safe_name(url)}.html").write_text(html, encoding="utf-8", errors="ignore")

        pages.append({
            "url": url,
            "final_url": result["final_url"],
            "http_status": result["status"],
            "error": result["error"],
            "text_length": len(text),
            "emails": list(dict.fromkeys(re.findall(EMAIL_RE, text)))[:10],
            "dates": extract_dates(text),
            "fees": extract_fees(text),
            "requirements": extract_requirement_hits(text),
            "deadline_clues": sentence_hits(text, DEADLINE_TERMS),
            "eligibility_clues": sentence_hits(text, ELIGIBILITY_TERMS),
            "relevant_links": links,
            "text_preview": text[:1200],
        })

        all_text.append(text)
        time.sleep(0.4)

    combined = "\n".join(all_text)

    emails = []
    dates = []
    fees = []
    reqs = []
    deadline_clues = []
    eligibility_clues = []
    relevant_links = []

    for p in pages:
        emails += p["emails"]
        dates += p["dates"]
        fees += p["fees"]
        reqs += p["requirements"]
        deadline_clues += p["deadline_clues"]
        eligibility_clues += p["eligibility_clues"]
        relevant_links += p["relevant_links"]

    return {
        "title": title,
        "source_urls_checked": urls,
        "pages": pages,
        "emails": list(dict.fromkeys(emails))[:10],
        "dates": list(dict.fromkeys(dates))[:20],
        "fees": list(dict.fromkeys(fees))[:10],
        "requirements": list(dict.fromkeys(reqs)),
        "deadline_clues": list(dict.fromkeys(deadline_clues))[:8],
        "eligibility_clues": list(dict.fromkeys(eligibility_clues))[:8],
        "relevant_links": relevant_links[:20],
    }

def main():
    targets = load(SRC, [])
    if not targets:
        raise SystemExit("memory/actionable_targets.json is missing or empty. Run run_actionable_target_builder.py first.")

    # Focus: top near-actionable targets only.
    targets = targets[:6]

    results = [extract_target(t) for t in targets]

    Path("memory").mkdir(exist_ok=True)
    json.dump(results, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = ["# Official Page Extraction Report", "", "Fuller extraction from official/application pages.", ""]
    for r in results:
        lines.append(f"## {r['title']}")
        lines.append(f"- URLs checked: {len(r['source_urls_checked'])}")
        lines.append(f"- Emails: {', '.join(r['emails']) or 'none'}")
        lines.append(f"- Dates: {', '.join(r['dates'][:6]) or 'none'}")
        lines.append(f"- Fees: {', '.join(r['fees']) or 'none'}")
        lines.append(f"- Requirements: {', '.join(r['requirements']) or 'none'}")
        if r["deadline_clues"]:
            lines.append("")
            lines.append("### Deadline clues")
            for c in r["deadline_clues"][:4]:
                lines.append(f"- {c}")
        if r["eligibility_clues"]:
            lines.append("")
            lines.append("### Eligibility clues")
            for c in r["eligibility_clues"][:4]:
                lines.append(f"- {c}")
        if r["relevant_links"]:
            lines.append("")
            lines.append("### Relevant links")
            for link in r["relevant_links"][:6]:
                lines.append(f"- {link.get('label') or '[no label]'} — {link.get('url')}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT)
    print("Wrote", REPORT)

if __name__ == "__main__":
    main()
