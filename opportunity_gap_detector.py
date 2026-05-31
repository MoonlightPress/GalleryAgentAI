
import json
from pathlib import Path

QUALITY = "memory/opportunity_quality_board.json"
EVIDENCE = "memory/opportunity_evidence.json"
PACKETS = "memory/application_packets.json"
CHECKLISTS = "memory/submission_checklists.json"

OUT_JSON = "memory/opportunity_gaps.json"
OUT_REPORT = "reports/opportunity_gaps.md"

GAP_WEIGHTS = {
    "application_fee": 12,
    "current_deadline": 15,
    "contact_route": 8,
    "past_winners_or_exhibitors": 16,
    "specific_requirements": 12,
    "eligibility": 10,
    "evidence_quality": 14,
    "submission_method": 10,
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def by_title(rows):
    return {r.get("title"): r for r in rows if r.get("title")}

def unknown(v):
    if v is None:
        return True
    return str(v).strip().lower() in {"", "unknown", "none", "null", "n/a"}

def detect_gaps(q, e, p, c):
    gaps = []

    title = q.get("title")
    evidence_strength = float(q.get("evidence_strength", 0) or 0)

    if not p or unknown(p.get("fee")):
        gaps.append(("application_fee", "Find application/booth/entry fee or confirm there is no fee."))

    if not p or unknown(p.get("deadline")):
        gaps.append(("current_deadline", "Find current application deadline."))

    if not p or (unknown(p.get("contact_email")) and unknown(p.get("contact_page"))):
        gaps.append(("contact_route", "Find official contact email, contact page, or inquiry form."))

    if evidence_strength < 70:
        gaps.append(("evidence_quality", "Find stronger evidence: past winners, past exhibitors, accepted artists, or partner organizations."))

    if e:
        names = e.get("possible_names", []) or []
        links = e.get("evidence_links", []) or []
        text = " ".join([str(x) for x in names] + [str(l.get("label", "")) for l in links]).lower()
        if not any(k in text for k in ["winner", "winners", "exhibitor", "exhibitors", "selected", "award", "受賞", "入賞", "出展者"]):
            gaps.append(("past_winners_or_exhibitors", "Find past winners, past exhibitors, selected artists, or example accepted works."))
    else:
        gaps.append(("past_winners_or_exhibitors", "Find past winners, past exhibitors, selected artists, or example accepted works."))

    if not c or not c.get("required_materials"):
        gaps.append(("specific_requirements", "Extract exact required materials from official guidelines or form."))
    else:
        mats = c.get("required_materials", [])
        confirmed = [m for m in mats if isinstance(m, dict) and m.get("confirmed")]
        if len(confirmed) < 2:
            gaps.append(("specific_requirements", "Confirm exact required materials; current checklist is mostly inferred."))

    if not c or not c.get("eligibility_clues"):
        gaps.append(("eligibility", "Find eligibility rules or confirm none are listed."))

    if not p or unknown(p.get("submission_method")):
        gaps.append(("submission_method", "Confirm whether submission happens by form, email, open call portal, or inquiry."))

    # de-dupe while preserving highest weighted priority
    seen = set()
    out = []
    for key, desc in gaps:
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "gap": key,
            "description": desc,
            "value": GAP_WEIGHTS.get(key, 5),
        })

    out.sort(key=lambda x: x["value"], reverse=True)
    return out

def main():
    quality = load(QUALITY, [])
    evidence = by_title(load(EVIDENCE, []))
    packets = by_title(load(PACKETS, []))
    checklists = by_title(load(CHECKLISTS, []))

    rows = []

    for q in quality:
        title = q.get("title")
        qscore = float(q.get("quality_score", 0) or 0)
        gaps = detect_gaps(
            q,
            evidence.get(title),
            packets.get(title),
            checklists.get(title),
        )

        potential_gain = sum(g["value"] for g in gaps[:3])
        projected_score = min(100, round(qscore + potential_gain, 1))
        best_gap = gaps[0] if gaps else None

        rows.append({
            "title": title,
            "current_quality": qscore,
            "quality_label": q.get("quality_label"),
            "evidence_strength": q.get("evidence_strength"),
            "best_next_gap": best_gap,
            "gaps": gaps,
            "estimated_gain_top_3": potential_gain,
            "projected_score_if_fixed": projected_score,
            "recommended_search": best_gap["description"] if best_gap else "No obvious gap detected.",
        })

    rows.sort(key=lambda x: (x["estimated_gain_top_3"], -x["current_quality"]), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(rows, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Opportunity Gap Detector",
        "",
        "This report identifies which missing facts would most improve each opportunity.",
        "",
    ]

    for r in rows:
        lines.append(f"## {r['title']}")
        lines.append(f"- Current quality: {r['current_quality']}/100 ({r['quality_label']})")
        lines.append(f"- Evidence strength: {r['evidence_strength']}%")
        lines.append(f"- Estimated gain if top 3 gaps are fixed: +{r['estimated_gain_top_3']}")
        lines.append(f"- Projected score: {r['projected_score_if_fixed']}/100")
        lines.append(f"- Best next research task: {r['recommended_search']}")
        lines.append("")
        lines.append("### Gaps")
        for g in r["gaps"][:6]:
            lines.append(f"- +{g['value']} — {g['description']}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
