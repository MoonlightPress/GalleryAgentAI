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


def save_json(path, data):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def infer_artist_profile(
    dossier,
    opportunities
):

    prompt = f"""
You are Agent P: Artist Profile Inference Agent.

Your job:
Infer a psychologically and strategically useful artist profile.

You are NOT creating objective truth.
You are creating:
- working assumptions
- confidence-weighted interpretations
- useful strategic modeling

Artist Dossier:
{dossier}

Current Opportunities:
{json.dumps(opportunities, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Schema:

{{
  "artist_name": "",
  "primary_mediums": [],
  "secondary_mediums": [],
  "themes": [],
  "visual_keywords": [],
  "career_stage": "",
  "institutional_fit": 1,
  "alternative_scene_fit": 1,
  "social_energy": 1,
  "travel_willingness": 1,
  "language_comfort": {{
    "english": 1,
    "japanese": 1,
    "chinese": 1
  }},
  "emotional_tolerance": {{
    "competitive_applications": 1,
    "cold_outreach": 1,
    "public_exposure": 1,
    "networking_events": 1
  }},
  "preferred_opportunity_types": [],
  "avoidance_patterns": [],
  "strategic_strengths": [],
  "strategic_risks": [],
  "recommended_next_steps": [],
  "confidence_notes": []
}}

Rules:
- Use 1-10 scoring conservatively.
- Avoid exaggerated confidence.
- Infer emotional/workflow patterns carefully.
- Prioritize practical usefulness.
- Do not invent biography.
- Focus on actionable modeling.
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

    cleaned = (
        output
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(cleaned)


def main():

    dossier = load_text(
        "artist_dossier.md"
    )

    opportunities = load_json(
        "memory/opportunities.json",
        []
    )

    print()
    print("Inferring artist profile...")
    print()

    profile = infer_artist_profile(
        dossier,
        opportunities
    )

    save_json(
        "memory/artist_profile.json",
        profile
    )

    print("Saved memory/artist_profile.json")
    print()


if __name__ == "__main__":
    main()