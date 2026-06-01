
import json
from pathlib import Path
from collections import Counter

ZINE_TARGETS = "memory/zine_category_targets.json"
OUT_JSON = "memory/category_metrics.json"
OUT_REPORT = "reports/category_metrics.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def score_category(known_targets, high_priority, local_targets, cost_level, speed_level, difficulty):
    score = 0
    score += min(35, known_targets * 2.5)
    score += min(25, high_priority * 4)
    score += min(20, local_targets * 3)

    cost_bonus = {"very_low": 20, "low": 16, "medium": 10, "high": 4}.get(cost_level, 8)
    speed_bonus = {"fast": 20, "medium": 12, "slow": 5}.get(speed_level, 8)
    difficulty_bonus = {"easy": 15, "medium": 9, "hard": 3}.get(difficulty, 6)

    score += cost_bonus + speed_bonus + difficulty_bonus
    return min(100, round(score))

def build_zine_metrics():
    data = load(ZINE_TARGETS, {"targets": []})
    targets = data.get("targets", [])

    by_neighborhood = Counter(t.get("neighborhood", "unknown") for t in targets)
    by_type = Counter(t.get("opportunity_type", "unknown") for t in targets)

    high_priority = [t for t in targets if t.get("tier") == 1]
    local = [t for t in targets if t.get("neighborhood") in {"Koenji", "Nakano"}]

    metrics = {
        "category_id": "zines",
        "title": "Zines / Artist Books",
        "difficulty": "easy",
        "cost": "low",
        "speed": "fast",
        "known_targets": len(targets),
        "high_priority_targets": len(high_priority),
        "local_targets": len(local),
        "koenji_targets": by_neighborhood.get("Koenji", 0),
        "nakano_targets": by_neighborhood.get("Nakano", 0),
        "kichijoji_targets": by_neighborhood.get("Kichijoji", 0),
        "shimokitazawa_targets": by_neighborhood.get("Shimokitazawa", 0),
        "neighborhood_counts": dict(by_neighborhood),
        "type_counts": dict(by_type),
        "estimated_cost_min_yen": 10000,
        "estimated_cost_max_yen": 25000,
        "expected_time_to_first_result": "1-3 months",
        "success_condition": "Two finished zines, five outreach attempts, one accepted placement.",
    }

    metrics["path_score"] = score_category(
        metrics["known_targets"],
        metrics["high_priority_targets"],
        metrics["local_targets"],
        metrics["cost"],
        metrics["speed"],
        metrics["difficulty"],
    )

    metrics["why_this_path"] = (
        "The zine path is currently the fastest route to public visibility. "
        f"There are {metrics['known_targets']} identified targets, including "
        f"{metrics['local_targets']} in Koenji/Nakano. Costs are relatively low, "
        "and one printed project can be reused for shop placement, applications, sales, fairs, "
        "portfolio proof, and later publishing outreach."
    )

    return metrics

def placeholder_categories():
    # These placeholders let the dashboard compare paths even before each category has deep data.
    return [
        {
            "category_id": "publishing",
            "title": "Publishing",
            "difficulty": "medium",
            "cost": "very_low",
            "speed": "medium",
            "known_targets": 8,
            "high_priority_targets": 3,
            "local_targets": 0,
            "estimated_cost_min_yen": 0,
            "estimated_cost_max_yen": 5000,
            "expected_time_to_first_result": "2-6 months",
            "success_condition": "One strong PDF pitch, five suitable publishers, two careful outreach attempts.",
            "why_this_path": "Publishing is a strong secondary path after a zine or artist-book object exists. It is low-cost but slower and more relationship-dependent.",
        },
        {
            "category_id": "galleries",
            "title": "Galleries",
            "difficulty": "hard",
            "cost": "low",
            "speed": "slow",
            "known_targets": 6,
            "high_priority_targets": 1,
            "local_targets": 1,
            "estimated_cost_min_yen": 0,
            "estimated_cost_max_yen": 10000,
            "expected_time_to_first_result": "3-12 months",
            "success_condition": "One coherent portfolio PDF, one statement, and targeted applications to best-fit spaces.",
            "why_this_path": "Galleries matter, but they are slower and more selective. They become stronger after real-world proof from zines, shops, or small fairs.",
        },
        {
            "category_id": "licensing",
            "title": "Licensing",
            "difficulty": "medium",
            "cost": "very_low",
            "speed": "medium",
            "known_targets": 0,
            "high_priority_targets": 0,
            "local_targets": 0,
            "estimated_cost_min_yen": 0,
            "estimated_cost_max_yen": 3000,
            "expected_time_to_first_result": "3-9 months",
            "success_condition": "A clean sample sheet, contact list, and one focused licensing vertical.",
            "why_this_path": "Licensing could matter later for book covers, stationery, magazines, or album art, but the current database is not built out yet.",
        },
        {
            "category_id": "cafes_shops",
            "title": "Cafés / Shops",
            "difficulty": "easy",
            "cost": "low",
            "speed": "medium",
            "known_targets": 0,
            "high_priority_targets": 0,
            "local_targets": 0,
            "estimated_cost_min_yen": 3000,
            "estimated_cost_max_yen": 15000,
            "expected_time_to_first_result": "1-4 months",
            "success_condition": "A small wall-ready set or print display and five local outreach attempts.",
            "why_this_path": "Cafés and shops can be useful for local visibility, but the current priority is stronger through zine/book targets.",
        },
    ]

def enrich_placeholder_scores(categories):
    for c in categories:
        c["path_score"] = score_category(
            c["known_targets"],
            c["high_priority_targets"],
            c["local_targets"],
            c["cost"],
            c["speed"],
            c["difficulty"],
        )
    return categories

def main():
    zines = build_zine_metrics()
    categories = [zines] + enrich_placeholder_scores(placeholder_categories())
    categories.sort(key=lambda x: x["path_score"], reverse=True)

    result = {
        "title": "Career Category Metrics",
        "categories": categories,
        "recommended_category": categories[0]["category_id"] if categories else None,
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Career Category Metrics",
        "",
        f"Recommended category: {categories[0]['title'] if categories else 'none'}",
        "",
        "| Category | Score | Difficulty | Cost | Speed | Targets | High Priority | Local |",
        "|---|---:|---|---|---|---:|---:|---:|",
    ]

    for c in categories:
        lines.append(
            f"| {c['title']} | {c['path_score']} | {c['difficulty']} | {c['cost']} | {c['speed']} | "
            f"{c['known_targets']} | {c['high_priority_targets']} | {c['local_targets']} |"
        )

    lines += ["", "## Zines / Artist Books", ""]
    for k in [
        "path_score",
        "difficulty",
        "cost",
        "speed",
        "known_targets",
        "high_priority_targets",
        "local_targets",
        "koenji_targets",
        "nakano_targets",
        "kichijoji_targets",
        "shimokitazawa_targets",
        "estimated_cost_min_yen",
        "estimated_cost_max_yen",
        "expected_time_to_first_result",
        "success_condition",
    ]:
        if k in zines:
            lines.append(f"- {k}: {zines[k]}")

    lines += ["", "## Why This Path", zines["why_this_path"]]

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
