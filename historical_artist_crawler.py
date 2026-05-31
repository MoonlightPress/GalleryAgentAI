
import json
from pathlib import Path

INPUT="memory/opportunity_evidence.json"
OUT="memory/historical_artist_data.json"
REPORT="reports/historical_artist_data.md"

KEYWORDS=["winner","winners","exhibitor","exhibitors","artist","artists","judge","publisher","gallery","selected"]

def load(p):
    return json.load(open(p,encoding="utf-8")) if Path(p).exists() else []

rows=load(INPUT)
out=[]

for r in rows:
    names=r.get("possible_names",[])
    artists=[]
    for n in names[:25]:
        artists.append({
            "name": n,
            "year": "unknown",
            "url": "unknown",
            "evidence": "Extracted from opportunity evidence pages"
        })

    out.append({
        "title": r.get("title"),
        "historical_artists": artists,
        "historical_publishers": [],
        "historical_galleries": [],
        "historical_judges": []
    })

Path("memory").mkdir(exist_ok=True)
json.dump(out,open(OUT,"w",encoding="utf-8"),indent=2,ensure_ascii=False)

lines=["# Historical Artist Data",""]
for r in out:
    lines.append(f"## {r['title']}")
    for a in r["historical_artists"][:10]:
        lines.append(f"- {a['name']}")
    lines.append("")

Path("reports").mkdir(exist_ok=True)
Path(REPORT).write_text("\n".join(lines),encoding="utf-8")
print("Wrote",OUT)
