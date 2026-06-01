
import json
from pathlib import Path
from collections import defaultdict, Counter

RAW = Path("memory/multi_ingress_raw_candidates.json")
COMPACT_PATHS = [
    Path("memory/compact_opportunities.json"),
    Path("Memory/compact_opportunities.json"),
    Path("deploy_data/compact_opportunities.json"),
]

OUT_JSON = Path("memory/category_context.json")
OUT_DEPLOY = Path("deploy_data/category_context.json")
OUT_REPORT = Path("reports/category_context.md")

CATEGORY_NAMES = {
    "contests": "Open Calls / Contests",
    "zines": "Art Book & Zine Fairs",
    "residencies": "Residencies",
    "publishing": "Publishing / Small Press",
}

CATEGORY_CONFIG = {
    "contests": {
        "actionability_base": 82,
        "estimated_cost": "¥0–¥10,000",
        "estimated_effort": "2–4 hours for first review; 1–2 days for a full submission",
        "timeline": "1–2 months",
        "why_this_matters": "Open calls have clear actions: verify deadline, prepare files, submit. They are the cleanest way to turn research into applications.",
        "recommendation": "Review the top five, then choose two with clear fit and manageable requirements.",
        "battle_plan": [
            "Open the top five sources.",
            "Confirm deadline, fee, eligibility, image requirements, and application form.",
            "Reject anything with poor fit or unclear terms.",
            "Prepare one reusable application package.",
            "Submit to two high-fit opportunities.",
        ],
    },
    "zines": {
        "actionability_base": 88,
        "estimated_cost": "¥10,000–¥50,000",
        "estimated_effort": "1–2 days to prepare fair/application research; 1–3 weeks if printing new work",
        "timeline": "1–6 months",
        "why_this_matters": "Zine and art-book fairs connect directly to the existing zine/shop path and give a finished printed object a public destination.",
        "recommendation": "Keep shop placement as Phase 1 and use fairs as Phase 2 once two zines exist.",
        "battle_plan": [
            "Confirm the next application windows for major fairs.",
            "Prepare two small zines or one polished artist-book prototype.",
            "Track booth fee, deadline, required images, and table size.",
            "Apply to one realistic fair and visit one major fair for research.",
            "Use shop placements as support material for fair applications.",
        ],
    },
    "residencies": {
        "actionability_base": 62,
        "estimated_cost": "Varies widely; often travel/time cost is larger than application cost",
        "estimated_effort": "4–8 hours to evaluate; several days for a serious application",
        "timeline": "3–12 months",
        "why_this_matters": "Residencies can be career-changing, but they are higher effort and usually require a stronger statement, portfolio, and project proposal.",
        "recommendation": "Monitor now. Apply only to unusually strong fits until the portfolio package is stronger.",
        "battle_plan": [
            "Identify the top three realistic residency programs.",
            "Check eligibility, duration, language, cost, and housing.",
            "Prepare a reusable artist statement and project proposal outline.",
            "Do not apply broadly; choose only high-fit programs.",
            "Revisit monthly as deadlines change.",
        ],
    },
    "publishing": {
        "actionability_base": 58,
        "estimated_cost": "¥0–¥5,000",
        "estimated_effort": "2–4 hours to research; longer once a proposal is ready",
        "timeline": "2–6 months",
        "why_this_matters": "Publishing is high-value but noisy. It becomes practical after a finished zine, artist book, or strong PDF pitch exists.",
        "recommendation": "Use publishing research to benchmark, not to spam submissions. Approach carefully after the printed object exists.",
        "battle_plan": [
            "Separate real publishers from articles, directories, and self-publishing services.",
            "Choose three publisher/platform references.",
            "Compare her work against similar books.",
            "Prepare one concise PDF pitch.",
            "Send at most two careful outreach messages.",
        ],
    },
}

def load(path, fallback):
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback

def find_existing(path_list, fallback):
    for p in path_list:
        if p.exists():
            return p, load(p, fallback)
    return None, fallback

def priority_bucket(score):
    try:
        s = float(score)
    except Exception:
        s = 0
    if s >= 75:
        return "high"
    if s >= 55:
        return "medium"
    return "low"

def is_noise(title, url):
    blob = f"{title} {url}".lower()
    bad_terms = [
        "top 10", "complete guide", "huge list", "list of", "directory",
        "worth visiting", "hidden gems", "recommended", "まとめ", "一覧",
        "guide", "ghostwriting", "wikipedia", "blog"
    ]
    return any(t in blob for t in bad_terms)

def clean_title(title):
    return str(title or "").strip()[:120]

def actionability_score(category, high, medium, total, has_forms, has_deadlines):
    cfg = CATEGORY_CONFIG.get(category, {})
    score = cfg.get("actionability_base", 50)

    score += min(10, high * 2)
    score += min(8, medium * 0.5)
    score += min(8, has_forms * 1.5)
    score += min(8, has_deadlines * 1.0)

    # Penalty if the category is large but few items are high priority.
    if total and high / total < 0.08:
        score -= 8

    return max(0, min(100, round(score)))

