
import json
from pathlib import Path
from collections import defaultdict

SRC = "memory/parsed_artist_biographies.json"
OUT_JSON = "memory/artist_career_graph.json"
OUT_REPORT = "reports/artist_career_graph.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    bios = load(SRC, [])

    artists = {}
    publishers = defaultdict(list)
    books = defaultdict(list)
    awards = defaultdict(list)
    opportunities = defaultdict(list)

    for b in bios:
        name = b.get("artist_name")
        if not name:
            continue

        artists[name] = {
            "artist_name": name,
            "roles": b.get("roles", []),
            "birth_year": b.get("birth_year"),
            "birth_place": b.get("birth_place"),
            "source_opportunities": sorted(set([b.get("source_opportunity")])),
            "source_url": b.get("source_url"),
            "books_or_works": b.get("books_or_works", []),
            "publishers_or_clients": b.get("publishers_or_clients", []),
            "awards_or_selections": b.get("awards_or_selections", []),
            "education": b.get("education", []),
            "career_clues": b.get("career_clues", []),
        }

        opp = b.get("source_opportunity")
        if opp:
            opportunities[opp].append(name)

        for pub in b.get("publishers_or_clients", []):
            publishers[pub].append(name)

        for book in b.get("books_or_works", []):
            books[book].append(name)

        for award in b.get("awards_or_selections", []):
            awards[award].append(name)

    graph = {
        "artists": list(artists.values()),
        "publishers": [{"name": k, "artists": sorted(set(v))} for k, v in publishers.items()],
        "books_or_works": [{"title": k, "artists": sorted(set(v))} for k, v in books.items()],
        "awards_or_selections": [{"name": k, "artists": sorted(set(v))} for k, v in awards.items()],
        "opportunities": [{"title": k, "artists": sorted(set(v))} for k, v in opportunities.items()],
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(graph, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Artist Career Graph",
        "",
        "Connects artists to books, publishers, awards, and source opportunities.",
        "",
        f"- Artists: {len(graph['artists'])}",
        f"- Publishers/clients: {len(graph['publishers'])}",
        f"- Books/works: {len(graph['books_or_works'])}",
        f"- Awards/selections: {len(graph['awards_or_selections'])}",
        "",
    ]

    lines.append("## Artists")
    lines.append("")
    for a in graph["artists"]:
        lines.append(f"### {a['artist_name']}")
        lines.append(f"- Roles: {', '.join(a.get('roles', []))}")
        lines.append(f"- Birth: {a.get('birth_year')} / {a.get('birth_place')}")
        lines.append(f"- Opportunity: {', '.join(a.get('source_opportunities', []))}")
        if a.get("books_or_works"):
            lines.append(f"- Books/works: {', '.join(a['books_or_works'][:6])}")
        if a.get("publishers_or_clients"):
            lines.append(f"- Publishers/clients: {', '.join(a['publishers_or_clients'][:6])}")
        if a.get("awards_or_selections"):
            lines.append(f"- Awards/selections: {len(a['awards_or_selections'])}")
        lines.append("")

    lines.append("## Publishers / Clients")
    lines.append("")
    for p in graph["publishers"][:40]:
        lines.append(f"- {p['name']} → {', '.join(p['artists'])}")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
