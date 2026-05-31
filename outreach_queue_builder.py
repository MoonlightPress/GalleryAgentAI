
import json
from pathlib import Path

SRC="memory/contact_targets.json"
OUT="reports/outreach_queue.md"

data=json.load(open(SRC,encoding="utf-8"))

lines=["# Outreach Queue",""]
for i,x in enumerate(data,1):
    lines.append(f"{i}. {x['title']}")
    lines.append(f"   - Link: {x['best_link']}")
    lines.append(f"   - First Contact: {x['contact_guesses'][0]}")
    lines.append("")

Path("reports").mkdir(exist_ok=True)
Path(OUT).write_text("\n".join(lines),encoding="utf-8")
print("Wrote",OUT)
