
import json
import os
from pathlib import Path

BUCKET_PATH = "memory/opportunity_buckets.json"
OUT_PATH = "reports/career_bucket_report.md"

LABELS = {
    "career_changing": "Career-Changing Targets",
    "high_confidence": "High-Confidence Matches",
    "publication_targets": "Publication Targets",
    "book_zine_targets": "Book / Zine / Photobook Targets",
    "global_reach": "Global Reach",
    "easy_wins": "Easy Wins",
    "relationship_builders": "Relationship Builders",
    "needs_research": "Needs Research",
    "low_priority": "Low Priority",
}

DESCRIPTIONS = {
    "career_changing": "High-upside opportunities that could meaningfully change her reputation, network, or publication history.",
    "high_confidence": "Strong matches with better verification.",
    "publication_targets": "Places where the work can become visible as printed matter, editorial sequence, or publication history.",
    "book_zine_targets": "The strongest match for her current visual language: quiet sequences, small press, books, zines, and artist-book contexts.",
    "global_reach": "International opportunities that expand beyond local Tokyo/Japan visibility.",
    "easy_wins": "Lower-friction opportunities that may create momentum without heavy emotional or application burden.",
    "relationship_builders": "Local or community spaces useful for soft contact, small steps, and future familiarity.",
    "needs_research": "Potentially useful, but not actionable until submission details, fee, deadline, or contact are verified.",
    "low_priority": "Weak fit or low evidence. Keep but do not foreground.",
}


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def item_line(item):
    title = item.get("title", "Unknown")
    score = item.get("score", "?")
    dscore = item.get("differentiated_score", "?")
    visual = item.get("visual_fit_score", "?")
    why = item.get("why", "")

    return f"- **{title}** — score {score}, differentiated {dscore}, visual fit {visual}. {why}"


def main():
    buckets = load_json(BUCKET_PATH, {})

    lines = [
        "# Career Bucket Report",
        "",
        "This report separates opportunities by strategic role instead of forcing everything into one flat ranking.",
        "",
    ]

    for key, label in LABELS.items():
        items = buckets.get(key, [])

        lines.append(f"## {label}")
        lines.append("")
        lines.append(DESCRIPTIONS.get(key, ""))
        lines.append("")

        if not items:
            lines.append("_No items in this bucket yet._")
            lines.append("")
            continue

        for item in items[:15]:
            lines.append(item_line(item))

            hits = item.get("visual_hits", [])
            if hits:
                lines.append(f"  - Visual match signals: {', '.join(hits[:8])}")

        lines.append("")

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
