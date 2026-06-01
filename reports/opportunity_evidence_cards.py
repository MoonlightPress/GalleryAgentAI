
import json
from pathlib import Path

RELEVANCE = "memory/relevance_scores.json"
NIN_RECS = "memory/nin_opportunity_recommendations.json"
ECOSYSTEMS = "memory/opportunity_ecosystems.json"
DENSITY = "memory/ecosystem_density_scores.json"

OUT_JSON = "memory/opportunity_evidence_cards.json"
OUT_REPORT = "reports/opportunity_evidence_cards.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def by_title(rows):
    return {r.get("title"): r for r in rows if r.get("title")}

def card_for_tabf(relevance):
    ents = relevance.get("TOKYO ART BOOK FAIR", {}).get("entities", [])
    top = [e for e in ents if e["relevance_score"] >= 45][:12]

    bullets = [
        "Japan's major art-book fair ecosystem: publishers, galleries, bookstores, artists, zines, and artist books.",
        "Directly relevant to zines, printed editions, and artist-book presentation.",
        "The crawler found named ecosystem entities rather than only generic application data.",
    ]

    if top:
        bullets.append("Strong named ecosystem examples include: " + ", ".join(e["name"] for e in top[:6]) + ".")

    return {
        "title": "TOKYO ART BOOK FAIR",
        "card_type": "publishing_ecosystem",
        "priority_label": "research priority",
        "why_it_matters": bullets,
        "evidence_entities": top,
        "next_action": "Validate current exhibitor application details and identify 5-10 recent exhibitors closest to Nin's zine/art-book practice.",
    }

def card_for_pinpoint(recs, ecosystems, density):
    rec = by_title(recs).get("Pinpoint Gallery", {})
    eco = by_title(ecosystems).get("Pinpoint Gallery", {})
    den = by_title(density).get("Pinpoint Gallery", {})

    similar = eco.get("similar_artists", [])[:5]
    publishers = eco.get("publishers", [])[:8]
    books = eco.get("books_or_works", [])[:8]

    bullets = [
        "Strong bridge between illustration, books, and gallery presentation.",
        f"Ecosystem density: {den.get('ecosystem_density', 'unknown')}/100.",
        f"Recommendation score: {rec.get('recommendation_score', 'unknown')}/100.",
    ]

    if similar:
        bullets.append("Similar artist evidence: " + ", ".join(a["name"] for a in similar) + ".")
    if publishers:
        bullets.append("Publishing/client evidence includes: " + ", ".join(p["name"] for p in publishers[:5]) + ".")
    if books:
        bullets.append("Book/work evidence includes: " + ", ".join(b["name"] for b in books[:5]) + ".")

    return {
        "title": "Pinpoint Gallery",
        "card_type": "illustration_publishing_bridge",
        "priority_label": "current strongest evidence-backed opportunity",
        "why_it_matters": bullets,
        "similar_artists": similar,
        "publishers": publishers,
        "books_or_works": books,
        "next_action": "Confirm current deadline, fee, and submission rules; prepare a concise application path.",
    }

def main():
    relevance = load(RELEVANCE, {})
    recs = load(NIN_RECS, [])
    ecosystems = load(ECOSYSTEMS, [])
    density = load(DENSITY, [])

    cards = [
        card_for_pinpoint(recs, ecosystems, density),
        card_for_tabf(relevance),
    ]

    Path("memory").mkdir(exist_ok=True)
    json.dump(cards, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Opportunity Evidence Cards",
        "",
        "Readable opportunity cards built from evidence chains, not raw keyword scores.",
        "",
    ]

    for c in cards:
        lines.append(f"## {c['title']}")
        lines.append(f"- Type: {c['card_type']}")
        lines.append(f"- Priority: {c['priority_label']}")
        lines.append("")
        lines.append("### Why this matters")
        for b in c.get("why_it_matters", []):
            lines.append(f"- {b}")
        lines.append("")
        if c.get("evidence_entities"):
            lines.append("### Evidence entities")
            for e in c["evidence_entities"][:10]:
                lines.append(f"- {e['name']} — {e['relevance_score']}/100 — {e['entity_type']}")
            lines.append("")
        if c.get("similar_artists"):
            lines.append("### Similar artists")
            for a in c["similar_artists"]:
                lines.append(f"- {a['name']} — {a.get('similarity_score')}/100")
            lines.append("")
        if c.get("publishers"):
            lines.append("### Publishers / clients")
            for p in c["publishers"][:8]:
                lines.append(f"- {p['name']}")
            lines.append("")
        lines.append("### Next action")
        lines.append(c.get("next_action", "No next action."))
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
