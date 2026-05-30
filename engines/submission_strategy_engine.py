
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/submission_strategies.json"

STRATEGIES = {
    "soft_intro": {
        "tone": "gentle and curious",
        "best_for": [
            "community",
            "artist-run",
            "cafe",
            "bookstore",
        ],
        "advice": [
            "Keep the first message short.",
            "Do not over-explain the work.",
            "Lead with atmosphere and sincerity.",
            "Focus on mutual fit."
        ]
    },

    "publication_pitch": {
        "tone": "focused and editorial",
        "best_for": [
            "photobook",
            "publication",
            "artist book",
            "zine",
            "book fair",
        ],
        "advice": [
            "Present a coherent sequence.",
            "Emphasize visual consistency.",
            "Include sequencing logic.",
            "Mention publication intentions."
        ]
    },

    "formal_application": {
        "tone": "clear and professional",
        "best_for": [
            "grant",
            "residency",
            "museum",
            "institution",
        ],
        "advice": [
            "Be precise.",
            "Answer requirements directly.",
            "Avoid emotional language.",
            "Demonstrate seriousness."
        ]
    },

    "quiet_high_prestige": {
        "tone": "restrained and confident",
        "best_for": [
            "international",
            "prestige",
            "gallery",
        ],
        "advice": [
            "Do not oversell.",
            "Let the work speak.",
            "Keep materials minimal and elegant.",
            "Signal artistic clarity."
        ]
    }
}

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def blob(opp):
    parts = []

    for key in [
        "title",
        "category",
        "category_label",
        "one_sentence",
        "why_this_fits_short",
    ]:
        if opp.get(key):
            parts.append(str(opp.get(key)))

    for tag in opp.get("tags", []):
        parts.append(str(tag))

    return " ".join(parts).lower()

def pick_strategy(text):

    scored = []

    for name, data in STRATEGIES.items():

        score = 0

        for word in data["best_for"]:
            if word.lower() in text:
                score += 1

        scored.append((score, name))

    scored.sort(reverse=True)

    return scored[0][1]

def main():

    opps = load_json(OPP_PATH, [])

    strategies = {}

    for opp in opps:

        text = blob(opp)

        strategy_name = pick_strategy(text)

        strategy = STRATEGIES[strategy_name]

        opp["submission_strategy"] = strategy_name
        opp["submission_tone"] = strategy["tone"]

        strategies[
            opp.get("title", "Unknown")
        ] = {
            "strategy": strategy_name,
            "tone": strategy["tone"],
            "advice": strategy["advice"],
        }

    save_json(
        OPP_PATH,
        opps,
    )

    save_json(
        OUT_PATH,
        strategies,
    )

    print(
        f"Built strategies for {len(opps)} opportunities."
    )

if __name__ == "__main__":
    main()
