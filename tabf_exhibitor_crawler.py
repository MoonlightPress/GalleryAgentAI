
import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

OUT_JSON = "memory/tabf_exhibitor_data.json"
OUT_REPORT = "reports/tabf_exhibitor_data.md"

HEADERS = {"User-Agent": "Mozilla/5.0 (MochiTABFCrawler/1.0)"}

SEED_URLS = [
    "https://tokyoartbookfair.com/",
    "https://tokyoartbookfair.com/archives/",
    "https://tokyoartbookfair.com/application/",
]

GOOD_LINK_TERMS = [
    "archive", "archives", "exhibitor", "exhibitors", "publisher", "publishers",
    "artist", "artists", "book", "books", "zine", "press", "gallery",
    "出展", "出展者", "参加", "出版社", "書店", "作家", "アーティスト"
]

BAD_LINK_TERMS = [
    "privacy", "policy", "contact", "access", "application", "agreement",
    "facebook", "instagram", "twitter", "x.com", "youtube", "login"
]

ENTITY_HINTS = {
    "publisher_or_press": ["publisher", "press", "publishing", "出版社", "出版", "書店"],
    "artist_or_collective": ["artist", "illustrator", "作家", "アーティスト", "collective", "studio"],
    "bookstore_gallery": ["bookstore", "book shop", "gallery", "書店", "ギャラリー"],
    "zine_or_book": ["zine", "book", "artist book", "publication", "ZINE", "本", "冊子"],
}

BAD_ENTITY_TERMS = [
    "TOKYO ART BOOK FAIR", "APPLICATION", "HOME", "ABOUT", "CONTACT", "ACCESS",
    "PRIVACY", "POLICY", "ARCHIVES", "COMMUNITY", "AGREEMENT", "MENU", "JP", "EN"
]

def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=18, allow_redirects=True)
        r.encoding = r.apparent_encoding or r.encoding
        return r.url, r.text, r.status_code, None
    except Exception as e:
        return url, "", None, str(e)

def text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    return "\n".join([line.strip() for line in soup.get_text("\n").splitlines() if line.strip()])

def candidate_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        label = " ".join(a.get_text(" ", strip=True).split())
        url = urljoin(base_url, a["href"])
        blob = (label + " " + url).lower()

        if any(b in blob for b in BAD_LINK_TERMS):
            continue
        if any(g.lower() in blob for g in GOOD_LINK_TERMS):
            links.append({"label": label or "[no label]", "url": url})

    out, seen = [], set()
    for l in links:
        if l["url"] not in seen:
            seen.add(l["url"])
            out.append(l)
    return out[:80]

def classify_entity(name, context):
    blob = f"{name} {context}".lower()
    found = []
    for typ, terms in ENTITY_HINTS.items():
        if any(t.lower() in blob for t in terms):
            found.append(typ)
    return found or ["unknown"]

def bad_entity(name):
    n = " ".join(str(name or "").split()).strip()
    if len(n) < 3 or len(n) > 80:
        return True
    up = n.upper()
    if any(b in up for b in BAD_ENTITY_TERMS):
        return True
    if up == n and len(n) < 20:
        return True
    return False

def extract_entities(text):
    entities = []

    # Western / brand / publisher style names.
    western = re.findall(r"\b[A-Z][A-Za-z0-9&'’.,\-]+(?:\s+[A-Z][A-Za-z0-9&'’.,\-]+){0,4}\b", text or "")
    # Japanese short name-ish chunks around relevant terms.
    jp_lines = []
    for line in (text or "").splitlines():
        if any(term in line for terms in ENTITY_HINTS.values() for term in terms):
            jp_lines.append(line)

    jp = []
    for line in jp_lines:
        for m in re.findall(r"[一-龥ぁ-んァ-ンーA-Za-z0-9・&'\-]{2,30}", line):
            if any(term in line for terms in ENTITY_HINTS.values() for term in terms):
                jp.append(m)

    raw = western + jp

    seen = set()
    for name in raw:
        name = " ".join(name.split()).strip(" ・,。:：-")
        if bad_entity(name) or name in seen:
            continue
        seen.add(name)

        context = ""
        for line in (text or "").splitlines():
            if name in line:
                context = " ".join(line.split())[:240]
                break

        entities.append({
            "name": name,
            "types": classify_entity(name, context),
            "context": context,
        })

    return entities[:120]

def main():
    pages = []
    all_links = []

    for seed in SEED_URLS:
        final_url, html, status, error = fetch(seed)
        links = candidate_links(html, final_url) if html else []
        pages.append({
            "url": seed,
            "final_url": final_url,
            "http_status": status,
            "error": error,
            "links_found": len(links),
        })
        all_links.extend(links)

    # De-dupe and crawl a limited archive-like set.
    seen = set()
    crawl_links = []
    for l in all_links:
        if l["url"] not in seen:
            seen.add(l["url"])
            crawl_links.append(l)

    crawl_links = crawl_links[:25]

    entities = []
    crawled_pages = []

    for link in crawl_links:
        final_url, html, status, error = fetch(link["url"])
        text = text_from_html(html) if html else ""
        page_entities = extract_entities(text)
        crawled_pages.append({
            "label": link.get("label"),
            "url": link.get("url"),
            "final_url": final_url,
            "http_status": status,
            "error": error,
            "entities_found": len(page_entities),
        })
        for e in page_entities:
            e["source_url"] = final_url
            e["source_label"] = link.get("label")
            entities.append(e)

    # De-dupe entities.
    deduped = []
    seen_names = set()
    for e in entities:
        if e["name"] not in seen_names:
            seen_names.add(e["name"])
            deduped.append(e)

    result = {
        "title": "TOKYO ART BOOK FAIR",
        "seed_pages": pages,
        "crawl_links": crawl_links,
        "crawled_pages": crawled_pages,
        "entities": deduped,
        "entity_count": len(deduped),
        "publishers_or_presses": [e for e in deduped if "publisher_or_press" in e["types"]],
        "artists_or_collectives": [e for e in deduped if "artist_or_collective" in e["types"]],
        "bookstores_or_galleries": [e for e in deduped if "bookstore_gallery" in e["types"]],
        "zines_or_books": [e for e in deduped if "zine_or_book" in e["types"]],
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Tokyo Art Book Fair Exhibitor / Ecosystem Data",
        "",
        "First TABF-specific crawler pass. This is designed to find ecosystem signals: publishers, artists, collectives, bookstores, galleries, zines, and books.",
        "",
        f"- Total entities: {result['entity_count']}",
        f"- Publishers / presses: {len(result['publishers_or_presses'])}",
        f"- Artists / collectives: {len(result['artists_or_collectives'])}",
        f"- Bookstores / galleries: {len(result['bookstores_or_galleries'])}",
        f"- Zines / books: {len(result['zines_or_books'])}",
        "",
        "## Crawled Pages",
        "",
    ]

    for p in crawled_pages[:30]:
        lines.append(f"- {p['label']} — {p['final_url']} — entities {p['entities_found']}")

    for section, key in [
        ("Publishers / Presses", "publishers_or_presses"),
        ("Artists / Collectives", "artists_or_collectives"),
        ("Bookstores / Galleries", "bookstores_or_galleries"),
        ("Zines / Books", "zines_or_books"),
    ]:
        lines.append("")
        lines.append(f"## {section}")
        if not result[key]:
            lines.append("_None found yet._")
        for e in result[key][:40]:
            lines.append(f"- {e['name']} — {', '.join(e['types'])}")
            if e.get("context"):
                lines.append(f"  - {e['context']}")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Entities:", result["entity_count"])

if __name__ == "__main__":
    main()
