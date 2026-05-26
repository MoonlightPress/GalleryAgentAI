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


system_journal = load_json("memory/system_journal.json", {})
artist_preferences = load_json("memory/artist_preferences.json", {})
opportunities = load_json("memory/opportunities.json", [])

artist_dossier = load_text("artist_dossier.md")
quest_report = load_text("quest_report.md")
recommendation_report = load_text("recommendation_report.md")
action_plan = load_text("action_plan.md")


prompt = f"""
You are Agent L: Executive Focus Agent.

Your job:
Reduce all available strategy into a small action plan.

You are NOT a brainstorming agent.
You are NOT allowed to add new strategy unless required.
You must suppress overwhelm.

Use:
- system journal
- artist dossier
- quest report
- recommendation report
- action plan
- artist preferences
- opportunities

System journal:
{json.dumps(system_journal, indent=2, ensure_ascii=False)}

Artist preferences:
{json.dumps(artist_preferences, indent=2, ensure_ascii=False)}

Opportunities:
{json.dumps(opportunities, indent=2, ensure_ascii=False)}

Artist dossier:
{artist_dossier}

Quest report:
{quest_report}

Recommendation report:
{recommendation_report}

Action plan:
{action_plan}

Return ONLY valid JSON.

Format:

{{
  "executive_summary": "",
  "do_now": [
    {{
      "task": "",
      "time_required": "",
      "why_it_matters": "",
      "success_condition": ""
    }}
  ],
  "do_this_week": [
    {{
      "task": "",
      "time_required": "",
      "why_it_matters": "",
      "success_condition": ""
    }}
  ],
  "do_later": [
    {{
      "task": "",
      "why_not_now": ""
    }}
  ],
  "blocked_until_we_know": [
    {{
      "unknown": "",
      "why_it_blocks_progress": ""
    }}
  ],
  "ignore_for_now": [
    {{
      "item": "",
      "reason": ""
    }}
  ]
}}

Rules:
- Maximum 3 items in do_now.
- Maximum 3 items in do_this_week.
- Maximum 5 items in do_later.
- Be blunt.
- Prefer action over analysis.
- Do not create a long list.
- If something is interesting but distracting, put it in ignore_for_now.
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

with open("executive_plan.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, indent=2, ensure_ascii=False)

with open("executive_plan.md", "w", encoding="utf-8") as f:
    f.write("# Executive Plan\n\n")
    f.write("## Summary\n")
    f.write(parsed["executive_summary"] + "\n\n")

    f.write("## Do Now\n")
    for item in parsed["do_now"]:
        f.write(f"- **{item['task']}** ({item['time_required']})\n")
        f.write(f"  - Why: {item['why_it_matters']}\n")
        f.write(f"  - Done when: {item['success_condition']}\n")

    f.write("\n## Do This Week\n")
    for item in parsed["do_this_week"]:
        f.write(f"- **{item['task']}** ({item['time_required']})\n")
        f.write(f"  - Why: {item['why_it_matters']}\n")
        f.write(f"  - Done when: {item['success_condition']}\n")

    f.write("\n## Do Later\n")
    for item in parsed["do_later"]:
        f.write(f"- **{item['task']}**\n")
        f.write(f"  - Not now: {item['why_not_now']}\n")

    f.write("\n## Blocked Until We Know\n")
    for item in parsed["blocked_until_we_know"]:
        f.write(f"- **{item['unknown']}**\n")
        f.write(f"  - Why it blocks progress: {item['why_it_blocks_progress']}\n")

    f.write("\n## Ignore For Now\n")
    for item in parsed["ignore_for_now"]:
        f.write(f"- **{item['item']}**\n")
        f.write(f"  - Reason: {item['reason']}\n")

print("\nSaved executive_plan.json and executive_plan.md")