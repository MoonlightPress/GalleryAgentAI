
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

    stretch_names = [
        "aperture",
        "mack",
        "photographers' gallery",
        "photovogue",
        "portfolio prize",
        "void",
    ]

    publication_terms = [
        "photobook",
        "photo book",
        "artist book",
        "printed matter",
        "publication",
        "small press",
        "self publish",
        "offprint",
    ]

    japan_book_terms = [
        "utrecht",
        "mount zine",
        "flotsam",
        "post",
        "nadiff",
        "tokyo art book fair",
        "book and sons",
        "shashasha",
        "fugensha",
        "akaaka",
        "t&m",
    ]

    relationship_terms = [
        "cafe",
        "bookstore",
        "shimokitazawa",
        "bonus track",
        "photobook cafe",
        "gallery wall",
        "community",
    ]

    if has(title, stretch_names):
        return "stretch_targets"

    if has(text, ["tokyo art book fair"]) or (visual >= 5 and has(text, publication_terms)):
        return "immediate_best_moves"

    if has(text, japan_book_terms):
        return "japan_book_ecosystem"

    if has(text, publication_terms):
        return "publication_targets"

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
