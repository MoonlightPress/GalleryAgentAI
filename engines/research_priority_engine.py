
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/research_priority_queue.json"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def missing_count(opp):
    missing = 0

    for key in [
        "submission_page",
        "fees",
        "deadline",
        "contact_email",
        "official_website",
    ]:
        if not opp.get(key):
            missing += 1

    return missing


def research_score(opp):

    overall = float(
        opp.get("overall_score", 0) or 0
    )

    prestige = float(
        opp.get("prestige_score", 0) or 0
    )

    missing = missing_count(opp)

    global_bonus = 0

    country = str(
        opp.get("country", "")
    ).lower()

    if country not in ["", "japan"]:
        global_bonus = 1.5

    return round(
        overall
        + (prestige * 0.35)
        + global_bonus
        + (missing * 0.4),
        2,
    )


def build_item(opp):

    missing_fields = []

    for key in [
        "submission_page",
        "fees",
        "deadline",
        "contact_email",
        "official_website",
    ]:
        if not opp.get(key):
            missing_fields.append(key)

    return {
        "title": opp.get("title"),
        "score": opp.get("overall_score"),
        "research_priority_score": research_score(opp),
        "country": opp.get("country"),
        "category": opp.get("category"),
        "missing_fields": missing_fields,
        "quick_action": opp.get(
            "quick_action",
            "",
        ),
    }


def main():

    opps = load_json(OPP_PATH, [])

    ranked = sorted(
        opps,
        key=research_score,
        reverse=True,
    )

    queue = [
        build_item(x)
        for x in ranked[:40]
    ]

    save_json(OUT_PATH, queue)

    print(
        f"Built research queue: {len(queue)} items"
    )


if __name__ == "__main__":
    main()
