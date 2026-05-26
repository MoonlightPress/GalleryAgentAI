import json
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime


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


seed = load_json(
    "artist_research_seed.json",
    {}
)

if not seed:
    raise Exception("artist_research_seed.json missing or empty.")


prompt = f"""
You are an artist career research analyst.

Your job is to transform messy artist information into a cautious, useful intelligence profile for opportunity matching.

IMPORTANT RULES:
- Separate confirmed facts from interpretation.
- Do not claim the artist wants something unless explicitly stated.
- Do not psychoanalyze.
- Do not overstate.
- Do not invent exhibitions, publications, sales, or goals.
- Mark unknowns clearly.
- Use the artist's own language when available.
- Create useful opportunity-matching signals.

Artist research seed:
{json.dumps(seed, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Format:
{{
  "last_updated": "",
  "artist_identity": {{
    "artist_name": "",
    "public_name": "",
    "portfolio_url": "",
    "instagram_urls": [],
    "website_urls": []
  }},
  "confirmed_facts": {{
    "exhibitions": [],
    "publications": [],
    "sales_or_commissions": [],
    "education_or_training": [],
    "locations_connected_to_artist": [],
    "media_used": [],
    "languages": []
  }},
  "artist_self_description": {{
    "direct_phrases": [],
    "recurring_words": [],
    "stated_themes": [],
    "stated_goals": []
  }},
  "external_descriptions": {{
    "direct_phrases": [],
    "recurring_words": [],
    "positioning_signals": []
  }},
  "work_analysis": {{
    "confirmed_subjects": [],
    "possible_subjects": [],
    "confirmed_themes": [],
    "possible_themes": [],
    "visual_language": [],
    "materials_and_process": [],
    "emotional_register": [],
    "audience_likely_to_respond": []
  }},
  "career_positioning": {{
    "current_strengths": [],
    "current_gaps": [],
    "likely_next_steps": [],
    "low_friction_paths": [],
    "higher_ambition_paths": [],
    "paths_to_avoid_claiming_until_confirmed": []
  }},
  "opportunity_matching_signals": {{
    "good_contexts": [],
    "maybe_contexts": [],
    "high_friction_contexts": [],
    "keywords_for_search": [],
    "cities_or_regions_to_prioritize": [],
    "institutions_or_space_types_to_prioritize": []
  }},
  "artist_preference_unknowns": [
    {{
      "question": "",
      "why_it_matters": "",
      "affects_paths": []
    }}
  ],
  "profile_confidence": {{
    "high_confidence": [],
    "medium_confidence": [],
    "low_confidence": []
  }},
  "safety_notes": [
    "Do not present interpretations as facts.",
    "Ask the artist before assuming career goals.",
    "Use this profile to suggest possibilities, not define identity."
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
data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

save_json(
    "memory/artist_intelligence.json",
    data
)

print("Saved memory/artist_intelligence.json")