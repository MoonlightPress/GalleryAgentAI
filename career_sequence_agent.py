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

top = opps[:40]

prompt = f"""
You are building strategic opportunity sequences.

Meaning:
do NOT recommend isolated opportunities.

Instead:
build chains that compound.

Examples:
small zine
→ bookstore
→ fair
→ gallery
→ publisher visibility

Career:
{json.dumps(career, indent=2, ensure_ascii=False)}

Top opportunities:
{json.dumps(top, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Format:
{{
  "strategic_sequences": [
    {{
      "name": "",
      "goal": "",
      "sequence": [
        {{
          "step": 1,
          "opportunity_title": "",
          "why_now": "",
          "unlocks": []
        }}
      ],
      "estimated_time_horizon": "",
      "risk_level": "",
      "compounding_value": "",
      "best_for": []
    }}
  ]
}}
"""

response = client.messages.create(
    model=MODEL,
    max_tokens=5000,
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

save_json(
    "memory/strategic_sequences.json",
    data
)

print("Saved strategic sequences.")