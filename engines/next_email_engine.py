
import json
import os
from pathlib import Path

PROJECT_PATH = "memory/next_projects.json"
OUT_JSON = "memory/next_emails.json"
OUT_REPORT = "reports/next_emails.md"
OUT_DIR = "drafts/next_emails"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def safe_filename(text):
    bad = '<>:"/\\|?*'
    text = str(text or "untitled")
    for ch in bad:
        text = text.replace(ch, "_")
    return text[:80].strip(" ._") or "untitled"


def make_email(project, target):
    title = project["title"]
    target_name = target.get("title") or target.get("name") or "this space"

    return {
        "project": title,
        "target": target_name,
        "subject": f"Photography / artist book inquiry — {title}",
        "body": f"""Hello,

I am researching whether {target_name} is currently open to quiet photography, photobook, artist-book, or zine-related submissions.

The project I am considering is titled "{title}." It is a small photographic sequence about ordinary neighborhoods, lived-in spaces, memory, and human traces in daily life.

Could you let me know whether there is a current submission process, open call, or appropriate contact for this kind of work?

Thank you."""
    }


def main():
    projects = load_json(PROJECT_PATH, [])

    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

    emails = []

    for project in projects:
        for target in project.get("best_opportunity_targets", [])[:3]:
            email = make_email(project, target)
            emails.append(email)

            path = Path(OUT_DIR) / f"{safe_filename(email['target'])} - {safe_filename(project['title'])}.md"
            path.write_text(
                f"# {email['subject']}\n\n{email['body']}\n",
                encoding="utf-8",
            )

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(emails, f, indent=2, ensure_ascii=False)

    lines = [
        "# Next Email Drafts",
        "",
        "Short, low-pressure emails connected to actual project concepts.",
        "",
    ]

    for email in emails:
        lines.append(f"## {email['target']} — {email['project']}")
        lines.append("")
        lines.append(f"**Subject:** {email['subject']}")
        lines.append("")
        lines.append(email["body"])
        lines.append("")

    Path(OUT_REPORT).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_REPORT}")
    print(f"Wrote drafts to {OUT_DIR}")


if __name__ == "__main__":
    main()
