from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime
import os
import json

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
action_plan = load_text("action_plan.md")
collaboration_report = load_text("collaboration_report.md")
artist_preferences = load_json("memory/artist_preferences.json", {})

prompt = f"""
You are Agent F: Artist Career Quest Designer.

Create a small, non-overwhelming quest list for this artist.

Use:
- the artist dossier
- action plan
- collaboration report
- artist preferences

Artist dossier:
{artist_dossier}

Action plan:
{action_plan}

Collaboration report:
{collaboration_report}

Artist preferences:
{json.dumps(artist_preferences, indent=2, ensure_ascii=False)}

Output exactly these sections:

# Daily Quests
Give 5 tiny actions, each 5-15 minutes.

# Weekly Quests
Give 5 medium actions, each 30-90 minutes.

# Major Quests
Give 3 larger career-building actions.

# Reflection Quests
Give 5 prompts that help improve the artist profile.

# System Improvement Requests
Give 5 things the artist could provide to improve future recommendations.

Rules:
- Do not overwhelm.
- Make each quest concrete.
- Include why each quest matters.
- Do not suggest sending emails unless the action plan supports it.
- No fake motivation language.

You MUST adapt the quests to:
- the artist's emotional temperament
- tolerance for self-promotion
- desire for authentic community
- preference for slow growth vs aggressive commercialization

Avoid:
- hustle culture advice
- generic startup energy
- over-commercialization
- pushing scale too quickly
"""

response = client.messages.create(
    model=MODEL,
    max_tokens=3000,
    messages=[{"role": "user", "content": prompt}]
)

quest_report = response.content[0].text

print(quest_report)

with open("quest_report.md", "w", encoding="utf-8") as f:
    f.write(quest_report)

memory_entry = {
    "date_created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "quest_report_file": "quest_report.md",
    "status": "quest_generation_complete"
}

with open("memory/latest_quest_run.json", "w", encoding="utf-8") as f:
    json.dump(memory_entry, f, indent=2, ensure_ascii=False)

print("\nSaved quest_report.md")