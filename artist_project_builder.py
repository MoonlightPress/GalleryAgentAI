
import json
import os
from pathlib import Path

PROFILE_PATH = "memory/artist_visual_profile.json"
PUBLISHER_PATH = "memory/publisher_matches.json"
OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/artist_project_concepts.json"
REPORT_PATH = "reports/artist_project_concepts.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def opp_text(opp):
    parts = []
    for key in ["title", "name", "organization", "category", "why_this_fits_short", "one_sentence"]:
        if opp.get(key):
            parts.append(str(opp[key]))
    return " ".join(parts).lower()


def match_opportunities(terms, opps, limit=8):
    matches = []

    for opp in opps:
        text = opp_text(opp)
        hits = [t for t in terms if t.lower() in text]

        if hits:
            matches.append({
                "title": opp.get("title") or opp.get("name") or "Unknown",
                "score": opp.get("overall_score"),
                "differentiated_score": opp.get("differentiated_score"),
                "hits": hits,
                "why": opp.get("why_this_fits_short") or opp.get("one_sentence") or "",
            })

    matches.sort(key=lambda x: float(x.get("differentiated_score", x.get("score", 0)) or 0), reverse=True)

    return matches[:limit]


def project_concepts(profile):
    return [
        {
            "id": "neighborhood_memory",
            "title": "Neighborhood Memory",
            "format": "photobook / zine sequence",
            "one_sentence": "A quiet photographic sequence about ordinary neighborhoods, lived-in architecture, small shops, plants, thresholds, and the emotional memory held by everyday places.",
            "visual_logic": [
                "ordinary streets",
                "small storefronts",
                "aged walls",
                "thresholds",
                "plants against buildings",
                "human presence through absence",
                "slow accumulation"
            ],
            "best_images_to_select": [
                "streets and buildings with no obvious spectacle",
                "places that feel inhabited but not staged",
                "plants, laundry, signs, steps, fences, yards",
                "images with traces of use or habit",
                "images that quietly imply someone was here"
            ],
            "avoid": [
                "single-image spectacle",
                "tourist feeling",
                "cute-only images",
                "images that rely on captions to make sense"
            ],
            "target_terms": ["photobook", "zine", "artist book", "printed matter", "small press", "book fair", "memory", "place"],
        },
        {
            "id": "human_trace",
            "title": "Human Trace",
            "format": "small artist book / exhibition sequence",
            "one_sentence": "A focused body of work about indirect human presence: fences, laundry, paths, windows, plants, signs, and objects shaped by daily life.",
            "visual_logic": [
                "absence as evidence",
                "architecture shaped by use",
                "domestic edges",
                "objects and surfaces carrying time",
                "quiet documentary observation"
            ],
            "best_images_to_select": [
                "empty places that feel recently used",
                "details of maintenance, care, neglect, or adaptation",
                "small architectural decisions",
                "images where the subject is a trace rather than an event"
            ],
            "avoid": [
                "too many wide street views",
                "images where nothing indicates human use",
                "anything that feels merely pretty"
            ],
            "target_terms": ["human trace", "memory", "architecture", "daily life", "documentary", "artist book"],
        },
        {
            "id": "small_press_city_walk",
            "title": "Small Press City Walk",
            "format": "short zine / local publication",
            "one_sentence": "A compact, low-pressure zine built from a walk through a neighborhood, edited as a sequence of small visual discoveries.",
            "visual_logic": [
                "walk-based structure",
                "small discoveries",
                "visual rhythm",
                "local specificity",
                "approachable sequencing"
            ],
            "best_images_to_select": [
                "10–20 images from one neighborhood or walk",
                "strong beginning and ending images",
                "repeated motifs",
                "visual pauses",
                "one or two quiet surprises"
            ],
            "avoid": [
                "too many unrelated locations",
                "over-editing",
                "trying to make it too important"
            ],
            "target_terms": ["zine", "small press", "bookstore", "book fair", "artist book", "local"],
        },
        {
            "id": "quiet_architecture",
            "title": "Quiet Architecture",
            "format": "portfolio sequence / open call submission",
            "one_sentence": "A portfolio sequence centered on vernacular architecture, domestic structures, surfaces, and ordinary built environments.",
            "visual_logic": [
                "ordinary architecture",
                "urban vernacular",
                "soft documentary restraint",
                "place as subject",
                "surface and time"
            ],
            "best_images_to_select": [
                "buildings and structures with emotional weight",
                "facades, steps, walls, alleys, shopfronts",
                "images with formal clarity",
                "images that feel calm but specific"
            ],
            "avoid": [
                "generic street photography",
                "busy scenes",
                "overly commercial-looking architecture"
            ],
            "target_terms": ["architecture", "urban vernacular", "documentary", "photography", "portfolio review", "open call"],
        }
    ]


