
import json, os
from pathlib import Path

OPP="deploy_data/compact_opportunities.json"
OUT="reports/verification_queue.md"

def load(p,d):
    if os.path.exists(p):
        return json.load(open(p,encoding="utf-8"))
    return d

opps=load(OPP,[])

targets=[]
for o in opps:
    score=float(o.get("painting_priority_score",
          o.get("source_purity_score",
          o.get("truth_aligned_score",
          o.get("overall_score",0)))) or 0)

    if o.get("native_medium") not in ["painting","mixed"]:
        continue

    targets.append((score,o))

targets.sort(reverse=True,key=lambda x:x[0])

lines=["# Verification Queue","","Top opportunities that need human verification.",""]

queue=[]

for score,o in targets[:25]:
    item={
        "title":o.get("title"),
        "url":o.get("official_website") or o.get("source_url"),
        "score":score,
        "status":"unverified",
        "submission_open":"unknown",
        "deadline":"unknown",
        "contact":"unknown",
        "fee":"unknown"
    }
    queue.append(item)

    lines.append(f"- {item['title']} ({score})")
    lines.append(f"  - {item['url']}")

Path("memory").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)

json.dump(queue,open("memory/verification_queue.json","w",encoding="utf-8"),indent=2,ensure_ascii=False)
Path(OUT).write_text("\n".join(lines),encoding="utf-8")
print("Wrote verification queue")
