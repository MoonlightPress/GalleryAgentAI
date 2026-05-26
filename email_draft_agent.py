from anthropic import Anthropic
from dotenv import load_dotenv
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
executive_plan = load_text("executive_plan.md")
artist_preferences = load_json("memory/artist_preferences.json", {})
opportunities = load_json("memory/opportunities.json", [])


prompt = f"""
You are Agent N: Outreach Drafting Agent.

Create practical outreach drafts for the artist.

Use:
- artist dossier
- action plan
- executive plan
- opportunities
- artist preferences

Artist dossier:
{artist_dossier}

Action plan:
{action_plan}

Executive plan:
{executive_plan}

Opportunities:
{json.dumps(opportunities, indent=2, ensure_ascii=False)}

Artist preferences:
{json.dumps(artist_preferences, indent=2, ensure_ascii=False)}

Output:

# Email Drafts

Create 5 email drafts:
1. Gallery inquiry
2. Art fair / fair gallery inquiry
3. Print publisher inquiry
4. Cultural center / community exhibition inquiry
5. Collaboration inquiry

For each draft include:
- Use case
- Subject line
- Email body
- What to attach
- What the artist should customize before sending

Rules:
- Do not overstate credentials.
- Do not pretend the artist has representation.
- Do not sound desperate.
- Keep emails short.
- Make the tone sincere, clear, and professional.
- Avoid art-world jargon unless necessary.
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

with open("email_drafts.md", "w", encoding="utf-8") as f:
    f.write(output)

print("\nSaved email_drafts.md")