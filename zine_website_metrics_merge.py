
import json
from pathlib import Path

SECTION = "memory/zine_website_top_section.json"
METRICS = "memory/category_metrics.json"
PLAN = "memory/zine_battle_plan_metrics.json"

OUT_JSON = "memory/zine_website_section_final.json"
OUT_REPORT = "reports/zine_website_section_final.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    section = load(SECTION, {})
    metrics = load(METRICS, {"categories": []})
    plan = load(PLAN, {})

    zine_metrics = next((c for c in metrics.get("categories", []) if c.get("category_id") == "zines"), {})

    final = {
        **section,
        "metrics": zine_metrics,
        "battle_plan": plan,
        "top_stat_cards": [
            {"label": "Path Score", "value": zine_metrics.get("path_score")},
            {"label": "Known Targets", "value": zine_metrics.get("known_targets")},
            {"label": "High Priority", "value": zine_metrics.get("high_priority_targets")},
            {"label": "Local Targets", "value": zine_metrics.get("local_targets")},
            {"label": "Estimated Cost", "value": plan.get("estimated_cost")},
            {"label": "Timeline", "value": plan.get("expected_timeline")},
        ],
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(final, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Final Website Section: Zines / Artist Books",
        "",
        section.get("positioning", ""),
        "",
        "## Top Stats",
    ]

    for card in final["top_stat_cards"]:
        lines.append(f"- {card['label']}: {card['value']}")

    lines += ["", "## Why This Path", zine_metrics.get("why_this_path", "")]

    lines += ["", "## Practical Solution"]
    for step in plan.get("steps", []):
        lines.append(f"- {step}")

    lines += ["", "## Phase 1 Targets"]
    for t in plan.get("phase_1_targets", []):
        lines.append(f"- {t['display_name']} — {t['neighborhood']} — {t['opportunity_type']}")

    lines += ["", "## Good Samples"]
    for t in section.get("top_samples", []):
        lines.append(f"### {t['display_name']}")
        lines.append(f"- {t['neighborhood']} — {t['opportunity_type']}")
        lines.append(f"- {t['why_it_matters']}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
