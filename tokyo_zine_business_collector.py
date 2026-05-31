
import json
from pathlib import Path
from urllib.parse import quote_plus

OUT_JSON = "memory/tokyo_zine_businesses.json"
OUT_REPORT = "reports/tokyo_zine_businesses.md"

# Place-first collector.
# This is not pretending every record is verified. It creates a practical research queue
# for actual shops, bookstores, fairs, studios, and consignment targets.

KNOWN_PLACES = [
    {
        "name": "MOUNT ZINE",
        "category": "zine_store_fair",
        "neighborhood": "unknown",
        "city": "Tokyo",
        "website": "https://mount.co.jp/",
        "known_status": "known_target",
        "why_relevant": "Direct zine ecosystem target; likely one of the first places to verify for zine placement or participation.",
        "priority": 95,
    },
    {
        "name": "UTRECHT",
        "category": "artist_book_store",
        "neighborhood": "Omotesando/Aoyama",
        "city": "Tokyo",
        "website": "https://utrecht.jp/",
        "known_status": "known_target",
        "why_relevant": "Art book, zine, and independent publishing context; strong printed-matter fit.",
        "priority": 92,
    },
    {
        "name": "flotsam books",
        "category": "photobook_artist_book_store",
        "neighborhood": "unknown",
        "city": "Tokyo",
        "website": "https://flotsambooks.com/",
        "known_status": "known_target",
        "why_relevant": "Photobook / artist-book bookstore; useful benchmark and possible distribution/contact target.",
        "priority": 90,
    },
    {
        "name": "NADiff a/p/a/r/t",
        "category": "art_book_store",
        "neighborhood": "Ebisu",
        "city": "Tokyo",
        "website": "https://www.nadiff.com/",
        "known_status": "known_target",
        "why_relevant": "Art book store and exhibition/bookstore context; good for research and possible book placement.",
        "priority": 88,
    },
    {
        "name": "POST",
        "category": "art_book_store",
        "neighborhood": "Ebisu",
        "city": "Tokyo",
        "website": "https://post-books.info/",
        "known_status": "known_target",
        "why_relevant": "Publication-oriented art book store; useful for benchmarking artist-book presentation.",
        "priority": 86,
    },
    {
        "name": "B&B Shimokitazawa",
        "category": "independent_bookstore",
        "neighborhood": "Shimokitazawa",
        "city": "Tokyo",
        "website": "https://bookandbeer.com/",
        "known_status": "known_target",
        "why_relevant": "Independent bookstore/community space; useful for printed matter research and events.",
        "priority": 82,
    },
    {
        "name": "Book and Sons",
        "category": "art_book_store",
        "neighborhood": "Gakugeidaigaku",
        "city": "Tokyo",
        "website": "https://bookandsons.com/",
        "known_status": "known_target",
        "why_relevant": "Bookstore/gallery context; possible audience for quiet printed work.",
        "priority": 80,
    },
    {
        "name": "TOKYO ART BOOK FAIR",
        "category": "artist_book_fair",
        "neighborhood": "Kiyosumi-shirakawa",
        "city": "Tokyo",
        "website": "https://tokyoartbookfair.com/",
        "known_status": "known_target",
        "why_relevant": "Major ecosystem anchor for artist books, zines, publishers, and small presses.",
        "priority": 100,
    },
    {
        "name": "COMITIA",
        "category": "self_publishing_fair",
        "neighborhood": "Ariake",
        "city": "Tokyo",
        "website": "https://www.comitia.co.jp/",
        "known_status": "watchlist",
        "why_relevant": "Large self-publishing event; useful only if zine/art-object framing fits.",
        "priority": 55,
    },
    {
        "name": "Design Festa",
        "category": "print_market",
        "neighborhood": "Ariake",
        "city": "Tokyo",
        "website": "https://designfesta.com/",
        "known_status": "watchlist",
        "why_relevant": "Market/sales context; possible testing ground but less curatorial.",
        "priority": 50,
    },
]

