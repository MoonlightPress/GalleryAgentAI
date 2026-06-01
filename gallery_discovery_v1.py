
import json
from pathlib import Path
from urllib.parse import quote_plus, urlparse
import requests
from bs4 import BeautifulSoup

OUT_JSON = Path("memory/gallery_candidates.json")
OUT_REPORT = Path("reports/gallery_candidates.md")

HEADERS = {"User-Agent": "Mozilla/5.0 (MochiGalleryDiscovery/1.0)"}

QUERIES = [
    "Tokyo contemporary gallery emerging artists",
    "Tokyo gallery artist submission",
    "Tokyo gallery open call artist",
    "Koenji gallery artist",
    "Nakano gallery artist",
    "Kichijoji gallery contemporary art",
    "Shimokitazawa gallery artist",
    "Tokyo artist run space gallery",
    "東京 ギャラリー 若手作家 募集",
    "東京 ギャラリー 公募 アーティスト",
    "高円寺 ギャラリー 作家",
    "中野 ギャラリー 作家",
    "吉祥寺 ギャラリー 作家",
    "下北沢 ギャラリー 作家",
]

BAD_DOMAINS = ["youtube", "instagram.com/p/", "facebook", "wikipedia", "tripadvisor", "navitime", "pinterest"]

def bad(url):
    low = url.lower()
    return any(x in low for x in BAD_DOMAINS)

def search(query, max_results=8):
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
        if not title or not href or bad(href):
            continue
        rows.append({"title": title[:120], "url": href, "query": query})
    return rows[:max_results]

def infer_neighborhood(title, query, url):
    blob = f"{title} {query} {url}".lower()
    pairs = {
        "Koenji": ["koenji", "高円寺"],
        "Nakano": ["nakano", "中野"],
        "Kichijoji": ["kichijoji", "吉祥寺"],
        "Shimokitazawa": ["shimokitazawa", "下北沢"],
        "Tokyo": ["tokyo", "東京"],
    }
    for hood, terms in pairs.items():
        if any(t.lower() in blob for t in terms):
            return hood
    return "Tokyo"

def score(row):
    blob = f"{row['title']} {row['url']} {row['query']}".lower()
    s = 35
    if "gallery" in blob or "ギャラリー" in blob:
        s += 25
    if "submission" in blob or "open call" in blob or "公募" in blob or "募集" in blob:
        s += 20
    if "emerging" in blob or "若手" in blob:
        s += 10
    if any(x in blob for x in ["koenji", "nakano", "kichijoji", "shimokitazawa", "高円寺", "中野", "吉祥寺", "下北沢"]):
        s += 8
    if any(x in blob for x in ["top", "best", "guide", "まとめ", "一覧"]):
        s -= 15
    return max(0, min(100, s))

def main():
    candidates = []
    seen = set()
    for q in QUERIES:
        print("SEARCH:", q)
        for r in search(q):
            key = (r["title"].lower(), r["url"].lower())
            if key in seen:
                continue
            seen.add(key)
            row = {
                "candidate_id": f"GAL-{len(candidates)+1:04d}",
                "title": r["title"],
                "url": r["url"],
                "query": q,
                "career_category": "galleries",
                "category": "gallery",
                "neighborhood": infer_neighborhood(r["title"], q, r["url"]),
                "score": 0,
                "status": "research_next",
            }
            row["score"] = score(row)
            candidates.append(row)

    candidates.sort(key=lambda x: x["score"], reverse=True)

    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    OUT_JSON.write_text(json.dumps({"candidate_count": len(candidates), "candidates": candidates}, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Gallery Candidates", "", f"- Candidates: {len(candidates)}", ""]
    for c in candidates[:80]:
        lines.append(f"### {c['candidate_id']} — {c['title']}")
        lines.append(f"- Score: {c['score']}")
        lines.append(f"- Neighborhood: {c['neighborhood']}")
        lines.append(f"- URL: {c['url']}")
        lines.append(f"- Query: {c['query']}")
        lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Gallery candidates:", len(candidates))

if __name__ == "__main__":
    main()
