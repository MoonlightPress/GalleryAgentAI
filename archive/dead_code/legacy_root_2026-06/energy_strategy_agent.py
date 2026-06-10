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


energy = load_json(
    "energy_profile.json",
    {}
)

career = load_json(
    "memory/career_reconstruction.json",
    {}
)

strategy = load_json(
    "memory/adaptive_strategy.json",
    {}
)

prompt = f"""
You are analyzing artist energy sustainability.

IMPORTANT:
This is NOT therapy.
This is strategic energy budgeting.

Analyze:
- what kinds of opportunities are likely energizing
- what kinds are likely draining
- where burnout risk exists
- where compounding excitement exists
- where sustainable momentum exists

Energy profile:
{json.dumps(energy, indent=2, ensure_ascii=False)}

Career:
{json.dumps(career, indent=2, ensure_ascii=False)}

Strategy:
{json.dumps(strategy, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Format:
{{
  "high_energy_positive_paths": [],
  "high_energy_negative_paths": [],
  "low_energy_high_roi_paths": [],
  "burnout_risks": [],
  "sustainable_growth_patterns": [],
  "dangerous_overcommitments": [],
  "recommended_monthly_balance": [],
  "confidence": 0
}}
"""

response = client.messages.create(
    model=MODEL,
    max_tokens=3000,
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
    "memory/energy_strategy.json",
    data
)

print("Saved energy strategy.")