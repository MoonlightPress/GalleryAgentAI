
import json
from pathlib import Path

SRC = "memory/submission_requirements.json"
OUT = "reports/actionable_opportunities.md"

data = json.load(open(SRC, encoding="utf-8"))

lines = ["# Artist Action Targets", ""]

for item in data[:20]:
    lines.append(f"## {item.get('title')}")
    lines.append(f"- Contact: {item.get('contact','unknown')}")
    links = item.get("submission_links", [])
    lines.append(f"- Submission links found: {len(links)}")
    lines.append(f"- Requirements: {', '.join(item.get('estimated_requirements',[]))}")

    if links:
        lines.append("")
        lines.append("### Submission / Application Links")
        for link in links[:6]:
            label = link.get("label") or "[no label]"
            url = link.get("url")
            score = link.get("submission_link_score", "")
            lines.append(f"- {label} — {url} — score {score}")

    lines.append("")

Path("reports").mkdir(exist_ok=True)
Path(OUT).write_text("\n".join(lines), encoding="utf-8")
print("Wrote", OUT)
