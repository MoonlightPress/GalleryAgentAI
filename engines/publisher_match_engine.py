
import json
import os
from pathlib import Path

SEED_PATH = "artist_intelligence_seed_data.json"
PROFILE_PATH = "memory/artist_visual_profile.json"
OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/publisher_matches.json"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def blob(item):
    parts = []
    for key in ["name", "why", "best_use"]:
        if item.get(key):
            parts.append(str(item[key]))
    for tag in item.get("fit_tags", []):
        parts.append(str(tag))
    return " ".join(parts).lower()


def score_publisher(pub, profile, opps):
    text = blob(pub)
    score = 0.0

    for term in profile.get("best_formats", []):
        if term.lower() in text:
            score += 0.7

    for term in profile.get("curatorial_keywords", []):
        if term.lower() in text:
            score += 0.5

    strength = pub.get("match_strength", "")
    if strength == "high":
        score += 2.0
    elif strength == "medium-high":
        score += 1.4
    elif strength == "stretch":
        score += 0.8

    # If this publisher/institution already appears in opportunities, boost it.
    pub_name = pub.get("name", "").lower()
    for opp in opps:
        title = str(opp.get("title") or opp.get("name") or "").lower()
        org = str(opp.get("organization") or "").lower()
        if pub_name and (pub_name in title or pub_name in org):
            score += 1.0
            break

    pub["fit_score"] = round(score, 2)
    return pub


def main():
    seed = load_json(SEED_PATH, {})
    profile = load_json(PROFILE_PATH, {})
    opps = load_json(OPP_PATH, [])

    pubs = [score_publisher(dict(p), profile, opps) for p in seed.get("publisher_matches", [])]
    pubs.sort(key=lambda x: float(x.get("fit_score", 0) or 0), reverse=True)

    save_json(OUT_PATH, pubs)

    print(f"Wrote {OUT_PATH}")
    print(f"Publisher matches: {len(pubs)}")


if __name__ == "__main__":
    main()
