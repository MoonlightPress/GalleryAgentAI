
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
STRATEGY_PATH = "memory/strategy_feed.json"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def title_of(opp):
    return opp.get("title") or opp.get("name") or "Unknown"


def is_global(opp):
    country = str(opp.get("country") or "").lower()
    tags = [str(t).lower() for t in opp.get("tags", [])]
    category = str(opp.get("category") or "").lower()
    return (
        country not in {"", "japan"}
        or "global" in tags
        or category.startswith("global_")
        or opp.get("source_type") == "global_seed"
    )


def item_from_opp(opp, bucket):
    return {
        "title": title_of(opp),
        "bucket": bucket,
        "score": opp.get("overall_score"),
        "confidence": opp.get("confidence_level", "medium"),
        "reason": strategic_reason(opp, bucket),
        "category": opp.get("category_label") or opp.get("category"),
        "city": opp.get("city"),
        "country": opp.get("country", ""),
        "image": opp.get("card_image", ""),
    }


def strategic_reason(opp, bucket):
    if bucket == "global_targets":
        return "International opportunity that may expand visibility beyond local Tokyo/Japan options."
    if bucket == "publication_targets":
        return "Useful for photobook, zine, artist-book, or publication history."
    if bucket == "career_changing":
        return "Higher-prestige opportunity with stronger long-term career signaling."
    return opp.get("why_this_fits_short") or opp.get("one_sentence") or "Potentially useful depending on current goals."


def build_global_sections():
    opps = load_json(OPP_PATH, [])
    feed = load_json(STRATEGY_PATH, {})

    global_targets = []
    publication_targets = []
    career_changing = feed.get("career_changing", [])

    sorted_opps = sorted(opps, key=lambda x: float(x.get("overall_score", 0) or 0), reverse=True)

    for opp in sorted_opps:
        category = str(opp.get("category") or "").lower()
        tags = [str(t).lower() for t in opp.get("tags", [])]

        if is_global(opp) and len(global_targets) < 18:
            global_targets.append(item_from_opp(opp, "global_targets"))

        if (
            any(t in tags for t in ["photobook", "publication", "artist_book", "zine"])
            or any(word in category for word in ["book", "zine", "publication", "photo"])
        ) and len(publication_targets) < 18:
            publication_targets.append(item_from_opp(opp, "publication_targets"))

        prestige = float(opp.get("prestige_score", 0) or 0)
        score = float(opp.get("overall_score", 0) or 0)
        if prestige >= 8 and score >= 7:
            title = title_of(opp)
            if title not in {x.get("title") for x in career_changing}:
                career_changing.append(item_from_opp(opp, "career_changing"))

    feed["global_targets"] = global_targets
    feed["publication_targets"] = publication_targets
    feed["career_changing"] = career_changing[:18]

    save_json(STRATEGY_PATH, feed)

    print(f"Global targets: {len(global_targets)}")
    print(f"Publication targets: {len(publication_targets)}")
    print(f"Career-changing: {len(feed['career_changing'])}")


if __name__ == "__main__":
    build_global_sections()
