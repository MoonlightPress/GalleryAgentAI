
import json
from pathlib import Path

INFILE="memory/deadline_filtered_results.json"

items=json.load(open(INFILE,encoding="utf-8"))

for item in items:
    score=0

    if item.get("verified"):
        score+=2

    if item.get("contact") not in ["unknown",None,""]:
        score+=2

    if item.get("contact_pages"):
        score+=2

    if item.get("submission_status")=="possible_open_call":
        score+=3

    if item.get("best_deadline")!="unknown":
        score+=2

    item["verification_score"]=score

items.sort(key=lambda x:x.get("verification_score",0),reverse=True)

json.dump(items,open(INFILE,"w",encoding="utf-8"),indent=2,ensure_ascii=False)

lines=["# High Confidence Opportunities",""]
for item in items[:25]:
    lines.append(f"## {item.get('title')}")
    lines.append(f"- Score: {item.get('verification_score')}")
    lines.append(f"- Contact: {item.get('contact')}")
    lines.append(f"- Submission: {item.get('submission_status')}")
    lines.append(f"- Deadline: {item.get('best_deadline')}")
    lines.append("")

Path("reports").mkdir(exist_ok=True)
Path("reports/high_confidence_opportunities.md").write_text("\n".join(lines),encoding="utf-8")

print("Built verification scores")
