import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import os
from dotenv import load_dotenv
from anthropic import Anthropic


load_dotenv(dotenv_path=".env")

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

MODEL = "claude-sonnet-4-5"


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


def evaluate_one(profile, opportunity):

    prompt = f"""
You are Agent F: Opportunity Filtering Agent.

Your job:
Decide whether this opportunity should remain visible.

Artist Profile:
{json.dumps(profile, indent=2, ensure_ascii=False)}

Opportunity:
{json.dumps(opportunity, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Schema:

{{
  "keep": true,
  "filter_reason": "",
  "visibility": "",
  "updated_opportunity": {{}}
}}

Valid visibility values:
- primary
- secondary
- hidden
- archive

Rules:
- Hide opportunities that are emotionally draining.
- Hide bad ecosystem fits.
- Hide impossible opportunities.
- Hide predatory opportunities.
- Prefer realistic momentum.
- Avoid prestige obsession.
- Preserve unusual but meaningful opportunities.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2500,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    cleaned = (
        response.content[0].text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(cleaned)


def main():

    profile = load_json(
        "memory/artist_profile.json",
        {}
    )

    opportunities = load_json(
        "memory/opportunities.json",
        []
    )

    kept = []
    hidden = []

    print()
    print("Filtering opportunities...")
    print()

    for opp in opportunities:

        name = opp.get("name", "UNKNOWN")

        print(f"Evaluating: {name}")

        try:

            result = evaluate_one(
                profile,
                opp
            )

            updated = result.get(
                "updated_opportunity",
                opp
            )

            updated["visibility"] = result.get(
                "visibility",
                "primary"
            )

            updated["filter_reason"] = result.get(
                "filter_reason",
                ""
            )

            if not updated.get("name"):
                updated["name"] = (
                    updated.get("title")
                    or updated.get("opportunity_name")
                    or "Unknown"
                )

            if not updated.get("type"):
                updated["type"] = (
                    updated.get("category")
                    or updated.get("opportunity_type")
                    or "unknown"
                )

            if result.get("keep", True):

                kept.append(updated)

                print(
                    f"  KEPT ({updated['visibility']})"
                )

            else:

                hidden.append(updated)

                print("  FILTERED")
        except Exception as e:

            print(f"  FAILED: {e}")

            kept.append(opp)

    save_json(
        "memory/opportunities.json",
        kept
    )

    save_json(
        "memory/filtered_out_opportunities.json",
        hidden
    )

    print()
    print(f"Kept: {len(kept)}")
    print(f"Filtered: {len(hidden)}")
    print()


if __name__ == "__main__":
    main()