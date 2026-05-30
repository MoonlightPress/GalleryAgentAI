
import json
import os
from pathlib import Path

BUCKET_PATH = "memory/exclusive_strategy_buckets.json"
OUT_PATH = "reports/strategic_action_report.md"

ORDER = [
    ("immediate_best_moves", "Immediate Best Moves"),
    ("publication_targets", "Publication Targets"),
    ("japan_book_ecosystem", "Japan Book / Zine Ecosystem"),
    ("stretch_targets", "Stretch Targets"),
    ("relationship_builders", "Relationship Builders"),
    ("research_needed", "Needs Research"),
    ("low_priority", "Low Priority"),
]

DESCRIPTIONS = {
    "immediate_best_moves": "Best current options: good fit, useful direction, and worth acting on first.",
    "publication_targets": "Strong places to research if the work becomes a sequence, zine, or photobook.",
    "japan_book_ecosystem": "Local book/zine/art-book spaces that fit her visual language and are plausible relationship targets.",
    "stretch_targets": "Prestige or difficult targets. Useful as benchmarks even if not immediate.",
    "relationship_builders": "Lower-pressure spaces useful for familiarity, soft outreach, or small first steps.",
    "research_needed": "Do not recommend yet. These need submission/contact/deadline verification.",
    "low_priority": "Keep out of the main UI unless specifically requested.",
}


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def line(item, rank):
    title = item.get("title", "Unknown")
    score = item.get("score", "?")
    visual = item.get("visual_fit_score", "?")
    verify = item.get("verification_bucket", "")
    why = item.get("why", "")

    return f"{rank}. **{title}** — score {score}, visual {visual}, verification {verify}. {why}"


def main():
    buckets = load_json(BUCKET_PATH, {})

    lines = [
        "# Strategic Action Report",
        "",
        "This is the cleaner action report: each opportunity appears in one primary role instead of repeating across every category.",
        "",
    ]

    for key, label in ORDER:
        items = buckets.get(key, [])
        visible = [
            item for item in items
            if "facebook" not in item.get("title", "").lower()
            and "instagram" not in item.get("title", "").lower()
            and "pinterest" not in item.get("title", "").lower()
            and "continue reading" not in item.get("title", "").lower()
        ]

        lines.append(f"## {label}")
        lines.append("")
        lines.append(DESCRIPTIONS.get(key, ""))
        lines.append("")

        if not visible:
            lines.append("_No items._")
            lines.append("")
            continue

        for i, item in enumerate(visible[:8], start=1):
            lines.append(line(item, i))

        lines.append("")

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