def build_context_for_category(category, rows):
    cfg = CATEGORY_CONFIG.get(category, {})
    rows = sorted(rows, key=lambda x: x.get("score", 0), reverse=True)

    buckets = Counter(priority_bucket(r.get("score", 0)) for r in rows)
    has_forms = len([r for r in rows if r.get("form_signal")])
    has_deadlines = len([r for r in rows if r.get("deadline_signal")])

    # Keep a cleaner top list by skipping obvious article/directory noise unless score is very high.
    clean_rows = []
    seen_urls = set()
    seen_titles = set()
    for r in rows:
        title = clean_title(r.get("title"))
        url = r.get("source_url", "")
        key = (title.lower(), url.lower())
        if key in seen_urls:
            continue
        seen_urls.add(key)
        if title.lower() in seen_titles:
            continue
        seen_titles.add(title.lower())

        if is_noise(title, url) and r.get("score", 0) < 76:
            continue
        clean_rows.append(r)

    best_moves = clean_rows[:10]
    best_first = best_moves[0] if best_moves else (rows[0] if rows else None)

    score = actionability_score(
        category,
        buckets.get("high", 0),
        buckets.get("medium", 0),
        len(rows),
        has_forms,
        has_deadlines,
    )

    return {
        "category_id": category,
        "title": CATEGORY_NAMES.get(category, category),
        "opportunities_found": len(rows),
        "high_priority": buckets.get("high", 0),
        "medium_priority": buckets.get("medium", 0),
        "low_priority": buckets.get("low", 0),
        "items_with_forms": has_forms,
        "items_with_deadlines": has_deadlines,
        "actionability_score": score,
        "estimated_cost": cfg.get("estimated_cost", "Check source"),
        "estimated_effort": cfg.get("estimated_effort", "Check source"),
        "timeline": cfg.get("timeline", "Check source"),
        "why_this_matters": cfg.get("why_this_matters", ""),
        "recommendation": cfg.get("recommendation", ""),
        "battle_plan": cfg.get("battle_plan", []),
        "best_first_move": {
            "title": best_first.get("title") if best_first else "",
            "score": best_first.get("score") if best_first else "",
            "url": best_first.get("source_url") if best_first else "",
            "quick_action": quick_action(category),
        },
        "best_moves": [
            {
                "title": r.get("title"),
                "score": r.get("score"),
                "url": r.get("source_url"),
                "deadline_signal": r.get("deadline_signal"),
                "fee_signal": r.get("fee_signal"),
                "form_signal": r.get("form_signal"),
                "candidate_id": r.get("candidate_id"),
            }
            for r in best_moves
        ],
    }

def quick_action(category):
    if category == "contests":
        return "Confirm deadline, fee, eligibility, and application requirements."
    if category == "zines":
        return "Check exhibitor/application requirements, booth fee, and next event date."
    if category == "residencies":
        return "Confirm eligibility, duration, cost, housing, and project proposal requirements."
    if category == "publishing":
        return "Decide whether this is a real publisher/platform or only a reference source."
    return "Open source and verify requirements."

def main():
    raw = load(RAW, {"candidates": []})
    candidates = raw.get("candidates", [])

    grouped = defaultdict(list)
    for c in candidates:
        grouped[c.get("career_category", "other")].append(c)

    contexts = []
    for category in ["zines", "contests", "residencies", "publishing"]:
        contexts.append(build_context_for_category(category, grouped.get(category, [])))

    contexts.sort(key=lambda x: x["actionability_score"], reverse=True)

    result = {
        "title": "Category Context",
        "source_candidate_count": len(candidates),
        "categories": contexts,
        "recommended_order": [c["category_id"] for c in contexts],
    }

    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_DEPLOY.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_DEPLOY.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Category Context",
        "",
        f"- Source candidates: {len(candidates)}",
        f"- Recommended order: {', '.join(result['recommended_order'])}",
        "",
        "| Category | Actionability | Found | High | Medium | Low | Forms | Deadlines |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for c in contexts:
        lines.append(
            f"| {c['title']} | {c['actionability_score']} | {c['opportunities_found']} | "
            f"{c['high_priority']} | {c['medium_priority']} | {c['low_priority']} | "
            f"{c['items_with_forms']} | {c['items_with_deadlines']} |"
        )

    for c in contexts:
        lines += [
            "",
            f"## {c['title']}",
            "",
            f"- Actionability score: {c['actionability_score']}",
            f"- Opportunities found: {c['opportunities_found']}",
            f"- High priority: {c['high_priority']}",
            f"- Medium priority: {c['medium_priority']}",
            f"- Low priority: {c['low_priority']}",
            f"- Estimated cost: {c['estimated_cost']}",
            f"- Estimated effort: {c['estimated_effort']}",
            f"- Timeline: {c['timeline']}",
            "",
            "### Why this matters",
            c["why_this_matters"],
            "",
            "### Recommendation",
            c["recommendation"],
            "",
            "### Best first move",
            f"{c['best_first_move']['title']} — score {c['best_first_move']['score']}",
            c['best_first_move']['url'],
            "",
            "### Battle plan",
        ]
        for step in c["battle_plan"]:
            lines.append(f"- {step}")

        lines += ["", "### Best moves"]
        for m in c["best_moves"][:10]:
            lines.append(f"- {m['title']} — score {m['score']} — {m['url']}")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_DEPLOY)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
