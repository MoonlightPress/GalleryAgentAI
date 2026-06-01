
import json
import os
from pathlib import Path

PROFILE_PATH = "memory/artist_visual_profile.json"
OPP_PATH = "deploy_data/compact_opportunities.json"
PUBLISHER_PATH = "memory/publisher_matches.json"
ECOSYSTEM_PATH = "memory/ecosystem_graph.json"

OUT_JSON = "memory/next_projects.json"
OUT_REPORT = "reports/next_projects.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def text_blob(item):
    parts = []
    for key in [
        "title", "name", "organization", "category", "category_label",
        "one_sentence", "why_this_fits_short", "exclusive_primary_bucket",
        "primary_bucket"
    ]:
        if item.get(key):
            parts.append(str(item[key]))

    for key in ["visual_fit_hits", "fit_keyword_hits", "tags"]:
        for x in item.get(key, []) or []:
            parts.append(str(x))

    return " ".join(parts).lower()


def score_target(opp, terms):
    blob = text_blob(opp)
    score = float(opp.get("differentiated_score", opp.get("overall_score", 0)) or 0)
    hits = []

    for term in terms:
        if term.lower() in blob:
            score += 1.2
            hits.append(term)

    if opp.get("recommendation_visibility") == "hidden":
        score -= 10

    if opp.get("verification_bucket") == "reject":
        score -= 10

    return score, hits


def find_targets(opps, terms, limit=6):
    matches = []

    for opp in opps:
        score, hits = score_target(opp, terms)
        if hits and score > 0:
            matches.append({
                "title": opp.get("title") or opp.get("name") or "Unknown",
                "score": opp.get("overall_score"),
                "differentiated_score": opp.get("differentiated_score"),
                "verification": opp.get("verification_bucket", opp.get("verification_status", "")),
                "hits": hits,
                "why": opp.get("why_this_fits_short") or opp.get("one_sentence") or "",
                "source": (
                    opp.get("source_url")
                    or opp.get("official_website")
                    or opp.get("source_link")
                    or opp.get("submission_page")
                    or ""
                ),
            })

    matches.sort(key=lambda x: float(x.get("differentiated_score", x.get("score", 0)) or 0), reverse=True)
    return matches[:limit]


def find_publishers(publishers, terms, limit=5):
    out = []
    for pub in publishers:
        blob = " ".join([
            str(pub.get("name", "")),
            str(pub.get("why", "")),
            str(pub.get("best_use", "")),
            " ".join(pub.get("fit_tags", []) or []),
        ]).lower()

        hits = [t for t in terms if t.lower() in blob]

        if hits:
            out.append({
                "name": pub.get("name"),
                "fit_score": pub.get("fit_score"),
                "match_strength": pub.get("match_strength"),
                "why": pub.get("why"),
                "hits": hits,
            })

    out.sort(key=lambda x: float(x.get("fit_score", 0) or 0), reverse=True)
    return out[:limit]


