import json
import os
from datetime import datetime


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


contact_memory = load_json(
    "memory/contact_memory.json",
    {"contacts": []}
)

contacts = contact_memory.get("contacts", [])

lines = []
lines.append("# CRM Summary\n")
lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
lines.append(f"Total contacts: {len(contacts)}\n")

for contact in contacts:
    analysis = contact.get("crm_analysis", {})

    lines.append("---\n")
    lines.append(f"## {contact.get('name', 'Unknown')}\n")
    lines.append(f"- Type: {contact.get('type', '')}\n")
    lines.append(f"- City: {contact.get('city', '')}, {contact.get('country', '')}\n")
    lines.append(f"- Status: {contact.get('status', '')}\n")
    lines.append(f"- Priority: {analysis.get('priority', '')}\n")
    lines.append(f"- Relationship stage: {analysis.get('relationship_stage', '')}\n")
    lines.append(f"- Recommended status: {analysis.get('recommended_status', '')}\n")
    lines.append(f"- Follow-up timing: {analysis.get('follow_up_timing', '')}\n")
    lines.append(f"- Next action: {analysis.get('next_action', '')}\n")
    lines.append(f"- Risk notes: {analysis.get('risk_notes', '')}\n")
    web = contact.get("web_verification", {})

    lines.append(f"- Official website: {contact.get('official_website', '')}\n")
    lines.append(f"- Contact page: {contact.get('contact_page', '')}\n")
    lines.append(f"- Submission page: {contact.get('submission_page', '')}\n")
    lines.append(f"- Contact email: {contact.get('contact_email', '')}\n")
    lines.append(f"- Instagram: {web.get('instagram', '')}\n")
    lines.append(f"- Web verification status: {web.get('verification_status', '')}\n")
    lines.append(f"- Last verified: {web.get('last_verified', '')}\n") 

with open("crm_summary.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\n".join(lines))
print("\nSaved crm_summary.md")