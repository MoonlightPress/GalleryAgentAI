import json
import os
from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env")

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-5"


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


opportunities = load_json(
    "memory/opportunities_master.json",
    []
)

artist_intel = load_json(
    "memory/artist_intelligence.json",
    {}
)

if not artist_intel:
    raise Exception("Run artist_intelligence_agent.py first.")

upgraded = []

for opp in opportunities:

    prompt = f"""
You are upgrading an artist opportunity match.

Use the artist intelligence profile, but be cautious.

RULES:
- Do not say the artist wants something unless confirmed.
- Phrase uncertain fit as "may fit" or "could be useful if..."
- Separate opportunity value from artist preference uncertainty.
- Do not over-reject opportunities because of assumed goals.
- If something is useful only for one pathway, name that pathway.

Artist intelligence:
{json.dumps(artist_intel, indent=2, ensure_ascii=False)}

Opportunity:
{json.dumps(opp, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Format:
{{
  "pathway_fit": {{
    "publishing": 0,
    "local_visibility": 0,
    "direct_sales": 0,
    "gallery_path": 0,
    "residency_path": 0,
    "licensing_path": 0,
    "peer_network": 0
  }},
  "best_use_case": "",
  "why_this_might_fit": "",
  "why_it_might_not_fit": "",
  "what_to_verify_first": [],
  "artist_preference_questions_before_action": [],
  "suggested_display_summary": "",
  "suggested_next_action": "",
  "confidence": 0
}}
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1800,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response.content[0].text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    match = json.loads(text)

    opp["artist_intelligence_match"] = match
    upgraded.append(opp)

    print("Upgraded:", opp.get("name", opp.get("title", "Unknown")))

save_json(
    "memory/opportunities_master.json",
    upgraded
)

print("Saved upgraded opportunities_master.json")