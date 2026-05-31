
import json
from pathlib import Path

PROFILE_PATHS = [
    "memory/watercolor_artist_profile.json",
    "memory/artist_dna.json",
]

OUT = "memory/personalized_artist_context.json"
REPORT = "reports/personalized_artist_context.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    watercolor = load("memory/watercolor_artist_profile.json", {})
    dna = load("memory/artist_dna.json", {})

    context = {
        "version": 1,
        "primary_medium": "watercolor painting",
        "secondary_formats": [
            "zines",
            "artist books",
            "works on paper",
            "small publications"
        ],
        "known_existing_publications": True,
        "estimated_zine_count": 5,
        "book_fair_readiness": "medium-high",
        "zine_fair_readiness": "high",
        "gallery_submission_readiness": "medium",
        "open_exhibition_readiness": "medium",
        "competition_readiness": "medium-low until deadlines/fees are verified",
        "strongest_positioning": [
            "watercolor painter with existing zine/publication practice",
            "works-on-paper artist",
            "quiet urban/domestic observation",
            "small press compatible artist",
            "bookstore/gallery crossover fit"
        ],
        "priority_boosts": {
            "gallery_submission": 1.1,
            "book_fair": 1.4,
            "zine_fair": 1.6,
            "publication": 1.0,
            "open_exhibition": 0.7,
            "competition": 0.3,
            "unknown": -1.2
        },
        "priority_penalties": {
            "wrong_medium": -3.0,
            "catalog_page": -2.5,
            "specific_past_event": -2.5,
            "no_contact_no_link": -1.0,
            "deadline_unknown": -0.4,
            "requires_unmade_publication": 0.0
        },
        "note": "Because Nin already has around five zines, book fair, zine fair, bookstore, and small press opportunities should be treated as plausible targets rather than later-only targets."
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(context, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Personalized Artist Context",
        "",
        context["note"],
        "",
        "## Readiness",
        "",
        f"- Existing publications: {context['known_existing_publications']}",
        f"- Estimated zine count: {context['estimated_zine_count']}",
        f"- Book fair readiness: {context['book_fair_readiness']}",
        f"- Zine fair readiness: {context['zine_fair_readiness']}",
        f"- Gallery submission readiness: {context['gallery_submission_readiness']}",
        "",
        "## Strongest Positioning",
        "",
    ]

    for item in context["strongest_positioning"]:
        lines.append(f"- {item}")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT)
    print("Wrote", REPORT)

if __name__ == "__main__":
    main()
