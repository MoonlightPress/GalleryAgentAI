import json
import os
from datetime import datetime


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


opportunities = load_json(
    "memory/opportunities.json",
    []
)

new_opportunity = load_json(
    "opportunity_entry.json",
    {}
)

if not new_opportunity:
    raise Exception("opportunity_entry.json is empty or missing.")

now = datetime.now().strftime("%Y-%m-%d %H:%M")
new_opportunity["date_updated"] = now

existing_index = None

for i, opp in enumerate(opportunities):
    if opp.get("name", "").lower() == new_opportunity.get("name", "").lower():
        existing_index = i
        break

if existing_index is not None:
    old_opp = opportunities[existing_index]
    old_opp.update(new_opportunity)
    opportunities[existing_index] = old_opp
else:
    new_opportunity["date_added"] = now
    opportunities.append(new_opportunity)

save_json(
    "memory/opportunities.json",
    opportunities
)

print(f"Saved opportunity: {new_opportunity.get('name', 'Unnamed')}")
print("Updated memory/opportunities.json")