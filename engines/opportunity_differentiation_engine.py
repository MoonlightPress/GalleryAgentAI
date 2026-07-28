
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
PROFILE_PATH = "memory/artist_visual_profile.json"
OUT_PATH = "memory/opportunity_buckets.json"

BUCKETS = [
    "career_changing",
    "high_confidence",
    "publication_targets",
    "book_zine_targets",
    "global_reach",
    "easy_wins",
    "relationship_builders",
    "needs_research",
    "low_priority",
]


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def num(value):
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def blob(opp):
    parts = []
    for key in [
        "title",
        "organization",
        "category",
        "category_label",
        "one_sentence",
        "why_this_fits_short",
        "submission_strategy",
        "recommended_body_of_work",
    ]:
        if opp.get(key):
            parts.append(str(opp[key]))

    for key in ["tags", "three_bullets", "fit_keyword_hits"]:
        for x in opp.get(key, []) or []:
            parts.append(str(x))

    return " ".join(parts).lower()


def has_any(text, terms):
    return any(t.lower() in text for t in terms)


def verification_score(opp):
    # Each concept checks BOTH spellings of its split-field pair. rumor_mill
    # writes `submission_url` and `fee`; older engines wrote `submission_page`
    # and `fees`. Counting only one side meant an item rumor_mill had fully
    # answered still scored <= 2 and was refiled into needs_research on the
    # next pass — the root cause of the ever-growing research backlog
    # (714 items by 2026-07-28).
    score = 0
    if opp.get("url_verification_status") == "ok":
        score += 2
    if opp.get("submission_page") or opp.get("submission_url"):
        score += 2
    if opp.get("deadline"):
        score += 1
    if opp.get("fees") or opp.get("fee"):
        score += 1
    if opp.get("contact") or opp.get("email") or opp.get("contact_url") or opp.get("contact_email"):
        score += 1
    return score


def visual_fit_score(opp, profile):
    text = blob(opp)
    keywords = profile.get("curatorial_keywords", [])
    best_formats = profile.get("best_formats", [])
    bad_fits = profile.get("bad_fit_contexts", [])
    weights = profile.get("opportunity_weighting", {})

    score = 0.0
    hits = []

    for term in keywords + best_formats:
        if term.lower() in text:
            score += 0.45
            hits.append(term)

    for key, weight in weights.items():
        key_text = key.replace("_", " ").lower()
        if key_text in text or key.lower() in text:
            score += float(weight)
            hits.append(key)

    for term in bad_fits:
        if term.lower() in text:
            score -= 1.25
            hits.append("bad_fit:" + term)

    return round(score, 2), hits[:12]


def assign_buckets(opp, profile):
    text = blob(opp)
    overall = num(opp.get("overall_score"))
    prestige = num(opp.get("prestige_score"))
    difficulty = num(opp.get("difficulty_score"))
    verify = verification_score(opp)
    visual_score, hits = visual_fit_score(opp, profile)

    buckets = []

    publication_terms = [
        "photobook",
        "artist book",
        "zine",
        "printed matter",
        "publication",
        "small press",
        "book fair",
    ]

    global_terms = [
        "global",
        "international",
        "london",
        "new york",
        "paris",
        "online",
        "uk",
        "usa",
        "germany",
        "france",
    ]

    local_easy_terms = [
        "cafe",
        "bookstore",
        "wall",
        "market",
        "popup",
        "community",
    ]

    if prestige >= 8 or has_any(text, ["aperture", "printed matter", "photovogue", "tokyo art book fair"]):
        buckets.append("career_changing")

    if overall >= 8 and verify >= 3:
        buckets.append("high_confidence")

    if has_any(text, publication_terms):
        buckets.append("publication_targets")

    if has_any(text, ["photobook", "artist book", "zine", "bookstore", "small press"]):
        buckets.append("book_zine_targets")

    country = str(opp.get("country", "")).lower()
    if country not in {"", "japan"} or has_any(text, global_terms):
        buckets.append("global_reach")

    if difficulty <= 5 and overall >= 7:
        buckets.append("easy_wins")

    if has_any(text, local_easy_terms):
        buckets.append("relationship_builders")

    if verify <= 2 or opp.get("manual_review_needed"):
        buckets.append("needs_research")

    if overall < 6 or visual_score < -0.5:
        buckets.append("low_priority")

    if not buckets:
        buckets.append("needs_research")

    opp["visual_fit_score"] = visual_score
    opp["visual_fit_hits"] = hits
    opp["career_buckets"] = buckets
    opp["primary_bucket"] = buckets[0]

    # A differentiated score that avoids endless 9.4 ties.
    opp["differentiated_score"] = round(
        overall
        + min(1.4, visual_score * 0.35)
        + min(0.8, prestige * 0.05)
        + min(0.7, verify * 0.12)
        - max(0, difficulty - 7) * 0.12,
        2,
    )

    return buckets


def compact_item(opp):
    return {
        "title": opp.get("title") or opp.get("name") or "Unknown",
        "score": opp.get("overall_score"),
        "differentiated_score": opp.get("differentiated_score"),
        "visual_fit_score": opp.get("visual_fit_score"),
        "verification": opp.get("verification_status", ""),
        "url_status": opp.get("url_verification_status", ""),
        "category": opp.get("category", ""),
        "country": opp.get("country", ""),
        "why": opp.get("why_this_fits_short") or opp.get("one_sentence") or "",
        "visual_hits": opp.get("visual_fit_hits", []),
        "source": (
            opp.get("source_url")
            or opp.get("source_link")
            or opp.get("official_website")
            or opp.get("submission_page")
            or ""
        ),
    }


def main():
    opps = load_json(OPP_PATH, [])
    profile = load_json(PROFILE_PATH, {})

    if not profile:
        print("No visual profile found. Run artist_visual_profile_v1.py first.")
        profile = {}

    buckets = {name: [] for name in BUCKETS}

    for opp in opps:
        assigned = assign_buckets(opp, profile)
        for bucket in assigned:
            buckets.setdefault(bucket, []).append(compact_item(opp))

    for bucket, items in buckets.items():
        items.sort(
            key=lambda x: float(x.get("differentiated_score", 0) or 0),
            reverse=True,
        )

    opps.sort(
        key=lambda x: float(x.get("differentiated_score", x.get("overall_score", 0)) or 0),
        reverse=True,
    )

    save_json(OPP_PATH, opps)
    save_json(OUT_PATH, buckets)

    print("Built differentiated opportunity buckets:")
    for bucket, items in buckets.items():
        print(f"{bucket}: {len(items)}")


if __name__ == "__main__":
    main()
