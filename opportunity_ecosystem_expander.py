
import json
import re
from pathlib import Path
from collections import defaultdict

CAREER_GRAPH = "memory/artist_career_graph.json"
VALIDATED_BIOS = "memory/validated_artist_biographies.json"
VALIDATED_PROFILES = "memory/validated_artist_profiles.json"
EVIDENCE = "memory/opportunity_evidence.json"
MATCHES = "memory/nin_artist_matches.json"

OUT_JSON = "memory/opportunity_ecosystems.json"
OUT_REPORT = "reports/opportunity_ecosystems.md"

JUDGE_TERMS = ["judge", "juror", "審査員", "審査", "editor", "編集者"]
PUBLISHER_TERMS = ["publisher", "press", "bookstore", "出版社", "書店", "小学館", "福音館書店", "PHP研究所", "学研", "NHK", "理論社", "偕成社", "小峰書店", "ブロンズ新社", "大日本図書"]
ORG_TERMS = ["partner", "sponsor", "協力", "後援", "gallery", "ギャラリー", "university", "foundation", "society", "association"]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def by_title(rows):
    return {r.get("title"): r for r in rows if r.get("title")}

def add_unique(lst, item, key="name"):
    val = item.get(key)
    if not val:
        return
    if val not in {x.get(key) for x in lst}:
        lst.append(item)

def extract_term_entities(text, terms):
    found = []
    if not text:
        return found
    sentences = re.split(r"[。．.!?\n]", text)
    for s in sentences:
        s = " ".join(s.split())
        if len(s) < 8 or len(s) > 260:
            continue
        if any(t.lower() in s.lower() for t in terms):
            found.append(s)
    return found[:20]

def main():
    graph = load(CAREER_GRAPH, {})
    bios = load(VALIDATED_BIOS, [])
    profiles = load(VALIDATED_PROFILES, [])
    evidence = load(EVIDENCE, [])
    matches = load(MATCHES, [])

    match_by_artist = {m.get("artist_name"): m for m in matches}

    ecosystems = defaultdict(lambda: {
        "title": "",
        "artists": [],
        "publishers": [],
        "books_or_works": [],
        "awards_or_selections": [],
        "judges_or_gatekeepers": [],
        "organizations": [],
        "similar_artists": [],
        "evidence_clues": [],
    })

    # From parsed career graph.
    for artist in graph.get("artists", []):
        for opp in artist.get("source_opportunities", []):
            eco = ecosystems[opp]
            eco["title"] = opp

            sim = match_by_artist.get(artist.get("artist_name"), {})
            artist_row = {
                "name": artist.get("artist_name"),
                "roles": artist.get("roles", []),
                "birth_year": artist.get("birth_year"),
                "birth_place": artist.get("birth_place"),
                "similarity_score": sim.get("similarity_score", 0),
                "reasons": sim.get("reasons", []),
                "source_url": artist.get("source_url"),
            }
            add_unique(eco["artists"], artist_row)

            if artist_row["similarity_score"] >= 45:
                add_unique(eco["similar_artists"], artist_row)

            for pub in artist.get("publishers_or_clients", []):
                add_unique(eco["publishers"], {"name": pub, "artist": artist.get("artist_name"), "source": "career_graph"})

            for book in artist.get("books_or_works", []):
                add_unique(eco["books_or_works"], {"name": book, "artist": artist.get("artist_name"), "source": "career_graph"})

            for award in artist.get("awards_or_selections", []):
                add_unique(eco["awards_or_selections"], {"name": award, "artist": artist.get("artist_name"), "source": "career_graph"})

    # From validated biographies: judges/publishers/org clues.
    for b in bios:
        opp = b.get("source_opportunity")
        if not opp:
            continue
        eco = ecosystems[opp]
        eco["title"] = opp
        text = b.get("bio_text", "")

        for clue in extract_term_entities(text, JUDGE_TERMS):
            add_unique(eco["judges_or_gatekeepers"], {"name": clue[:120], "source": "bio_text"}, key="name")

        for clue in extract_term_entities(text, PUBLISHER_TERMS):
            add_unique(eco["publishers"], {"name": clue[:120], "artist": b.get("artist_name"), "source": "bio_text"}, key="name")

        for clue in extract_term_entities(text, ORG_TERMS):
            add_unique(eco["organizations"], {"name": clue[:120], "source": "bio_text"}, key="name")

    # From raw opportunity evidence, but only as clues.
    for e in evidence:
        opp = e.get("title")
        if not opp:
            continue
        eco = ecosystems[opp]
        eco["title"] = opp

        for sent in e.get("evidence_sentences", []) or []:
            text = sent.get("text", "")
            if any(t.lower() in text.lower() for t in PUBLISHER_TERMS + JUDGE_TERMS + ORG_TERMS):
                add_unique(eco["evidence_clues"], {"name": text[:180], "source": "opportunity_evidence"}, key="name")

    rows = list(ecosystems.values())
    rows.sort(key=lambda x: (len(x["similar_artists"]), len(x["artists"]), len(x["publishers"])), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(rows, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Opportunity Ecosystems",
        "",
        "Builds evidence chains: artists, similar artists, publishers, books, awards, judges/gatekeepers, and organizations.",
        "",
    ]

    for eco in rows:
        lines.append(f"## {eco['title']}")
        lines.append(f"- Artists: {len(eco['artists'])}")
        lines.append(f"- Similar artists: {len(eco['similar_artists'])}")
        lines.append(f"- Publishers/clients: {len(eco['publishers'])}")
        lines.append(f"- Books/works: {len(eco['books_or_works'])}")
        lines.append(f"- Awards/selections: {len(eco['awards_or_selections'])}")
        lines.append(f"- Judges/gatekeepers: {len(eco['judges_or_gatekeepers'])}")
        lines.append(f"- Organizations/clues: {len(eco['organizations']) + len(eco['evidence_clues'])}")
        lines.append("")

        if eco["similar_artists"]:
            lines.append("### Similar artists")
            for a in sorted(eco["similar_artists"], key=lambda x: x.get("similarity_score", 0), reverse=True)[:8]:
                lines.append(f"- {a['name']} — {a.get('similarity_score')}/100 — {', '.join(a.get('reasons', []))}")

        if eco["publishers"]:
            lines.append("")
            lines.append("### Publishers / clients")
            for p in eco["publishers"][:12]:
                lines.append(f"- {p['name']} ({p.get('artist', 'unknown')})")

        if eco["books_or_works"]:
            lines.append("")
            lines.append("### Books / works")
            for b in eco["books_or_works"][:12]:
                lines.append(f"- {b['name']} ({b.get('artist', 'unknown')})")

        if eco["awards_or_selections"]:
            lines.append("")
            lines.append("### Awards / selections")
            for a in eco["awards_or_selections"][:8]:
                lines.append(f"- {a['name']} ({a.get('artist', 'unknown')})")

        if eco["judges_or_gatekeepers"]:
            lines.append("")
            lines.append("### Judges / gatekeepers")
            for j in eco["judges_or_gatekeepers"][:8]:
                lines.append(f"- {j['name']}")

        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
