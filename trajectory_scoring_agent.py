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

upgraded = []

for opp in opps[:120]:

    prompt = f"""
You are analyzing career trajectory fit.

IMPORTANT:
Do not merely judge aesthetic fit.

Instead ask:
- Is this the right NEXT STEP?
- Is this premature?
- What would this unlock?
- What should happen before this?
- What credibility signals does this build?

Career reconstruction:
{json.dumps(career, indent=2, ensure_ascii=False)}

Opportunity:
{json.dumps(opp, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Format:
{{
  "career_stage_fit": {{
    "early": 0,
    "developing": 0,
    "established": 0
  }},
  "best_used_for": [],
  "requires_before_attempting": [],
  "credibility_signals_gained": [],
  "unlocks_after_completion": [],
  "strategic_value": "",
  "timing_analysis": "",
  "why_now_or_why_not_now": "",
  "possible_better_pre_steps": [],
  "career_compounding_score": 0,
  "risk_of_attempting_too_early": "",
  "confidence": 0
}}
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2200,
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

    opp["trajectory_analysis"] = data

    upgraded.append(opp)

    print(
        "Trajectory analyzed:",
opp.get("title") or opp.get("name") or "Unknown"
    )

save_json(
    "memory/opportunities_master.json",
    upgraded
)

print("Saved trajectory analysis.")