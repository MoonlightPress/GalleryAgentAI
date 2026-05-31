
import json
import re
from pathlib import Path
from urllib.parse import quote_plus, urlparse

import requests
from bs4 import BeautifulSoup

OUT_JSON = "memory/tokyo_zine_ecosystem.json"
OUT_REPORT = "reports/tokyo_zine_ecosystem.md"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (MochiTokyoZineCrawler/1.0; +https://example.com)"
}

SEARCH_QUERIES = [
    "zine shop Koenji",
    "zine shop Nakano Tokyo",
    "zine shop Shimokitazawa",
    "zine shop Kichijoji",
    "zine shop Tokyo",
    "artist book store Tokyo",
    "photobook store Tokyo",
    "independent bookstore Tokyo zine",
    "risograph studio Tokyo zine",
    "Tokyo zine fair",
    "Tokyo art book store",
    "Tokyo small press publisher artist book",
    "Tokyo zine consignment shop",
    "東京 ZINE ショップ 高円寺",
    "東京 ZINE ショップ 中野",
    "東京 ZINE ショップ 下北沢",
    "東京 アートブック 書店",
    "東京 リソグラフ スタジオ ZINE",
]

KNOWN_SEEDS = [
    {
        "name": "MOUNT ZINE",
        "url": "https://mount.co.jp/",
        "category": "zine_fair_store",
        "area": "Tokyo",
        "neighborhood": "unknown",
        "source_query": "known seed",
        "confidence": 85,
        "notes": "Known zine ecosystem target from existing data.",
    },
    {
        "name": "UTRECHT",
        "url": "https://utrecht.jp/",
        "category": "artist_book_store",
        "area": "Tokyo",
        "neighborhood": "Omotesando/Aoyama",
        "source_query": "known seed",
        "confidence": 85,
        "notes": "Art book / zine / independent publishing context.",
    },
    {
        "name": "flotsam books",
        "url": "https://flotsambooks.com/",
        "category": "photobook_artist_book_store",
        "area": "Tokyo",
        "neighborhood": "unknown",
        "source_query": "known seed",
        "confidence": 85,
        "notes": "Photobook / artist-book bookstore target.",
    },
    {
        "name": "NADiff a/p/a/r/t",
        "url": "https://www.nadiff.com/",
        "category": "art_book_store",
        "area": "Tokyo",
        "neighborhood": "Ebisu",
        "source_query": "known seed",
        "confidence": 80,
        "notes": "Art book store / exhibition context.",
    },
    {
        "name": "B&B Shimokitazawa",
        "url": "https://bookandbeer.com/",
        "category": "independent_bookstore",
        "area": "Tokyo",
        "neighborhood": "Shimokitazawa",
        "source_query": "known seed",
        "confidence": 75,
        "notes": "Independent bookstore/community space.",
    },
    {
        "name": "POST",
        "url": "https://post-books.info/",
        "category": "art_book_store",
        "area": "Tokyo",
        "neighborhood": "Ebisu",
        "source_query": "known seed",
        "confidence": 80,
        "notes": "Art book / publication-oriented space.",
    },
    {
        "name": "Book and Sons",
        "url": "https://bookandsons.com/",
        "category": "art_book_store",
        "area": "Tokyo",
        "neighborhood": "Gakugeidaigaku",
        "source_query": "known seed",
        "confidence": 75,
        "notes": "Bookstore/gallery context.",
    },
    {
        "name": "TOKYO ART BOOK FAIR",
        "url": "https://tokyoartbookfair.com/",
        "category": "artist_book_fair",
        "area": "Tokyo",
        "neighborhood": "Kiyosumi-shirakawa / MOT",
        "source_query": "known seed",
        "confidence": 95,
        "notes": "Major art-book fair and ecosystem anchor.",
    },
    {
        "name": "COMITIA",
        "url": "https://www.comitia.co.jp/",
        "category": "self_publishing_fair",
        "area": "Tokyo",
        "neighborhood": "Ariake",
        "source_query": "known seed",
        "confidence": 60,
        "notes": "Large self-publishing fair; may be too manga/doujinshi-oriented.",
    },
    {
        "name": "Design Festa",
        "url": "https://designfesta.com/",
        "category": "print_market",
        "area": "Tokyo",
        "neighborhood": "Ariake",
        "source_query": "known seed",
        "confidence": 55,
        "notes": "Sales visibility, but less curatorial.",
    },
]

