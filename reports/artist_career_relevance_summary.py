
import json
from pathlib import Path

GRAPH = "memory/artist_career_graph.json"
OUT = "reports/artist_career_relevance_summary.md"

def main():
    graph = json.load(open(GRAPH, encoding="utf-8"))

    lines = [
        "# Artist Career Relevance Summary",
        "",
        "Highlights why the extracted artists matter for opportunity evaluation.",
        "",
    ]

    for a in graph.get("artists", []):
        score = 0
        reasons = []

        if a.get("books_or_works"):
            score += 25
            reasons.append("has books/works listed")
        if a.get("publishers_or_clients"):
            score += 25
            reasons.append("has publishers/clients listed")
        if a.get("awards_or_selections"):
            score += 25
            reasons.append("has awards/selections listed")
        if any("絵本" in r or "picture" in r.lower() for r in a.get("roles", [])):
            score += 15
            reasons.append("picture-book / publishing ecosystem")
        if any("illustr" in r.lower() or "イラスト" in r for r in a.get("roles", [])):
            score += 10
            reasons.append("illustration-adjacent")

        label = "high relevance" if score >= 60 else "medium relevance" if score >= 30 else "low relevance"

        lines.append(f"## {a['artist_name']}")
        lines.append(f"- Relevance: {score}/100 ({label})")
        lines.append(f"- Why: {', '.join(reasons) or 'limited structured career data'}")
        lines.append(f"- Opportunity: {', '.join(a.get('source_opportunities', []))}")
        if a.get("books_or_works"):
            lines.append(f"- Books/works: {', '.join(a['books_or_works'][:5])}")
        if a.get("publishers_or_clients"):
            lines.append(f"- Publishers/clients: {', '.join(a['publishers_or_clients'][:5])}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
