
import json
import os

OPP_PATH = "deploy_data/compact_opportunities.json"

PERSONALITIES = {
    "quiet_poetic": [
        "quiet",
        "poetic",
        "memory",
        "stillness",
        "daily life",
        "atmospheric",
    ],

    "independent_experimental": [
        "artist-run",
        "collective",
        "alternative",
        "experimental",
        "independent",
    ],

    "publication_ecosystem": [
        "photobook",
        "artist book",
        "publication",
        "small press",
        "zine",
        "printed matter",
    ],

    "institutional_formal": [
        "museum",
        "biennale",
        "institution",
        "academic",
        "archive",
    ],

    "commercial_surface": [
        "brand",
        "marketing",
        "commercial",
        "startup",
        "activation",
    ],
}

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def blob(opp):

    parts = []

    for key in [
        "title",
        "one_sentence",
        "why_this_fits_short",
        "category",
    ]:
        val = opp.get(key)

        if val:
            parts.append(str(val))

    for tag in opp.get(
        "tags",
        []
    ):
        parts.append(str(tag))

    return " ".join(parts).lower()

def personality_scores(text):

    scores = {}

    for name, words in (
        PERSONALITIES.items()
    ):

        hits = sum(
            1 for w in words
            if w in text
        )

        scores[name] = hits

    return scores

def dominant(scores):

    if not scores:
        return "unknown"

    return max(
        scores.items(),
        key=lambda x: x[1]
    )[0]

def main():

    opps = load_json(
        OPP_PATH,
        []
    )

    for opp in opps:

        text = blob(opp)

        scores = personality_scores(
            text
        )

        opp["curator_personality_scores"] = scores

        opp["dominant_curator_personality"] = dominant(
            scores
        )

        if (
            opp["dominant_curator_personality"]
            == "commercial_surface"
        ):
            opp["overall_score"] = max(
                0,
                float(
                    opp.get(
                        "overall_score",
                        0
                    ) or 0
                ) - 1.8
            )

    opps.sort(
        key=lambda x: float(
            x.get("overall_score", 0)
            or 0
        ),
        reverse=True,
    )

    with open(
        OPP_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            opps,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Updated {len(opps)} opportunities with curator personality modeling."
    )

if __name__ == "__main__":
    main()
