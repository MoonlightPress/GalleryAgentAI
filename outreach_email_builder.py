
import json
import re
from pathlib import Path

SRC = "memory/actionable_target_shortlist.json"
OUT = "drafts/outreach_emails"
REPORT = "reports/outreach_email_index.md"

def safe_name(text):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", str(text or "untitled"))[:80].strip("_") or "untitled"

def contact_for(p):
    emails = p.get("emails", [])
    if emails:
        return emails[0]
    c = p.get("source_contact", "unknown")
    return c if c else "unknown"

def build_email(p):
    target = p.get("source_title", "this opportunity")
    page = p.get("submission_page_url", "")
    contact = contact_for(p)

    subject = f"Watercolor / works on paper inquiry — {target}"

    body = f"""Hello,

I am writing to ask whether {target} is currently open to watercolor, drawing, or works-on-paper submissions.

The artist's work is a quiet watercolor practice focused on ordinary architecture, plants, local places, and traces of daily life. I am preparing a compact portfolio PDF and wanted to confirm the appropriate submission path before sending materials.

I found this page while researching:
{page}

Could you let me know whether this is the correct place to inquire, or whether there is a current application / open-call process?

Thank you."""

    return {
        "target": target,
        "to": contact,
        "subject": subject,
        "body": body,
        "source_page": page,
    }

def main():
    if not Path(SRC).exists():
        raise SystemExit("Missing memory/actionable_target_shortlist.json. Run target_shortlist_builder.py first.")

    targets = json.loads(Path(SRC).read_text(encoding="utf-8"))

    Path(OUT).mkdir(parents=True, exist_ok=True)

    emails = []
    for p in targets[:12]:
        email = build_email(p)
        emails.append(email)

        filename = f"{safe_name(email['target'])}.md"
        Path(OUT, filename).write_text(
            f"# {email['subject']}\n\nTo: {email['to']}\n\n{email['body']}\n",
            encoding="utf-8",
        )

    lines = [
        "# Outreach Email Index",
        "",
    ]

    for e in emails:
        lines.append(f"## {e['target']}")
        lines.append(f"- To: {e['to']}")
        lines.append(f"- Subject: {e['subject']}")
        lines.append(f"- Source page: {e['source_page']}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")
    Path("memory/outreach_emails.json").write_text(json.dumps(emails, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote emails to {OUT}")
    print(f"Wrote {REPORT}")

if __name__ == "__main__":
    main()
