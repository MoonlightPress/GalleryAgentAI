
import json
import os
from pathlib import Path

SEED_PATH = "artist_intelligence_seed_data.json"
PROFILE_PATH = "memory/artist_visual_profile.json"
OUT_PATH = "memory/peer_artists.json"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def score_peer(peer, profile):
    profile_terms = set([x.lower() for x in profile.get("curatorial_keywords", [])])
    profile_terms.update([x.lower() for x in profile.get("emotional_tone", [])])
    profile_terms.update([x.lower() for x in profile.get("recurring_motifs", [])])

    peer_terms = set([x.lower() for x in peer.get("shared_traits", [])])

    overlap = profile_terms.intersection(peer_terms)

    score = len(overlap) * 1.2

    if "photobook" in peer_terms:
        score += 1.0
    if "memory" in peer_terms:
        score += 0.8
    if "daily life" in peer_terms:
        score += 0.8
    if "architecture" in peer_terms or "urban vernacular" in peer_terms:
        score += 0.7

    peer["fit_score"] = round(score, 2)
    peer["overlap_terms"] = sorted(list(overlap))

    return peer


def main():
    seed = load_json(SEED_PATH, {})
    profile = load_json(PROFILE_PATH, {})

    peers = [score_peer(dict(p), profile) for p in seed.get("peer_artists", [])]
    peers.sort(key=lambda x: float(x.get("fit_score", 0) or 0), reverse=True)

    save_json(OUT_PATH, peers)

    print(f"Wrote {OUT_PATH}")
    print(f"Peer artists: {len(peers)}")


if __name__ == "__main__":
    main()