def build_projects(profile):
    return [
        {
            "id": "quiet_neighborhood_memory",
            "title": "Quiet Neighborhood Memory",
            "type": "photobook / zine sequence",
            "promise": "A quiet sequence about ordinary neighborhoods, small shops, plants, thresholds, and traces of daily life.",
            "why_this_matters": "This is the clearest fit with the visual profile: memory, human trace, lived-in architecture, and slow observational photography.",
            "image_brief": [
                "Select 18–24 images.",
                "Prioritize streets, small businesses, plants, doors, laundry, fences, stairs, yards, and quiet shopfronts.",
                "Choose images that imply human presence without needing people in the frame.",
                "Avoid travel-postcard images and isolated cute details unless they add rhythm."
            ],
            "sequence_shape": [
                "Open with a strong place-setting image.",
                "Move through repeated motifs: plants, walls, thresholds, traces of use.",
                "Include 2–3 wider street/context images as breathers.",
                "End with an image that feels unresolved rather than final."
            ],
            "target_terms": ["photobook", "zine", "artist book", "small press", "book fair", "memory", "place", "daily life"],
            "first_action": "Make a 20-image edit and title it provisionally. Do not write the full statement yet."
        },
        {
            "id": "human_trace_study",
            "title": "Human Trace Study",
            "type": "artist-book / portfolio sequence",
            "promise": "A tighter study of spaces shaped by use: fences, laundry, paths, windows, plants, signs, worn surfaces, and domestic edges.",
            "why_this_matters": "This gives the work a sharper conceptual hook without making it heavy or academic.",
            "image_brief": [
                "Select 12–18 images.",
                "Each image should show evidence of human life without making people the subject.",
                "Favor surfaces, repairs, improvised arrangements, plants, signage, and domestic thresholds.",
                "Remove anything that is only pretty."
            ],
            "sequence_shape": [
                "Start with an image that clearly establishes trace.",
                "Build through variations: care, neglect, adaptation, routine.",
                "Keep the edit restrained.",
                "End with the quietest image, not the most dramatic one."
            ],
            "target_terms": ["human trace", "memory", "architecture", "daily life", "documentary", "artist book", "portfolio review"],
            "first_action": "Build the edit as a PDF contact sheet first, then reduce it by half."
        },
        {
            "id": "small_press_walk",
            "title": "Small Press City Walk",
            "type": "short zine",
            "promise": "A small, approachable zine built from one neighborhood walk, structured by visual rhythm rather than explanation.",
            "why_this_matters": "This is the fastest project to finish and the best low-pressure way into zine/bookstore opportunities.",
            "image_brief": [
                "Use one neighborhood or one walk.",
                "Select 10–16 images.",
                "Make the sequence feel like noticing things while moving through a place.",
                "Include small surprises but avoid novelty for its own sake."
            ],
            "sequence_shape": [
                "Begin outside.",
                "Move toward details.",
                "Return to a wider image near the end.",
                "Close with something modest but memorable."
            ],
            "target_terms": ["zine", "small press", "bookstore", "book fair", "artist book", "local", "independent publishing"],
            "first_action": "Create a 12-image version first. This is the easiest thing to make real."
        }
    ]


def main():
    profile = load_json(PROFILE_PATH, {})
    opps = load_json(OPP_PATH, [])
    publishers = load_json(PUBLISHER_PATH, [])

    projects = build_projects(profile)

    for project in projects:
        terms = project["target_terms"]
        project["best_opportunity_targets"] = find_targets(opps, terms, limit=8)
        project["best_publisher_targets"] = find_publishers(publishers, terms, limit=6)

    save_json(OUT_JSON, projects)

    lines = [
        "# Next Project Recommendations",
        "",
        "This report answers the question: what should she actually make or submit next?",
        "",
    ]

    for p in projects:
        lines.append(f"## {p['title']}")
        lines.append("")
        lines.append(f"**Format:** {p['type']}")
        lines.append("")
        lines.append(f"**Promise:** {p['promise']}")
        lines.append("")
        lines.append(f"**Why this matters:** {p['why_this_matters']}")
        lines.append("")

        lines.append("### Image Brief")
        for item in p["image_brief"]:
            lines.append(f"- {item}")
        lines.append("")

        lines.append("### Sequence Shape")
        for item in p["sequence_shape"]:
            lines.append(f"- {item}")
        lines.append("")

        lines.append("### Best Opportunity Targets")
        targets = p.get("best_opportunity_targets", [])
        if not targets:
            lines.append("_No current targets found._")
        else:
            for t in targets:
                lines.append(f"- **{t['title']}** — {t.get('score')} / {t.get('differentiated_score')}. {t.get('why')}")
        lines.append("")

        lines.append("### Best Publisher / Platform Targets")
        pubs = p.get("best_publisher_targets", [])
        if not pubs:
            lines.append("_No publisher targets found._")
        else:
            for pub in pubs:
                lines.append(f"- **{pub['name']}** — {pub.get('match_strength')} — {pub.get('why')}")
        lines.append("")

        lines.append("### First Action")
        lines.append(p["first_action"])
        lines.append("")

    Path(OUT_REPORT).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_REPORT}")


if __name__ == "__main__":
    main()
