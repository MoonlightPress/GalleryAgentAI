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

for opp in opportunities:

    text = json.dumps(
        opp,
        ensure_ascii=False
    ).lower()

    if opp.get("name") == "Unknown":

        if "tokas" in text:
            opp["name"] = "TOKAS-Emerging"

        elif "kyoto art center" in text:
            opp["name"] = "Kyoto Art Center Residency"

        elif "studio kura" in text:
            opp["name"] = "Studio Kura Residency"

        elif "saruya" in text:
            opp["name"] = "Saruya Residency"

        elif "fujiyoshida" in text:
            opp["name"] = "Fujiyoshida Research Residency"

        elif "asian art contemporary" in text:
            opp["name"] = "Asian Art Contemporary Interview Program"

        elif "tcaa" in text:
            opp["name"] = "Tokyo Contemporary Art Award"

    if opp.get("type") == "unknown":

        if "residency" in text:
            opp["type"] = "residency"

        elif "award" in text:
            opp["type"] = "award"

        elif "interview" in text:
            opp["type"] = "publication"

        elif "exhibition" in text:
            opp["type"] = "open_call"

save_json(
    "memory/opportunities.json",
    opportunities
)

print("Repaired unknown opportunities.")