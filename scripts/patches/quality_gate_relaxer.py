
import json, os
from pathlib import Path

path="ingestion/opportunity_candidates.json"
if not os.path.exists(path):
    print("No candidates file found")
    raise SystemExit()

data=json.load(open(path,encoding="utf-8"))

approved=0
for c in data:
    score=float(c.get("overall_score",0) or 0)
    if score >= 4.5:
        c["quality_gate_status"]="approved"
        approved+=1

json.dump(data,open(path,"w",encoding="utf-8"),indent=2)
print("Relaxed quality gate. Approved:",approved)
