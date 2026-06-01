
import json
from pathlib import Path
from datetime import date

RAW = Path("memory/multi_ingress_raw_candidates.json")
COMPACT_PATHS = [
    Path("memory/compact_opportunities.json"),
    Path("Memory/compact_opportunities.json"),
    Path("deploy_data/compact_opportunities.json"),
]

OUT_MEMORY = Path("memory/compact_opportunities.json")
OUT_DEPLOY = Path("deploy_data/compact_opportunities.json")
OUT_REPORT = Path("reports/multi_ingress_opportunities_added.md")

SOURCE_TAG = "multi_ingress_sprint_v1"

CATEGORY_LABELS = {
    "contests": "Open Calls / Contests",
    "zines": "Art Book & Zine Fairs",
    "residencies": "Residencies",
    "publishing": "Publishing / Small Press",
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

def title_key(opp):
    return (opp.get("title") or opp.get("name") or opp.get("organization") or "").strip().lower()

def quick_action(c):
    cat = c["career_category"]
    if cat == "contests":
        return "Open the source and confirm deadline, fee, eligibility, and required image files."
    if cat == "zines":
        return "Check exhibitor/application requirements, booth fee, and next event date."
    if cat == "residencies":
        return "Confirm deadline, duration, cost, location, and whether visual artists are eligible."
    if cat == "publishing":
        return "Review recent titles and decide whether this is a publisher, distributor, bookstore, or article reference."
    return "Open the source and verify current requirements."

def bullets(c):
    out = [
        f"Source category: {CATEGORY_LABELS.get(c['career_category'], c['career_category'])}.",
        f"Search group: {c.get('source_query', '')}.",
        f"First action: {quick_action(c)}",
    ]
    signals = []
    if c.get("deadline_signal"):
        signals.append("deadline signal")
    if c.get("fee_signal"):
        signals.append("fee signal")
    if c.get("form_signal"):
        signals.append("application/form signal")
    if signals:
        out.append("Detected signals: " + ", ".join(signals) + ".")
    return out

def to_opp(c):
    title = c["title"]
    score = round(max(4.5, min(9.2, c.get("score", 50) / 10)), 1)
    cat_label = CATEGORY_LABELS.get(c["career_category"], c["career_category"])

    return {
        "title": title,
        "name": title,
        "organization": title,
        "category": c["category"],
        "city": "Japan / Tokyo / Online",
        "overall_score": score,
        "one_sentence": f"{cat_label} lead found through targeted research; useful if requirements and fit check out.",
        "suggested_display_summary": f"{cat_label} lead. Needs source review for details.",
        "why_this_fits_short": (
            "Potential fit because it belongs to a structured opportunity category where requirements, dates, fees, or submission routes can usually be verified."
        ),
        "quick_action": quick_action(c),
        "source_url": c.get("source_url", ""),
        "source_link": c.get("source_url", ""),
        "official_website": c.get("source_url", ""),
        "submission_page": c.get("source_url", "") if c.get("form_signal") else "",
        "deadline": "Check source" if c.get("deadline_signal") else "",
        "fees": "Check source" if c.get("fee_signal") else "",
        "difficulty": "medium",
        "three_bullets": bullets(c),
        "career_category": c["career_category"],
        "opportunity_type": c.get("source_query", ""),
        "status": "research_next",
        "confidence": c.get("score", 50),
        "import_source": SOURCE_TAG,
        "source_candidate_id": c.get("candidate_id"),
        "imported_at": str(date.today()),
    }

def main():
    raw = load(RAW, {"candidates": []})
    compact_path, existing = find_existing(COMPACT_PATHS, [])

    if not isinstance(existing, list):
        raise SystemExit("compact_opportunities.json is not a list. Aborting.")

    candidates = raw.get("candidates", [])
    # Keep the top 12 per category for now to avoid flooding the page.
    selected = []
    for cat in ["contests", "zines", "residencies", "publishing"]:
        rows = [c for c in candidates if c["career_category"] == cat and c.get("score", 0) >= 50]
        selected.extend(rows[:12])

    new_opps = [to_opp(c) for c in selected]

    # Repeatable run: remove prior import batch first.
    preserved = [o for o in existing if o.get("import_source") != SOURCE_TAG]
    keys = {title_key(o) for o in preserved}

    added, skipped = [], []
    for opp in new_opps:
        key = title_key(opp)
        if key in keys:
            skipped.append(opp["title"])
            continue
        preserved.append(opp)
        keys.add(key)
        added.append(opp["title"])

    OUT_MEMORY.parent.mkdir(exist_ok=True)
    OUT_DEPLOY.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    OUT_MEMORY.write_text(json.dumps(preserved, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_DEPLOY.write_text(json.dumps(preserved, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Multi-Ingress Opportunities Added",
        "",
        f"- Compact source: {compact_path}",
        f"- Raw candidates: {len(candidates)}",
        f"- Selected candidates: {len(selected)}",
        f"- Added opportunities: {len(added)}",
        f"- Skipped duplicates: {len(skipped)}",
        "",
        "## Added",
    ]
    for title in added:
        lines.append(f"- {title}")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_MEMORY)
    print("Wrote", OUT_DEPLOY)
    print("Wrote", OUT_REPORT)
    print("Added:", len(added))

if __name__ == "__main__":
    main()
