
import json
from pathlib import Path

DATA_PATH = "memory/verified_opportunities.json"
REPORT_PATH = "reports/link_audit_report.md"

data = json.loads(Path(DATA_PATH).read_text(encoding="utf-8"))

lines = [
    "# Link Audit Report",
    "",
    "This confirms whether verified opportunity records now contain links for the submission crawler.",
    "",
]

for item in data:
    links = item.get("relevant_links", [])
    submission = [x for x in links if x.get("kind") == "submission_candidate"]
    contact = [x for x in links if x.get("kind") == "contact_candidate"]

    lines.append(f"## {item.get('title')}")
    lines.append(f"- Verified: {item.get('verified')}")
    lines.append(f"- Total links saved: {len(links)}")
    lines.append(f"- Submission candidate links: {len(submission)}")
    lines.append(f"- Contact candidate links: {len(contact)}")
    lines.append(f"- Contact: {item.get('contact')}")
    lines.append(f"- Submission signal: {item.get('submission_open')}")

    if submission:
        lines.append("- Submission candidates:")
        for link in submission[:10]:
            label = link.get("label") or "[no label]"
            lines.append(f"  - {label} — {link.get('url')}")

    if contact:
        lines.append("- Contact candidates:")
        for link in contact[:6]:
            label = link.get("label") or "[no label]"
            lines.append(f"  - {label} — {link.get('url')}")

    lines.append("")

Path("reports").mkdir(exist_ok=True)
Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")

print(f"Wrote {REPORT_PATH}")
