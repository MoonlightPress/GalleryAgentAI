import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import os
from dotenv import load_dotenv
from anthropic import Anthropic


load_dotenv(dotenv_path=".env")

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-5"


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def parse_json(text):
    cleaned = text.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)


def rerank_one(profile, opportunity):
    prompt = f"""
You are Agent S: Strategic Opportunity Ranking Agent.

Re-rank this ONE opportunity using the inferred artist profile.

Artist Profile:
{json.dumps(profile, indent=2, ensure_ascii=False)}

Opportunity:
{json.dumps(opportunity, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Return the FULL updated opportunity object.

Add or update:
- fit_score
- strategic_score
- emotional_resistance
- recommendation_tier
- strategic_reasoning

Valid recommendation_tier values:
- ideal_next_step
- stretch_goal
- low_pressure
- avoid_for_now
- prestige_but_costly
- emotionally_sustainable

Rules:
- Emotional sustainability matters heavily.
- Avoid prestige obsession.
- Penalize overwhelming opportunities.
- Reward ecosystem fit.
- Reward realistic momentum.
- Be conservative and nuanced.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}]
    )

    return parse_json(response.content[0].text)


def main():
    profile = load_json("memory/artist_profile.json", {})
    opportunities = load_json("memory/opportunities.json", [])

    reranked = []

    print()
    print("Re-ranking opportunities one by one...")
    print()

    for i, opp in enumerate(opportunities):
        name = opp.get("name", "UNKNOWN")
        print(f"Ranking {i + 1}/{len(opportunities)}: {name}")

        try:
            updated = rerank_one(profile, opp)
            reranked.append(updated)
            print("  OK")
        except Exception as e:
            print(f"  FAILED: {e}")
            opp["ranking_error"] = str(e)
            reranked.append(opp)

    save_json("memory/opportunities.json", reranked)

    print()
    print("Saved reranked opportunities.")
    print()


if __name__ == "__main__":
    main()