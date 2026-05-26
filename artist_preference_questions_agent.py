import json
import os


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


intel = load_json(
    "memory/artist_intelligence.json",
    {}
)

unknowns = intel.get(
    "artist_preference_unknowns",
    []
)

starter_questions = [
    {
        "question": "Do you want publishing opportunities, such as zines, artist books, or small press features?",
        "why_it_matters": "This affects whether bookstore and zine opportunities should be ranked highly.",
        "affects_paths": ["publishing", "zines", "bookstores", "artist books"]
    },
    {
        "question": "Do you want local cafe or small wall exhibitions, or do those feel too casual?",
        "why_it_matters": "These can build local visibility, but may not fit every artist's preferred positioning.",
        "affects_paths": ["local visibility", "cafe walls", "community presence"]
    },
    {
        "question": "Do you want to sell directly at booths or markets?",
        "why_it_matters": "Booths can create income and audience feedback, but require social and sales energy.",
        "affects_paths": ["direct sales", "markets", "booths", "merchandise"]
    },
    {
        "question": "Are residencies interesting to you right now?",
        "why_it_matters": "Residencies require more preparation, but can help with research, CV value, and focused work time.",
        "affects_paths": ["residencies", "research", "CV building"]
    },
    {
        "question": "Are licensing or product collaborations a long-term goal?",
        "why_it_matters": "Licensing requires proof of audience, repeatable visual identity, and product-ready work.",
        "affects_paths": ["licensing", "stationery", "calendars", "brand collaborations"]
    },
    {
        "question": "What kinds of opportunities would feel embarrassing, draining, or not worth it?",
        "why_it_matters": "The system should avoid pushing paths that create resistance or misrepresent the artist.",
        "affects_paths": ["all paths"]
    }
]

combined = unknowns + starter_questions

save_json(
    "memory/artist_preference_questions.json",
    {
        "questions": combined
    }
)

print("Saved memory/artist_preference_questions.json")