
import json
from pathlib import Path
from urllib.parse import quote_plus, urlparse, parse_qs, unquote
import requests
from bs4 import BeautifulSoup

OUT_JSON = Path("memory/art_fair_candidates.json")
OUT_REPORT = Path("reports/art_fair_candidates.md")

HEADERS = {"User-Agent": "Mozilla/5.0 (MochiArtFairExpansion/1.0)"}

QUERIES = {
    "art_fairs": [
        "Tokyo art fair application artist 2026",
        "Independent Tokyo artist application",
        "Tokyo International Art Fair apply to exhibit",
        "Art Fair Asia Fukuoka exhibitor application",
        "日本 アートフェア 出展 募集 アーティスト",
        "東京 アートフェア 出展 募集 作家",
    ],
    "illustration_markets": [
        "Tokyo illustration market artist application",
        "Japan illustration fair exhibitor application",
        "Design Festa Tokyo artist booth application",
        "コミティア 出展 イラストレーター 申し込み",
        "デザインフェスタ 出展 募集 アーティスト",
        "イラスト マーケット 出展 募集 東京",
    ],
    "artist_markets": [
        "Tokyo artist market vendor application",
        "Tokyo handmade art market artist application",
        "creators market Japan exhibitor application",
        "art market Tokyo artist booth",
        "クリエイターズマーケット 出展 募集",
        "アートマーケット 東京 出展 募集",
    ],
}

BAD = ["youtube", "facebook", "pinterest", "tripadvisor", "navitime", "wikipedia"]

def unwrap(url):
    if not url:
        return ""
    if url.startswith("//"):
        url = "https:" + url
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    if "uddg" in qs and qs["uddg"]:
        return unquote(qs["uddg"][0])
    return url

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
        href = unwrap(a.get("href", ""))
        if not title or not href:
            continue
        if any(b in href.lower() for b in BAD):
            continue
        rows.append({"title": title[:140], "url": href, "query": query})
    return rows[:max_results]

def score(row, group):
    blob = f"{row['title']} {row['url']} {row['query']}".lower()
    s = 35
    if any(x in blob for x in ["application", "apply", "exhibitor", "出展", "申し込み", "申込", "募集"]):
        s += 30
    if any(x in blob for x in ["deadline", "応募期間", "締切"]):
        s += 10
    if any(x in blob for x in ["booth", "table", "出展料", "fee"]):
        s += 8
    if group in {"art_fairs", "illustration_markets", "artist_markets"}:
        s += 8
    if any(x in blob for x in ["guide", "top", "まとめ", "一覧", "press release"]):
        s -= 12
    return max(0, min(100, s))

def main():
    candidates = []
    seen = set()
    for group, queries in QUERIES.items():
        for q in queries:
            print("SEARCH:", group, q)
            for r in search(q):
                key = (r["title"].lower(), r["url"].lower())
                if key in seen:
                    continue
                seen.add(key)
                row = {
                    "candidate_id": f"FAIR-{len(candidates)+1:04d}",
                    "title": r["title"],
                    "url": r["url"],
                    "query": q,
                    "fair_group": group,
                    "career_category": "fairs",
                    "category": "fair_popup",
                    "score": 0,
                    "status": "research_next",
                }
                row["score"] = score(row, group)
                candidates.append(row)

    candidates.sort(key=lambda x: x["score"], reverse=True)

    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)
    OUT_JSON.write_text(json.dumps({"candidate_count": len(candidates), "candidates": candidates}, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Art Fair / Artist Market Candidates", "", f"- Candidates: {len(candidates)}", ""]
    for group in QUERIES:
        rows = [c for c in candidates if c["fair_group"] == group]
        lines += [f"## {group} ({len(rows)})", ""]
        for c in rows[:30]:
            lines.append(f"### {c['candidate_id']} — {c['title']}")
            lines.append(f"- Score: {c['score']}")
            lines.append(f"- URL: {c['url']}")
            lines.append(f"- Query: {c['query']}")
            lines.append("")
        lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Candidates:", len(candidates))

if __name__ == "__main__":
    main()
