
import json
import re
from pathlib import Path
from urllib.parse import quote_plus, urlparse

import requests
from bs4 import BeautifulSoup

QUEUE = "memory/candidate_business_review_queue.json"
OUT_JSON = "memory/extracted_business_candidates.json"
OUT_REPORT = "reports/extracted_business_candidates.md"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (MochiBusinessExtractor/1.0)"
}

BAD_NAMES = {
    "Google", "Google Maps", "Sign in", "Images", "Videos", "News", "Shopping",
    "Maps", "Search", "More", "Directions", "Save", "Share", "Website"
}

BAD_TERMS = [
    "google", "youtube", "facebook", "instagram.com/p/", "reddit",
    "amazon", "rakuten", "tripadvisor", "pinterest"
]

CATEGORY_KEYWORDS = {
    "zine_shop": ["zine", "ZINE", "ジン"],
    "artist_book_store": ["artist book", "art book", "アートブック", "アーティストブック"],
    "photobook_store": ["photobook", "photo book", "写真集"],
    "independent_bookstore": ["bookstore", "book shop", "本屋", "書店", "books"],
    "risograph_studio": ["risograph", "riso", "リソグラフ"],
    "small_press_publisher": ["small press", "publisher", "press", "出版", "出版社"],
    "zine_fair": ["zine fair", "book fair", "イベント", "フェア"],
    "print_market": ["print market", "popup", "market", "ポップアップ"],
}

NEIGHBORHOODS = ["Koenji", "Nakano", "Shimokitazawa", "Kichijoji", "Tokyo"]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def ddg_search(query, max_results=10):
    url = "https://duckduckgo.com/html/?q=" + quote_plus(query)
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.encoding = r.apparent_encoding or r.encoding
    except Exception:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    rows = []

    for a in soup.select("a.result__a"):
        title = " ".join(a.get_text(" ", strip=True).split())
        href = a.get("href", "")
        if not title or not href:
            continue
        if is_bad(title, href):
            continue
        rows.append({
            "title": title,
            "url": href,
            "source": "duckduckgo",
            "query": query,
        })

    return rows[:max_results]

def is_bad(title, url):
    low = (title + " " + url).lower()
    if title.strip() in BAD_NAMES:
        return True
    return any(b in low for b in BAD_TERMS)

def clean_name(title):
    title = re.sub(r"\s*[-|–—]\s*(公式|Official|Instagram|Facebook|X|Twitter|Google Maps|地図|アクセス).*$", "", title, flags=re.I)
    title = re.sub(r"\s*[-|–—]\s*.*?(Tokyo|東京|Koenji|高円寺|Nakano|中野|Shimokitazawa|下北沢|Kichijoji|吉祥寺).*$", "", title, flags=re.I)
    title = title.strip(" -|–—")
    return title[:80]

def infer_category(text, fallback_categories=None):
    blob = text.lower()
    scores = {}
    for cat, terms in CATEGORY_KEYWORDS.items():
        score = sum(1 for t in terms if t.lower() in blob)
        if score:
            scores[cat] = score

    if scores:
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[0][0]

    if fallback_categories:
        return fallback_categories[0]

    return "unknown"

def score_candidate(name, title, url, query, neighborhood, category):
    blob = f"{name} {title} {url} {query}".lower()
    score = 30

    if category != "unknown":
        score += 20
    if neighborhood != "Tokyo":
        score += 10
    if any(x in blob for x in ["zine", "artist book", "art book", "bookstore", "book shop", "risograph"]):
        score += 20
    if any(x in blob for x in ["高円寺", "中野", "下北沢", "吉祥寺"]):
        score += 10
    if "maps" in url.lower():
        score += 10
    if len(name) >= 3:
        score += 5

    return min(100, score)

def google_maps_search_url(query):
    return "https://www.google.com/maps/search/" + quote_plus(query)

def google_search_url(query):
    return "https://www.google.com/search?q=" + quote_plus(query)

def main():
    queue = load(QUEUE, {})
    search_candidates = queue.get("candidates", [])

    extracted = []
    seen = set()

    for c in search_candidates:
        query = c.get("query")
        neighborhood = c.get("neighborhood", "unknown")
        fallback_categories = c.get("suggested_categories", [])

        if not query:
            continue

        print("SEARCH:", query)
        results = ddg_search(query, max_results=8)

        for r in results:
            name = clean_name(r["title"])
            if not name or len(name) < 3:
                continue

            key = (name.lower(), urlparse(r["url"]).netloc.lower())
            if key in seen:
                continue
            seen.add(key)

            category = infer_category(f"{r['title']} {query} {r['url']}", fallback_categories)
            score = score_candidate(name, r["title"], r["url"], query, neighborhood, category)

            extracted.append({
                "candidate_id": f"BIZ-{len(extracted)+1:04d}",
                "review_status": "unreviewed",
                "name": name,
                "category": category,
                "neighborhood": neighborhood,
                "source_query": query,
                "source_candidate_id": c.get("candidate_id"),
                "source_title": r["title"],
                "website": r["url"],
                "google_maps_url": google_maps_search_url(name + " " + neighborhood),
                "google_search_url": google_search_url(name + " " + neighborhood),
                "confidence": score,
                "review_fields": {
                    "address": "",
                    "instagram": "",
                    "email": "",
                    "phone": "",
                    "accepts_consignment": "unknown",
                    "accepts_submissions": "unknown",
                    "notes": "",
                },
                "review_instruction": "Open Maps link. Approve only if this is a real place, publisher, studio, fair, or shop relevant to zines/art books/printed matter.",
            })

    extracted.sort(key=lambda x: x["confidence"], reverse=True)

    result = {
        "title": "Extracted Business Candidates",
        "source_search_count": len(search_candidates),
        "candidate_count": len(extracted),
        "candidates": extracted,
        "note": "These are business-like candidates extracted from search results. They still need review.",
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Extracted Business Candidates",
        "",
        f"- Source search queries: {len(search_candidates)}",
        f"- Extracted candidates: {len(extracted)}",
        "",
        "These are now actual candidate records, not just search queries.",
        "",
    ]

    by_neighborhood = {}
    for e in extracted:
        by_neighborhood.setdefault(e["neighborhood"], []).append(e)

    for hood, rows in sorted(by_neighborhood.items()):
        lines.append(f"## {hood}")
        for e in rows[:50]:
            lines.append(f"### {e['candidate_id']} — {e['name']}")
            lines.append(f"- Category: {e['category']}")
            lines.append(f"- Confidence: {e['confidence']}")
            lines.append(f"- Source query: `{e['source_query']}`")
            lines.append(f"- Website/source: {e['website']}")
            lines.append(f"- Maps check: {e['google_maps_url']}")
            lines.append(f"- Review status: {e['review_status']}")
            lines.append("")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Extracted:", len(extracted))

if __name__ == "__main__":
    main()
