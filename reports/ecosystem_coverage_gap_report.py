
import json
from pathlib import Path

ECOSYSTEMS = "memory/opportunity_ecosystems.json"
DENSITY = "memory/ecosystem_density_scores.json"
TABF = "memory/tabf_exhibitor_data.json"

OUT_JSON = "memory/ecosystem_coverage_gaps.json"
OUT_REPORT = "reports/ecosystem_coverage_gaps.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def by_title(rows):
    return {r.get("title"): r for r in rows if r.get("title")}

def coverage_score(row, tabf=None):
    if row.get("title") == "TOKYO ART BOOK FAIR" and tabf:
        entity_count = tabf.get("entity_count", 0)
        pubs = len(tabf.get("publishers_or_presses", []))
        artists = len(tabf.get("artists_or_collectives", []))
        books = len(tabf.get("zines_or_books", []))
        return min(100, entity_count + pubs * 3 + artists * 2 + books * 2)

    return min(100,
        row.get("artist_count", 0) * 12
        + row.get("similar_artist_count", 0) * 20
        + row.get("publisher_count", 0) * 4
        + row.get("book_count", 0) * 3
        + row.get("award_count", 0) * 2
    )

def gaps_for(title, row, tabf=None):
    gaps = []

    if title == "TOKYO ART BOOK FAIR" and tabf:
        if len(tabf.get("publishers_or_presses", [])) < 5:
            gaps.append("Find more past publishers / presses.")
        if len(tabf.get("artists_or_collectives", [])) < 5:
            gaps.append("Find past artists / collectives.")
        if len(tabf.get("zines_or_books", [])) < 5:
            gaps.append("Find specific zines, books, or publication examples.")
        if tabf.get("entity_count", 0) < 20:
            gaps.append("Find better archive/exhibitor pages.")
        return gaps or ["TABF has usable initial ecosystem coverage; next step is cleanup and relevance scoring."]

    if row.get("similar_artist_count", 0) == 0:
        gaps.append("Find artists similar to Nin.")
    if row.get("publisher_count", 0) == 0:
        gaps.append("Find publishers / presses / clients.")
    if row.get("book_count", 0) == 0:
        gaps.append("Find books, zines, or works.")
    if row.get("artist_count", 0) == 0:
        gaps.append("Find past artists / exhibitors / winners.")
    return gaps or ["Coverage is usable; next step is quality cleanup."]

def main():
    density = load(DENSITY, [])
    tabf = load(TABF, None)

    rows = []
    for d in density:
        title = d.get("title")
        score = coverage_score(d, tabf)
        rows.append({
            "title": title,
            "coverage_score": score,
            "ecosystem_density": d.get("ecosystem_density"),
            "density_label": d.get("density_label"),
            "gaps": gaps_for(title, d, tabf),
        })

    # Add TABF if density file did not include it.
    if tabf and "TOKYO ART BOOK FAIR" not in {r["title"] for r in rows}:
        rows.append({
            "title": "TOKYO ART BOOK FAIR",
            "coverage_score": coverage_score({"title": "TOKYO ART BOOK FAIR"}, tabf),
            "ecosystem_density": 0,
            "density_label": "unknown",
            "gaps": gaps_for("TOKYO ART BOOK FAIR", {"title": "TOKYO ART BOOK FAIR"}, tabf),
        })

    rows.sort(key=lambda x: x["coverage_score"], reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(rows, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Ecosystem Coverage Gaps",
        "",
        "Coverage is not quality. Coverage means: how much useful ecosystem evidence have we found so far?",
        "",
    ]

    for r in rows:
        lines.append(f"## {r['title']}")
        lines.append(f"- Coverage: {r['coverage_score']}/100")
        lines.append(f"- Existing density: {r['ecosystem_density']}/100 ({r['density_label']})")
        lines.append("")
        lines.append("### Gaps / next research")
        for g in r["gaps"]:
            lines.append(f"- {g}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
