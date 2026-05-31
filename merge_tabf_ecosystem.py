
import json
from pathlib import Path

ECOSYSTEMS = "memory/opportunity_ecosystems.json"
TABF = "memory/tabf_exhibitor_data.json"
OUT_JSON = "memory/opportunity_ecosystems_with_tabf.json"
OUT_REPORT = "reports/opportunity_ecosystems_with_tabf.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    ecosystems = load(ECOSYSTEMS, [])
    tabf = load(TABF, None)

    if tabf:
        tabf_row = {
            "title": "TOKYO ART BOOK FAIR",
            "artists": [
                {"name": e["name"], "roles": e["types"], "source_url": e.get("source_url")}
                for e in tabf.get("artists_or_collectives", [])
            ],
            "similar_artists": [],
            "publishers": [
                {"name": e["name"], "source": "tabf_crawler", "source_url": e.get("source_url")}
                for e in tabf.get("publishers_or_presses", [])
            ],
            "books_or_works": [
                {"name": e["name"], "source": "tabf_crawler", "source_url": e.get("source_url")}
                for e in tabf.get("zines_or_books", [])
            ],
            "awards_or_selections": [],
            "judges_or_gatekeepers": [],
            "organizations": [
                {"name": e["name"], "source": "tabf_crawler", "source_url": e.get("source_url")}
                for e in tabf.get("bookstores_or_galleries", [])
            ],
            "evidence_clues": [],
        }

        ecosystems = [e for e in ecosystems if e.get("title") != "TOKYO ART BOOK FAIR"]
        ecosystems.append(tabf_row)

    ecosystems.sort(key=lambda e: (len(e.get("similar_artists", [])), len(e.get("publishers", [])), len(e.get("artists", []))), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(ecosystems, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = ["# Opportunity Ecosystems With TABF", "", "Merged TABF-specific ecosystem evidence into the ecosystem layer.", ""]
    for e in ecosystems:
        lines.append(f"## {e.get('title')}")
        lines.append(f"- Artists/collectives: {len(e.get('artists', []))}")
        lines.append(f"- Similar artists: {len(e.get('similar_artists', []))}")
        lines.append(f"- Publishers/presses: {len(e.get('publishers', []))}")
        lines.append(f"- Books/zines/works: {len(e.get('books_or_works', []))}")
        lines.append(f"- Organizations/bookstores/galleries: {len(e.get('organizations', []))}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