CATEGORY_TERMS = {
    "zine_shop": ["zine shop", "zines", "ZINE", "ジン", "zine"],
    "artist_book_store": ["artist book", "art book", "アートブック", "アーティストブック"],
    "photobook_store": ["photobook", "photo book", "写真集"],
    "independent_bookstore": ["independent bookstore", "bookstore", "book shop", "書店", "本屋"],
    "risograph_studio": ["risograph", "riso", "リソグラフ"],
    "zine_fair": ["zine fair", "book fair", "zine event", "フェア"],
    "small_press_publisher": ["small press", "publisher", "press", "出版", "出版社"],
    "print_market": ["print market", "market", "popup", "ポップアップ"],
}

NEIGHBORHOOD_TERMS = {
    "Koenji": ["Koenji", "Kōenji", "高円寺"],
    "Nakano": ["Nakano", "中野"],
    "Shimokitazawa": ["Shimokitazawa", "下北沢"],
    "Kichijoji": ["Kichijoji", "吉祥寺"],
    "Ebisu": ["Ebisu", "恵比寿"],
    "Aoyama/Omotesando": ["Aoyama", "Omotesando", "青山", "表参道"],
    "Shibuya": ["Shibuya", "渋谷"],
    "Shinjuku": ["Shinjuku", "新宿"],
    "Ariake": ["Ariake", "有明", "Big Sight", "ビッグサイト"],
    "Kiyosumi-shirakawa": ["Kiyosumi", "清澄", "MOT", "東京都現代美術館"],
}

BAD_DOMAINS = [
    "google.", "youtube.", "facebook.", "instagram.", "twitter.", "x.com",
    "tiktok.", "pinterest.", "reddit.", "amazon.", "rakuten.",
]

BAD_TITLES = [
    "Google Search", "Images", "Videos", "Maps", "Shopping", "News",
    "Sign in", "Log in", "YouTube", "Instagram", "Facebook",
]

def safe_get(url, timeout=12):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        r.encoding = r.apparent_encoding or r.encoding
        return r.url, r.text, r.status_code, None
    except Exception as e:
        return url, "", None, str(e)

def search_duckduckgo(query):
    # HTML endpoint; tends to be simpler than normal search pages.
    url = "https://duckduckgo.com/html/?q=" + quote_plus(query)
    final_url, html, status, error = safe_get(url)
    results = []

    if not html:
        return results

    soup = BeautifulSoup(html, "html.parser")
    for a in soup.select("a.result__a"):
        title = " ".join(a.get_text(" ", strip=True).split())
        href = a.get("href")
        if not title or not href:
            continue
        if any(bad.lower() in title.lower() for bad in BAD_TITLES):
            continue
        if bad_url(href):
            continue
        results.append({
            "title": title,
            "url": href,
            "source_query": query,
        })

    # Fallback if DDG changes markup.
    if not results:
        for a in soup.find_all("a", href=True):
            title = " ".join(a.get_text(" ", strip=True).split())
            href = a.get("href")
            if len(title) < 4:
                continue
            blob = (title + " " + href).lower()
            if any(t in blob for t in ["zine", "artist book", "bookstore", "risograph", "アートブック", "書店"]):
                if not bad_url(href):
                    results.append({"title": title, "url": href, "source_query": query})

    return dedupe(results)[:12]

def bad_url(url):
    low = url.lower()
    return any(d in low for d in BAD_DOMAINS)

def dedupe(rows):
    out, seen = [], set()
    for r in rows:
        u = r.get("url")
        if not u or u in seen:
            continue
        seen.add(u)
        out.append(r)
    return out

def classify(title, text=""):
    blob = f"{title} {text}".lower()
    scores = {}
    for cat, terms in CATEGORY_TERMS.items():
        count = sum(1 for t in terms if t.lower() in blob)
        if count:
            scores[cat] = count
    if not scores:
        return "unknown"
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[0][0]

def infer_neighborhood(title, text="", query=""):
    blob = f"{title} {text} {query}"
    for hood, terms in NEIGHBORHOOD_TERMS.items():
        if any(t.lower() in blob.lower() for t in terms):
            return hood
    return "unknown"

def evidence_snippet(text):
    if not text:
        return ""
    cleaned = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
    terms = ["zine", "ZINE", "artist book", "art book", "bookstore", "risograph", "アートブック", "書店", "リソグラフ"]
    for line in cleaned.splitlines():
        if any(t.lower() in line.lower() for t in terms) and 25 <= len(line) <= 240:
            return line
    return cleaned[:220]

