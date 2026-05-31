
import json
from pathlib import Path

SEED = "memory/zine_ecosystem_seed.json"
SUMMARY = "memory/zine_ecosystem_summary.json"

OUT_JSON = "memory/zine_battle_plan.json"
OUT_REPORT = "reports/zine_battle_plan.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    seed = load(SEED, {})
    summary = load(SUMMARY, {})

    plan = {
        "channel": "Book / Zine Path",
        "current_coverage": summary.get("coverage_percent"),
        "target_total": summary.get("target_total"),
        "known_count": summary.get("known_count"),
        "strategic_goal": "Turn one body of work into a zine or artist-book object, then place it into a local small-press ecosystem.",
        "maximum_impact_action": "Map Koenji + Nakano first, then physically visit the top 3 shops with one sample zine.",
        "30_day_plan": [
            "Map 3 Koenji zine/book shops.",
            "Map 1 Nakano zine/book shop.",
            "Map 10 shops/fairs/studios within 20km of Koenji.",
            "Choose one zine or artist-book concept.",
            "Prepare a 12-20 page PDF.",
            "Print 20 test copies.",
            "Visit 3 shops with one sample copy.",
            "Track: accepts consignment, buys wholesale, accepts event applications, no fit."
        ],
        "60_day_plan": [
            "Secure 1-3 placements.",
            "Approach 5 additional shops.",
            "Prepare a short bilingual zine description.",
            "Document real-world placements on Instagram/TikTok.",
            "Use placements as proof-of-activity for TABF or similar applications."
        ],
        "metrics": [
            "shops mapped",
            "shops visited",
            "copies printed",
            "copies placed",
            "copies sold",
            "contacts collected",
            "follow-up dates"
        ],
        "next_research_queries": [
            "zine shop Koenji",
            "independent bookstore Koenji zine",
            "artist book store Tokyo",
            "risograph studio Tokyo zine",
            "zine fair Tokyo",
            "small press publisher Tokyo artist book",
            "photobook store Tokyo",
            "independent bookstore Shimokitazawa zine"
        ]
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(plan, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Zine Battle Plan",
        "",
        f"Channel: {plan['channel']}",
        f"Current coverage: {plan['known_count']} / {plan['target_total']} ({plan['current_coverage']}%)",
        "",
        "## Strategic Goal",
        plan["strategic_goal"],
        "",
        "## Maximum Impact Action",
        plan["maximum_impact_action"],
        "",
        "## 30-Day Plan",
    ]

    for x in plan["30_day_plan"]:
        lines.append(f"- {x}")

    lines += ["", "## 60-Day Plan"]
    for x in plan["60_day_plan"]:
        lines.append(f"- {x}")

    lines += ["", "## Metrics"]
    for x in plan["metrics"]:
        lines.append(f"- {x}")

    lines += ["", "## Next Research Queries"]
    for x in plan["next_research_queries"]:
        lines.append(f"- {x}")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
