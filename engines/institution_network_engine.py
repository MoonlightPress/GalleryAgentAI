
import json
import os
from collections import defaultdict
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/institution_network.json"

SIMILARITY_WORDS = [
    "photobook",
    "artist book",
    "zine",
    "publication",
    "community",
    "artist-run",
    "quiet",
    "atmospheric",
    "documentary",
    "architecture",
    "poetic",
    "book fair",
    "independent",
    "memory",
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

def title_of(opp):
    return opp.get("title") or opp.get("name") or "Unknown"

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

    for tag in opp.get("tags", []):
        parts.append(str(tag))

    return " ".join(parts).lower()

def similarity(a, b):

    score = 0

    for word in SIMILARITY_WORDS:

        aw = word in a
        bw = word in b

        if aw and bw:
            score += 1

    return score

def build_network(opps):

    network = defaultdict(list)

    blobs = {
        title_of(o): blob(o)
        for o in opps
    }

    for opp in opps:

        title = title_of(opp)

        scored = []

        for other in opps:

            other_title = title_of(other)

            if title == other_title:
                continue

            s = similarity(
                blobs[title],
                blobs[other_title],
            )

            if s >= 3:
                scored.append({
                    "title": other_title,
                    "score": s,
                    "country": other.get("country", ""),
                    "category": other.get("category", ""),
                })

        scored.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        network[title] = scored[:12]

    return network

def main():

    opps = load_json(OPP_PATH, [])

    network = build_network(opps)

    save_json(OUT_PATH, network)

    print(
        f"Built institution network for {len(network)} opportunities."
    )

if __name__ == "__main__":
    main()
