
import json
from pathlib import Path

SRC = "memory/opportunity_ecosystems.json"
OUT_JSON = "memory/ecosystem_density_scores.json"
OUT_REPORT = "reports/ecosystem_density_scores.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def score(eco):
    artist_count = len(eco.get("artists", []))
    similar_count = len(eco.get("similar_artists", []))
    publisher_count = len(eco.get("publishers", []))
    book_count = len(eco.get("books_or_works", []))
    award_count = len(eco.get("awards_or_selections", []))
    judge_count = len(eco.get("judges_or_gatekeepers", []))
    org_count = len(eco.get("organizations", [])) + len(eco.get("evidence_clues", []))

    value = (
        min(30, similar_count * 10)
        + min(20, artist_count * 4)
        + min(20, publisher_count * 3)
        + min(15, book_count * 2)
        + min(10, award_count * 2)
        + min(5, judge_count + org_count)
    )

    return min(100, value)

def label(value):
    if value >= 80:
        return "dense ecosystem"
    if value >= 55:
        return "promising ecosystem"
    if value >= 30:
        return "thin ecosystem"
    return "weak ecosystem"

def main():
    ecosystems = load(SRC, [])
    rows = []

    for eco in ecosystems:
        value = score(eco)
        rows.append({
            "title": eco.get("title"),
            "ecosystem_density": value,
            "density_label": label(value),
            "artist_count": len(eco.get("artists", [])),
            "similar_artist_count": len(eco.get("similar_artists", [])),
            "publisher_count": len(eco.get("publishers", [])),
            "book_count": len(eco.get("books_or_works", [])),
            "award_count": len(eco.get("awards_or_selections", [])),
            "judge_count": len(eco.get("judges_or_gatekeepers", [])),
            "organization_count": len(eco.get("organizations", [])) + len(eco.get("evidence_clues", [])),
        })

    rows.sort(key=lambda x: x["ecosystem_density"], reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(rows, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Ecosystem Density Scores",
        "",
        "Scores whether an opportunity has a visible career ecosystem around it.",
        "",
    ]

    for r in rows:
        lines.append(f"## {r['title']}")
        lines.append(f"- Ecosystem density: {r['ecosystem_density']}/100 ({r['density_label']})")
        lines.append(f"- Similar artists: {r['similar_artist_count']}")
        lines.append(f"- Artists: {r['artist_count']}")
        lines.append(f"- Publishers/clients: {r['publisher_count']}")
        lines.append(f"- Books/works: {r['book_count']}")
        lines.append(f"- Awards/selections: {r['award_count']}")
        lines.append(f"- Judges/gatekeepers: {r['judge_count']}")
        lines.append(f"- Organizations/clues: {r['organization_count']}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
