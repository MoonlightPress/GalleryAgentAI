
import json
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SRC = "memory/ranked_submission_links.json"
OUT = "memory/application_page_results.json"

HEADERS = {"User-Agent": "Mozilla/5.0 (MochiApplicationCrawler/1.0)"}

EMAIL_RE = r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
DATE_RE = [
    r"\b20[2-9][0-9][-/\.][0-9]{1,2}[-/\.][0-9]{1,2}\b",
    r"\b[0-9]{1,2}[-/\.][0-9]{1,2}[-/\.]20[2-9][0-9]\b",
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+[0-9]{1,2},?\s+20[2-9][0-9]\b",
    r"\b20[2-9][0-9]年\s*[0-9]{1,2}月\s*[0-9]{1,2}日\b",
]

REQUIREMENT_TERMS = [
    "portfolio", "artist statement", "cv", "resume", "images",
    "作品", "ポートフォリオ", "ステートメント", "略歴", "画像",
    "fee", "entry fee", "application fee", "応募料", "参加費",
    "deadline", "締切", "締め切り", "due"
]

def fetch(url):
    try:
        r = requests.get(url, timeout=15, headers=HEADERS, allow_redirects=True)
        return r.status_code, r.url, r.text, None
    except Exception as e:
        return None, url, "", str(e)

def visible_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return " ".join(soup.get_text(" ", strip=True).split())

def extract_dates(text):
    out = []
    for pat in DATE_RE:
        out.extend(re.findall(pat, text, flags=re.I))
    return list(dict.fromkeys(out))[:12]

def extract_requirements(text):
    low = text.lower()
    hits = []
    for term in REQUIREMENT_TERMS:
        if term.lower() in low:
            hits.append(term)
    return hits[:20]

def main():
    data = json.load(open(SRC, encoding="utf-8"))

    for item in data:
        pages = []
        for link in item.get("ranked_submission_links", [])[:3]:
            url = link.get("url")
            if not url:
                continue

            status, final_url, html, error = fetch(url)
            result = {
                "label": link.get("label"),
                "url": url,
                "final_url": final_url,
                "http_status": status,
                "error": error,
                "emails": [],
                "date_candidates": [],
                "requirement_hits": [],
                "text_preview": "",
            }

            if html:
                text = visible_text(html)
                result["emails"] = list(dict.fromkeys(re.findall(EMAIL_RE, text)))[:8]
                result["date_candidates"] = extract_dates(text)
                result["requirement_hits"] = extract_requirements(text)
                result["text_preview"] = text[:700]

            pages.append(result)
            time.sleep(0.4)

        item["application_page_results"] = pages

    json.dump(data, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
