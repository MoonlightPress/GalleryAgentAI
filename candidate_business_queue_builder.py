
import json
import re
from pathlib import Path
from urllib.parse import quote_plus

BUSINESSES = "memory/tokyo_zine_businesses.json"
OUT_JSON = "memory/candidate_business_review_queue.json"
OUT_REPORT = "reports/candidate_business_review_queue.md"

SEARCH_SURFACES = [
    {
        "source_type": "google_maps",
        "neighborhood": "Koenji",
        "queries": [
            "高円寺 ZINE ショップ",
            "高円寺 本屋 ZINE",
            "高円寺 アートブック 書店",
            "Koenji zine shop",
            "Koenji independent bookstore zine",
        ],
    },
    {
        "source_type": "google_maps",
        "neighborhood": "Nakano",
        "queries": [
            "中野 ZINE ショップ",
            "中野 本屋 ZINE",
            "中野 アートブック 書店",
            "Nakano zine shop Tokyo",
            "Nakano independent bookstore zine",
        ],
    },
    {
        "source_type": "google_maps",
        "neighborhood": "Shimokitazawa",
        "queries": [
            "下北沢 ZINE ショップ",
            "下北沢 アートブック 書店",
            "下北沢 本屋 ZINE",
            "Shimokitazawa zine shop",
            "Shimokitazawa independent bookstore zine",
        ],
    },
    {
        "source_type": "google_maps",
        "neighborhood": "Kichijoji",
        "queries": [
            "吉祥寺 ZINE ショップ",
            "吉祥寺 アートブック 書店",
            "吉祥寺 本屋 ZINE",
            "Kichijoji zine shop",
        ],
    },
    {
        "source_type": "web_search",
        "neighborhood": "Tokyo",
        "queries": [
            "東京 ZINE 委託販売",
            "東京 ZINE イベント",
            "東京 リソグラフ スタジオ ZINE",
            "Tokyo risograph studio zine",
            "Tokyo artist book store",
            "Tokyo photobook bookstore",
            "Tokyo small press publisher artist book",
            "Tokyo independent bookstore zine",
            "Tokyo zine fair",
            "Tokyo art book fair exhibitors bookstore zine",
        ],
    },
]

CATEGORY_HINTS = {
    "zine_shop": ["zine", "ZINE", "ジン"],
    "artist_book_store": ["artist book", "art book", "アートブック", "アーティストブック"],
    "photobook_store": ["photobook", "photo book", "写真集"],
    "independent_bookstore": ["bookstore", "book shop", "本屋", "書店"],
    "risograph_studio": ["risograph", "riso", "リソグラフ"],
    "small_press_publisher": ["small press", "press", "publisher", "出版", "出版社"],
    "zine_fair": ["zine fair", "book fair", "イベント", "フェア"],
    "print_market": ["print", "market", "popup", "ポップアップ"],
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def maps_url(query):
    return "https://www.google.com/maps/search/" + quote_plus(query)

def search_url(query):
    return "https://www.google.com/search?q=" + quote_plus(query)

def infer_category(query):
    low = query.lower()
    hits = []
    for cat, terms in CATEGORY_HINTS.items():
        if any(t.lower() in low for t in terms):
            hits.append(cat)
    return hits or ["unknown"]

def score_candidate(query, neighborhood, source_type):
    score = 40
    low = query.lower()

    if neighborhood in {"Koenji", "Nakano", "Shimokitazawa", "Kichijoji"}:
        score += 15
    if "zine" in low or "zine" in query:
        score += 20
    if "アートブック" in query or "artist book" in low:
        score += 15
    if "本屋" in query or "書店" in query or "bookstore" in low:
        score += 10
    if "リソグラフ" in query or "risograph" in low:
        score += 10
    if source_type == "google_maps":
        score += 10

    return min(100, score)

def known_business_names():
    data = load(BUSINESSES, {})
    names = set()
    for p in data.get("known_places", []):
        if p.get("name"):
            names.add(p["name"].lower())
    return names

def main():
    known = known_business_names()
    candidates = []
    cid = 1

    for surface in SEARCH_SURFACES:
        for q in surface["queries"]:
            candidates.append({
                "candidate_id": f"CAND-{cid:04d}",
                "status": "unreviewed",
                "neighborhood": surface["neighborhood"],
                "source_type": surface["source_type"],
                "query": q,
                "suggested_categories": infer_category(q),
                "priority_score": score_candidate(q, surface["neighborhood"], surface["source_type"]),
                "google_maps_url": maps_url(q),
                "google_search_url": search_url(q),
                "review_fields": {
                    "name": "",
                    "address": "",
                    "website": "",
                    "instagram": "",
                    "email": "",
                    "phone": "",
                    "category": "",
                    "accepts_consignment": "unknown",
                    "accepts_submissions": "unknown",
                    "notes": "",
                },
                "review_instructions": [
                    "Open Maps first for physical places.",
                    "Copy name, address, website, and Instagram if visible.",
                    "Mark accepts_consignment only if explicitly stated or confirmed.",
                    "Reject if it is only a generic article, chain bookstore, unrelated café, or manga-only shop with no zine/art-book relevance.",
                ],
            })
            cid += 1

    candidates.sort(key=lambda x: x["priority_score"], reverse=True)

    result = {
        "title": "Candidate Business Review Queue",
        "candidate_count": len(candidates),
        "approved_count": 0,
        "rejected_count": 0,
        "skipped_count": 0,
        "candidates": candidates,
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Candidate Business Review Queue",
        "",
        "Fast review queue for building verified zine / artist-book business records.",
        "",
        f"- Candidates: {len(candidates)}",
        "",
        "## How to review",
        "",
        "For each candidate, open the Maps link first. If it looks relevant, copy the business details into the review fields or into `candidate_business_decisions.json`.",
        "",
        "Statuses:",
        "- approved",
        "- rejected",
        "- skipped",
        "",
    ]

    for c in candidates:
        lines.append(f"## {c['candidate_id']} — {c['neighborhood']} — {', '.join(c['suggested_categories'])}")
        lines.append(f"- Priority: {c['priority_score']}")
        lines.append(f"- Query: `{c['query']}`")
        lines.append(f"- Maps: {c['google_maps_url']}")
        lines.append(f"- Search: {c['google_search_url']}")
        lines.append(f"- Status: {c['status']}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Candidates:", len(candidates))

if __name__ == "__main__":
    main()
