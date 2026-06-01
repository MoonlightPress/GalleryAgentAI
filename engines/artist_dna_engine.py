
import json
from pathlib import Path
from collections import Counter

OUT_JSON = "memory/artist_dna.json"
OUT_REPORT = "reports/artist_dna.md"

# Hand-authored starting profile.
# Replace or extend this later with image/caption analysis.
ARTIST_DNA = {
    "artist_name": "Nin",
    "visual_language": [
        "quiet observational work",
        "muted urban atmosphere",
        "watercolor softness",
        "absence and stillness",
        "everyday scenes",
        "contemporary realism",
        "small intimate works",
        "print and zine compatible imagery",
    ],
    "mediums": [
        "watercolor",
        "works on paper",
        "prints",
        "zines",
    ],
    "career_contexts": [
        "zine shops",
        "artist book fairs",
        "small press publishers",
        "illustration-adjacent galleries",
        "quiet contemporary galleries",
        "print fairs",
        "bookstore exhibitions",
    ],
    "strong_fit_opportunity_types": [
        "artist_book_fair",
        "zine_fair",
        "zine_shop",
        "artist_book_store",
        "small_press_publisher",
        "illustration_gallery",
        "bookstore_gallery",
        "print_market",
        "quiet_contemporary_gallery",
    ],
    "weak_fit_opportunity_types": [
        "traditional_painting_society",
        "large_formal_competition",
        "generic_social_media_growth",
        "highly_commercial_merchandising",
    ],
    "positioning_sentence": "A quiet watercolor and works-on-paper artist whose practice fits best around zines, artist books, intimate print editions, small press culture, and illustration-adjacent galleries.",
}

def main():
    Path("memory").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    json.dump(ARTIST_DNA, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Artist DNA",
        "",
        f"Artist: {ARTIST_DNA['artist_name']}",
        "",
        "## Positioning",
        ARTIST_DNA["positioning_sentence"],
        "",
        "## Visual Language",
    ]

    for x in ARTIST_DNA["visual_language"]:
        lines.append(f"- {x}")

    lines += ["", "## Mediums"]
    for x in ARTIST_DNA["mediums"]:
        lines.append(f"- {x}")

    lines += ["", "## Best Career Contexts"]
    for x in ARTIST_DNA["career_contexts"]:
        lines.append(f"- {x}")

    lines += ["", "## Strong Fit Opportunity Types"]
    for x in ARTIST_DNA["strong_fit_opportunity_types"]:
        lines.append(f"- {x}")

    lines += ["", "## Weak Fit Opportunity Types"]
    for x in ARTIST_DNA["weak_fit_opportunity_types"]:
        lines.append(f"- {x}")

    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
