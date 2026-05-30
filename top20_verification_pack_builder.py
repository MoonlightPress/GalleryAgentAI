
import json, os
from pathlib import Path

queue="memory/verification_queue.json"
out="reports/top20_verification_targets.md"

items=json.load(open(queue,encoding="utf-8"))[:20]

lines=["# Top 20 Verification Targets","","Verify these before anything else.",""]

for n,i in enumerate(items,1):
    lines.append(f"{n}. {i['title']}")
    lines.append(f"   URL: {i['url']}")

Path(out).write_text("\n".join(lines),encoding="utf-8")
print("Top20 report written")
