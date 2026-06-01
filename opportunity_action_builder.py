
import json
from pathlib import Path

SRC = "memory/submission_targets.json"
REPORT = "reports/actionable_opportunities.md"

data = json.loads(Path(SRC).read_text(encoding="utf-8"))

lines = [
    "# Artist Action Targets",
    "",
    "This report uses saved homepage links to identify possible submission/contact paths.",
    "",
]

for item in data[:20]:
    links = item.get("submission_links", [])

    lines.append(f"## {item.get('title')}")
    lines.append(f"- Contact: {item.get('contact', 'unknown')}")
    lines.append(f"- Submission links found: {len(links)}")
    lines.append(f"- Submission signal: {item.get('submission_open', 'unknown')}")
    lines.append(f"- Deadline/date candidate: {item.get('deadline', 'unknown')}")

    if links:
        lines.append("- Best submission/action links:")
        for link in links[:5]:
            label = link.get("label") or "[no label]"
            lines.append(f"  - {label} — {link.get('url')}")

    lines.append("- Default requirements to prepare: portfolio PDF, artist statement, images of work")
    lines.append("")

Path("reports").mkdir(exist_ok=True)
Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

print(f"Wrote {REPORT}")
