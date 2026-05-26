from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv(dotenv_path=".env")

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

MODEL = "claude-sonnet-4-5"


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


feedback_memory = load_json(
    "memory/feedback_memory.json",
    {
        "platform_results": [],
        "gallery_responses": [],
        "collector_responses": [],
        "sales": [],
        "engagement_patterns": [],
        "pricing_feedback": [],
        "lessons": []
    }
)


entry = load_json(
    "feedback_entry.json",
    {}
)

entry["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")


feedback_type = entry.get("type", "general")


if feedback_type == "sale":
    feedback_memory["sales"].append(entry)

elif feedback_type == "gallery":
    feedback_memory["gallery_responses"].append(entry)

elif feedback_type == "collector":
    feedback_memory["collector_responses"].append(entry)

elif feedback_type == "pricing":
    feedback_memory["pricing_feedback"].append(entry)

elif feedback_type == "engagement":
    feedback_memory["engagement_patterns"].append(entry)

else:
    feedback_memory["platform_results"].append(entry)


prompt = f"""
You are Agent M: Reality Feedback Synthesizer.

Analyze this real-world feedback.

Feedback:
{json.dumps(entry, indent=2, ensure_ascii=False)}

Existing feedback memory:
{json.dumps(feedback_memory, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Format:

{{
  "lesson": "",
  "strategic_adjustment": "",
  "confidence_impact": "",
  "emotional_warning": "",
  "next_best_action": ""
}}
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

parsed = json.loads(cleaned)

feedback_memory["lessons"].append({
    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "feedback": entry,
    "analysis": parsed
})

save_json(
    "memory/feedback_memory.json",
    feedback_memory
)

print("\nSaved memory/feedback_memory.json")