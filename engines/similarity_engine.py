
import json
from pathlib import Path

INPUT="memory/historical_artist_data.json"
OUT="memory/opportunity_similarity.json"
REPORT="reports/opportunity_similarity.md"

rows=json.load(open(INPUT,encoding="utf-8")) if Path(INPUT).exists() else []

results=[]
for r in rows:
    sims=[]
    for a in r.get("historical_artists",[])[:10]:
        sims.append({
            "name": a["name"],
            "similarity": 0.5,
            "reason":["placeholder until artist-DNA matching is connected"]
        })

    results.append({
        "title": r["title"],
        "similar_artists": sims
    })

json.dump(results,open(OUT,"w",encoding="utf-8"),indent=2,ensure_ascii=False)

lines=["# Opportunity Similarity",""]
for r in results:
    lines.append(f"## {r['title']}")
    for a in r["similar_artists"][:5]:
        lines.append(f"- {a['name']} ({a['similarity']})")
    lines.append("")

Path(REPORT).write_text("\n".join(lines),encoding="utf-8")
print("Wrote",OUT)
