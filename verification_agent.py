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


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


opportunities = load_json(
    "memory/opportunities.json",
    []
)


prompt = f"""
You are Agent K: Verification and Skepticism Agent.

Your ONLY purpose:
Critically evaluate the existing opportunities.

You are skeptical.

For EACH opportunity:
- determine if it seems realistic
- determine if it likely exists
- determine if the fit may be overstated
- determine if the opportunity is too ambitious
- determine if the recommendation should be downgraded

Return ONLY valid JSON array.

Format:

[
  {{
    "name": "",
    "verification_status": "",
    "confidence_adjustment": 0,
    "fit_adjustment": 0,
    "main_risk": "",
    "recommended_action": "",
    "reasoning": ""
  }}
]

Rules:
- verification_status must be:
    "likely_real"
    "needs_manual_verification"
    "probably_bad_fit"
    "too_ambitious"
    "strong_match"

- confidence_adjustment:
    -1.0 to 1.0

- fit_adjustment:
    -3 to 3

- Be conservative.
- Downgrade weak recommendations aggressively.
- Avoid hype.
- Do not invent certainty.

Current opportunities:
{json.dumps(opportunities, indent=2, ensure_ascii=False)}
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

print(output)

cleaned = output.replace("```json", "").replace("```", "").strip()

parsed = json.loads(cleaned)

with open(
    "verification_report.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(parsed, f, indent=2, ensure_ascii=False)

print("\nSaved verification_report.json")