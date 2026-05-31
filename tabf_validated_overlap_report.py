
import json
from pathlib import Path

SRC = "memory/tabf_validated_entities.json"
OUT_JSON = "memory/tabf_validated_overlap.json"
OUT_REPORT = "reports/tabf_validated_overlap.md"

NIN_TERMS = {
    "zines": ["zine", "ZINE", "ジン"],
    "artist_books": ["artist book", "art book", "アーティストブック", "アートブック"],
    "publishing": ["publisher", "press", "publishing", "出版", "出版社"],
    "gallery": ["gallery", "ギャラリー"],
    "bookstore": ["bookstore", "book shop", "書店"],
    "prints": ["print", "prints", "リソグラフ", "risograph"],
    "international": ["Germany", "Italy", "France", "Brazil", "international", "国内外", "海外"],
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def overlap(entity):
    blob = " ".join([entity.get("name", "")] + entity.get("contexts", []) + entity.get("types_seen", []))
    hits = []
    for bucket, terms in NIN_TERMS.items():
        if any(t.lower() in blob.lower() for t in terms):
            hits.append(bucket)
    score = min(100, len(hits) * 16 + entity.get("validation_score", 0) * 0.4 + entity.get("mentions", 0) * 3)
    return round(score, 1), hits

def main():
    data = load(SRC, {})
    entities = data.get("validated_entities", [])

    rows = []
    for e in entities:
        score, hits = overlap(e)
        if hits:
            row = dict(e)
            row["nin_overlap_score"] = score
            row["overlap_buckets"] = hits
            rows.append(row)

    rows.sort(key=lambda x: x["nin_overlap_score"], reverse=True)

    result = {
        "title": "TOKYO ART BOOK FAIR",
        "validated_entity_count": len(entities),
        "overlap_count": len(rows),
        "top_overlap": rows[:80],
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# TABF Validated Overlap",
        "",
        "Uses only validated entities. This should be cleaner than the previous TABF overlap report.",
        "",
        f"- Validated entities: {result['validated_entity_count']}",
        f"- Overlap entities: {result['overlap_count']}",
        "",
        "## Summary",
        "",
        "TABF is relevant to Nin because its strongest validated entities sit inside art-book, zine, publishing, gallery, and international small-press ecosystems.",
        "",
        "## Top validated overlaps",
        "",
    ]

    for e in rows[:50]:
        lines.append(f"### {e['name']}")
        lines.append(f"- Overlap: {e['nin_overlap_score']}/100")
        lines.append(f"- Type: {e.get('validated_type')}")
        lines.append(f"- Buckets: {', '.join(e.get('overlap_buckets', []))}")
        lines.append(f"- Validation: {e.get('validation_score')} ({e.get('validation_reason')})")
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
