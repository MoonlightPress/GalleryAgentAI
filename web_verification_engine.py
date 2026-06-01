
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

QUEUE_PATH = "memory/verification_queue.json"
OUT_PATH = "memory/verified_opportunities.json"

EMAIL_RE = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
DATE_RE = r"20[2-9][0-9][-/\.][0-9]{1,2}[-/\.][0-9]{1,2}"

SUBMISSION_WORDS = [
    "submit", "submission", "apply", "application", "entry",
    "open call", "artist call", "opportunity", "opportunities",
    "contest", "award", "exhibition",
    "応募", "公募", "募集", "出展", "申し込み", "申込"
]

CONTACT_WORDS = [
    "contact", "about", "inquiry", "inquiries",
    "お問い合わせ", "問合せ", "連絡", "会社概要"
]

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8,zh;q=0.7",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def fetch_with_fallback(url):
    r = requests.get(url, timeout=20, headers=BROWSER_HEADERS)
    if r.status_code < 400:
        return r
    parsed = urlparse(url)
    root = f"{parsed.scheme}://{parsed.netloc}/"
    if root.rstrip("/") != url.rstrip("/"):
        try:
            r2 = requests.get(root, timeout=20, headers=BROWSER_HEADERS)
            if r2.status_code < 400:
                return r2
        except Exception:
            pass
    return r


def load_json(path, fallback):
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return fallback


def save_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def same_domain(a, b):
    try:
        da = urlparse(a).netloc.lower().replace("www.", "")
        db = urlparse(b).netloc.lower().replace("www.", "")
        return da == db
    except Exception:
        return False


def classify_link(label, href):
    blob = f"{label} {href}".lower()

    if any(word in blob for word in SUBMISSION_WORDS):
        return "submission_candidate"

    if any(word in blob for word in CONTACT_WORDS):
        return "contact_candidate"

    return "other"


def extract_links(html, base_url, limit=250):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a.get("href", "").strip())
        label = " ".join(a.get_text(" ", strip=True).split())

        if not href.startswith(("http://", "https://")):
            continue

        if href in seen:
            continue

        seen.add(href)

        kind = classify_link(label, href)

        links.append({
            "label": label[:180],
            "url": href,
            "kind": kind,
            "same_domain": same_domain(base_url, href),
        })

    priority = {
        "submission_candidate": 0,
        "contact_candidate": 1,
        "other": 2,
    }

    links.sort(key=lambda x: (priority.get(x["kind"], 9), not x["same_domain"], x["url"]))
    return links[:limit]


def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return " ".join(soup.get_text(" ", strip=True).split())


def verify_one(item):
    row = dict(item)

    url = row.get("url") or row.get("source_url") or row.get("official_website")

    row["verified"] = False
    row["http_status"] = "not_checked"
    row.setdefault("contact", "unknown")
    row.setdefault("deadline", "unknown")
    row.setdefault("submission_open", "unknown")
    row["contact_candidates"] = []
    row["date_candidates"] = []
    row["relevant_links"] = []

    if not url:
        row["http_status"] = "missing_url"
        return row

    try:
        r = fetch_with_fallback(url)
        row["http_status"] = r.status_code

        if r.status_code >= 400:
            return row

        html = r.text
        text = extract_text(html)
        low = text.lower()

        emails = list(dict.fromkeys(re.findall(EMAIL_RE, html)))
        dates = list(dict.fromkeys(re.findall(DATE_RE, text)))
        links = extract_links(html, url)

        row["verified"] = True
        row["relevant_links"] = links
        row["contact_candidates"] = emails[:10]
        row["date_candidates"] = dates[:10]

        if emails:
            row["contact"] = emails[0]

        if dates:
            row["deadline"] = dates[0]

        if any(word in low for word in SUBMISSION_WORDS) or any(
            link["kind"] == "submission_candidate" for link in links
        ):
            row["submission_open"] = "possible"
        else:
            row["submission_open"] = "unknown"

    except Exception as e:
        row["http_status"] = "error"
        row["error"] = str(e)

    return row


def main():
    queue = load_json(QUEUE_PATH, [])

    if not queue:
        raise SystemExit("Missing or empty memory/verification_queue.json")

    results = []

    for i, item in enumerate(queue[:20], start=1):
        print(f"[{i}/20] {item.get('title')}")
        results.append(verify_one(item))

    save_json(OUT_PATH, results)

    print(f"Wrote {OUT_PATH}")
    if results:
        print("First record keys:", sorted(results[0].keys()))
        print("First record link count:", len(results[0].get("relevant_links", [])))


if __name__ == "__main__":
    main()
