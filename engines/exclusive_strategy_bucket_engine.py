
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/exclusive_strategy_buckets.json"

BUCKET_ORDER = [
    "immediate_best_moves",
    "publication_targets",
    "japan_book_ecosystem",
    "stretch_targets",
    "relationship_builders",
    "research_needed",
    "low_priority",
    "reject",
]

LABELS = {
    "immediate_best_moves": "Immediate Best Moves",
    "publication_targets": "Publication Targets",
    "japan_book_ecosystem": "Japan Book / Zine Ecosystem",
    "stretch_targets": "Stretch Targets",
    "relationship_builders": "Relationship Builders",
    "research_needed": "Needs Research",
    "low_priority": "Low Priority",
    "reject": "Reject / Hide",
}


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def text_blob(opp):
    parts = []
    for key in [
        "title",
        "name",
        "organization",
        "category",
        "category_label",
        "one_sentence",
        "why_this_fits_short",
    ]:
        if opp.get(key):
            parts.append(str(opp[key]))

    for key in ["tags", "visual_fit_hits", "fit_keyword_hits"]:
        for item in opp.get(key, []) or []:
            parts.append(str(item))

    return " ".join(parts).lower()


def num(value):
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def has(text, terms):
    return any(t in text for t in terms)


def choose_bucket(opp):
    text = text_blob(opp)
    title = str(opp.get("title") or opp.get("name") or "").lower()

    score = num(opp.get("overall_score"))
    dscore = num(opp.get("differentiated_score"))
    visual = num(opp.get("visual_fit_score"))

    if opp.get("recommendation_visibility") == "hidden":
        return "reject"

    if opp.get("verification_bucket") == "reject":
        return "reject"

    if score <= 4 or dscore <= 4:
        return "low_priority"

    if has(title, ["facebook", "instagram", "pinterest", "tiktok", "continue reading"]):
        return "reject"

    # Tier 4 — Prestige Targets: always stretch_targets, never immediate_best_moves.
    # These are future goals for the deep-work year at ~30, not current actions.
    tier_4_terms = [
        "royal watercolour society",
        "american watercolor society",
        "cité internationale des arts",
        "cite internationale des arts",
        "asian cultural council",
        "printed matter art book fairs",
        "center for book arts",
        "offprint",
        "aperture",
        "mack",
    ]

    # Tier 1 — Ambient Visibility: zine/bookshop ecosystem, art book fairs.
    # Weight higher for current phase. Route to immediate or japan_book_ecosystem.
    tier_1_terms = [
        "tokyo art book fair",
        "mount zine",
        "utrecht",
        "book and sons",
        "flotsam",
        "b&b shimokitazawa",
        "bookandbeer",
        "nadiff",
        "shashasha",
        "torch press",
        "zine fest",
        "zine fair",
        "fugensha",
        "akaaka",
    ]

    # Tier 1-2 publication / artist-book terms
    publication_terms = [
        "artist book",
        "printed matter",
        "publication",
        "small press",
        "self publish",
        "zine",
    ]

    # Tier 2 — Networking: artist-run spaces and relationship venues
    relationship_terms = [
        "cafe",
        "bookstore",
        "shimokitazawa",
        "bonus track",
        "gallery wall",
        "community",
        "artist-run",
    ]

    # Tier 4 check is first — prestige targets never reach immediate_best_moves
    if has(text, tier_4_terms):
        return "stretch_targets"

    # Tier 1 ambient visibility — immediate or japan book ecosystem
    if has(text, tier_1_terms):
        if visual >= 3 or score >= 7.5:
            return "immediate_best_moves"
        return "japan_book_ecosystem"

    # High visual fit + publication angle → immediate
    if visual >= 5 and has(text, publication_terms):
        return "immediate_best_moves"

    # Tier 1-2 publication targets
    if has(text, publication_terms):
        return "publication_targets"

    # Tier 2 relationship / networking venues
    if has(text, relationship_terms):
        return "relationship_builders"

    if opp.get("verification_bucket") in {"research_needed", None}:
        return "research_needed"

    if score >= 8 and visual >= 1:
        return "immediate_best_moves"

    return "research_needed"


def compact(opp):
    return {
        "title": opp.get("title") or opp.get("name") or "Unknown",
        "score": opp.get("overall_score"),
        "differentiated_score": opp.get("differentiated_score"),
        "visual_fit_score": opp.get("visual_fit_score"),
        "verification_bucket": opp.get("verification_bucket", ""),
        "verification_score": opp.get("verification_score", ""),
        "why": opp.get("why_this_fits_short") or opp.get("one_sentence") or "",
        "source": (
            opp.get("source_url")
            or opp.get("official_website")
            or opp.get("source_link")
            or opp.get("submission_page")
            or ""
        ),
        "visual_hits": opp.get("visual_fit_hits", []) or [],
        "opportunity_type": opp.get("opportunity_type", "open_call"),
        "action_type": opp.get("action_type", "apply"),
        "relationship_note": opp.get("relationship_note", ""),
        "draft_introduction_ja": opp.get("draft_introduction_ja", ""),
    }


def main():
    opps = load_json(OPP_PATH, [])

    buckets = {key: [] for key in BUCKET_ORDER}

    for opp in opps:
        bucket = choose_bucket(opp)
        opp["exclusive_primary_bucket"] = bucket
        buckets.setdefault(bucket, []).append(compact(opp))

    for key in buckets:
        buckets[key].sort(
            key=lambda x: float(x.get("differentiated_score", x.get("score", 0)) or 0),
            reverse=True,
        )

    save_json(OPP_PATH, opps)
    save_json(OUT_PATH, buckets)

    print("Built exclusive strategic buckets:")
    for key in BUCKET_ORDER:
        print(f"{LABELS[key]}: {len(buckets.get(key, []))}")


if __name__ == "__main__":
    main()
