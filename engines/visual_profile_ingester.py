
import json
import os
from pathlib import Path

PROFILE_PATH = "artist_visual_profile_template.json"
MASTER_PATH = "memory/artist_master_profile.json"
OUT_REPORT = "reports/artist_visual_profile_report.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    visual = load_json(PROFILE_PATH, {})
    master = load_json(MASTER_PATH, {})

    if not visual.get("summary"):
        print("artist_visual_profile_template.json is still blank. Fill it after image analysis.")
        return

    master["visual_profile"] = visual

    # Merge useful fields into existing profile.
    for key in ["emotional_tone", "curatorial_keywords", "best_formats"]:
        values = visual.get(key, [])
        if values:
            master_key = {
                "emotional_tone": "visual_language",
                "curatorial_keywords": "core_themes",
                "best_formats": "ideal_opportunity_types"
            }.get(key, key)

            existing = master.get(master_key, [])
            merged = list(dict.fromkeys(existing + values))
            master[master_key] = merged

    save_json(MASTER_PATH, master)

    lines = [
        "# Artist Visual Profile",
        "",
        visual.get("summary", ""),
        "",
        "## Curatorial Keywords",
        "",
    ]

    for item in visual.get("curatorial_keywords", []):
        lines.append(f"- {item}")

    lines += ["", "## Best Formats", ""]

    for item in visual.get("best_formats", []):
        lines.append(f"- {item}")

    Path(OUT_REPORT).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print(f"Updated {MASTER_PATH}")
    print(f"Wrote {OUT_REPORT}")


if __name__ == "__main__":
    main()
