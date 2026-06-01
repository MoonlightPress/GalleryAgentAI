
import json
import re
from pathlib import Path
from urllib.parse import quote_plus, urlparse, parse_qs, unquote

import requests
from bs4 import BeautifulSoup

SEEDS = Path("memory/multi_ingress_seed_queries.json")
OUT_JSON = Path("memory/multi_ingress_raw_candidates.json")
OUT_REPORT = Path("reports/multi_ingress_raw_candidates.md")

HEADERS = {"User-Agent": "Mozilla/5.0 (MochiMultiIngress/1.0)"}

BAD_DOMAINS = [
    "youtube.com", "facebook.com", "pinterest.", "reddit.com", "amazon.",
    "rakuten.", "wikipedia.org", "tripadvisor.", "navitime."
]

def load(path, fallback):
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback

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

def bad_url(url):
    low = url.lower()
    return any(d in low for d in BAD_DOMAINS)

def ddg_search(query, max_results=8):
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
        if not title or not href or bad_url(href):
            continue
        rows.append({"title": title, "url": href, "query": query})
    return rows[:max_results]

def clean_title(title):
    title = re.sub(r"\s+[|｜]\s+.*$", "", title).strip()
    title = re.sub(r"\s+[-–—]\s+(Official|公式|Home|トップ).*$", "", title, flags=re.I).strip()
    return title[:120]

def infer_fields(title, url, group, meta):
    blob = f"{title} {url}".lower()

    deadline_signal = any(x in blob for x in ["deadline", "締切", "応募期間", "application", "公募", "open call"])
    fee_signal = any(x in blob for x in ["fee", "fees", "entry fee", "出展料", "参加費", "応募料"])
    form_signal = any(x in blob for x in ["apply", "application", "submit", "応募", "申込", "フォーム"])

    return {
        "title": clean_title(title),
        "organization": clean_title(title),
        "career_category": meta["career_category"],
        "category": meta["category"],
        "source_url": url,
        "source_query": group,
        "source_search": meta.get("_current_query", ""),
        "deadline_signal": deadline_signal,
        "fee_signal": fee_signal,
        "form_signal": form_signal,
    }

def score_candidate(c):
    score = 35
    blob = f"{c['title']} {c['source_url']}".lower()

    if c["deadline_signal"]:
        score += 15
    if c["fee_signal"]:
        score += 8
    if c["form_signal"]:
        score += 12

    if c["career_category"] == "contests":
        if any(x in blob for x in ["open call", "公募", "competition", "contest", "call for entries"]):
            score += 20
    elif c["career_category"] == "zines":
        if any(x in blob for x in ["zine", "artist book", "book fair", "出展", "フェア"]):
            score += 20
    elif c["career_category"] == "residencies":
        if any(x in blob for x in ["residency", "レジデンス", "air", "artist-in-residence"]):
            score += 20
    elif c["career_category"] == "publishing":
        if any(x in blob for x in ["publisher", "press", "publishing", "出版", "photobook", "artist book"]):
            score += 18

    domain = urlparse(c["source_url"]).netloc.lower()
    if any(x in domain for x in ["tokyoartbeat", "artfair", "artbook", "gallery", "museum", "residency", "air"]):
        score += 6

    return min(100, score)

def main():
    seeds = load(SEEDS, {})
    candidates = []
    seen = set()

    for group, meta in seeds.items():
        for q in meta["queries"]:
            meta["_current_query"] = q
            print("SEARCH:", group, q)
            for r in ddg_search(q):
                key = (r["title"].lower(), r["url"].lower())
                if key in seen:
                    continue
                seen.add(key)
                c = infer_fields(r["title"], r["url"], group, meta)
                c["candidate_id"] = f"MULTI-{len(candidates)+1:04d}"
                c["score"] = score_candidate(c)
                c["status"] = "research_next"
                candidates.append(c)

    candidates.sort(key=lambda x: x["score"], reverse=True)

    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)
    json.dump({"candidate_count": len(candidates), "candidates": candidates}, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = ["# Multi-Ingress Raw Candidates", "", f"- Candidates: {len(candidates)}", ""]
    for cat in ["contests", "zines", "residencies", "publishing"]:
        rows = [c for c in candidates if c["career_category"] == cat]
        lines.append(f"## {cat} ({len(rows)})")
        for c in rows[:40]:
            lines.append(f"### {c['candidate_id']} — {c['title']}")
            lines.append(f"- Score: {c['score']}")
            lines.append(f"- Category: {c['career_category']} / {c['category']}")
            lines.append(f"- URL: {c['source_url']}")
            lines.append(f"- Signals: deadline={c['deadline_signal']}, fee={c['fee_signal']}, form={c['form_signal']}")
            lines.append("")
        lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Candidates:", len(candidates))

if __name__ == "__main__":
    main()
