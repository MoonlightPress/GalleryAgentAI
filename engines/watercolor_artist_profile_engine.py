
import json, os
from pathlib import Path

OUT_PATH = "memory/watercolor_artist_profile.json"
REPORT_PATH = "reports/watercolor_artist_profile.md"

PROFILE = {
    "version": 1,
    "primary_medium": "watercolor painting",
    "secondary_media": ["drawing", "works on paper", "small-scale painting", "artist book / zine translation"],
    "not_primary_medium": ["photography", "street photography", "photobook-only practice"],
    "strategic_thesis": "Nin should be treated as a watercolor painter whose visual interests overlap with photobook and artist-book culture. Photos are reference evidence, not the career category.",
    "core_positioning": [
        "contemporary watercolor",
        "quiet observational painting",
        "works on paper",
        "architecture and domestic space",
        "plants and lived-in environments",
        "memory and human trace",
        "small-scale poetic realism",
        "urban / neighborhood observation"
    ],
    "best_opportunity_types": [
        "works on paper exhibitions",
        "watercolor open calls",
        "drawing and painting group shows",
        "small works exhibitions",
        "artist-run galleries",
        "paper-based art fairs",
        "illustration and picture-book adjacent opportunities",
        "small gallery representation",
        "residencies for painters",
        "artist grants for works on paper",
        "bookstore/gallery hybrid shows",
        "zine or artist-book translations of watercolor series"
    ],
    "bad_opportunity_types": [
        "street photography awards",
        "photography portfolio reviews",
        "photobook-only competitions unless paintings are translated into a book",
        "generic craft markets",
        "commercial design fairs",
        "AI/NFT/tech art",
        "large booth events with no curatorial framing"
    ],
    "project_directions": [
        {
            "title": "Quiet Neighborhood Watercolors",
            "format": "small watercolor series",
            "description": "A coherent watercolor series based on ordinary neighborhoods, shopfronts, plants, walls, doors, and lived-in architectural details."
        },
        {
            "title": "Human Trace / Works on Paper",
            "format": "works on paper exhibition proposal",
            "description": "A focused group of watercolors about indirect human presence in domestic and public spaces."
        },
        {
            "title": "Small Places",
            "format": "gallery-ready small works series",
            "description": "A low-pressure series of small watercolors for bookstores, cafes, artist-run spaces, or small gallery walls."
        },
        {
            "title": "Watercolor Artist Book",
            "format": "printed sequence",
            "description": "A zine or artist-book translation of watercolor works, using book sequencing while keeping painting primary."
        }
    ]
}

def main():
    Path("memory").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    Path(OUT_PATH).write_text(json.dumps(PROFILE, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = ["# Watercolor Artist Profile", "", PROFILE["strategic_thesis"], "", "## Core Positioning", ""]
    lines += [f"- {x}" for x in PROFILE["core_positioning"]]
    lines += ["", "## Best Opportunity Types", ""]
    lines += [f"- {x}" for x in PROFILE["best_opportunity_types"]]
    lines += ["", "## Bad Opportunity Types", ""]
    lines += [f"- {x}" for x in PROFILE["bad_opportunity_types"]]
    lines += ["", "## Project Directions", ""]
    for p in PROFILE["project_directions"]:
        lines += [f"### {p['title']}", f"- Format: {p['format']}", f"- {p['description']}", ""]
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")
    print(f"Wrote {REPORT_PATH}")

if __name__ == "__main__":
    main()
