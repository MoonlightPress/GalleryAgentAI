
import json
import os

OPP_PATH = "deploy_data/compact_opportunities.json"
LINEAGE_PATH = "artist_lineage_profiles.json"

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
        "category_label",
    ]:
        val = opp.get(key)
        if val:
            parts.append(str(val))

    for tag in opp.get("tags", []):
        parts.append(str(tag))

    return " ".join(parts).lower()

def score_lineages(text, lineages):

    matched = []
    total = 0

    for lineage in lineages:

        hits = 0

        for signal in lineage["signals"]:
            if signal.lower() in text:
                hits += 1

        if hits >= 2:
            boost = lineage["boost"] * (hits * 0.25)
            total += boost

            matched.append({
                "name": lineage["name"],
                "hits": hits,
                "boost": round(boost, 2),
            })

    return round(total, 2), matched

def negative_penalty(text, negatives):

    penalty = 0

    for signal in negatives:
        if signal.lower() in text:
            penalty += 1.2

    return round(penalty, 2)

def main():

    opps = load_json(OPP_PATH, [])

    lineage_data = load_json(
        LINEAGE_PATH,
        {}
    )

    lineages = lineage_data.get(
        "lineages",
        []
    )

    negatives = lineage_data.get(
        "negative_signals",
        []
    )

    for opp in opps:

        text = blob(opp)

        lineage_score, matches = (
            score_lineages(
                text,
                lineages,
            )
        )

        penalty = negative_penalty(
            text,
            negatives,
        )

        original = float(
            opp.get(
                "overall_score",
                0
            ) or 0
        )

        final = max(
            0,
            min(
                10,
                original
                + lineage_score
                - penalty
            )
        )

        opp["lineage_matches"] = matches
        opp["lineage_score"] = lineage_score
        opp["corporate_penalty"] = penalty
        opp["overall_score"] = round(final, 2)

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
        f"Updated {len(opps)} opportunities with lineage intelligence."
    )

if __name__ == "__main__":
    main()
