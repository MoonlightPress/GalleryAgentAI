
import json
import os
from pathlib import Path

QUEUE_PATH = "memory/research_priority_queue.json"
OUT_DIR = "drafts/outreach"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_text(path, text):
    Path(path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    Path(path).write_text(
        text,
        encoding="utf-8",
    )


def generate_email(item):

    title = item.get("title", "")
    category = item.get("category", "")

    return f"""
Subject: Inquiry About Opportunities / Submission Information

Hello,

I hope you are doing well.

I am researching potential opportunities for a contemporary photographer and artist working primarily with atmospheric photography, printed matter, and artist books.

I wanted to ask whether there are currently any:
- open calls
- portfolio reviews
- publication opportunities
- exhibitions
- artist-book opportunities
- residency programs
- collaborative projects

connected to {title}.

I would also appreciate any clarification regarding:
- submission process
- deadlines
- fees
- artist eligibility
- international participation

Thank you very much for your time.

Best regards,
[Name]
""".strip()


def main():

    queue = load_json(
        QUEUE_PATH,
        [],
    )

    created = 0

    for item in queue[:20]:

        title = (
            item.get("title", "unknown")
            .replace("/", "_")
            .replace("\\", "_")
        )

        email = generate_email(item)

        save_text(
            f"{OUT_DIR}/{title}.txt",
            email,
        )

        created += 1

    print(
        f"Generated {created} outreach drafts."
    )


if __name__ == "__main__":
    main()
