
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
BODIES_PATH = "portfolio_bodies.json"
OUT_PATH = "memory/portfolio_matches.json"


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


def blob(opp):
    parts = []
    for key in ["title", "category", "category_label", "one_sentence", "why_this_fits_short"]:
        if opp.get(key):
            parts.append(str(opp.get(key)))
    for tag in opp.get("tags", []):
        parts.append(str(tag))
    for bullet in opp.get("three_bullets", []):
        parts.append(str(bullet))
    return " ".join(parts).lower()


def match_body(opp, body):
    text = blob(opp)
    hits = []

    for keyword in body.get("keywords", []):
        if keyword.lower() in text:
            hits.append(keyword)

    score = len(hits)

    # Extra boost if opportunity category matches best format language.
    for fmt in body.get("best_formats", []):
        if fmt.lower() in text:
            score += 1

    return score, hits


def main():
    opps = load_json(OPP_PATH, [])
    bodies = load_json(BODIES_PATH, {}).get("bodies_of_work", [])

    results = {}

    for opp in opps:
        matches = []

        for body in bodies:
            score, hits = match_body(opp, body)

            if score > 0:
                matches.append({
                    "body_id": body["id"],
                    "title": body["title"],
                    "description": body["description"],
                    "score": score,
                    "hits": hits,
                    "best_formats": body.get("best_formats", []),
                })

        matches.sort(key=lambda x: x["score"], reverse=True)

        opp["portfolio_matches"] = matches[:3]

        if matches:
            opp["recommended_body_of_work"] = matches[0]["title"]
            opp["portfolio_match_score"] = matches[0]["score"]
        else:
            opp["recommended_body_of_work"] = "General Portfolio"
            opp["portfolio_match_score"] = 0

        results[title_of(opp)] = matches[:3]

    opps.sort(
        key=lambda x: (
            float(x.get("overall_score", 0) or 0),
            float(x.get("portfolio_match_score", 0) or 0),
        ),
        reverse=True,
    )

    save_json(OPP_PATH, opps)
    save_json(OUT_PATH, results)

    print(f"Matched {len(opps)} opportunities against {len(bodies)} portfolio bodies.")


if __name__ == "__main__":
    main()
