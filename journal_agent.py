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


system_journal = load_json(
    "memory/system_journal.json",
    {
        "runs": [],
        "successful_patterns": [],
        "failed_patterns": [],
        "emerging_themes": [],
        "important_discoveries": []
    }
)

artist_dossier = load_text("artist_dossier.md")
recommendation_report = load_text("recommendation_report.md")
quest_report = load_text("quest_report.md")
collaboration_report = load_text("collaboration_report.md")


prompt = f"""
You are Agent J: System Memory Analyst.

Your job:
Analyze the CURRENT state of the system.

Identify:
- recurring themes
- strong directions
- weak assumptions
- emerging strategic identity
- opportunities that repeatedly appear
- emotional patterns
- market positioning patterns

Current system journal:
{json.dumps(system_journal, indent=2, ensure_ascii=False)}

Artist dossier:
{artist_dossier}

Recommendation report:
{recommendation_report}

Quest report:
{quest_report}

Collaboration report:
{collaboration_report}

Return ONLY valid JSON.

Format:

{{
  "run_summary": {{
    "date": "",
    "major_direction": "",
    "emerging_identity": "",
    "strongest_market": "",
    "biggest_risk": "",
    "most_promising_city": "",
    "most_promising_collaborator_type": ""
  }},
  "successful_patterns": [],
  "failed_patterns": [],
  "emerging_themes": [],
  "important_discoveries": []
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

output = response.content[0].text

print(output)

cleaned = output.replace("```json", "").replace("```", "").strip()

parsed = json.loads(cleaned)

system_journal["runs"].append(parsed["run_summary"])

system_journal["successful_patterns"].extend(
    parsed["successful_patterns"]
)

system_journal["failed_patterns"].extend(
    parsed["failed_patterns"]
)

system_journal["emerging_themes"].extend(
    parsed["emerging_themes"]
)

system_journal["important_discoveries"].extend(
    parsed["important_discoveries"]
)

with open("memory/system_journal.json", "w", encoding="utf-8") as f:
    json.dump(system_journal, f, indent=2, ensure_ascii=False)

print("\nUpdated memory/system_journal.json")