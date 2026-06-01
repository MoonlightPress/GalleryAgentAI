
import json
import re
from pathlib import Path
from urllib.parse import urlparse

SRC = "memory/clean_business_candidates.json"
OUT_JSON = "memory/normalized_opportunities.json"
OUT_REPORT = "reports/normalized_opportunities.md"

CANONICAL_RULES = [
    ("Tacoche", ["タコシェ", "TACO ché", "Tacoche", "taco.shop-pro", "tacoche.com"]),
    ("Dig A Hole Zines", ["Dig A Hole", "digaholezines"]),
    ("そぞろ書房", ["そぞろ書房", "sozoroshobou"]),
    ("本店・本屋の実験室", ["本店・本屋の実験室", "honnonagaya-honten"]),
    ("tata bookshop/gallery", ["tata bookshop/gallery", "bookshop / gallery タタ", "tata-books"]),
    ("LOCAL Gallery・Books", ["LOCAL Gallery・Books", "Local Gallery・Books", "localgallerybooks", "LOCAL"]),
    ("ZINE FARM TOKYO", ["ZINE FARM TOKYO", "Zine Farm Tokyo", "zinefarmtokyo"]),
    ("Book Culture Club", ["Book Culture Club", "book Culture Club", "bookcultureclub"]),
    ("B&B", ["本屋 B&B", "Book - 本屋 B&B", "bookandbeer", "Book and Beer"]),
    ("日記屋 月日", ["日記屋 月日", "tsukihi.stores"]),
    ("Book Obscura", ["Book Obscura", "bookobscura"]),
    ("Books Ruhe", ["Books Ruhe", "ブックス ルーエ", "books-ruhe"]),
    ("Nuts Book Stand", ["Nuts Book Stand", "nutsbookstand"]),
    ("loneliness books", ["loneliness books", "lonelinessbooks"]),
    ("studio zezezaza", ["studio zezezaza", "studiozezezaza"]),
]

ARTICLE_TERMS = [
    "guide", "top ", "best ", "まとめ", "紹介", "ランキング", "おすすめ", "map", "地図",
    "記事", "レポ", "ニュース", "誕生", "更新", "選", "一覧", "開催日程", "準備",
    "商業出版に", "こんな本屋を", "Zineの専門店", "若者に", "置いてもらうには",
]

GENERIC_NAMES = {
    "Instagram", "About", "Book", "zine", "ZINEお取り扱い店舗", "高円寺書店マップ",
    "中野駅周辺の大きい本屋（東京都）", "下北沢駅周辺の大きい本屋（東京都）",
}

OFFICIAL_DOMAIN_HINTS = [
    "tacoche.com", "taco.shop-pro.jp", "sozoroshobou.stores.jp",
    "honnonagaya-honten.com", "tata-books.com", "localgallerybooks.com",
    "bookandbeer.com", "tsukihi.stores.jp", "bookobscura.com", "books-ruhe.co.jp",
    "instagram.com", "stores.jp", "thebase.in", "base.shop"
]

ARTICLE_DOMAIN_HINTS = [
    "brutus.jp", "trilltrill.jp", "timeout.jp", "san-tatsu.jp", "note.com",
    "bookshop-lover.com", "kj-weekly.jp", "tokyoartbeat.com", "tokyoweekender.com",
    "ya-hachi.com", "honnomachi.com", "honya-map.info", "ekiten.jp", "metI.go.jp",
]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def domain(url):
    try:
        return urlparse(url or "").netloc.lower().replace("www.", "")
    except Exception:
        return ""

def canonical_name(c):
    blob = " ".join([
        c.get("name", ""),
        c.get("original_name", ""),
        c.get("website", ""),
        c.get("domain", ""),
    ])
    for canon, patterns in CANONICAL_RULES:
        if any(p.lower() in blob.lower() for p in patterns):
            return canon
    return c.get("name", "").strip()

def is_articleish(c):
    blob = " ".join([
        c.get("name", ""),
        c.get("original_name", ""),
        c.get("website", ""),
        c.get("domain", ""),
    ]).lower()
    return any(t.lower() in blob for t in ARTICLE_TERMS)

def is_generic(c):
    name = c.get("name", "").strip()
    return name in GENERIC_NAMES or len(name) < 3

def source_type(c):
    d = c.get("domain") or domain(c.get("website"))
    if any(h in d for h in OFFICIAL_DOMAIN_HINTS):
        return "official_or_social"
    if any(h in d for h in ARTICLE_DOMAIN_HINTS) or is_articleish(c):
        return "article_reference"
    return "other_reference"

