
import json
from pathlib import Path

CLEAN = "memory/tabf_clean_entities.json"
RANKED = "memory/tabf_ranked_publishers.json"
OUT_JSON = "memory/tabf_nin_overlap.json"
OUT_REPORT = "reports/tabf_nin_overlap.md"

NIN_RELEVANCE_TERMS = [
    "zine", "ZINE", "artist book", "art book", "book", "books", "press", "publisher",
    "gallery", "independent", "publication", "illustration", "print", "prints",
    "アートブック", "アーティストブック", "出版", "出版社", "ギャラリー", "書店", "作家"
]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def overlap_score(e):
    blob = " ".join([e.get("name", "")] + e.get("contexts", []) + e.get("types_seen", []))
    hits = []
    for term in NIN_RELEVANCE_TERMS:
        if term.lower() in blob.lower():
            hits.append(term)

    score = min(100, len(set(hits)) * 10 + e.get("mentions", 0) * 5)
    return score, sorted(set(hits))

def main():
    clean = load(CLEAN, {})
    ranked = load(RANKED, [])

    rows = []
    for e in ranked:
        score, hits = overlap_score(e)
        if score <= 0:
            continue
        row = dict(e)
        row["nin_overlap_score"] = score
        row["overlap_terms"] = hits
        rows.append(row)

    rows.sort(key=lambda x: (x["nin_overlap_score"], x.get("rank_score", 0)), reverse=True)

    result = {
        "title": "TOKYO ART BOOK FAIR",
        "overlap_count": len(rows),
        "top_overlap_entities": rows[:80],
        "summary": {
            "clean_entity_count": clean.get("clean_entity_count", 0),
            "raw_entity_count": clean.get("raw_entity_count", 0),
            "publishers_or_presses": len(clean.get("publishers_or_presses", [])),
            "artists_or_collectives": len(clean.get("artists_or_collectives", [])),
            "bookstores_or_galleries": len(clean.get("bookstores_or_galleries", [])),
            "zines_or_books": len(clean.get("zines_or_books", [])),
        }
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# TABF ↔ Nin Ecosystem Overlap",
        "",
        "Shows why Tokyo Art Book Fair matters for Nin's zine / publication / art-book direction.",
        "",
        f"- Raw entities: {result['summary']['raw_entity_count']}",
        f"- Clean entities: {result['summary']['clean_entity_count']}",
        f"- Overlap entities: {result['overlap_count']}",
        f"- Publishers / presses: {result['summary']['publishers_or_presses']}",
        f"- Artists / collectives: {result['summary']['artists_or_collectives']}",
        f"- Bookstores / galleries: {result['summary']['bookstores_or_galleries']}",
        f"- Zines / books: {result['summary']['zines_or_books']}",
        "",
        "## Why TABF matters",
        "",
        "TABF is valuable because it is not merely an exhibition. It is a publishing and direct-sales ecosystem around art books, zines, publishers, galleries, bookstores, and artists.",
        "",
        "## Top overlap entities",
        "",
    ]

    for e in rows[:50]:
        lines.append(f"### {e['name']}")
        lines.append(f"- Nin overlap: {e['nin_overlap_score']}/100")
        lines.append(f"- Rank score: {e.get('rank_score')}/100")
        lines.append(f"- Type: {e.get('entity_type')}")
        lines.append(f"- Overlap terms: {', '.join(e.get('overlap_terms', []))}")
        if e.get("contexts"):
            lines.append("")
            lines.append("Evidence:")
            lines.append(f"- {e['contexts'][0]}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
