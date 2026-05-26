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

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-5"


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def parse_json(text):
    cleaned = (
        text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )
    return json.loads(cleaned)


def evaluate_opportunity(profile, opportunity):
    prompt = f"""
You are the Artist Opportunity Council.

Evaluate this opportunity using five internal reviewers:

1. Curator
2. Career Advisor
3. Peer Artist
4. Submission Reviewer
5. Protective Voice

Artist Profile:
{json.dumps(profile, indent=2, ensure_ascii=False)}

Opportunity:
{json.dumps(opportunity, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Schema:
{{
  "council_scores": {{
    "curator_score": 0,
    "career_score": 0,
    "peer_artist_score": 0,
    "submission_score": 0,
    "emotional_fit": 0,
    "predatory_risk": 0
  }},
  "overall_score": 0,
  "recommendation_strength": "",
  "difficulty": "",
  "compact_card": {{
    "one_sentence": "",
    "three_bullets": [],
    "quick_action": "",
    "why_this_fits_short": ""
  }},
  "protective_voice": {{
    "likely_emotional_response": "",
    "potential_friction": [],
    "softer_summary": "",
    "hide_by_default": []
  }},
  "council_notes": {{
    "curator": "",
    "career_advisor": "",
    "peer_artist": "",
    "submission_reviewer": "",
    "protective_voice": ""
  }}
}}

Rules:
- Scores are 0 to 10.
- predatory_risk: 0 means no concern, 10 means serious concern.
- Be practical.
- Do not flatter.
- Do not overstate certainty.
- Compact card text should be calm and artist-facing.
- Protective voice should reduce pressure, not infantilize the artist.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    return parse_json(response.content[0].text)


def main():
    print()
    print("Running council review...")
    print()

    profile = load_json("memory/artist_profile.json", {})
    opportunities = load_json("memory/opportunities.json", [])

    updated = []

    for i, opp in enumerate(opportunities):
        name = opp.get("name", "UNKNOWN")
        print(f"COUNCIL {i + 1}/{len(opportunities)}: {name}")

        try:
            council_review = evaluate_opportunity(profile, opp)
            opp["council_review"] = council_review
            updated.append(opp)
            print("  OK")

        except Exception as e:
            opp["council_error"] = str(e)
            updated.append(opp)
            print(f"  FAILED: {e}")

    save_json("memory/opportunities.json", updated)

    print()
    print("Saved council reviews to memory/opportunities.json")
    print()


if __name__ == "__main__":
    main()