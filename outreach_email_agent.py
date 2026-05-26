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


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


artist_dossier = load_text("artist_dossier.md")
artist_preferences = load_json("memory/artist_preferences.json", {})
opportunities = load_json("memory/opportunities.json", [])

if not opportunities:
    raise Exception("No opportunities found in memory/opportunities.json")

import sys

index = 0

if len(sys.argv) > 1:
    index = int(sys.argv[1])

opportunity = opportunities[index]

prompt = f"""
You are Agent P: Multilingual Outreach Email Agent.

Your job:
Create outreach materials for this opportunity.

You must generate THREE layers:

1. artist_summary_zh
A Simplified Chinese summary for the artist.
This should explain:
- what the opportunity is
- why it may fit
- what she should check
- what she needs to prepare
Tone: clear, calm, practical, not salesy.

2. debug_summary_en
An English explanation for the system builder to review.
This should explain:
- why the email is framed this way
- what assumptions were made
- what needs human verification

3. outreach_email_target_language
A draft email in the correct language for the opportunity.
Choose the language based on the opportunity country.
Examples:
- Japan: Japanese
- USA / UK / Canada / Australia: English
- France: French
- China: Simplified Chinese
- Taiwan / Hong Kong: Traditional Chinese unless the opportunity clearly uses Simplified Chinese
- Korea: Korean
If uncertain, choose English and explain uncertainty in debug_summary_en.

Also include:
4. outreach_email_en_translation
English translation of the target-language email for review.

Opportunity:
{json.dumps(opportunity, indent=2, ensure_ascii=False)}

Artist dossier:
{artist_dossier}

Artist preferences:
{json.dumps(artist_preferences, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Format:

{{
  "opportunity_name": "",
  "target_country": "",
  "target_language": "",
  "artist_summary_zh": "",
  "debug_summary_en": "",
  "email_subject_target_language": "",
  "outreach_email_target_language": "",
  "email_subject_en_translation": "",
  "outreach_email_en_translation": "",
  "attachment_checklist_zh": [],
  "attachment_checklist_en": [],
  "customization_notes_zh": [],
  "customization_notes_en": [],
  "human_verification_needed": []
}}

Rules:
- Do not invent credentials.
- Do not claim representation.
- Do not claim sales history unless provided.
- Do not sound desperate.
- Keep the email short.
- The email should be suitable for copy/paste after human review.
- If submission policy is unknown, the email should be framed as a polite inquiry, not a formal submission.
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

opportunity["multilingual_outreach"] = parsed
opportunity["outreach_generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

opportunities[index] = opportunity

save_json("memory/opportunities.json", opportunities)

with open("multilingual_outreach_preview.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, indent=2, ensure_ascii=False)

print("\nSaved multilingual outreach to memory/opportunities.json")
print("Saved preview to multilingual_outreach_preview.json")