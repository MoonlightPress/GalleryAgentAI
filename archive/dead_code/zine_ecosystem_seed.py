
import json
from pathlib import Path

OUT_JSON = "memory/zine_ecosystem_seed.json"
OUT_REPORT = "reports/zine_ecosystem_seed.md"

# Seed list. This is intentionally mixed: confirmed known targets + research placeholders.
# Later crawler/search passes should replace placeholders with verified records.
SEED = [
    {"name": "MOUNT ZINE", "category": "zine_fair_store", "area": "Tokyo", "neighborhood": "unknown", "status": "known_target", "reason": "Direct zine ecosystem target."},
    {"name": "UTRECHT", "category": "artist_book_store", "area": "Tokyo", "neighborhood": "Omotesando/Aoyama", "status": "known_target", "reason": "Art book / zine / independent publishing context."},
    {"name": "flotsam books", "category": "photobook_artist_book_store", "area": "Tokyo", "neighborhood": "Tokyo", "status": "known_target", "reason": "Bookshop/gallery hybrid and photobook/art-book context."},
    {"name": "NADiff a/p/a/r/t", "category": "art_book_store", "area": "Tokyo", "neighborhood": "Ebisu", "status": "known_target", "reason": "Art book ecosystem and exhibition/bookstore context."},
    {"name": "B&B Shimokitazawa", "category": "independent_bookstore", "area": "Tokyo", "neighborhood": "Shimokitazawa", "status": "known_target", "reason": "Bookstore/community space; useful for printed matter research."},
    {"name": "POST", "category": "art_book_store", "area": "Tokyo", "neighborhood": "Ebisu", "status": "known_target", "reason": "Art book / publication-oriented space."},
    {"name": "Book and Sons", "category": "art_book_store", "area": "Tokyo", "neighborhood": "Gakugeidaigaku", "status": "known_target", "reason": "Bookstore/gallery context; possible printed matter audience."},
    {"name": "Photobook Cafe", "category": "photobook_store", "area": "Tokyo", "neighborhood": "unknown", "status": "known_target", "reason": "Photobook/community target."},
    {"name": "TOKYO ART BOOK FAIR", "category": "artist_book_fair", "area": "Tokyo", "neighborhood": "Kiyosumi-shirakawa / MOT", "status": "known_target", "reason": "Major art-book fair and ecosystem anchor."},
    {"name": "COMITIA", "category": "self_publishing_fair", "area": "Tokyo", "neighborhood": "Big Sight / Ariake", "status": "watchlist", "reason": "Large self-publishing ecosystem; may be too manga/doujinshi-oriented."},
    {"name": "Design Festa", "category": "print_market", "area": "Tokyo", "neighborhood": "Big Sight / Ariake", "status": "watchlist", "reason": "Sales visibility but less curatorial; useful only as market test."},
    {"name": "Hand Saw Press", "category": "small_press_publisher", "area": "Tokyo", "neighborhood": "unknown", "status": "known_target", "reason": "TABF-linked small press / publishing ecosystem."},
    {"name": "Studio Yukiko", "category": "small_press_publisher", "area": "Germany/Tokyo link", "neighborhood": "international", "status": "known_target", "reason": "TABF-linked independent publishing ecosystem."},
    {"name": "The Thing Quarterly", "category": "small_press_publisher", "area": "International", "neighborhood": "international", "status": "known_target", "reason": "Art publication / edition model."},
    {"name": "Self Publish, Be Happy", "category": "self_publishing_platform", "area": "International", "neighborhood": "online/global", "status": "known_target", "reason": "Strong photobook/zine/self-publishing relevance."},
    {"name": "Offprint", "category": "artist_book_fair", "area": "International", "neighborhood": "global", "status": "known_target", "reason": "International art publishing fair."},
    {"name": "Printed Matter Art Book Fairs", "category": "artist_book_fair", "area": "International", "neighborhood": "New York/LA", "status": "known_target", "reason": "Major artist-book fair ecosystem."},
    {"name": "Center for Book Arts", "category": "book_arts_opportunity", "area": "International", "neighborhood": "New York", "status": "watchlist", "reason": "Book arts, paper, editions; likely stretch target."},
]

RESEARCH_TARGETS = {
    "Koenji": {
        "zine_shops_target": 3,
        "artist_book_store_target": 1,
        "independent_bookstore_target": 3,
        "notes": "Priority local research zone. Fastest possible fieldwork."
    },
    "Nakano": {
        "zine_shops_target": 1,
        "artist_book_store_target": 1,
        "independent_bookstore_target": 2,
        "notes": "Secondary local zone near Koenji."
    },
    "Shimokitazawa": {
        "zine_shops_target": 4,
        "artist_book_store_target": 2,
        "independent_bookstore_target": 4,
        "notes": "Strong culture/bookstore/indie retail zone."
    },
    "Kichijoji": {
        "zine_shops_target": 2,
        "artist_book_store_target": 1,
        "independent_bookstore_target": 3,
        "notes": "Good west-side creative retail zone."
    },
    "20km radius of Koenji": {
        "zine_shops_target": 10,
        "artist_book_store_target": 8,
        "independent_bookstore_target": 20,
        "notes": "Main expansion zone."
    }
}

def main():
    Path("memory").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    data = {
        "seed_opportunities": SEED,
        "research_targets": RESEARCH_TARGETS,
        "target_total": 100,
        "current_seed_count": len(SEED),
    }

    json.dump(data, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Zine Ecosystem Seed",
        "",
        f"- Current seed count: {len(SEED)}",
        "- Target total: 100+",
        "",
        "## Seed Opportunities",
        "",
    ]

    for x in SEED:
        lines.append(f"### {x['name']}")
        lines.append(f"- Category: {x['category']}")
        lines.append(f"- Area: {x['area']}")
        lines.append(f"- Neighborhood: {x['neighborhood']}")
        lines.append(f"- Status: {x['status']}")
        lines.append(f"- Reason: {x['reason']}")
        lines.append("")

    lines.append("## Local Research Targets")
    lines.append("")
    for area, t in RESEARCH_TARGETS.items():
        lines.append(f"### {area}")
        for k, v in t.items():
            lines.append(f"- {k}: {v}")
        lines.append("")

    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
