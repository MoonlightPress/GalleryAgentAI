
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


SOURCE_PATH = "source_targets.json"
OUT_PATH = "ingestion/scraped_pages.json"
TIMEOUT = 14


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def clean_text(text):
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[:6000]


def fetch(url):
    headers = {
        "User-Agent": "Mozilla/5.0 MochiResearchBot/0.1 artist-opportunity-research"
    }

    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        return response.status_code, response.url, response.text
    except Exception as e:
        return 0, url, f"FETCH_ERROR: {e}"


def extract_links(base_url, soup):
    links = []

    for a in soup.find_all("a"):
        href = a.get("href")
        label = clean_text(a.get_text(" "))

        if not href:
            continue

        full = urljoin(base_url, href)

        if full.startswith("http"):
            links.append({
                "label": label[:180],
                "url": full
            })

    seen = set()
    unique = []

    for link in links:
        if link["url"] not in seen:
            seen.add(link["url"])
            unique.append(link)

    return unique[:80]


def page_record(source):
    status, final_url, html = fetch(source["url"])

    record = {
        "source_name": source["name"],
        "source_url": source["url"],
        "final_url": final_url,
        "status_code": status,
        "source_type": source.get("source_type", ""),
        "region": source.get("region", ""),
        "priority": source.get("priority", ""),
        "title": "",
        "text": "",
        "links": [],
        "error": "",
    }

    if status != 200:
        record["error"] = html[:500]
        return record

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    if soup.title:
        record["title"] = clean_text(soup.title.get_text(" "))

    record["text"] = clean_text(soup.get_text(" "))
    record["links"] = extract_links(final_url, soup)

    return record


def main():
    config = load_json(SOURCE_PATH, {})
    sources = config.get("seed_sources", [])

    if not sources:
        raise SystemExit("No sources found in source_targets.json")

    records = []

    for source in sources:
        print(f"Fetching {source['name']}...")
        records.append(page_record(source))
        time.sleep(0.8)

    save_json(OUT_PATH, records)

    print(f"Wrote {OUT_PATH}")
    print(f"Fetched {len(records)} sources.")


if __name__ == "__main__":
    main()
