import json
import os
from datetime import datetime


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


opps = load_json("memory/compact_opportunities.json", [])
pathways = load_json("memory/pathway_progress.json", {"pathways": []})


def score(opp):
    base = float(opp.get("overall_score", 0) or 0)

    difficulty = str(opp.get("difficulty", "")).lower()

    if "low" in difficulty or "easy" in difficulty:
        base += 1.5
    elif "medium" in difficulty or "moderate" in difficulty:
        base += 0.5
    elif "high" in difficulty:
        base -= 1.0

    if opp.get("source_url") or opp.get("official_website"):
        base += 0.75

    return base


ranked = sorted(opps, key=score, reverse=True)

today = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "headline": "Today's gentle starting points",
    "featured_opportunities": ranked[:5],
    "suggested_focus": [],
    "pathway_status": pathways.get("pathways", [])
}

for path in pathways.get("pathways", []):
    percent = path.get("percent_complete", 0)

    if percent < 40:
        today["suggested_focus"].append({
            "pathway": path.get("name"),
            "message": "Build the base materials first.",
            "percent_complete": percent
        })
    elif percent < 80:
        today["suggested_focus"].append({
            "pathway": path.get("name"),
            "message": "This path is forming. One or two tasks may unlock stronger opportunities.",
            "percent_complete": percent
        })
    else:
        today["suggested_focus"].append({
            "pathway": path.get("name"),
            "message": "This path is nearly ready for higher-value outreach.",
            "percent_complete": percent
        })

save_json("memory/daily_suggestions.json", today)

print("Saved memory/daily_suggestions.json")