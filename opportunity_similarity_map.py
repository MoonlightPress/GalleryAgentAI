
import json
from pathlib import Path
from collections import defaultdict

MATCHES = "memory/nin_artist_matches.json"
OUT_JSON = "memory/opportunity_similarity_map.json"
OUT_REPORT = "reports/opportunity_similarity_map.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    matches = load(MATCHES, [])
    by_opp = defaultdict(list)

    for m in matches:
        for opp in m.get("source_opportunities", []):
            by_opp[opp].append(m)

    rows = []
    for opp, artists in by_opp.items():
        artists.sort(key=lambda x: x["similarity_score"], reverse=True)
        top = artists[:5]
        avg = round(sum(a["similarity_score"] for a in top) / max(1, len(top)), 1)
        rows.append({
            "title": opp,
            "top_similarity_score": top[0]["similarity_score"] if top else 0,
            "average_top_similarity": avg,
            "similar_artist_count": len([a for a in artists if a["similarity_score"] >= 45]),
            "top_artists": top,
        })

    rows.sort(key=lambda x: (x["top_similarity_score"], x["average_top_similarity"]), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(rows, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Opportunity Similarity Map",
        "",
        "Ranks opportunities by artists in their ecosystem who resemble Nin's current career direction.",
        "",
    ]

    for row in rows:
        lines.append(f"## {row['title']}")
        lines.append(f"- Top similarity: {row['top_similarity_score']}/100")
        lines.append(f"- Average top similarity: {row['average_top_similarity']}/100")
        lines.append(f"- Similar artist count: {row['similar_artist_count']}")
        lines.append("")
        lines.append("### Similar artists")
        for a in row["top_artists"]:
            lines.append(f"- {a['artist_name']} — {a['similarity_score']}/100 — {', '.join(a.get('reasons', []))}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
