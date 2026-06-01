
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SRC = "memory/submission_targets.json"
OUT = "memory/submission_pages.json"

EMAIL_RE = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
DATE_PATTERNS = [
    r"20[2-9][0-9][-/\.][0-9]{1,2}[-/\.][0-9]{1,2}",
    r"[0-9]{1,2}[-/\.][0-9]{1,2}[-/\.]20[2-9][0-9]",
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+[0-9]{1,2},?\s+20[2-9][0-9]",
    r"20[2-9][0-9]年\s*[0-9]{1,2}月\s*[0-9]{1,2}日",
]

def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    text = " ".join(soup.get_text(" ", strip=True).split())
    return title, text

def fetch(url):
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code >= 400:
            return None, f"http_{r.status_code}"
        return r.text, "ok"
    except Exception as e:
        return None, str(e)

def extract_dates(text):
    found = []
    for pat in DATE_PATTERNS:
        found.extend(re.findall(pat, text, flags=re.I))
    return list(dict.fromkeys(found))[:20]

def main():
    data = json.loads(Path(SRC).read_text(encoding="utf-8"))
    pages = []

    for item in data:
        title = item.get("title")
        links = item.get("submission_links", [])[:8]

        for link in links:
            url = link.get("url")
            if not url:
                continue

            print(f"Reading {title}: {url}")
            html, status = fetch(url)

            row = {
                "source_title": title,
                "source_contact": item.get("contact", "unknown"),
                "submission_page_url": url,
                "link_label": link.get("label", ""),
                "fetch_status": status,
                "page_title": "",
                "emails": [],
                "date_candidates": [],
                "text_excerpt": "",
                "full_text": "",
            }

            if html:
                page_title, text = clean_text(html)
                row["page_title"] = page_title
                row["emails"] = list(dict.fromkeys(re.findall(EMAIL_RE, html)))[:10]
                row["date_candidates"] = extract_dates(text)
                row["text_excerpt"] = text[:1200]
                row["full_text"] = text[:15000]

            pages.append(row)

    Path("memory").mkdir(exist_ok=True)
    Path(OUT).write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Pages read: {len(pages)}")

if __name__ == "__main__":
    main()
