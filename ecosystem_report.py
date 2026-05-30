
import json
import os
from pathlib import Path

PEERS_PATH = "memory/peer_artists.json"
PUBLISHERS_PATH = "memory/publisher_matches.json"
BRIDGE_PATH = "memory/ecosystem_opportunity_bridge.json"
OUT_PATH = "reports/ecosystem_report.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def main():
    peers = load_json(PEERS_PATH, [])
    publishers = load_json(PUBLISHERS_PATH, [])
    bridge = load_json(BRIDGE_PATH, [])

    lines = [
        "# Artist Ecosystem Report",
        "",
        "This report tries to answer: who are her people, which publishing ecosystems fit her, and which current opportunities connect to that world.",
        "",
        "## Closest Peer References",
        "",
    ]

    for peer in peers:
        lines.append(f"### {peer.get('name')} — fit {peer.get('fit_score')}")
        lines.append(peer.get("fit_reason", ""))
        lines.append("")
        lines.append(f"- Region: {peer.get('region', '')}")
        lines.append(f"- Shared traits: {', '.join(peer.get('shared_traits', []))}")
        if peer.get("overlap_terms"):
            lines.append(f"- Overlap terms: {', '.join(peer.get('overlap_terms', []))}")
        lines.append(f"- Use as: {peer.get('use_as', '')}")
        lines.append("")

    lines.append("## Publisher / Platform Matches")
    lines.append("")

    for pub in publishers:
        lines.append(f"### {pub.get('name')} — fit {pub.get('fit_score')} — {pub.get('match_strength')}")
        lines.append(pub.get("why", ""))
        lines.append("")
        lines.append(f"- Region: {pub.get('region', '')}")
        lines.append(f"- Best use: {pub.get('best_use', '')}")
        lines.append(f"- Fit tags: {', '.join(pub.get('fit_tags', []))}")
        lines.append("")

    lines.append("## Ecosystem-to-Opportunity Bridge")
    lines.append("")

    for cluster in bridge:
        lines.append(f"### {cluster.get('cluster')}")
        lines.append(cluster.get("why_it_matters", ""))
        lines.append("")

        matches = cluster.get("matched_opportunities", [])
        if not matches:
            lines.append("_No current opportunities connected to this ecosystem yet._")
            lines.append("")
            continue

        for item in matches[:12]:
            lines.append(
                f"- **{item.get('title')}** — score {item.get('score')}, differentiated {item.get('differentiated_score')}; matched: {', '.join(item.get('hit_nodes', []))}"
            )
        lines.append("")

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
