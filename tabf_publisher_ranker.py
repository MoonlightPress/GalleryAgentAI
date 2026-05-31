
import json
from pathlib import Path

SRC = "memory/tabf_clean_entities.json"
OUT_JSON = "memory/tabf_ranked_publishers.json"
OUT_REPORT = "reports/tabf_ranked_publishers.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def score_entity(e):
    score = 0
    score += e.get("mentions", 0) * 8
    if e.get("contexts"):
        score += min(30, len(e["contexts"]) * 6)
    if e.get("source_urls"):
        score += min(20, len(e["source_urls"]) * 5)
    name = e.get("name", "")
    if any(x in name.lower() for x in ["press", "verlag", "book", "books", "steidl", "corraini", "mack"]):
        score += 15
    if len(name.split()) >= 2:
        score += 5
    return min(100, score)

def main():
    data = load(SRC, {})
    pubs = data.get("publishers_or_presses", [])
    galleries = data.get("bookstores_or_galleries", [])
    books = data.get("zines_or_books", [])

    ranked = []
    for e in pubs + galleries + books:
        row = dict(e)
        row["rank_score"] = score_entity(e)
        ranked.append(row)

    ranked.sort(key=lambda x: x["rank_score"], reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(ranked, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# TABF Ranked Publishers / Book Ecosystem",
        "",
        "Ranks cleaned TABF entities by strength of evidence and relevance to publishing / art-book ecosystem.",
        "",
    ]

    for e in ranked[:60]:
        lines.append(f"## {e['name']}")
        lines.append(f"- Score: {e['rank_score']}/100")
        lines.append(f"- Type: {e.get('entity_type')}")
        lines.append(f"- Mentions: {e.get('mentions')}")
        if e.get("source_urls"):
            lines.append(f"- Source: {e['source_urls'][0]}")
        if e.get("contexts"):
            lines.append("")
            lines.append("### Evidence")
            for c in e["contexts"][:3]:
                lines.append(f"- {c}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
