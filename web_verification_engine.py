
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

QUEUE = "memory/verification_queue.json"
OUT = "memory/verified_opportunities.json"
REPORT = "reports/web_verification_report.md"

EMAIL_RE = r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
DATE_RE = [
    r"\b20[2-9][0-9][-/\.][0-9]{1,2}[-/\.][0-9]{1,2}\b",
    r"\b20[2-9][0-9]年\s*[0-9]{1,2}月\s*[0-9]{1,2}日\b",
]

SUBMISSION_TERMS = [
    "open call", "submission", "submit", "apply", "application", "entry",
    "artist call", "opportunity", "exhibition", "contest", "award",
    "応募", "公募", "募集", "申込", "エントリー"
]

CONTACT_TERMS = [
    "contact", "about", "inquiry", "お問い合わせ", "問合せ", "アクセス"
]

HEADERS = {"User-Agent": "Mozilla/5.0 (MochiVerifier/2.0)"}


def load(path, fallback):
    if Path(path).exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback


def save(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    json.dump(data, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


def normalize_url(url):
    url = str(url or "").strip()
    if url and not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def same_domain(a, b):
    try:
        return urlparse(a).netloc.replace("www.", "") == urlparse(b).netloc.replace("www.", "")
    except Exception:
        return False


def fetch(url):
    try:
        r = requests.get(url, timeout=15, headers=HEADERS, allow_redirects=True)
        response.encoding = response.apparent_encoding
        return r.status_code, r.text, r.url, None
    except Exception as e:
        return None, "", url, str(e)


def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a.get("href", ""))
        label = " ".join(a.get_text(" ", strip=True).split())
        if not href.startswith(("http://", "https://")):
            continue

        blob = (label + " " + href).lower()

        link_type = "other"
        if any(t in blob for t in SUBMISSION_TERMS):
            link_type = "submission"
        elif any(t in blob for t in CONTACT_TERMS):
            link_type = "contact"

        links.append({
            "label": label[:160],
            "url": href,
            "type": link_type,
            "same_domain": same_domain(base_url, href),
        })

    out = []
    seen = set()
    for link in links:
        if link["url"] in seen:
            continue
        seen.add(link["url"])
        out.append(link)

    out.sort(key=lambda x: (
        0 if x["type"] == "submission" else 1 if x["type"] == "contact" else 2,
        0 if x["same_domain"] else 1,
        x["url"]
    ))

    return out[:200]


def extract_emails(text):
    emails = list(dict.fromkeys(re.findall(EMAIL_RE, text)))
    return [e for e in emails if not e.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))][:10]


def extract_dates(text):
    dates = []
    for pat in DATE_RE:
        dates.extend(re.findall(pat, text))
    return list(dict.fromkeys(dates))[:20]


def visible_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return " ".join(soup.get_text(" ", strip=True).split())


def submission_signal(text, links):
    blob = (text[:50000] + " " + " ".join([l["label"] + " " + l["url"] for l in links])).lower()
    return "possible" if any(t in blob for t in SUBMISSION_TERMS) else "unknown"


def main():
    queue = load(QUEUE, [])
    if not queue:
        raise SystemExit("Missing or empty memory/verification_queue.json")

    results = []

    for i, item in enumerate(queue[:20], 1):
        title = item.get("title", "Unknown")
        url = normalize_url(item.get("url"))
        print(f"[{i}/20] {title}")

        row = dict(item)
        row["url"] = url
        row["verified"] = False
        row["http_status"] = None
        row["submission_open"] = "unknown"
        row["deadline"] = "unknown"
        row["contact"] = "unknown"
        row["relevant_links"] = []
        row["date_candidates"] = []
        row["contact_candidates"] = []

        if not url:
            row["error"] = "missing url"
            results.append(row)
            continue

        status, html, final_url, error = fetch(url)
        row["http_status"] = status
        row["final_url"] = final_url

        if error or not html:
            row["error"] = error or "empty response"
            results.append(row)
            continue

        text = visible_text(html)
        links = extract_links(html, final_url)
        emails = extract_emails(text)
        dates = extract_dates(text)

        row["verified"] = bool(status and status < 400)
        row["relevant_links"] = links
        row["contact_candidates"] = emails
        row["date_candidates"] = dates
        row["contact"] = emails[0] if emails else "unknown"
        row["deadline"] = dates[0] if dates else "unknown"
        row["submission_open"] = submission_signal(text, links)
        row["last_checked"] = time.strftime("%Y-%m-%d")

        results.append(row)

    save(OUT, results)

    lines = ["# Web Verification Report", "", f"Verified records: {len(results)}", ""]
    for row in results:
        lines.append(f"## {row.get('title')}")
        lines.append(f"- URL: {row.get('url')}")
        lines.append(f"- Verified: {row.get('verified')}")
        lines.append(f"- HTTP: {row.get('http_status')}")
        lines.append(f"- Submission signal: {row.get('submission_open')}")
        lines.append(f"- Contact: {row.get('contact')}")
        lines.append(f"- Deadline: {row.get('deadline')}")
        lines.append(f"- Relevant links stored: {len(row.get('relevant_links', []))}")
        sublinks = [l for l in row.get("relevant_links", []) if l.get("type") == "submission"][:8]
        if sublinks:
            lines.append("- Submission-like links:")
            for link in sublinks:
                lines.append(f"  - {link.get('label') or '[no label]'} — {link.get('url')}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Verified:", len(results))
    print("Relevant links added to memory/verified_opportunities.json")
    print("Wrote", REPORT)


if __name__ == "__main__":
    main()