def assign_targets(concepts, publishers, opps):
    for concept in concepts:
        terms = concept.get("target_terms", [])

        matched_publishers = []

        for pub in publishers:
            blob = " ".join([
                pub.get("name", ""),
                pub.get("why", ""),
                pub.get("best_use", ""),
                " ".join(pub.get("fit_tags", [])),
            ]).lower()

            hits = [t for t in terms if t.lower() in blob]

            if hits:
                matched_publishers.append({
                    "name": pub.get("name"),
                    "fit_score": pub.get("fit_score"),
                    "match_strength": pub.get("match_strength"),
                    "why": pub.get("why"),
                    "hits": hits,
                })

        matched_publishers.sort(key=lambda x: float(x.get("fit_score", 0) or 0), reverse=True)

        concept["publisher_targets"] = matched_publishers[:6]
        concept["opportunity_targets"] = match_opportunities(terms, opps, limit=8)

    return concepts


def write_report(concepts):
    lines = [
        "# Artist Project Concepts",
        "",
        "This report answers the practical question: what should she actually make or submit?",
        "",
    ]

    for concept in concepts:
        lines.append(f"## {concept['title']}")
        lines.append("")
        lines.append(f"**Format:** {concept['format']}")
        lines.append("")
        lines.append(concept["one_sentence"])
        lines.append("")

        lines.append("### Visual Logic")
        for item in concept.get("visual_logic", []):
            lines.append(f"- {item}")
        lines.append("")

        lines.append("### Image Selection")
        for item in concept.get("best_images_to_select", []):
            lines.append(f"- {item}")
        lines.append("")

        lines.append("### Avoid")
        for item in concept.get("avoid", []):
            lines.append(f"- {item}")
        lines.append("")

        lines.append("### Publisher / Platform Targets")
        pubs = concept.get("publisher_targets", [])
        if not pubs:
            lines.append("_No publisher targets yet._")
        else:
            for pub in pubs:
                lines.append(f"- **{pub.get('name')}** — {pub.get('match_strength')} — {pub.get('why')}")
        lines.append("")

        lines.append("### Current Opportunity Targets")
        opps = concept.get("opportunity_targets", [])
        if not opps:
            lines.append("_No opportunity targets yet._")
        else:
            for opp in opps:
                lines.append(f"- **{opp.get('title')}** — {opp.get('score')} / {opp.get('differentiated_score')}. {opp.get('why')}")
        lines.append("")

        lines.append("### First Action")
        lines.append("Build a 12–20 image edit. Do not write a long statement yet. First prove the sequence works visually.")
        lines.append("")

    Path(REPORT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")


def main():
    profile = load_json(PROFILE_PATH, {})
    publishers = load_json(PUBLISHER_PATH, [])
    opps = load_json(OPP_PATH, [])

    concepts = project_concepts(profile)
    concepts = assign_targets(concepts, publishers, opps)

    save_json(OUT_PATH, concepts)
    write_report(concepts)

    print(f"Wrote {OUT_PATH}")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