# Business discovery queue: searches to run manually or through a future Places/API crawler.
DISCOVERY_QUERIES = [
    # Koenji
    {"neighborhood": "Koenji", "query": "高円寺 ZINE ショップ", "category": "zine_shop"},
    {"neighborhood": "Koenji", "query": "高円寺 本屋 ZINE", "category": "independent_bookstore"},
    {"neighborhood": "Koenji", "query": "Koenji zine shop", "category": "zine_shop"},
    {"neighborhood": "Koenji", "query": "Koenji independent bookstore zine", "category": "independent_bookstore"},
    {"neighborhood": "Koenji", "query": "高円寺 アートブック 書店", "category": "artist_book_store"},

    # Nakano
    {"neighborhood": "Nakano", "query": "中野 ZINE ショップ", "category": "zine_shop"},
    {"neighborhood": "Nakano", "query": "中野 本屋 ZINE", "category": "independent_bookstore"},
    {"neighborhood": "Nakano", "query": "Nakano zine shop Tokyo", "category": "zine_shop"},
    {"neighborhood": "Nakano", "query": "Nakano independent bookstore zine", "category": "independent_bookstore"},

    # Shimokitazawa
    {"neighborhood": "Shimokitazawa", "query": "下北沢 ZINE ショップ", "category": "zine_shop"},
    {"neighborhood": "Shimokitazawa", "query": "下北沢 アートブック 書店", "category": "artist_book_store"},
    {"neighborhood": "Shimokitazawa", "query": "Shimokitazawa zine shop", "category": "zine_shop"},
    {"neighborhood": "Shimokitazawa", "query": "Shimokitazawa independent bookstore zine", "category": "independent_bookstore"},

    # Kichijoji / west side
    {"neighborhood": "Kichijoji", "query": "吉祥寺 ZINE ショップ", "category": "zine_shop"},
    {"neighborhood": "Kichijoji", "query": "吉祥寺 アートブック 書店", "category": "artist_book_store"},
    {"neighborhood": "Kichijoji", "query": "Kichijoji zine shop", "category": "zine_shop"},

    # Tokyo-wide
    {"neighborhood": "Tokyo", "query": "東京 ZINE 委託販売", "category": "consignment_target"},
    {"neighborhood": "Tokyo", "query": "東京 ZINE イベント", "category": "zine_fair"},
    {"neighborhood": "Tokyo", "query": "東京 リソグラフ スタジオ ZINE", "category": "risograph_studio"},
    {"neighborhood": "Tokyo", "query": "Tokyo risograph studio zine", "category": "risograph_studio"},
    {"neighborhood": "Tokyo", "query": "Tokyo artist book store", "category": "artist_book_store"},
    {"neighborhood": "Tokyo", "query": "Tokyo photobook bookstore", "category": "photobook_store"},
    {"neighborhood": "Tokyo", "query": "Tokyo small press publisher artist book", "category": "small_press_publisher"},
]

def google_maps_url(query):
    return "https://www.google.com/maps/search/" + quote_plus(query)

def google_search_url(query):
    return "https://www.google.com/search?q=" + quote_plus(query)

def enrich_place(place):
    p = dict(place)
    p.setdefault("address", "")
    p.setdefault("phone", "")
    p.setdefault("instagram", "")
    p.setdefault("email", "")
    p.setdefault("accepts_consignment", "unknown")
    p.setdefault("accepts_submissions", "unknown")
    p.setdefault("visit_status", "not_visited")
    p.setdefault("outreach_status", "not_contacted")
    p.setdefault("next_action", next_action_for(p))
    return p

def next_action_for(p):
    if p.get("category") in {"zine_store_fair", "zine_shop", "artist_book_store", "photobook_artist_book_store", "independent_bookstore"}:
        return "Verify address, check whether they carry small-press zines, then visit with one sample copy."
    if p.get("category") in {"artist_book_fair", "zine_fair", "self_publishing_fair"}:
        return "Check next application window, booth fee, and whether artist-book/zine submissions fit."
    if p.get("category") == "risograph_studio":
        return "Check printing cost, minimum quantity, paper options, and sample quality."
    return "Verify contact and relevance."

def main():
    places = [enrich_place(p) for p in KNOWN_PLACES]

    discovery_tasks = []
    for q in DISCOVERY_QUERIES:
        discovery_tasks.append({
            "neighborhood": q["neighborhood"],
            "category": q["category"],
            "query": q["query"],
            "google_maps_url": google_maps_url(q["query"]),
            "google_search_url": google_search_url(q["query"]),
            "status": "needs_search",
            "goal": "Find real place records: name, address, website, Instagram, consignment/submission policy.",
        })

    result = {
        "title": "Tokyo Zine Business Collector",
        "known_places": places,
        "known_place_count": len(places),
        "discovery_tasks": discovery_tasks,
        "discovery_task_count": len(discovery_tasks),
        "target_place_count": 100,
        "collector_note": "This is a business-first collector. It prioritizes physical/place-based targets over generic web pages.",
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Tokyo Zine Business Collector",
        "",
        "Business-first collector for zine shops, artist-book stores, photobook stores, risograph studios, fairs, and consignment targets.",
        "",
        f"- Known places: {len(places)}",
        f"- Discovery searches queued: {len(discovery_tasks)}",
        "- Target: 100 verified place/business records",
        "",
        "## Known Places",
        "",
    ]

    for p in places:
        lines.append(f"### {p['name']}")
        lines.append(f"- Category: {p['category']}")
        lines.append(f"- Neighborhood: {p['neighborhood']}")
        lines.append(f"- Website: {p['website']}")
        lines.append(f"- Priority: {p['priority']}")
        lines.append(f"- Why relevant: {p['why_relevant']}")
        lines.append(f"- Next action: {p['next_action']}")
        lines.append("")

    lines.append("## Discovery Queue")
    lines.append("")
    for t in discovery_tasks:
        lines.append(f"### {t['neighborhood']} — {t['category']}")
        lines.append(f"- Query: `{t['query']}`")
        lines.append(f"- Maps: {t['google_maps_url']}")
        lines.append(f"- Search: {t['google_search_url']}")
        lines.append(f"- Goal: {t['goal']}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
