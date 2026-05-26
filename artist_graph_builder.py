import json
import os


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


career = load_json(
    "memory/career_reconstruction.json",
    {}
)

graph = {
    "nodes": [],
    "edges": []
}


def add_node(node_type, name):
    graph["nodes"].append({
        "type": node_type,
        "name": name
    })


def add_edge(source, target, relation):
    graph["edges"].append({
        "source": source,
        "target": target,
        "relation": relation
    })


eco = career.get("ecosystem_map", {})

for city in eco.get("cities", []):
    add_node("city", city)

for space in eco.get("spaces", []):
    add_node("space", space)

for pub in eco.get("publishers", []):
    add_node("publisher", pub)

for artist in eco.get("peer_artists", []):
    add_node("artist", artist)

for cluster in eco.get("community_clusters", []):
    add_node("cluster", cluster)

for cluster in eco.get("community_clusters", []):
    for city in eco.get("cities", []):
        add_edge(cluster, city, "exists_in")

for pub in eco.get("publishers", []):
    for cluster in eco.get("community_clusters", []):
        add_edge(pub, cluster, "participates_in")

save_json(
    "memory/artist_ecosystem_graph.json",
    graph
)

print("Saved memory/artist_ecosystem_graph.json")