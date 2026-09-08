import json
import os
import re
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


# Words that overlap between any two art descriptions and so carry no signal.
_STOP = {
    "and", "the", "of", "a", "an", "in", "on", "as", "to", "with", "through",
    "for", "from", "by", "that", "its", "it", "or", "at", "into", "across",
    "work", "works", "practice", "based", "career", "artist", "art",
}


def _tokens(phrase):
    """Lowercase content words in a free-text trait phrase."""
    return {w for w in re.findall(r"[a-z]+", str(phrase).lower()) if w not in _STOP}


def score_peer(peer, profile):
    """Score a peer by vocabulary overlap with her visual profile.

    Compares at WORD level, not whole-phrase level. The original did
    ``set(profile_terms) & set(peer_terms)`` on entire free-text phrases —
    "atmospheric watercolor" against "atmospheric painting" — which can only
    match on an exact string. The two vocabularies were authored separately and
    never once collided, so every peer scored 0.0, the sort was a no-op, and the
    order she saw was just the order of the seed file. The bonus terms could not
    fire either: they tested for a trait of exactly "architecture", while the
    real trait reads "architecture and urban environments".
    """
    profile_phrases = []
    for key in ("curatorial_keywords", "emotional_tone", "recurring_motifs"):
        profile_phrases.extend(profile.get(key, []) or [])
    profile_words = set()
    for phrase in profile_phrases:
        profile_words |= _tokens(phrase)

    peer_phrases = peer.get("shared_traits", []) or []
    peer_words = set()
    for phrase in peer_phrases:
        peer_words |= _tokens(phrase)

    overlap = profile_words & peer_words
    score = len(overlap) * 1.2

    # Subject bonuses, matched against the peer's trait TEXT so a multi-word
    # trait still counts.
    blob = " ".join(peer_phrases).lower()
    if "photobook" in blob:
        score += 1.0
    if "memory" in blob:
        score += 0.8
    if "daily life" in blob:
        score += 0.8
    if "architecture" in blob or "urban vernacular" in blob:
        score += 0.7

    peer["fit_score"] = round(score, 2)
    peer["overlap_terms"] = sorted(overlap)

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
