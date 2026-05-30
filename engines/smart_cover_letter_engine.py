
import json
import os
from pathlib import Path
from utils_filename import safe_filename

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_DIR = "drafts/smart_cover_letters"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def letter(opp):

    title = opp.get("title", "Unknown")
    tone = opp.get(
        "submission_tone",
        "professional"
    )

    why = opp.get(
        "why_this_fits_short",
        ""
    )

    body = opp.get(
        "recommended_body_of_work",
        "Selected Works"
    )

    return f"""# Smart Cover Letter — {title}

Tone:
{tone}

Recommended Body of Work:
{body}

Core Fit:
{why}

Draft Structure:

1. Short greeting
2. Brief introduction
3. Mention why the venue/publication specifically fits the work
4. Mention the body of work
5. Offer portfolio/PDF/Instagram
6. Thank them briefly

Important:
- Do not make the message too long.
- Avoid sounding desperate.
- Avoid generic praise.
- Match the emotional tone of the institution.
"""

def main():

    opps = load_json(
        OPP_PATH,
        []
    )

    Path(OUT_DIR).mkdir(
        parents=True,
        exist_ok=True,
    )

    count = 0

    for opp in opps[:120]:

        title = opp.get(
            "title",
            "Unknown"
        )

        path = Path(
            OUT_DIR
        ) / f"{safe_filename(title, max_len=90)}.md"

        path.write_text(
            letter(opp),
            encoding="utf-8",
        )

        count += 1

    print(
        f"Generated {count} smart cover letters."
    )

if __name__ == "__main__":
    main()
