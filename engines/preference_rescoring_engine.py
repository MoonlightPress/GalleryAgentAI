
import json
import os
from pathlib import Path

from feedback_learning_engine import tokens_from_opp

OPP_PATH = "deploy_data/compact_opportunities.json"
LEARNED_PROFILE_PATH = "memory/learned_artist_preferences.json"
BACKUP_PATH = "deploy_data/compact_opportunities_before_preference_rescore.json"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def preference_adjustment(opp, weights):
    total = 0.0
    hits = []

    for token in tokens_from_opp(opp):
        if token in weights:
            weight = float(weights[token])
            total += weight
            hits.append((token, weight))

    total = max(-2.0, min(2.0, total))
    return round(total, 2), hits[:8]


def main():
    opps = load_json(OPP_PATH, [])
    learned = load_json(LEARNED_PROFILE_PATH, {})
    weights = learned.get("preference_weights", {})

    if not opps:
        raise SystemExit("No opportunities found.")

    if not weights:
        print("No learned preference weights yet. Run feedback_learning_engine.py after using relationship states.")
        return

    if not os.path.exists(BACKUP_PATH):
        save_json(BACKUP_PATH, opps)

    for opp in opps:
        base = float(opp.get("overall_score", 0) or 0)
        adjustment, hits = preference_adjustment(opp, weights)

        opp["preference_adjustment"] = adjustment
        opp["preference_signal_hits"] = hits
        opp["overall_score"] = round(max(0, min(10, base + adjustment)), 2)

    opps.sort(key=lambda x: float(x.get("overall_score", 0) or 0), reverse=True)

    save_json(OPP_PATH, opps)

    print(f"Preference-rescored {len(opps)} opportunities.")


if __name__ == "__main__":
    main()