def fetch_page_context(url):
    final_url, html, status, error = safe_get(url, timeout=10)
    if not html:
        return {
            "final_url": final_url,
            "http_status": status,
            "error": error,
            "text": "",
            "snippet": "",
        }
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    text = "\n".join([line.strip() for line in soup.get_text("\n").splitlines() if line.strip()])
    return {
        "final_url": final_url,
        "http_status": status,
        "error": error,
        "page_title": title,
        "text": text[:5000],
        "snippet": evidence_snippet(text),
    }

def name_from_result(title):
    title = re.sub(r"\s*[-|–—]\s*.*$", "", title).strip()
    title = re.sub(r"\s+\|\s+.*$", "", title).strip()
    title = re.sub(r"公式.*$", "", title).strip()
    return title[:80] if title else "unknown"

def confidence_for(row):
    score = 35
    if row.get("category") != "unknown":
        score += 25
    if row.get("neighborhood") != "unknown":
        score += 15
    if row.get("snippet"):
        score += 10
    if row.get("source_query") == "known seed":
        score += 20
    if row.get("url"):
        score += 5
    return min(100, score)

def main():
    found = []

    # Known seeds first.
    for seed in KNOWN_SEEDS:
        row = dict(seed)
        row["search_found"] = False
        found.append(row)

    # Search/crawl.
    raw_results = []
    for q in SEARCH_QUERIES:
        print("SEARCH:", q)
        raw_results.extend(search_duckduckgo(q))

    raw_results = dedupe(raw_results)

    for r in raw_results:
        ctx = fetch_page_context(r["url"])
        title = r.get("title") or ctx.get("page_title") or ""
        name = name_from_result(title)
        blob_text = f"{title}\n{ctx.get('page_title','')}\n{ctx.get('text','')[:1200]}"

        category = classify(title, blob_text)
        neighborhood = infer_neighborhood(title, blob_text, r.get("source_query", ""))

        # Keep only likely useful rows.
        if category == "unknown" and neighborhood == "unknown":
            continue

        row = {
            "name": name,
            "url": ctx.get("final_url") or r["url"],
            "category": category,
            "area": "Tokyo" if neighborhood != "unknown" or "tokyo" in blob_text.lower() else "unknown",
            "neighborhood": neighborhood,
            "source_query": r.get("source_query"),
            "confidence": 0,
            "notes": "Search-discovered candidate. Needs human verification before outreach.",
            "snippet": ctx.get("snippet"),
            "http_status": ctx.get("http_status"),
            "search_found": True,
        }
        row["confidence"] = confidence_for(row)
        found.append(row)

    # De-dupe by normalized name/url.
    cleaned = []
    seen = set()
    for row in found:
        key = (row.get("name", "").lower(), urlparse(row.get("url", "")).netloc.lower())
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(row)

    cleaned.sort(key=lambda x: (x.get("confidence", 0), x.get("neighborhood") != "unknown"), reverse=True)

    result = {
        "title": "Tokyo Zine Ecosystem",
        "target_count": 100,
        "entry_count": len(cleaned),
        "entries": cleaned,
        "queries": SEARCH_QUERIES,
        "note": "Search-discovered entries require verification. Known seeds are more reliable.",
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Tokyo Zine Ecosystem Crawl",
        "",
        f"- Entries found: {len(cleaned)}",
        "- Target: 100",
        f"- Coverage: {round(len(cleaned)/100*100,1)}%",
        "",
        "Search-discovered entries require human verification before outreach.",
        "",
    ]

    by_hood = {}
    for e in cleaned:
        by_hood.setdefault(e.get("neighborhood", "unknown"), []).append(e)

    lines.append("## By Neighborhood")
    lines.append("")
    for hood, rows in sorted(by_hood.items(), key=lambda x: len(x[1]), reverse=True):
        lines.append(f"### {hood}")
        for e in rows[:25]:
            lines.append(f"- {e['name']} — {e['category']} — confidence {e['confidence']}")
            if e.get("url"):
                lines.append(f"  - {e['url']}")
            if e.get("snippet"):
                lines.append(f"  - {e['snippet'][:220]}")
        lines.append("")

    lines.append("## All Entries")
    lines.append("")
    for e in cleaned:
        lines.append(f"### {e['name']}")
        lines.append(f"- Category: {e['category']}")
        lines.append(f"- Neighborhood: {e['neighborhood']}")
        lines.append(f"- Confidence: {e['confidence']}")
        lines.append(f"- Source query: {e['source_query']}")
        lines.append(f"- URL: {e['url']}")
        if e.get("snippet"):
            lines.append(f"- Evidence: {e['snippet']}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Entries:", len(cleaned))

if __name__ == "__main__":
    main()
