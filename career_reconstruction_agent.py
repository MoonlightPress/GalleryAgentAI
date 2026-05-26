import json
import os
from anthropic import Anthropic
from dotenv import load_dotenv
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


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


seed = load_json(
    "career_reconstruction_seed.json",
    {}
)

if not seed:
    raise Exception("career_reconstruction_seed.json missing.")


prompt = f"""
You are reconstructing an artist career history.

Your task is to carefully reconstruct:
- career trajectory
- artistic development
- ecosystem position
- audience development
- credibility signals
- recurring collaborators
- recurring themes
- institutional progression
- aesthetic continuity
- market positioning

IMPORTANT:
- Separate confirmed evidence from interpretation.
- Never invent exhibitions or accomplishments.
- If uncertain, mark it clearly.
- Track chronology carefully.
- Extract ecosystem relationships when possible.

Artist data:
{json.dumps(seed, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Format:
{{
  "generated_at": "",
  "career_timeline": [
    {{
      "period": "",
      "confirmed_events": [],
      "possible_developments": [],
      "evidence": [],
      "confidence": ""
    }}
  ],
  "ecosystem_map": {{
    "cities": [],
    "spaces": [],
    "publishers": [],
    "peer_artists": [],
    "institutions": [],
    "recurring_collaborators": [],
    "community_clusters": []
  }},
  "credibility_signals": {{
    "publication_history": [],
    "collector_signals": [],
    "installation_evidence": [],
    "repeat_exhibitions": [],
    "professional_language_signals": [],
    "cross_platform_signals": [],
    "consistency_signals": []
  }},
  "aesthetic_evolution": {{
    "persistent_themes": [],
    "emerging_themes": [],
    "declining_themes": [],
    "persistent_materials": [],
    "visual_language": [],
    "audience_responses": []
  }},
  "career_position_estimate": {{
    "overall_stage": "",
    "evidence_for_stage": [],
    "possible_next_steps": [],
    "high_probability_paths": [],
    "high_risk_paths": [],
    "institutional_readiness": [],
    "commercial_readiness": []
  }},
  "opportunity_ecosystem_bridges": [
    {{
      "entry_point": "",
      "possible_unlocks": [],
      "why_it_matters": ""
    }}
  ],
  "unknowns": [
    {{
      "question": "",
      "why_it_matters": ""
    }}
  ]
}}
"""

response = client.messages.create(
    model=MODEL,
    max_tokens=7000,
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

data["generated_at"] = datetime.now().strftime(
    "%Y-%m-%d %H:%M"
)

save_json(
    "memory/career_reconstruction.json",
    data
)

print("Saved memory/career_reconstruction.json")