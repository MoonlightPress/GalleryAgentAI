
import json,re
from datetime import datetime

INFILE="memory/open_call_results.json"
OUTFILE="memory/deadline_filtered_results.json"

items=json.load(open(INFILE,encoding="utf-8"))
current_year=datetime.now().year

for item in items:
    dates=item.get("date_candidates",[])

    best="unknown"
    conf=0.0

    for d in dates:
        if str(current_year) in str(d) or str(current_year+1) in str(d):
            best=d
            conf=0.9
            break

    item["best_deadline"]=best
    item["deadline_confidence"]=conf

json.dump(items,open(OUTFILE,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
print("Wrote",OUTFILE)
