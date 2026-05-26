import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import os


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def build_compact_view(opportunity):
    council = opportunity.get("council_review", {})
    compact = council.get("compact_card", {})
    scores = council.get("council_scores", {})
    packet = opportunity.get("submission_packet", {})

    requirements = (
        packet.get("submission_requirements", {})
    )

    return {
    "title":
        opportunity.get("name")
        or opportunity.get("title")
        or opportunity.get("opportunity_name")
        or "Unknown",

    "category":
        opportunity.get("type")
        or opportunity.get("category")
        or opportunity.get("opportunity_type")
        or "unknown",

    "city":
        opportunity.get("city")
        or opportunity.get("location")
        or "",

    "priority":
        opportunity.get("priority", "C"),

    "overall_score":
        council.get("overall_score", 0),

    "difficulty":
        council.get("difficulty", "unknown"),

    "recommendation_strength":
        council.get("recommendation_strength", ""),

    "one_sentence":
        compact.get("one_sentence", ""),

    "three_bullets":
        compact.get("three_bullets", [])[:5],   

    "quick_action":
        compact.get("quick_action", ""),

    "why_this_fits_short":
        compact.get("why_this_fits_short", ""),

    "deadline":
        requirements.get("deadline", "Unknown"),

    "fees":
        requirements.get("fees", "Unknown"),

    "predatory_risk":
        scores.get("predatory_risk", 0),

    "emotional_fit":
        scores.get("emotional_fit", 0),

    "submission_score":
        scores.get("submission_score", 0),

        "official_website":
    opportunity.get("official_website", ""),

"submission_page":
    opportunity.get("submission_page", ""),

"source_url":
    opportunity.get("source_url", ""),

"organization":
    opportunity.get("organization", ""),

    "tags": [
        opportunity.get("visibility", ""),
        opportunity.get("recommendation_tier", ""),
        council.get("difficulty", "")
    ]
}


def main():
    opportunities = load_json(
        "memory/opportunities.json",
        []
    )

    compact_views = []

    print()
    print("Building compact views...")
    print()

    for opp in opportunities:
        compact_views.append(
            build_compact_view(opp)
        )

    save_json(
        "memory/compact_opportunities.json",
        compact_views
    )

    print("Saved memory/compact_opportunities.json")
    print()


if __name__ == "__main__":
    main()