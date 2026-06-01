
import json
from pathlib import Path

TARGETS = "memory/zine_category_targets.json"
METRICS = "memory/category_metrics.json"
OUT_JSON = "memory/zine_battle_plan_metrics.json"
OUT_REPORT = "reports/zine_battle_plan_metrics.md"

PHASE_1_NAMES = {
    "Tacoche",
    "LOCAL Gallery・Books",
    "Dig A Hole Zines",
    "本店・本屋の実験室",
    "そぞろ書房",
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    targets_data = load(TARGETS, {"targets": []})
    metrics_data = load(METRICS, {"categories": []})

    targets = targets_data.get("targets", [])
    zine_metrics = next((c for c in metrics_data.get("categories", []) if c.get("category_id") == "zines"), {})

    phase1 = [t for t in targets if t["display_name"] in PHASE_1_NAMES]
    phase2 = [t for t in targets if t["display_name"] not in PHASE_1_NAMES][:7]

    plan = {
        "title": "Zine / Artist Book Battle Plan",
        "current_position": {
            "placements": 0,
            "known_targets": zine_metrics.get("known_targets", len(targets)),
            "high_priority_targets": zine_metrics.get("high_priority_targets", 0),
            "local_targets": zine_metrics.get("local_targets", 0),
        },
        "score": zine_metrics.get("path_score"),
        "difficulty": zine_metrics.get("difficulty"),
        "cost": zine_metrics.get("cost"),
        "speed": zine_metrics.get("speed"),
        "estimated_cost": f"¥{zine_metrics.get('estimated_cost_min_yen', 10000):,}–¥{zine_metrics.get('estimated_cost_max_yen', 25000):,}",
        "expected_timeline": zine_metrics.get("expected_time_to_first_result", "1-3 months"),
        "success_condition": zine_metrics.get("success_condition"),
        "best_route": "Koenji + Nakano",
        "phase_1_targets": phase1,
        "phase_2_targets": phase2,
        "steps": [
            "Select one coherent body of work.",
            "Create two small zines: one image-led, one quieter narrative/atmosphere sequence.",
            "Print 20 copies of each.",
            "Visit or contact the five Phase 1 targets.",
            "Track whether each accepts consignment, direct purchase, event participation, or no submissions.",
            "Use any placement as proof-of-activity for fairs, publishers, and galleries.",
        ],
        "tracking_fields": [
            "target",
            "contacted",
            "visited",
            "accepts_consignment",
            "copies_placed",
            "copies_sold",
            "follow_up_date",
            "notes",
        ],
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(plan, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Zine / Artist Book Battle Plan",
        "",
        f"- Score: {plan['score']}",
        f"- Difficulty: {plan['difficulty']}",
        f"- Cost: {plan['cost']}",
        f"- Speed: {plan['speed']}",
        f"- Estimated cost: {plan['estimated_cost']}",
        f"- Expected timeline: {plan['expected_timeline']}",
        f"- Success condition: {plan['success_condition']}",
        "",
        "## Current Position",
        f"- Current placements: {plan['current_position']['placements']}",
        f"- Known targets: {plan['current_position']['known_targets']}",
        f"- High-priority targets: {plan['current_position']['high_priority_targets']}",
        f"- Local targets: {plan['current_position']['local_targets']}",
        "",
        "## Best Route",
        plan["best_route"],
        "",
        "## Phase 1 Targets",
    ]

    for t in phase1:
        lines.append(f"- {t['display_name']} — {t['neighborhood']} — {t['opportunity_type']}")

    lines += ["", "## Phase 2 Targets"]
    for t in phase2:
        lines.append(f"- {t['display_name']} — {t['neighborhood']} — {t['opportunity_type']}")

    lines += ["", "## Steps"]
    for s in plan["steps"]:
        lines.append(f"- {s}")

    lines += ["", "## Tracking Fields"]
    for f in plan["tracking_fields"]:
        lines.append(f"- {f}")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
