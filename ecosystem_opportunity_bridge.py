
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
GRAPH_PATH = "memory/ecosystem_graph.json"
OUT_PATH = "memory/ecosystem_opportunity_bridge.json"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def opp_text(opp):
    parts = []
    for key in ["title", "name", "organization", "category", "why_this_fits_short", "one_sentence"]:
        if opp.get(key):
            parts.append(str(opp[key]))
    return " ".join(parts).lower()


def main():
    opps = load_json(OPP_PATH, [])
    graph = load_json(GRAPH_PATH, {})

    bridge = []

    for cluster in graph.get("ecosystem_nodes", []):
        cluster_name = cluster.get("cluster", "")
        nodes = cluster.get("nodes", [])

        matches = []

        for opp in opps:
            text = opp_text(opp)
            hit_nodes = []

            for node in nodes:
                if node.lower() in text:
                    hit_nodes.append(node)

            if hit_nodes:
                matches.append({
                    "title": opp.get("title") or opp.get("name") or "Unknown",
                    "score": opp.get("overall_score"),
                    "differentiated_score": opp.get("differentiated_score"),
                    "hit_nodes": hit_nodes,
                    "why": opp.get("why_this_fits_short") or opp.get("one_sentence") or ""
                })

        matches.sort(key=lambda x: float(x.get("differentiated_score", x.get("score", 0)) or 0), reverse=True)

        bridge.append({
            "cluster": cluster_name,
            "why_it_matters": cluster.get("why_it_matters", ""),
            "matched_opportunities": matches,
        })

    save_json(OUT_PATH, bridge)

    print(f"Wrote {OUT_PATH}")
    print(f"Clusters bridged: {len(bridge)}")


if __name__ == "__main__":
    main()
