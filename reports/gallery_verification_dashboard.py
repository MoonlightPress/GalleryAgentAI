
import json, os
from pathlib import Path

queue="memory/verification_queue.json"
out="reports/verified_opportunities_dashboard.md"

if not os.path.exists(queue):
    raise SystemExit("Run verification queue first")

items=json.load(open(queue,encoding="utf-8"))

lines=["# Verified Opportunities Dashboard","",""]

for i in items:
    lines.append(f"## {i['title']}")
    lines.append(f"- Status: {i['status']}")
    lines.append(f"- Open: {i['submission_open']}")
    lines.append(f"- Deadline: {i['deadline']}")
    lines.append(f"- Contact: {i['contact']}")
    lines.append("")

Path(out).write_text("\n".join(lines),encoding="utf-8")
print("Dashboard written")
