import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from anthropic import Anthropic


load_dotenv(dotenv_path=".env")

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

MODEL = "claude-sonnet-4-5"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def load_json(path, fallback):

    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def fetch_page_text(url):

    if not url:
        return ""

    try:
        r = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        r.raise_for_status()

    except Exception:
        return ""

    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text("\n", strip=True)

    return text[:12000]


def resolve_questions(opportunity, page_text):

    unresolved = opportunity.get(
        "human_verification_needed",
        []
    )

    if not unresolved:
        return opportunity

    prompt = f"""
You are Agent R: Opportunity Resolution Agent.

Your job:
Attempt to resolve missing information questions
using the webpage text.

Opportunity:
{json.dumps(opportunity, indent=2, ensure_ascii=False)}

Website Text:
{page_text}

Tasks:
1. Resolve as many verification questions as possible.
2. Update the opportunity with discovered facts.
3. Remove resolved verification items.
4. Keep unresolved items only if genuinely uncertain.
5. Be conservative and factual.
6. Never invent information.

Return ONLY valid JSON.

Return the FULL updated opportunity object.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    output = response.content[0].text

    cleaned = (
        output
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(cleaned)


def main():

    opportunities = load_json(
        "memory/opportunities.json",
        []
    )

    updated = []

    print()
    print("Resolving opportunity uncertainties...")
    print()

    for opp in opportunities:

        name = opp.get("name", "UNKNOWN")

        unresolved = opp.get(
            "human_verification_needed",
            []
        )

        if not unresolved:

            print(f"SKIP: {name}")
            updated.append(opp)
            continue

        print(f"RESOLVING: {name}")

        url = (
            opp.get("submission_page")
            or opp.get("contact_page")
            or opp.get("official_website")
        )

        page_text = fetch_page_text(url)

        if not page_text:

            print("  Could not fetch page.")
            updated.append(opp)
            continue

        try:

            resolved = resolve_questions(
                opp,
                page_text
            )

            updated.append(resolved)

            remaining = resolved.get(
                "human_verification_needed",
                []
            )

            print(
                f"  Remaining questions: {len(remaining)}"
            )

        except Exception as e:

            print(f"  FAILED: {e}")
            updated.append(opp)

    save_json(
        "memory/opportunities.json",
        updated
    )

    print()
    print("Saved updated opportunities.")


if __name__ == "__main__":
    main()