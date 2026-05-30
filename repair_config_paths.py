
from pathlib import Path
import shutil
import json

CONFIG_DIR = Path("data/config")

NEEDED_CONFIGS = [
    "source_targets.json",
    "global_photo_source_pack.json",
    "artist_visual_profile_template.json",
    "artist_intelligence_seed_data.json",
    "expanded_visual_source_registry.json",
    "global_opportunity_seeds.json",
    "portfolio_bodies.json",
    "artist_lineage_profiles.json",
]

DEFAULT_SOURCE_TARGETS = {
    "seed_sources": [
        {
            "name": "Tokyo Art Beat",
            "url": "https://www.tokyoartbeat.com/en/events",
            "source_type": "event_listing",
            "region": "Japan",
            "priority": "high"
        },
        {
            "name": "Tokyo Art Book Fair",
            "url": "https://tokyoartbookfair.com/",
            "source_type": "art_book_fair",
            "region": "Japan",
            "priority": "high"
        },
        {
            "name": "Printed Matter",
            "url": "https://www.printedmatter.org/",
            "source_type": "art_book",
            "region": "Global",
            "priority": "high"
        },
        {
            "name": "Self Publish Be Happy",
            "url": "https://selfpublishbehappy.com/",
            "source_type": "photobook",
            "region": "Global",
            "priority": "high"
        }
    ],
    "fit_keywords": [
        "photobook",
        "artist book",
        "zine",
        "printed matter",
        "open call",
        "submission",
        "residency",
        "portfolio review",
        "photography",
        "independent publishing",
        "book fair",
        "small press",
        "exhibition",
        "artist-run",
        "quiet",
        "memory",
        "architecture",
        "place",
        "daily life"
    ],
    "reject_keywords": [
        "crypto",
        "nft",
        "ai art",
        "commercial expo",
        "brand activation",
        "marketing summit"
    ]
}

DEFAULT_GLOBAL_PHOTO_SOURCE_PACK = {
    "sources": [
        "POST",
        "Shashasha",
        "FUGENSHA",
        "Reminders Photography Stronghold",
        "IMA Online",
        "T3 Photo Festival",
        "KYOTOGRAPHIE",
        "MACK",
        "VOID",
        "PhotoBookMuseum",
        "Offprint",
        "PhotoIreland",
        "Unseen",
        "Aperture",
        "Printed Matter",
        "ICP",
        "Center for Photography at Woodstock",
        "Taipei Art Book Fair",
        "Singapore International Photography Festival",
        "Angkor Photo Festival",
        "Jimei x Arles",
        "ArtConnect",
        "CuratorSpace",
        "ArtRabbit",
        "ArtDeadline",
        "Photo Contest Insider"
    ]
}


def write_json(path, data):
    Path(path).write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def copy_back_config(name):
    root_path = Path(name)
    config_path = CONFIG_DIR / name

    if root_path.exists() and root_path.stat().st_size > 5:
        return "exists"

    if config_path.exists() and config_path.stat().st_size > 5:
        shutil.copyfile(config_path, root_path)
        return "copied"

    return "missing"


def main():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    results = {}

    for name in NEEDED_CONFIGS:
        results[name] = copy_back_config(name)

    if results.get("source_targets.json") == "missing":
        write_json("source_targets.json", DEFAULT_SOURCE_TARGETS)
        results["source_targets.json"] = "created default"

    if results.get("global_photo_source_pack.json") == "missing":
        write_json("global_photo_source_pack.json", DEFAULT_GLOBAL_PHOTO_SOURCE_PACK)
        results["global_photo_source_pack.json"] = "created default"

    report_lines = [
        "# Config Path Repair Report",
        "",
    ]

    for name, status in results.items():
        report_lines.append(f"- {name}: {status}")

    Path("reports").mkdir(exist_ok=True)
    Path("reports/config_path_repair_report.md").write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    print("Config path repair complete.")
    for name, status in results.items():
        print(f"{name}: {status}")


if __name__ == "__main__":
    main()
