import json
import os
from pathlib import Path
from datetime import date


VENUE_DIR = Path("memory/venues")
OUTPUT_DIR = Path("memory/venue_history")


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def summarize_venue(venue):
    aesthetic = venue.get("known_aesthetic", [])
    mediums = venue.get("typical_mediums", [])
    fit_notes = venue.get("fit_notes", [])

    lines = []

    lines.append(f"Venue type: {venue.get('venue_type')}")

    if aesthetic:
        lines.append(
            "Known aesthetic signals: "
            + ", ".join(aesthetic[:8])
        )

    if mediums:
        lines.append(
            "Typical mediums: "
            + ", ".join(mediums[:8])
        )

    if fit_notes:
        lines.append(
            "Fit notes: "
            + " ".join(fit_notes[:3])
        )

    if not aesthetic and not mediums:
        lines.append(
            "Venue still needs deeper aesthetic research."
        )

    return " ".join(lines)


def build_memory_record(venue):
    return {
        "venue_name": venue.get("venue_name"),
        "venue_slug": venue.get("venue_slug"),
        "memory_version": 1,
        "summary": summarize_venue(venue),
        "last_updated": date.today().isoformat(),
        "confidence": "low" if not venue.get("known_aesthetic") else "medium",
        "future_research": venue.get("missing_information", []),
        "curatorial_direction": [],
        "artist_overlap_signals": [],
        "notes": [],
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    venue_files = list(VENUE_DIR.glob("*.json"))

    for venue_file in venue_files:
        venue = load_json(venue_file, {})

        memory_record = build_memory_record(venue)

        out_path = OUTPUT_DIR / venue_file.name

        save_json(out_path, memory_record)

    print(f"Built {len(venue_files)} venue memory records.")


if __name__ == "__main__":
    main()