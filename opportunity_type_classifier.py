
import json
from pathlib import Path

SOURCES = [
    "memory/nin_opportunity_recommendations.json",
    "memory/opportunity_briefs.json",
    "memory/opportunity_evidence_cards.json",
]

OUT_JSON = "memory/opportunity_type_classifications.json"
OUT_REPORT = "reports/opportunity_type_classifications.md"

TYPE_RULES = {
    "artist_book_fair": ["art book fair", "artist book", "book fair", "TABF", "tokyo art book"],
    "zine_fair": ["zine fair", "zine", "ZINE"],
    "zine_shop": ["zine shop", "zines"],
    "artist_book_store": ["artist book store", "bookstore", "book shop"],
    "small_press_publisher": ["small press", "publisher", "press", "publishing"],
    "illustration_gallery": ["illustration", "picture book", "絵本", "Pinpoint"],
    "bookstore_gallery": ["bookstore", "gallery", "book shop"],
    "print_market": ["print", "prints", "risograph", "リソグラフ"],
    "quiet_contemporary_gallery": ["contemporary", "quiet", "gallery"],
    "traditional_painting_society": ["watercolour society", "watercolor society", "painters in water colours", "pastel society", "royal institute"],
    "large_formal_competition": ["art prize", "competition", "open exhibition"],
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def collect_opportunities():
    rows = {}
    for src in SOURCES:
        data = load(src, [])
        if isinstance(data, dict):
            continue
        for item in data:
            title = item.get("title")
            if not title:
                continue
            rows.setdefault(title, {"title": title, "text": ""})
            rows[title]["text"] += " " + json.dumps(item, ensure_ascii=False)
    return list(rows.values())

def classify(text):
    low = text.lower()
    types = []
    for typ, terms in TYPE_RULES.items():
        if any(term.lower() in low for term in terms):
            types.append(typ)
    return types or ["unknown"]

def main():
    rows = collect_opportunities()
    out = []
    for r in rows:
        types = classify(r["title"] + " " + r["text"])
        out.append({
            "title": r["title"],
            "opportunity_types": types,
        })

    out.sort(key=lambda x: x["title"])

    Path("memory").mkdir(exist_ok=True)
    json.dump(out, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = ["# Opportunity Type Classifications", ""]
    for r in out:
        lines.append(f"## {r['title']}")
        lines.append(f"- Types: {', '.join(r['opportunity_types'])}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
