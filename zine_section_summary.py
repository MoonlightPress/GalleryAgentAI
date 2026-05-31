
import json
from pathlib import Path
from collections import Counter, defaultdict

SRC = "memory/tokyo_zine_ecosystem.json"
OUT_JSON = "memory/zine_section_summary.json"
OUT_REPORT = "reports/zine_section_summary.md"

NEAR_KOENJI = {
    "Koenji",
    "Nakano",
    "Shimokitazawa",
    "Kichijoji",
    "Shinjuku",
    "Shibuya",
    "Aoyama/Omotesando",
    "Ebisu",
    "Kiyosumi-shirakawa",
    "unknown",  # treated separately in text
}

SHOPLIKE = {
    "zine_shop",
    "artist_book_store",
    "photobook_store",
    "independent_bookstore",
    "photobook_artist_book_store",
    "zine_fair_store",
    "art_book_store",
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    data = load(SRC, {})
    entries = data.get("entries", [])

    by_category = Counter(e.get("category", "unknown") for e in entries)
    by_neighborhood = Counter(e.get("neighborhood", "unknown") for e in entries)

    shoplike_entries = [e for e in entries if e.get("category") in SHOPLIKE]
    known_local = [e for e in entries if e.get("neighborhood") != "unknown"]
    near_koenji = [e for e in entries if e.get("neighborhood") in NEAR_KOENJI and e.get("neighborhood") != "unknown"]
    koenji = [e for e in entries if e.get("neighborhood") == "Koenji"]
    nakano = [e for e in entries if e.get("neighborhood") == "Nakano"]

    top_five = sorted(shoplike_entries, key=lambda x: x.get("confidence", 0), reverse=True)[:5]

    summary = {
        "title": "Book / Zine Path",
        "total_entries": len(entries),
        "shoplike_entries": len(shoplike_entries),
        "known_local_entries": len(known_local),
        "estimated_within_100km_of_koenji": len([e for e in entries if e.get("area") == "Tokyo" or e.get("neighborhood") != "unknown"]),
        "koenji_count": len(koenji),
        "nakano_count": len(nakano),
        "near_koenji_count": len(near_koenji),
        "by_category": dict(by_category),
        "by_neighborhood": dict(by_neighborhood),
        "benefits": [
            "Lowest-friction career path: a zine can be made, printed, placed, and tested without waiting for formal gallery approval.",
            "Good fit for quiet watercolor and works-on-paper images because small printed sequences can carry mood, atmosphere, and intimacy.",
            "Creates proof-of-activity: shop placements, small sales, and documented local distribution can strengthen later TABF or gallery applications.",
            "Builds relationships gradually through bookstores, zine shops, fairs, and small presses.",
        ],
        "practical_solution": [
            "Create two small zines: one image-led and one quieter narrative/sequence-led.",
            "Print 20 copies of each.",
            "Place or pitch them to the top 5 verified shops first.",
            "Add 1 new shop or fair target each month.",
            "Track acceptance, consignment terms, copies placed, copies sold, and follow-up date.",
        ],
        "top_five_initial_targets": top_five,
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(summary, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Zine Section Summary",
        "",
        f"There are currently {summary['estimated_within_100km_of_koenji']} Tokyo-area zine/book ecosystem entries in the database.",
        f"Known Koenji count: {summary['koenji_count']}. Known Nakano count: {summary['nakano_count']}. Known nearby-neighborhood count: {summary['near_koenji_count']}.",
        "",
        "Note: these are crawler/database counts, not verified physical shop counts. Search-discovered entries need human confirmation.",
        "",
        "## Benefits",
    ]

    for b in summary["benefits"]:
        lines.append(f"- {b}")

    lines += ["", "## Practical Solution"]
    for p in summary["practical_solution"]:
        lines.append(f"- {p}")

    lines += ["", "## Initial Top 5 Targets"]
    if top_five:
        for e in top_five:
            lines.append(f"- {e['name']} — {e['category']} — {e['neighborhood']} — confidence {e['confidence']}")
    else:
        lines.append("- No shoplike targets found yet.")

    lines += ["", "## Counts by Category"]
    for k, v in by_category.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Counts by Neighborhood"]
    for k, v in by_neighborhood.most_common():
        lines.append(f"- {k}: {v}")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
