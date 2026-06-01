
import json
from pathlib import Path

GRAPH = "memory/artist_career_graph.json"
OUT_JSON = "memory/nin_artist_matches.json"
OUT_REPORT = "reports/nin_artist_matches.md"

NIN_PROFILE = {
    "artist_name": "Nin",
    "keywords": [
        "watercolor",
        "works on paper",
        "quiet atmosphere",
        "urban scenes",
        "observational work",
        "contemporary realism",
        "books",
        "zines",
        "prints",
        "illustration",
        "gallery",
        "publishing",
        "small works",
        "intimate scale",
        "poetic realism",
    ],
    "career_targets": [
        "gallery exposure",
        "book/zine opportunities",
        "print sales",
        "artist book ecosystem",
        "illustration-adjacent exhibitions",
        "international visibility",
    ],
}

TOKEN_MAP = {
    "絵本": ["books", "illustration", "publishing"],
    "絵本作家": ["books", "illustration", "publishing"],
    "作家": ["artist"],
    "イラスト": ["illustration"],
    "illustrator": ["illustration"],
    "picture_book_artist": ["books", "illustration", "publishing"],
    "author": ["books", "publishing"],
    "artist": ["artist"],
    "painter": ["painting", "gallery"],
    "watercolor": ["watercolor", "works on paper"],
    "watercolour": ["watercolor", "works on paper"],
    "paper": ["works on paper"],
    "publisher": ["publishing"],
    "client": ["career evidence"],
    "award": ["career evidence"],
    "selection": ["career evidence"],
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def normalize_tokens(artist):
    tokens = set()

    for role in artist.get("roles", []):
        r = str(role)
        tokens.add(r.lower())
        for key, mapped in TOKEN_MAP.items():
            if key.lower() in r.lower():
                tokens.update(mapped)

    for book in artist.get("books_or_works", []):
        tokens.add("books")
        tokens.add("publishing")

    for pub in artist.get("publishers_or_clients", []):
        tokens.add("publishing")
        tokens.add("career evidence")

    for award in artist.get("awards_or_selections", []):
        tokens.add("award")
        tokens.add("career evidence")

    for clue in artist.get("career_clues", []):
        c = str(clue).lower()
        for key, mapped in TOKEN_MAP.items():
            if key.lower() in c:
                tokens.update(mapped)

    return tokens

def score_artist(artist):
    nin_tokens = set(NIN_PROFILE["keywords"] + NIN_PROFILE["career_targets"])
    artist_tokens = normalize_tokens(artist)

    shared = sorted(nin_tokens.intersection(artist_tokens))

    score = 0
    reasons = []

    if "books" in artist_tokens:
        score += 18
        reasons.append("book / publication ecosystem")
    if "publishing" in artist_tokens:
        score += 18
        reasons.append("publisher or publication evidence")
    if "illustration" in artist_tokens:
        score += 14
        reasons.append("illustration-adjacent")
    if "watercolor" in artist_tokens or "works on paper" in artist_tokens:
        score += 14
        reasons.append("works-on-paper / watercolor-adjacent")
    if artist.get("awards_or_selections"):
        score += 12
        reasons.append("award or selection history")
    if artist.get("publishers_or_clients"):
        score += 10
        reasons.append("real publisher/client links")
    if artist.get("books_or_works"):
        score += 10
        reasons.append("finished books or works listed")
    if "gallery" in artist_tokens:
        score += 6
        reasons.append("gallery/exhibition context")

    # Penalty for thin traditional-art entries with only award data.
    if not artist.get("books_or_works") and not artist.get("publishers_or_clients") and len(artist.get("awards_or_selections", [])) <= 2:
        score -= 15
        reasons.append("thin evidence")

    score = max(0, min(100, score))

    return {
        "artist_name": artist.get("artist_name"),
        "similarity_score": score,
        "shared_tokens": shared,
        "reasons": reasons,
        "source_opportunities": artist.get("source_opportunities", []),
        "books_or_works": artist.get("books_or_works", []),
        "publishers_or_clients": artist.get("publishers_or_clients", []),
        "awards_or_selections": artist.get("awards_or_selections", []),
        "roles": artist.get("roles", []),
        "source_url": artist.get("source_url"),
    }

def main():
    graph = load(GRAPH, {})
    artists = graph.get("artists", [])

    matches = [score_artist(a) for a in artists]
    matches.sort(key=lambda x: x["similarity_score"], reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(matches, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Nin Artist Matches",
        "",
        "Compares extracted career-graph artists against Nin's current opportunity profile.",
        "",
        "## Nin Profile",
        "",
        f"- Keywords: {', '.join(NIN_PROFILE['keywords'])}",
        f"- Career targets: {', '.join(NIN_PROFILE['career_targets'])}",
        "",
        "## Matches",
        "",
    ]

    for m in matches:
        label = "strong" if m["similarity_score"] >= 70 else "promising" if m["similarity_score"] >= 45 else "weak"
        lines.append(f"### {m['artist_name']}")
        lines.append(f"- Similarity: {m['similarity_score']}/100 ({label})")
        lines.append(f"- Opportunities: {', '.join(m.get('source_opportunities', []))}")
        lines.append(f"- Roles: {', '.join(m.get('roles', []))}")
        lines.append(f"- Reasons: {', '.join(m.get('reasons', [])) or 'none'}")
        if m.get("books_or_works"):
            lines.append(f"- Books/works: {', '.join(m['books_or_works'][:6])}")
        if m.get("publishers_or_clients"):
            lines.append(f"- Publishers/clients: {', '.join(m['publishers_or_clients'][:6])}")
        if m.get("awards_or_selections"):
            lines.append(f"- Awards/selections: {len(m['awards_or_selections'])}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
