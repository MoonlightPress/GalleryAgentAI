
import json
from pathlib import Path

SUMMARY_PATH = Path("memory/artist_image_analysis/image_summary.json")
CATALOG_PATH = Path("memory/artist_image_analysis/image_catalog.json")
OUT_PATH = Path("memory/artist_visual_profile_draft.json")
REPORT_PATH = Path("reports/artist_visual_profile_draft.md")


def load_json(path, fallback):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return fallback


def infer_profile(summary, catalog):
    folders = summary.get("folders", {})
    temp = summary.get("temperature_distribution", {})
    bright = summary.get("brightness_distribution", {})
    aspects = summary.get("aspect_distribution", {})

    folder_names = " ".join(folders.keys()).lower()

    curatorial_keywords = []
    recurring_motifs = []
    emotional_tone = []
    best_formats = []

    if "architecture" in folder_names or "place" in folder_names or "memory" in folder_names:
        curatorial_keywords += ["architecture", "memory", "place", "quiet urban observation"]
        recurring_motifs += ["buildings", "streets", "interiors", "spatial fragments"]

    if "daily" in folder_names or "life" in folder_names:
        curatorial_keywords += ["daily life", "ordinary spaces", "intimate observation"]
        recurring_motifs += ["domestic details", "small moments", "ordinary scenes"]

    if "printed" in folder_names or "book" in folder_names or "matter" in folder_names:
        best_formats += ["artist book", "photobook", "zine", "printed matter"]

    if not best_formats:
        best_formats += ["photobook", "zine", "small exhibition", "artist-run space"]

    if bright.get("dark", 0) > bright.get("bright", 0):
        emotional_tone += ["muted", "low-key", "restrained"]
    else:
        emotional_tone += ["quiet", "observational", "clear"]

    if temp.get("warm", 0) > temp.get("cool", 0):
        emotional_tone += ["warm", "intimate"]
    elif temp.get("cool", 0) > temp.get("warm", 0):
        emotional_tone += ["cool", "distant", "contemplative"]

    if aspects.get("portrait", 0) > aspects.get("landscape", 0):
        composition_patterns = ["vertical framing", "isolated subjects", "narrow attention"]
    elif aspects.get("landscape", 0) > aspects.get("portrait", 0):
        composition_patterns = ["horizontal framing", "environmental context", "spatial observation"]
    else:
        composition_patterns = ["mixed aspect ratios", "variable distance", "flexible sequencing"]

    profile = {
        "summary": "Initial machine-assisted visual profile based on local image folder structure and image statistics. Review manually after looking at contact sheets.",
        "dominant_subjects": list(dict.fromkeys(recurring_motifs)),
        "recurring_motifs": list(dict.fromkeys(recurring_motifs)),
        "composition_patterns": composition_patterns,
        "color_palette": [
            f"average brightness {summary.get('average_brightness')}",
            f"temperature distribution {temp}",
        ],
        "emotional_tone": list(dict.fromkeys(emotional_tone)),
        "pace": "slow / observational",
        "scale": "intimate to environmental",
        "best_formats": list(dict.fromkeys(best_formats)),
        "bad_fit_contexts": ["corporate branding", "commercial expo", "loud trend-based open calls"],
        "artist_statement_phrases": [
            "memory of place",
            "quiet attention to ordinary spaces",
            "the emotional residue of architecture",
        ],
        "curatorial_keywords": list(dict.fromkeys(curatorial_keywords or ["quiet photography", "memory", "place", "atmosphere"])),
        "portfolio_bodies_to_create": list(folders.keys()),
    }

    return profile


def main():
    summary = load_json(SUMMARY_PATH, {})
    catalog = load_json(CATALOG_PATH, [])

    if not summary:
        raise SystemExit("No image summary found. Run python local_image_processor.py first.")

    profile = infer_profile(summary, catalog)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(profile, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    lines = [
        "# Artist Visual Profile Draft",
        "",
        profile["summary"],
        "",
        "## Curatorial Keywords",
        "",
    ]

    for item in profile["curatorial_keywords"]:
        lines.append(f"- {item}")

    lines += ["", "## Emotional Tone", ""]

    for item in profile["emotional_tone"]:
        lines.append(f"- {item}")

    lines += ["", "## Best Formats", ""]

    for item in profile["best_formats"]:
        lines.append(f"- {item}")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
