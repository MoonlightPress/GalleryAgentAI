from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv(dotenv_path=".env")

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

MODEL = "claude-sonnet-4-5"


def load_text(path, fallback=""):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


artist_dossier = load_text("artist_dossier.md")
collaboration_report = load_text("collaboration_report.md")
action_plan = load_text("action_plan.md")

artist_preferences = load_json(
    "memory/artist_preferences.json",
    {}
)

existing_opportunities = load_json(
    "memory/opportunities.json",
    []
)


prompt = f"""
You are Agent G: Structured Opportunity Scorer.

Your job:
Generate structured opportunity recommendations.

Use:
- artist dossier
- collaboration report
- action plan
- artist preferences

Artist dossier:
{artist_dossier}

Collaboration report:
{collaboration_report}

Action plan:
{action_plan}

Artist preferences:
{json.dumps(artist_preferences, indent=2, ensure_ascii=False)}

Existing opportunities:
{json.dumps(existing_opportunities, indent=2, ensure_ascii=False)}

OUTPUT RULES:

Return ONLY valid JSON.

Return a JSON array.

Each item MUST contain:

{{
  "name": "",
  "city": "",
  "country": "",
  "type": "",
  "why_fit": "",
  "gallery_fit_score": 0,
  "commercial_fit_score": 0,
  "institutional_fit_score": 0,
  "collaboration_fit_score": 0,
  "confidence_score": 0,
  "priority": "",
  "status": "unverified",
  "next_action": "",
  "risk_notes": "",
  "search_terms": [],
  "related_themes": []
}}

SCORING RULES:
- Scores are 0-10
- Confidence is 0-1
- Avoid generic recommendations
- Avoid mega-famous unrealistic institutions
- Prefer realistic ecosystem fit
- Include galleries, fairs, publishers, art book fairs, and collaborative opportunities
"""

response = client.messages.create(
    model=MODEL,
    max_tokens=3500,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

output = response.content[0].text

print(output)

try:
    parsed = json.loads(output)

    with open("memory/opportunities.json", "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)

    print("\nSaved structured opportunities.")

except Exception as e:
    print("\nJSON FAILED:")
    print(e)