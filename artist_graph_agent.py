from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv(dotenv_path=".env")

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
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
artist_graph = load_json("memory/artist_graph.json", {
    "artists": [],
    "connections": [],
    "group_show_ideas": [],
    "shared_themes": []
})

prompt = f"""
You are Agent H: Artist Graph Builder.

Convert the collaboration report into structured graph data.

Artist dossier:
{artist_dossier}

Collaboration report:
{collaboration_report}

Existing artist graph:
{json.dumps(artist_graph, indent=2, ensure_ascii=False)}

Return ONLY valid JSON with this structure:

{{
  "artists": [
    {{
      "name": "",
      "medium": "",
      "city_or_region": "",
      "country": "",
      "why_relevant": "",
      "fit_score": 0,
      "confidence_score": 0,
      "verification_needed": true,
      "search_terms": []
    }}
  ],
  "connections": [
    {{
      "source": "Target Artist",
      "target": "",
      "relationship_type": "",
      "shared_themes": [],
      "reason": "",
      "confidence_score": 0
    }}
  ],
  "group_show_ideas": [
    {{
      "title": "",
      "concept": "",
      "ideal_artist_types": [],
      "possible_cities": [],
      "fit_score": 0
    }}
  ],
  "shared_themes": []
}}

Rules:
- Do not invent certainty.
- If an artist name needs verification, set verification_needed to true.
- Scores are 0-10.
- Confidence is 0-1.
"""

response = client.messages.create(
    model=MODEL,
    max_tokens=7500,
    messages=[{"role": "user", "content": prompt}]
)

output = response.content[0].text

print(output)

# REMOVE MARKDOWN FENCES
cleaned = output.replace("```json", "").replace("```", "").strip()

# TRY TO PARSE
parsed = json.loads(cleaned)

with open("memory/artist_graph.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, indent=2, ensure_ascii=False)

with open("artist_graph_report.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, indent=2, ensure_ascii=False)

print("\nSaved memory/artist_graph.json")