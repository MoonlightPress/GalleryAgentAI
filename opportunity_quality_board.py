
import json
from pathlib import Path

PITCHES = "memory/opportunity_pitches.json"
EVIDENCE = "memory/opportunity_evidence.json"

OUT_JSON = "memory/opportunity_quality_board.json"
OUT_REPORT = "reports/opportunity_quality_board.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def by_title(rows):
    return {r.get("title"): r for r in rows if r.get("title")}

def quality_label(score):
    if score >= 80:
        return "strong"
    if score >= 60:
        return "promising"
    if score >= 40:
        return "needs evidence"
    return "weak"

def main():
    pitches = load(PITCHES, [])
    evidence_by = by_title(load(EVIDENCE, []))

    rows = []
    for p in pitches:
        e = evidence_by.get(p.get("title"), {})
        match = p.get("pitch_score") or 0
        evidence_strength = e.get("evidence_strength", 0)

        # The score rewards both fit and concrete evidence.
        quality = round((float(match) * 7) + (float(evidence_strength) * 0.3), 1)

        rows.append({
            "title": p.get("title"),
            "quality_score": min(100, quality),
            "quality_label": quality_label(quality),
            "match_score": match,
            "evidence_strength": evidence_strength,
            "evidence_status": e.get("evidence_status", "missing"),
            "recommended_url": p.get("recommended_url"),
            "why_it_fits": p.get("fit_paragraph"),
            "top_evidence": (e.get("evidence_sentences") or [{}])[0].get("text", ""),
            "evidence_links": e.get("evidence_links", [])[:5],
        })

    rows.sort(key=lambda x: x["quality_score"], reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(rows, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Opportunity Quality Board",
        "",
        "Combines fit score with evidence strength. This helps distinguish exciting targets from under-researched targets.",
        "",
    ]

    for r in rows:
        lines.append(f"## {r['title']}")
        lines.append(f"- Quality: {r['quality_score']}/100 ({r['quality_label']})")
        lines.append(f"- Match: {r['match_score']}/10")
        lines.append(f"- Evidence: {r['evidence_strength']}% ({r['evidence_status']})")
        lines.append(f"- Link: {r['recommended_url']}")
        lines.append("")
        lines.append("### Why it fits")
        lines.append(r["why_it_fits"] or "No fit paragraph available.")
        if r["top_evidence"]:
            lines.append("")
            lines.append("### Best extracted evidence")
            lines.append(r["top_evidence"])
        if r["evidence_links"]:
            lines.append("")
            lines.append("### Evidence links")
            for l in r["evidence_links"]:
                lines.append(f"- {l.get('label')} — {l.get('url')}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
