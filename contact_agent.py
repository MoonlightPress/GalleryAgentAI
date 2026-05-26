print("COUNCIL AGENT FILE LOADED")
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json
print("STARTING COUNCIL AGENT")
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
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


contact_memory = load_json(
    "memory/contact_memory.json",
    {
        "contacts": []
    }
)

new_contact = load_json(
    "contact_entry.json",
    {}
)

if not new_contact:
    raise Exception("contact_entry.json is empty or missing.")

now = datetime.now().strftime("%Y-%m-%d %H:%M")
new_contact["date_updated"] = now

existing_index = None

for i, contact in enumerate(contact_memory["contacts"]):
    if contact.get("name", "").lower() == new_contact.get("name", "").lower():
        existing_index = i
        break

if existing_index is not None:
    old_contact = contact_memory["contacts"][existing_index]
    old_contact.update(new_contact)
    contact_memory["contacts"][existing_index] = old_contact
else:
    new_contact["date_added"] = now
    contact_memory["contacts"].append(new_contact)

prompt = f"""
You are Agent O: Artist Outreach CRM Agent.

Analyze this new contact entry and decide how it should be tracked.

New contact:
{json.dumps(new_contact, indent=2, ensure_ascii=False)}

Existing contact memory:
{json.dumps(contact_memory, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Format:

{{
  "contact_summary": "",
  "relationship_stage": "",
  "recommended_status": "",
  "follow_up_timing": "",
  "next_action": "",
  "risk_notes": "",
  "priority": ""
}}

Allowed relationship_stage values:
- not_contacted
- ready_to_contact
- contacted
- responded_positive
- responded_neutral
- responded_negative
- follow_up_later
- closed

Allowed priority values:
- A
- B
- C
"""

response = client.messages.create(
    model=MODEL,
    max_tokens=1200,
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
analysis = json.loads(cleaned)

if existing_index is not None:
    contact_memory["contacts"][existing_index]["crm_analysis"] = analysis
else:
    contact_memory["contacts"][-1]["crm_analysis"] = analysis

save_json(
    "memory/contact_memory.json",
    contact_memory
)

print("\nSaved memory/contact_memory.json")