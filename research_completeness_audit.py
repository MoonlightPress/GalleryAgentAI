
import json
from pathlib import Path

SRC = "memory/contextualized_opportunities.json"
DNA = "memory/dna_matches.json"
OUT_JSON = "memory/research_completeness.json"
OUT_REPORT = "reports/research_completeness.md"

FIELDS = {
    "website": 10,
    "application_link": 20,
    "application_page_crawled": 20,
    "contact": 15,
    "deadline": 15,
    "opportunity_type": 10,
    "fit_reasoning": 10,
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def has_value(v):
    if v is None:
        return False
    s = str(v).strip().lower()
    return bool(s and s not in {"unknown", "none", "null", "n/a", "not publicly listed"})

def best_link(item):
    ctx = item.get("context_summary", {})
    return ctx.get("best_link") or item.get("url") or item.get("source_url") or ""

def contact_present(item):
    if has_value(item.get("contact")):
        return True
    for page in item.get("application_page_results", []):
        if page.get("emails"):
            return True
    return False

def deadline_present(item):
    if has_value(item.get("deadline")):
        return True
    for page in item.get("application_page_results", []):
        if page.get("date_candidates"):
            return True
    return False

def application_link_present(item):
    return bool(item.get("ranked_submission_links") or item.get("submission_links"))

def application_page_crawled(item):
    return bool(item.get("application_page_results"))

def score_item(item, dna_lookup):
    title = item.get("title")
    score = 0
    missing = []

    checks = {
        "website": has_value(best_link(item)),
        "application_link": application_link_present(item),
        "application_page_crawled": application_page_crawled(item),
        "contact": contact_present(item),
        "deadline": deadline_present(item),
        "opportunity_type": has_value(item.get("opportunity_type")),
        "fit_reasoning": title in dna_lookup,
    }

    for field, ok in checks.items():
        if ok:
            score += FIELDS[field]
        else:
            missing.append(field)

    score = min(100, score)

    if score >= 80:
        status = "ready_for_review"
    elif score >= 55:
        status = "research_needed"
    else:
        status = "not_actionable_yet"

    return {
        "title": title,
        "score": score,
        "status": status,
        "opportunity_type": item.get("opportunity_type", "unknown"),
        "best_link": best_link(item),
        "missing": missing,
        "present": checks,
        "actionability": item.get("context_summary", {}).get("actionability", "unknown"),
    }

def main():
    items = load(SRC, [])
    dna = load(DNA, [])
    dna_lookup = {x.get("title"): x for x in dna}

    rows = [score_item(item, dna_lookup) for item in items]
    rows.sort(key=lambda x: x["score"], reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(rows, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    ready = [x for x in rows if x["status"] == "ready_for_review"]
    needs = [x for x in rows if x["status"] == "research_needed"]
    weak = [x for x in rows if x["status"] == "not_actionable_yet"]

    lines = [
        "# Research Completeness Audit",
        "",
        "This report measures whether an opportunity has enough information to act on.",
        "",
        f"- Ready for review: {len(ready)}",
        f"- Research needed: {len(needs)}",
        f"- Not actionable yet: {len(weak)}",
        "",
    ]

    def section(title, data):
        lines.append(f"## {title}")
        lines.append("")
        if not data:
            lines.append("_No items._")
            lines.append("")
            return
        for r in data:
            lines.append(f"### {r['title']}")
            lines.append(f"- Completeness: {r['score']}%")
            lines.append(f"- Status: {r['status']}")
            lines.append(f"- Type: {r['opportunity_type']}")
            lines.append(f"- Link: {r['best_link']}")
            lines.append(f"- Missing: {', '.join(r['missing']) or 'nothing obvious'}")
            lines.append("")

    section("Ready For Review", ready)
    section("Research Needed", needs)
    section("Not Actionable Yet", weak)

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
