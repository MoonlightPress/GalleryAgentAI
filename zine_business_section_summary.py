
import json
from pathlib import Path
from collections import Counter

SRC = "memory/tokyo_zine_businesses.json"
OUT_JSON = "memory/zine_business_section_summary.json"
OUT_REPORT = "reports/zine_business_section_summary.md"

SHOP_CATEGORIES = {
    "zine_store_fair", "zine_shop", "artist_book_store", "photobook_artist_book_store",
    "photobook_store", "independent_bookstore", "art_book_store"
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    data = load(SRC, {})
    places = data.get("known_places", [])
    tasks = data.get("discovery_tasks", [])

    by_neighborhood = Counter(p.get("neighborhood", "unknown") for p in places)
    by_category = Counter(p.get("category", "unknown") for p in places)
    task_by_neighborhood = Counter(t.get("neighborhood", "unknown") for t in tasks)

    shops = [p for p in places if p.get("category") in SHOP_CATEGORIES]
    tokyo_area = [p for p in places if p.get("city") == "Tokyo"]

    top_targets = sorted(shops, key=lambda x: x.get("priority", 0), reverse=True)[:5]

    summary = {
        "title": "Zine / Artist Book Business Strategy",
        "known_places": len(places),
        "known_shoplike_places": len(shops),
        "estimated_within_100km_of_koenji": len(tokyo_area),
        "known_koenji": by_neighborhood.get("Koenji", 0),
        "known_nakano": by_neighborhood.get("Nakano", 0),
        "known_shimokitazawa": by_neighborhood.get("Shimokitazawa", 0),
        "discovery_queries": len(tasks),
        "task_by_neighborhood": dict(task_by_neighborhood),
        "top_targets": top_targets,
        "benefits": [
            "This is the lowest-friction path: zines and small printed works can be produced and tested without waiting for a formal exhibition.",
            "A shop placement creates proof that the work exists in the world, which can support later applications to fairs and galleries.",
            "Local shops create relationship opportunities: the artist can learn what sells, what people respond to, and which formats are realistic.",
            "The path is modular: one zine can become shop inventory, fair inventory, application material, Instagram content, and a portfolio object."
        ],
        "practical_solution": [
            "Create two zines: one image-led and one quieter sequence/narrative-led.",
            "Print 20 copies of each.",
            "Start with the top 5 verified targets.",
            "Add 1 new shop, fair, or studio to the outreach list each month.",
            "Track consignment terms, copies placed, copies sold, and follow-up dates."
        ],
        "next_data_goal": "Turn discovery queries into verified place records with address, website, Instagram, and consignment/submission policy.",
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(summary, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Zine Business Section Summary",
        "",
        f"There are currently {summary['estimated_within_100km_of_koenji']} known Tokyo-area zine/book business targets in the database.",
        f"Known Koenji count: {summary['known_koenji']}. Known Nakano count: {summary['known_nakano']}. Known Shimokitazawa count: {summary['known_shimokitazawa']}.",
        f"Discovery searches queued: {summary['discovery_queries']}.",
        "",
        "These are database counts, not final verified physical-shop counts.",
        "",
        "## Benefits",
    ]

    for b in summary["benefits"]:
        lines.append(f"- {b}")

    lines += ["", "## Practical Solution"]
    for s in summary["practical_solution"]:
        lines.append(f"- {s}")

    lines += ["", "## Top 5 Initial Targets"]
    for p in top_targets:
        lines.append(f"- {p['name']} — {p['category']} — {p['neighborhood']} — priority {p['priority']}")

    lines += ["", "## Known Counts by Category"]
    for k, v in by_category.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Known Counts by Neighborhood"]
    for k, v in by_neighborhood.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Discovery Queue by Neighborhood"]
    for k, v in task_by_neighborhood.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Next Data Goal", summary["next_data_goal"]]

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
