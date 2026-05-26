from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv(dotenv_path=".env")

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-5"


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_text(path, fallback=""):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


artist_graph = load_json("memory/artist_graph.json", {})
artist_preferences = load_json("memory/artist_preferences.json", {})
opportunities = load_json("memory/opportunities.json", [])

artist_dossier = load_text("artist_dossier.md")
quest_report = load_text("quest_report.md")


prompt = f"""
You are Agent I: Career Recommendation Engine.

Generate useful recommendations automatically.

Use:
- artist graph
- opportunities
- artist preferences
- artist dossier
- quest report

Artist graph:
{json.dumps(artist_graph, indent=2, ensure_ascii=False)}

Opportunities:
{json.dumps(opportunities, indent=2, ensure_ascii=False)}

Artist preferences:
{json.dumps(artist_preferences, indent=2, ensure_ascii=False)}

Artist dossier:
{artist_dossier}

Quest report:
{quest_report}

Output sections:

# Recommended Collaborators
Give 3 artists worth researching immediately.

# Recommended Cities
Give 3 cities worth focusing on now.

# Recommended Group Shows
Give 3 strong show concepts.

# Recommended Opportunities
Give 5 high-value opportunities.

# Low-Effort Wins
Give 5 small things the artist could do this week.

# Long-Term Strategic Directions
Give 3 larger trajectories worth developing over 1-3 years.

Rules:
- Prefer specificity.
- Avoid generic hustle advice.
- Prioritize emotional sustainability.
- Do not recommend everything.
- Curate aggressively.
- Explain why each recommendation matters.
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

with open("recommendation_report.md", "w", encoding="utf-8") as f:
    f.write(output)

print("\nSaved recommendation_report.md")