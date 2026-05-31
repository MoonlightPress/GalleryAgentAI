
import json
from pathlib import Path

ECOSYSTEMS = "memory/opportunity_ecosystems.json"
DENSITY = "memory/ecosystem_density_scores.json"
OUT = "reports/opportunity_career_path_report.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def by_title(rows):
    return {r.get("title"): r for r in rows if r.get("title")}

def conclusion(eco, density):
    if density.get("ecosystem_density", 0) >= 80:
        return "This opportunity has a visible career ecosystem, not just an application form."
    if len(eco.get("similar_artists", [])) > 0:
        return "This opportunity has at least some evidence of artists similar to Nin succeeding or participating."
    if len(eco.get("artists", [])) > 0:
        return "This opportunity has artist evidence, but similarity to Nin is not yet strong."
    return "This opportunity needs more ecosystem evidence before it should be treated as a priority."

def main():
    ecosystems = load(ECOSYSTEMS, [])
    density_by = by_title(load(DENSITY, []))

    ecosystems.sort(key=lambda e: density_by.get(e.get("title"), {}).get("ecosystem_density", 0), reverse=True)

    lines = [
        "# Opportunity Career Path Report",
        "",
        "Explains the actual evidence chain behind each opportunity.",
        "",
    ]

    for eco in ecosystems:
        d = density_by.get(eco.get("title"), {})
        lines.append(f"## {eco.get('title')}")
        lines.append(f"- Ecosystem density: {d.get('ecosystem_density', 0)}/100 ({d.get('density_label', 'unknown')})")
        lines.append(f"- Conclusion: {conclusion(eco, d)}")
        lines.append("")

        if eco.get("similar_artists"):
            lines.append("### Artists similar to Nin")
            for a in sorted(eco["similar_artists"], key=lambda x: x.get("similarity_score", 0), reverse=True)[:5]:
                lines.append(f"- {a['name']} — {a.get('similarity_score')}/100")
            lines.append("")

        if eco.get("publishers"):
            lines.append("### Career ecosystem evidence: publishers / clients")
            for p in eco["publishers"][:8]:
                lines.append(f"- {p['name']} — connected to {p.get('artist', 'unknown')}")
            lines.append("")

        if eco.get("books_or_works"):
            lines.append("### Career ecosystem evidence: books / works")
            for b in eco["books_or_works"][:8]:
                lines.append(f"- {b['name']} — {b.get('artist', 'unknown')}")
            lines.append("")

        if eco.get("awards_or_selections"):
            lines.append("### Career ecosystem evidence: awards / selections")
            for a in eco["awards_or_selections"][:6]:
                lines.append(f"- {a['name']} — {a.get('artist', 'unknown')}")
            lines.append("")

        if not eco.get("similar_artists") and not eco.get("publishers") and not eco.get("books_or_works"):
            lines.append("_No strong career-path evidence yet._")
            lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT)

if __name__ == "__main__":
    main()
