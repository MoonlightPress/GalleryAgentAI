import json
import os
from anthropic import Anthropic
from dotenv import load_dotenv


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
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


career = load_json(
    "memory/career_reconstruction.json",
    {}
)

opps = load_json(
    "memory/opportunities_master.json",
    []
)

results = []

for opp in opps[:120]:

    prompt = f"""
You are analyzing whether an opportunity acts as an ecosystem bridge.

Meaning:
- entering one ecosystem may unlock nearby opportunities
- this is not just about one isolated event
- identify downstream career effects

Artist reconstruction:
{json.dumps(career, indent=2, ensure_ascii=False)}

Opportunity:
{json.dumps(opp, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Format:
{{
  "ecosystem_value": 0,
  "entry_point_strength": 0,
  "peer_visibility_gain": 0,
  "institutional_visibility_gain": 0,
  "community_overlap": [],
  "possible_downstream_unlocks": [],
  "why_this_might_matter_long_term": "",
  "career_compounding_potential": "",
  "danger_if_pursued_too_early": "",
  "best_timing": ""
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

    data = json.loads(text)

    opp["ecosystem_bridge_analysis"] = data

    results.append(opp)

    print(
        "Bridge analyzed:",
opp.get("title") or opp.get("name") or "Unknown"
    )

save_json(
    "memory/opportunities_master.json",
    results
)

print("Saved upgraded ecosystem bridge analysis.")