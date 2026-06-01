
import json
from pathlib import Path

SRC = "memory/verified_opportunities.json"
OUT = "memory/submission_targets.json"
REPORT = "reports/submission_link_report.md"

KEYWORDS = [
    "submit", "submission", "apply", "application", "entry",
    "open call", "artist call", "opportunity", "opportunities",
    "contest", "award", "exhibition",
    "応募", "公募", "募集", "出展", "申し込み", "申込"
]

data = json.loads(Path(SRC).read_text(encoding="utf-8"))

lines = [
    "# Submission Link Report",
    "",
]

for item in data:
    found = []

    for link in item.get("relevant_links", []):
        blob = f"{link.get('label', '')} {link.get('url', '')} {link.get('kind', '')}".lower()

        if link.get("kind") == "submission_candidate" or any(k in blob for k in KEYWORDS):
            found.append(link)

    item["submission_links"] = found

    lines.append(f"## {item.get('title')}")
    lines.append(f"- Submission links found: {len(found)}")

    for link in found[:10]:
        label = link.get("label") or "[no label]"
        lines.append(f"  - {label} — {link.get('url')}")

    lines.append("")

Path(OUT).parent.mkdir(parents=True, exist_ok=True)
Path(OUT).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

Path("reports").mkdir(exist_ok=True)
Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

print(f"Wrote {OUT}")
print(f"Wrote {REPORT}")
