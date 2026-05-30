
import json
import os
from pathlib import Path

SEED_PATH = "artist_intelligence_seed_data.json"
PROFILE_PATH = "memory/artist_visual_profile.json"
OUT_PATH = "memory/ecosystem_graph.json"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    seed = load_json(SEED_PATH, {})
    profile = load_json(PROFILE_PATH, {})

    graph = {
        "artist_profile_summary": profile.get("summary", ""),
        "core_visual_terms": profile.get("curatorial_keywords", []),
        "ecosystem_nodes": seed.get("ecosystem_nodes", []),
        "peer_artists": seed.get("peer_artists", []),
        "publisher_matches": seed.get("publisher_matches", []),
    }

    save_json(OUT_PATH, graph)

    print(f"Wrote {OUT_PATH}")
    print(f"Clusters: {len(graph['ecosystem_nodes'])}")


if __name__ == "__main__":
    main()
