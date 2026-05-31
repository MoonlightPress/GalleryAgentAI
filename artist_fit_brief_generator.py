
import json
from pathlib import Path

DNA = "memory/artist_dna.json"
FIT = "memory/artist_fit_scores.json"
OUT_JSON = "memory/artist_fit_briefs.json"
OUT_REPORT = "reports/artist_fit_briefs.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def make_brief(row, dna):
    title = row["title"]
    types = row.get("opportunity_types", [])
    label = row.get("fit_label")

    if row["combined_personal_score"] >= 75:
        verdict = "This is a strong personal fit."
    elif row["combined_personal_score"] >= 55:
        verdict = "This is worth researching further."
    elif row["combined_personal_score"] >= 35:
        verdict = "This may be useful, but it is not a primary fit."
    else:
        verdict = "This should be low priority for now."

    reasons = row.get("fit_reasons", [])
    return {
        "title": title,
        "verdict": verdict,
        "score": row["combined_personal_score"],
        "fit_label": label,
        "types": types,
        "brief": f"{verdict} It matches the artist profile through: {', '.join(reasons) if reasons else 'unclear or limited evidence'}.",
        "next_question": "What evidence would make this feel personally relevant rather than merely available?",
    }

def main():
    dna = load(DNA, {})
    rows = load(FIT, [])

    briefs = [make_brief(r, dna) for r in rows]

    Path("memory").mkdir(exist_ok=True)
    json.dump(briefs, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = ["# Artist Fit Briefs", ""]
    for b in briefs:
        lines.append(f"## {b['title']}")
        lines.append(f"- Score: {b['score']}/100 ({b['fit_label']})")
        lines.append(f"- Verdict: {b['verdict']}")
        lines.append(f"- Types: {', '.join(b['types'])}")
        lines.append("")
        lines.append(b["brief"])
        lines.append("")
        lines.append(f"Next question: {b['next_question']}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
