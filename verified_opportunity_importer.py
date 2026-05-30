
import json
from pathlib import Path

data=json.load(open("memory/verified_opportunities.json",encoding="utf-8"))

lines=["# Verified Opportunities","",""]
for x in data:
    lines.append(f"## {x.get('title')}")
    lines.append(f"- Verified: {x.get('verified')}")
    lines.append(f"- Submission: {x.get('submission_open')}")
    lines.append(f"- Deadline: {x.get('deadline')}")
    lines.append(f"- Contact: {x.get('contact')}")
    lines.append("")

Path("reports").mkdir(exist_ok=True)
Path("reports/verified_opportunities_dashboard.md").write_text(
    "\n".join(lines),encoding="utf-8"
)
print("Dashboard written")
