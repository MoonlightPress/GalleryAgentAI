
import json
from pathlib import Path

SIM_MAP = "memory/opportunity_similarity_map.json"
PITCHES = "memory/opportunity_pitches.json"
CRED = "memory/validated_opportunity_credibility.json"

OUT_JSON = "memory/nin_opportunity_recommendations.json"
OUT_REPORT = "reports/nin_opportunity_recommendations.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def by_title(rows):
    return {r.get("title"): r for r in rows if r.get("title")}

def main():
    sim_rows = load(SIM_MAP, [])
    pitches = by_title(load(PITCHES, []))
    cred = by_title(load(CRED, []))

    recs = []
    for s in sim_rows:
        title = s["title"]
        p = pitches.get(title, {})
        c = cred.get(title, {})

        recommendation_score = round(
            (s.get("top_similarity_score", 0) * 0.45)
            + (s.get("average_top_similarity", 0) * 0.25)
            + (c.get("credibility_score", 0) * 0.20)
            + ((p.get("pitch_score") or 0) * 1.0),
            1
        )

        recs.append({
            "title": title,
            "recommendation_score": min(100, recommendation_score),
            "top_similarity_score": s.get("top_similarity_score"),
            "average_top_similarity": s.get("average_top_similarity"),
            "similar_artist_count": s.get("similar_artist_count"),
            "credibility_score": c.get("credibility_score"),
            "pitch_score": p.get("pitch_score"),
            "recommended_url": p.get("recommended_url"),
            "fit_summary": p.get("fit_paragraph"),
            "top_artists": s.get("top_artists", []),
        })

    recs.sort(key=lambda x: x["recommendation_score"], reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(recs, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Nin Opportunity Recommendations",
        "",
        "Ranks opportunities by similarity evidence, credibility, and existing fit score.",
        "",
    ]

    for r in recs:
        label = "priority" if r["recommendation_score"] >= 70 else "watchlist" if r["recommendation_score"] >= 45 else "low priority"
        lines.append(f"## {r['title']}")
        lines.append(f"- Recommendation: {r['recommendation_score']}/100 ({label})")
        lines.append(f"- Top artist similarity: {r.get('top_similarity_score')}/100")
        lines.append(f"- Similar artist count: {r.get('similar_artist_count')}")
        lines.append(f"- Credibility: {r.get('credibility_score')}")
        lines.append(f"- Link: {r.get('recommended_url')}")
        lines.append("")
        lines.append("### Why this is relevant")
        lines.append(r.get("fit_summary") or "No fit summary available.")
        lines.append("")
        lines.append("### Similar artists found")
        for a in r.get("top_artists", [])[:5]:
            lines.append(f"- {a['artist_name']} — {a['similarity_score']}/100 — {', '.join(a.get('reasons', []))}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
