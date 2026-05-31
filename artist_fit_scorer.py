
import json
from pathlib import Path

SRC = "memory/contextualized_opportunities.json"
CONTEXT = "memory/personalized_artist_context.json"

OUT = "memory/personalized_fit_scores.json"
HIGH = "reports/high_priority_targets.md"
MED = "reports/medium_priority_targets.md"
LATER = "reports/later_targets.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def base_score(item):
    for k in ["verified_action_score", "painting_priority_score", "source_purity_score", "truth_aligned_score", "watercolor_adjusted_score", "overall_score", "score"]:
        try:
            if item.get(k) is not None:
                return float(item.get(k) or 0)
        except Exception:
            pass
    return 5.0

def score_item(item, context):
    typ = item.get("opportunity_type") or "unknown"
    ctx = item.get("context_summary", {})

    score = base_score(item)
    reasons = []

    boosts = context.get("priority_boosts", {})
    penalties = context.get("priority_penalties", {})

    if typ in boosts:
        score += boosts[typ]
        reasons.append(f"{typ} readiness adjustment: {boosts[typ]}")

    if ctx.get("actionability") == "actionable_research_target":
        score += 1.0
        reasons.append("application page or direct action path found")
    elif ctx.get("actionability") == "partial_action_target":
        score += 0.4
        reasons.append("partial contact/application path found")
    elif ctx.get("actionability") == "needs_manual_verification":
        score -= 0.6
        reasons.append("needs manual verification")
    elif ctx.get("actionability") == "reject_or_archive":
        score -= 4.0
        reasons.append("likely false positive or archive/catalog page")

    if ctx.get("deadline_status") == "deadline_unknown":
        score += penalties.get("deadline_unknown", -0.4)
        reasons.append("deadline unknown")

    if ctx.get("contact_status") == "contact_unknown" and ctx.get("application_status") == "no_application_link_found":
        score += penalties.get("no_contact_no_link", -1.0)
        reasons.append("no contact or application link found")

    title = str(item.get("title") or "").lower()
    if "printed matter editions" in title or "flashpoint" in title:
        score -= 3.0
        reasons.append("not a real target for this workflow")

    # Specific sensible boosts after personalization.
    title_upper = str(item.get("title") or "")
    if title_upper in {"UTRECHT", "Book and Sons", "MOUNT ZINE", "TOKYO ART BOOK FAIR"}:
        score += 0.8
        reasons.append("existing zines make this more plausible")
    if title_upper in {"HB Gallery", "OPA Gallery", "Pinpoint Gallery"}:
        score += 0.8
        reasons.append("gallery/bookstore crossover target")

    score = max(0, min(10, round(score, 2)))

    if score >= 8:
        priority = "high"
    elif score >= 6:
        priority = "medium"
    else:
        priority = "later"

    item["personalized_fit_score"] = score
    item["personalized_priority"] = priority
    item["personalized_fit_reasons"] = reasons
    return item

def write_report(path, title, items):
    lines = [f"# {title}", ""]
    if not items:
        lines.append("_No items._")
    for item in items:
        ctx = item.get("context_summary", {})
        lines.append(f"## {item.get('title')}")
        lines.append(f"- Score: {item.get('personalized_fit_score')}/10")
        lines.append(f"- Type: {item.get('opportunity_type', 'unknown')}")
        lines.append(f"- Actionability: {ctx.get('actionability', 'unknown')}")
        lines.append(f"- Best link: {ctx.get('best_link', item.get('url', ''))}")
        lines.append(f"- Missing: {', '.join(ctx.get('missing', [])) or 'none listed'}")
        lines.append("")
        lines.append("### Reasons")
        for r in item.get("personalized_fit_reasons", []):
            lines.append(f"- {r}")
        lines.append("")
        lines.append(f"### Next")
        lines.append(item.get("next_action_hint") or "Manual review.")
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")

def main():
    data = load(SRC, [])
    context = load(CONTEXT, {})
    scored = [score_item(dict(item), context) for item in data]

    scored.sort(key=lambda x: x.get("personalized_fit_score", 0), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(scored, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    high = [x for x in scored if x["personalized_priority"] == "high"]
    med = [x for x in scored if x["personalized_priority"] == "medium"]
    later = [x for x in scored if x["personalized_priority"] == "later"]

    Path("reports").mkdir(exist_ok=True)
    write_report(HIGH, "High Priority Targets", high)
    write_report(MED, "Medium Priority Targets", med)
    write_report(LATER, "Later / Skip For Now Targets", later)

    print("Wrote", OUT)
    print("High:", len(high), "Medium:", len(med), "Later:", len(later))

if __name__ == "__main__":
    main()
