import json
import os


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


opportunities = load_json(
    "memory/opportunities.json",
    []
)

normalized = []

print()
print("NORMALIZING OPPORTUNITIES")
print()

for opp in opportunities:

    if not opp.get("name"):
        opp["name"] = (
            opp.get("title")
            or opp.get("opportunity_name")
            or opp.get("organization")
            or "Unknown"
        )

    if not opp.get("type"):
        opp["type"] = (
            opp.get("category")
            or opp.get("opportunity_type")
            or "unknown"
        )

    if not opp.get("city"):
        opp["city"] = (
            opp.get("location")
            or ""
        )

    normalized.append(opp)

    print(f"NORMALIZED: {opp['name']}")

save_json(
    "memory/opportunities.json",
    normalized
)

print()
print("Saved normalized opportunities.")