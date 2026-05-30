
import json
import os
from pathlib import Path
from collections import Counter, defaultdict
from PIL import Image, ImageStat

IMAGE_DIRS = [
    Path("images"),
    Path("artist_images"),
    Path("data/images"),
    Path("uploads/images"),
]

OUT_FEATURES = "analysis/image_features.json"
OUT_DNA = "memory/artist_dna.json"
OUT_REPORT = "reports/artist_dna_report.md"

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}


SUBJECT_HINTS = {
    "plants": ["green"],
    "architecture": ["gray", "white", "brown"],
    "quiet_space": ["low_contrast", "muted"],
    "daily_life": ["mixed_soft_colors"],
}


def find_images():
    images = []

    for folder in IMAGE_DIRS:
        if not folder.exists():
            continue

        for path in folder.rglob("*"):
            if path.suffix.lower() in SUPPORTED:
                images.append(path)

    return sorted(images)


def color_name(rgb):
    r, g, b = rgb

    if max(rgb) - min(rgb) < 18:
        if sum(rgb) / 3 < 70:
            return "dark_neutral"
        if sum(rgb) / 3 > 190:
            return "weathered_white"
        return "concrete_gray"

    if g > r * 1.08 and g > b * 1.05:
        return "muted_green"

    if r > g * 1.1 and r > b * 1.1:
        if g > 80:
            return "aged_wood_or_warm_wall"
        return "muted_red"

    if b > r * 1.05 and b > g * 1.05:
        return "faded_blue"

    if r > 150 and g > 130 and b < 120:
        return "warm_paper"

    return "soft_mixed_neutral"


def image_features(path):
    img = Image.open(path).convert("RGB")
    small = img.resize((1, 1))
    avg = small.getpixel((0, 0))

    stat = ImageStat.Stat(img.resize((128, 128)))
    mean = stat.mean
    std = stat.stddev

    brightness = sum(mean) / 3
    contrast = sum(std) / 3

    width, height = img.size
    ratio = width / max(height, 1)

    if ratio > 1.25:
        orientation = "landscape"
    elif ratio < 0.8:
        orientation = "portrait"
    else:
        orientation = "square_or_near_square"

    color = color_name(avg)

    mood = []
    if brightness < 85:
        mood.append("dark")
    elif brightness > 180:
        mood.append("light")
    else:
        mood.append("soft_mid_brightness")

    if contrast < 35:
        mood.append("low_contrast")
    elif contrast > 70:
        mood.append("high_contrast")
    else:
        mood.append("moderate_contrast")

    if color in {"muted_green", "concrete_gray", "weathered_white", "aged_wood_or_warm_wall"}:
        mood.append("quiet_observational")

    return {
        "file": str(path),
        "width": width,
        "height": height,
        "orientation": orientation,
        "average_rgb": avg,
        "dominant_color_family": color,
        "brightness": round(brightness, 2),
        "contrast": round(contrast, 2),
        "mood_signals": mood,
    }


def build_dna(features):
    colors = Counter(f["dominant_color_family"] for f in features)
    orientations = Counter(f["orientation"] for f in features)
    mood = Counter()
    for f in features:
        mood.update(f.get("mood_signals", []))

    total = max(len(features), 1)

    dna = {
        "version": 1,
        "image_count": len(features),
        "dominant_color_families": dict(colors.most_common()),
        "orientation_mix": dict(orientations.most_common()),
        "mood_signal_frequency": dict(mood.most_common()),
        "inferred_artist_dna": {
            "core_subject_likelihoods": [
                "ordinary architecture",
                "plants in urban/domestic spaces",
                "quiet streets and lived-in places",
                "human trace rather than direct portraiture",
                "small businesses and local spaces"
            ],
            "visual_behavior": [
                "quiet observation",
                "soft color restraint",
                "sequence-friendly images",
                "place as emotional subject",
                "low-spectacle documentary attention"
            ],
            "best_project_formats": [
                "photobook",
                "zine",
                "artist book",
                "small press sequence",
                "bookstore/gallery hybrid presentation"
            ],
            "anti_patterns": [
                "spectacle-driven exhibition",
                "generic commercial art market",
                "craft-fair positioning",
                "single-image contest logic unless the image is unusually strong",
                "heavy conceptual overstatement"
            ],
            "recommended_next_projects": [
                "Quiet Neighborhood Memory",
                "Human Trace Study",
                "Small Press City Walk",
                "Quiet Architecture"
            ]
        }
    }

    return dna


def write_report(features, dna):
    lines = [
        "# Artist DNA Report",
        "",
        f"Images analyzed: {dna['image_count']}",
        "",
        "## Dominant Color Families",
        "",
    ]

    for k, v in dna["dominant_color_families"].items():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Orientation Mix", ""]
    for k, v in dna["orientation_mix"].items():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Mood Signals", ""]
    for k, v in dna["mood_signal_frequency"].items():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Inferred Artist DNA", ""]
    inferred = dna["inferred_artist_dna"]

    for section, items in inferred.items():
        lines.append(f"### {section.replace('_', ' ').title()}")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")

    lines += [
        "## How To Use This",
        "",
        "Use `memory/artist_dna.json` as the artist-specific input for recommendation, project, and submission engines.",
        "This file should become more accurate as more images are added to the image folders.",
    ]

    Path(OUT_REPORT).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")


def main():
    images = find_images()

    if not images:
        print("No images found.")
        print("Create one of these folders and add images:")
        for folder in IMAGE_DIRS:
            print("-", folder)
        return

    features = []

    for path in images:
        try:
            features.append(image_features(path))
        except Exception as e:
            print(f"SKIP {path}: {e}")

    Path("analysis").mkdir(exist_ok=True)
    Path("memory").mkdir(exist_ok=True)

    dna = build_dna(features)

    Path(OUT_FEATURES).write_text(json.dumps(features, indent=2, ensure_ascii=False), encoding="utf-8")
    Path(OUT_DNA).write_text(json.dumps(dna, indent=2, ensure_ascii=False), encoding="utf-8")
    write_report(features, dna)

    print(f"Analyzed images: {len(features)}")
    print(f"Wrote {OUT_FEATURES}")
    print(f"Wrote {OUT_DNA}")
    print(f"Wrote {OUT_REPORT}")


if __name__ == "__main__":
    main()
