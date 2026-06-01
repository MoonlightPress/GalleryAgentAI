
import json
from pathlib import Path

OUT_TARGETS = "memory/publishing_category_targets.json"
OUT_SECTION = "memory/publishing_website_section.json"
OUT_REPORT = "reports/publishing_website_section.md"

TARGETS = [
    {
        "display_name": "torch press",
        "career_category": "publishing",
        "opportunity_type": "small_press_publisher",
        "tier": 1,
        "neighborhood": "Tokyo",
        "confidence": 72,
        "why_it_matters": "Small press / art-book publishing target. Useful for artist-book positioning after a finished object exists.",
        "first_action": "Review recent titles and identify whether her work fits their publication style.",
        "status": "Not started",
    },
    {
        "display_name": "twelvebooks",
        "career_category": "publishing",
        "opportunity_type": "art_book_distributor_publisher",
        "tier": 1,
        "neighborhood": "Tokyo",
        "confidence": 70,
        "why_it_matters": "Art-book distribution/publishing ecosystem target. Useful for understanding professional presentation standards.",
        "first_action": "Research comparable books and presentation formats.",
        "status": "Not started",
    },
    {
        "display_name": "shashasha",
        "career_category": "publishing",
        "opportunity_type": "photobook_platform",
        "tier": 1,
        "neighborhood": "Tokyo",
        "confidence": 68,
        "why_it_matters": "Photobook-oriented platform. Relevant if her work develops into book sequencing or editioned projects.",
        "first_action": "Review listed artists/books and compare format, pricing, and tone.",
        "status": "Not started",
    },
    {
        "display_name": "Komiyama Tokyo",
        "career_category": "publishing",
        "opportunity_type": "art_photobook_store",
        "tier": 2,
        "neighborhood": "Tokyo",
        "confidence": 60,
        "why_it_matters": "Strong art/photo book reference point. Better as research/benchmark than first outreach.",
        "first_action": "Use as benchmark for book quality and audience expectations.",
        "status": "Not started",
    },
    {
        "display_name": "Book Obscura",
        "career_category": "publishing",
        "opportunity_type": "photobook_store",
        "tier": 2,
        "neighborhood": "Kichijoji",
        "confidence": 58,
        "why_it_matters": "Photobook specialist. Useful if her project becomes image-sequence or book-object focused.",
        "first_action": "Research whether the work belongs closer to photobook or zine format.",
        "status": "Not started",
    },
    {
        "display_name": "Books Ruhe",
        "career_category": "publishing",
        "opportunity_type": "independent_bookstore",
        "tier": 2,
        "neighborhood": "Kichijoji",
        "confidence": 55,
        "why_it_matters": "Independent bookstore reference and possible later placement target.",
        "first_action": "Research stock and independent publication compatibility.",
        "status": "Not started",
    },
]

def main():
    Path("memory").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    section = {
        "career_category": "publishing",
        "title": "Publishing",
        "subtitle": "Small presses, art-book publishers, photobook platforms, and publication-oriented stores.",
        "positioning": "Publishing is the next step after the zine path: once there is a finished printed object, it can become a pitch, sample, portfolio proof, and conversation starter.",
        "top_stat_cards": [
            {"label": "Path Score", "value": 73},
            {"label": "Known Targets", "value": len(TARGETS)},
            {"label": "High Priority", "value": 3},
            {"label": "Local Targets", "value": 0},
            {"label": "Estimated Cost", "value": "¥0–¥5,000"},
            {"label": "Timeline", "value": "2–6 months"},
        ],
        "metrics": {
            "difficulty": "medium",
            "cost": "very low",
            "speed": "medium",
            "known_targets": len(TARGETS),
            "high_priority_targets": 3,
            "local_targets": 0,
            "path_score": 73,
            "why_this_path": "Publishing is low-cost and potentially high-value, but slower than zines. It becomes much stronger after the artist has one finished zine or artist-book prototype to show.",
        },
        "battle_plan": {
            "success_condition": "One strong publication package, five researched publishers/platforms, and two careful outreach attempts.",
            "estimated_cost": "¥0–¥5,000",
            "expected_timeline": "2–6 months",
            "steps": [
                "Finish one zine or artist-book prototype first.",
                "Create a short portfolio PDF.",
                "Research three Tier 1 publishing targets.",
                "Compare her work to 5–10 published books or artists.",
                "Prepare one concise publication pitch.",
                "Send two careful outreach emails only when the material is ready.",
            ],
            "phase_1_targets": [t for t in TARGETS if t["tier"] == 1],
            "phase_2_targets": [t for t in TARGETS if t["tier"] == 2],
        },
        "top_samples": TARGETS,
    }

    json.dump({"career_category": "publishing", "target_count": len(TARGETS), "targets": TARGETS}, open(OUT_TARGETS, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(section, open(OUT_SECTION, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Website Section: Publishing",
        "",
        section["positioning"],
        "",
        "## Top Stats",
    ]
    for card in section["top_stat_cards"]:
        lines.append(f"- {card['label']}: {card['value']}")

    lines += ["", "## Why This Path", section["metrics"]["why_this_path"], "", "## Battle Plan"]
    for step in section["battle_plan"]["steps"]:
        lines.append(f"- {step}")

    lines += ["", "## Phase 1 Targets"]
    for t in section["battle_plan"]["phase_1_targets"]:
        lines.append(f"- {t['display_name']} — {t['opportunity_type']}")

    lines += ["", "## Good Samples"]
    for t in TARGETS:
        lines.append(f"### {t['display_name']}")
        lines.append(f"- {t['neighborhood']} — {t['opportunity_type']}")
        lines.append(f"- {t['why_it_matters']}")
        lines.append("")

    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_TARGETS)
    print("Wrote", OUT_SECTION)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
