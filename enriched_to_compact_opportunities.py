
import json
from pathlib import Path
from datetime import date

ENRICHED = Path("memory/enriched_opportunities.json")
COMPACT_PATHS = [
    Path("memory/compact_opportunities.json"),
    Path("Memory/compact_opportunities.json"),
    Path("deploy_data/compact_opportunities.json"),
]

OUT_MEMORY = Path("memory/compact_opportunities.json")
OUT_DEPLOY = Path("deploy_data/compact_opportunities.json")
OUT_REPORT = Path("reports/enriched_opportunities_added.md")

SOURCE_TAG = "opportunity_intelligence_sprint_v1"

CATEGORY_MAP = {
    "zines": "fair_popup",
    "contests": "gallery_event",
    "residencies": "residency",
    "galleries": "gallery",
    "publishing": "book_publishing",
}

def load(path, fallback):
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback

def find_existing(paths, fallback):
    for p in paths:
        if p.exists():
            return p, load(p, fallback)
    return None, fallback

def key(o):
    return (o.get("title") or o.get("name") or o.get("organization") or "").strip().lower()

def to_compact(o):
    title = o.get("canonical_name", "Untitled Opportunity")
    cat = o.get("career_category", "other")
    url = o.get("best_url", "")
    score = round(max(4.0, min(9.8, ((o.get("fit_score", 50) + o.get("actionability_score", 50)) / 20))), 1)

    return {
        "title": title,
        "name": title,
        "organization": title,
        "category": CATEGORY_MAP.get(cat, cat),
        "city": o.get("neighborhood") or "Japan / Tokyo / Online",
        "overall_score": score,
        "one_sentence": o.get("why_for_nin", ""),
        "suggested_display_summary": o.get("why_for_nin", ""),
        "why_this_fits_short": o.get("why_for_nin", ""),
        "quick_action": o.get("recommended_next_action", ""),
        "source_url": url,
        "source_link": url,
        "official_website": url,
        "submission_page": url if o.get("has_application") else "",
        "deadline": "Check source" if o.get("has_deadline_signal") else "",
        "fees": "Check source" if o.get("has_fee_signal") else "",
        "difficulty": "medium",
        "three_bullets": [
            f"Fit score: {o.get('fit_score')}.",
            f"Actionability score: {o.get('actionability_score')}.",
            f"Risk score: {o.get('risk_score')}.",
            "Risk: " + "; ".join(o.get("risks", [])[:2]),
        ],
        "career_category": cat,
        "opportunity_type": "enriched_opportunity",
        "status": "research_next",
        "fit_score": o.get("fit_score"),
        "actionability_score": o.get("actionability_score"),
        "risk_score": o.get("risk_score"),
        "import_source": SOURCE_TAG,
        "imported_at": str(date.today()),
    }

def main():
    enriched = load(ENRICHED, {"opportunities": []}).get("opportunities", [])
    compact_path, existing = find_existing(COMPACT_PATHS, [])
    if not isinstance(existing, list):
        raise SystemExit("compact_opportunities.json is not a list.")

    # replace prior sprint imports
    preserved = [o for o in existing if o.get("import_source") != SOURCE_TAG]
    keys = {key(o) for o in preserved}
    added = []

    for o in enriched:
        c = to_compact(o)
        if key(c) in keys:
            continue
        preserved.append(c)
        keys.add(key(c))
        added.append(c["title"])

    OUT_MEMORY.parent.mkdir(exist_ok=True)
    OUT_DEPLOY.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    OUT_MEMORY.write_text(json.dumps(preserved, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_DEPLOY.write_text(json.dumps(preserved, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Enriched Opportunities Added", "", f"- Added: {len(added)}", ""]
    for a in added:
        lines.append(f"- {a}")
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_MEMORY)
    print("Wrote", OUT_DEPLOY)
    print("Wrote", OUT_REPORT)
    print("Added:", len(added))

if __name__ == "__main__":
    main()