def opportunity_score(rows):
    score = 40
    official = len([r for r in rows if r["source_type"] == "official_or_social"])
    articles = len([r for r in rows if r["source_type"] == "article_reference"])
    source_count = len(rows)

    score += min(35, official * 15)
    score += min(15, articles * 5)
    score += min(15, source_count * 3)

    if source_count >= 3:
        score += 10

    return min(100, score)

def choose_best_category(rows):
    counts = {}
    for r in rows:
        cat = r.get("category") or "unknown"
        counts[cat] = counts.get(cat, 0) + 1
    if not counts:
        return "unknown"
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[0][0]

def choose_best_neighborhood(rows):
    counts = {}
    for r in rows:
        hood = r.get("neighborhood") or "unknown"
        counts[hood] = counts.get(hood, 0) + 1
    if not counts:
        return "unknown"
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[0][0]

def main():
    data = load(SRC, {})
    candidates = data.get("candidates", [])

    usable = []
    rejected = []

    for c in candidates:
        if c.get("cleanup_bucket") == "auto_reject":
            rejected.append({**c, "normalizer_reject_reason": "auto_reject_bucket"})
            continue
        if is_generic(c):
            rejected.append({**c, "normalizer_reject_reason": "generic_name"})
            continue

        cc = dict(c)
        cc["canonical_name"] = canonical_name(c)
        cc["source_type"] = source_type(c)

        # If it is only article-ish and did not canonicalize into a known place, keep as weak reference only.
        if is_articleish(c) and cc["canonical_name"] == c.get("name"):
            rejected.append({**cc, "normalizer_reject_reason": "article_without_canonical_business"})
            continue

        usable.append(cc)

    grouped = {}
    for c in usable:
        key = c["canonical_name"]
        grouped.setdefault(key, []).append(c)

    opportunities = []
    for name, rows in grouped.items():
        websites = []
        article_refs = []
        other_refs = []
        for r in rows:
            url = r.get("website")
            if not url:
                continue
            if r["source_type"] == "official_or_social":
                websites.append(url)
            elif r["source_type"] == "article_reference":
                article_refs.append(url)
            else:
                other_refs.append(url)

        def dedupe(seq):
            out, seen = [], set()
            for x in seq:
                if x not in seen:
                    seen.add(x)
                    out.append(x)
            return out

        opp = {
            "canonical_name": name,
            "category": choose_best_category(rows),
            "neighborhood": choose_best_neighborhood(rows),
            "confidence": opportunity_score(rows),
            "source_count": len(rows),
            "websites": dedupe(websites),
            "article_references": dedupe(article_refs),
            "other_references": dedupe(other_refs),
            "source_candidate_ids": [r.get("candidate_id") for r in rows],
            "status": "needs_review",
        }
        opportunities.append(opp)

    opportunities.sort(key=lambda x: (x["confidence"], x["source_count"]), reverse=True)

    result = {
        "source_candidate_count": len(candidates),
        "usable_candidate_count": len(usable),
        "rejected_candidate_count": len(rejected),
        "normalized_opportunity_count": len(opportunities),
        "opportunities": opportunities,
        "rejected_samples": rejected[:100],
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Normalized Opportunities",
        "",
        f"- Source candidates: {len(candidates)}",
        f"- Usable candidates: {len(usable)}",
        f"- Rejected candidates: {len(rejected)}",
        f"- Normalized opportunities: {len(opportunities)}",
        "",
    ]

    by_hood = {}
    for o in opportunities:
        by_hood.setdefault(o["neighborhood"], []).append(o)

    for hood, rows in sorted(by_hood.items()):
        lines.append(f"## {hood}")
        for o in rows:
            lines.append(f"### {o['canonical_name']}")
            lines.append(f"- Category: {o['category']}")
            lines.append(f"- Confidence: {o['confidence']}")
            lines.append(f"- Source count: {o['source_count']}")
            lines.append(f"- Status: {o['status']}")
            if o["websites"]:
                lines.append("- Websites:")
                for w in o["websites"][:5]:
                    lines.append(f"  - {w}")
            if o["article_references"]:
                lines.append("- Article references:")
                for a in o["article_references"][:5]:
                    lines.append(f"  - {a}")
            lines.append("")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Normalized opportunities:", len(opportunities))

if __name__ == "__main__":
    main()
