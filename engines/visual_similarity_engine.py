
import json
import os
from pathlib import Path

PROFILE_PATH = "memory/visual_language_profile.json"
OPP_PATH = "deploy_data/compact_opportunities.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def blob(opp):

    parts = []

    for key in [
        "title",
        "category",
        "one_sentence",
        "why_this_fits_short",
    ]:

        if opp.get(key):
            parts.append(str(opp.get(key)))

    for tag in opp.get("tags", []):
        parts.append(str(tag))

    return " ".join(parts).lower()

def score_similarity(opp, visual):

    text = blob(opp)

    score = 0
    hits = []

    for group in [
        "visual_language",
        "recurring_subjects",
        "emotional_register",
    ]:

        for term in visual.get(group, []):

            t = str(term).lower()

            if t and t in text:
                score += 1
                hits.append(term)

    return score, hits

def main():

    visual = load_json(
        PROFILE_PATH,
        {}
    )

    opps = load_json(
        OPP_PATH,
        []
    )

    for opp in opps:

        score, hits = score_similarity(
            opp,
            visual
        )

        opp["visual_similarity_score"] = score
        opp["visual_similarity_hits"] = hits

        opp["overall_score"] = min(
            9.5,
            float(
                opp.get(
                    "overall_score",
                    0
                ) or 0
            ) + (score * 0.22)
        )

    opps.sort(
        key=lambda x: float(
            x.get(
                "overall_score",
                0
            ) or 0
        ),
        reverse=True,
    )

    save_json(
        OPP_PATH,
        opps
    )

    print(
        f"Updated {len(opps)} opportunities with visual similarity."
    )

if __name__ == "__main__":
    main()
