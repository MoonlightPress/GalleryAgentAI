
import json
from pathlib import Path
from collections import Counter

TARGETS = "memory/zine_category_targets.json"
OUT_JSON = "memory/zine_website_top_section.json"
OUT_REPORT = "reports/zine_website_top_section.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    data = load(TARGETS, {"targets": []})
    targets = data.get("targets", [])

    by_neighborhood = Counter(t["neighborhood"] for t in targets)
    tier1 = [t for t in targets if t["tier"] == 1]
    koenji_nakano = [t for t in targets if t["neighborhood"] in {"Koenji", "Nakano"}]

    top_samples = targets[:10]
    phase1 = [
        t for t in targets
        if t["display_name"] in {
            "Tacoche",
            "LOCAL Gallery・Books",
            "Dig A Hole Zines",
            "本店・本屋の実験室",
            "そぞろ書房",
        }
    ]

    section = {
        "career_category": "zines",
        "title": "Zines / Artist Books",
        "subtitle": "Small printed works, zine shops, artist-book stores, bookstore galleries, and local publishing communities.",
        "positioning": "This is the lowest-friction career path: make a small printed object, place it in a few real shops, and use those placements as proof-of-activity for larger fairs, galleries, and publishers.",
        "known_target_count": len(targets),
        "high_priority_count": len(tier1),
        "koenji_nakano_count": len(koenji_nakano),
        "neighborhood_counts": dict(by_neighborhood),
        "benefits": [
            "Fast to test: a zine can be made and printed faster than waiting for gallery approval.",
            "Personal fit: quiet watercolor, works-on-paper, and intimate visual sequences suit small printed formats.",
            "Real-world proof: shop placements and small sales make later applications stronger.",
            "Relationship path: bookstores and zine communities create gradual, low-pressure career contacts.",
            "Reusable asset: one zine can function as product, portfolio object, application material, and social-media content.",
        ],
        "practical_solution": {
            "goal": "Place two small zines in five strong targets.",
            "make": [
                "Zine A: image-led, strongest visual sequence.",
                "Zine B: quieter narrative/atmosphere sequence.",
                "Print 20 copies of each."
            ],
            "first_route": "Koenji + Nakano",
            "phase_1_targets": phase1,
            "monthly_habit": "Add one new shop, fair, publisher, or bookstore-gallery target each month.",
            "track": [
                "contacted",
                "visited",
                "accepted consignment",
                "copies placed",
                "copies sold",
                "follow-up date"
            ],
        },
        "top_samples": top_samples,
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(section, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Website Top Section: Zines / Artist Books",
        "",
        section["positioning"],
        "",
        f"- Known website-ready targets: {section['known_target_count']}",
        f"- High-priority targets: {section['high_priority_count']}",
        f"- Koenji + Nakano targets: {section['koenji_nakano_count']}",
        "",
        "## Neighborhood Counts",
    ]

    for k, v in by_neighborhood.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Benefits"]
    for b in section["benefits"]:
        lines.append(f"- {b}")

    lines += ["", "## Practical Solution"]
    lines.append(f"- Goal: {section['practical_solution']['goal']}")
    lines.append(f"- First route: {section['practical_solution']['first_route']}")
    for x in section["practical_solution"]["make"]:
        lines.append(f"- {x}")
    lines.append(f"- Monthly habit: {section['practical_solution']['monthly_habit']}")

    lines += ["", "## Phase 1 Targets"]
    for t in phase1:
        lines.append(f"- {t['display_name']} — {t['neighborhood']} — {t['opportunity_type']}")

    lines += ["", "## Good Samples"]
    for t in top_samples:
        lines.append(f"### {t['display_name']}")
        lines.append(f"- Neighborhood: {t['neighborhood']}")
        lines.append(f"- Type: {t['opportunity_type']}")
        lines.append(f"- Why it matters: {t['why_it_matters']}")
        lines.append(f"- First action: {t['first_action']}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
