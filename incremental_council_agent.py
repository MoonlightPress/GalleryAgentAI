import json
import os
import subprocess


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


opportunities = load_json("memory/opportunities.json", [])

needs_review = []
cached = []

for opp in opportunities:
    review = opp.get("council_review")

    if review and review.get("overall_score") is not None:
        cached.append(opp)
    else:
        needs_review.append(opp)

if not needs_review:
    print("No council review needed.")
    raise SystemExit

save_json("memory/opportunities.json", needs_review)

print(f"Reviewing only {len(needs_review)} new opportunities...")

result = subprocess.run(["python", "council_agent.py"])

reviewed = load_json("memory/opportunities.json", [])

combined = cached + reviewed

save_json("memory/opportunities.json", combined)

print(f"Restored full opportunity set: {len(combined)}")