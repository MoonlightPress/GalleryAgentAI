
import json
from pathlib import Path

SRC = "memory/normalized_opportunities.json"
OUT = "memory/normalized_opportunity_decisions.json"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    data = load(SRC, {})
    decisions = []
    for o in data.get("opportunities", []):
        decisions.append({
            "canonical_name": o["canonical_name"],
            "decision": "skipped",
            "category": o.get("category", ""),
            "neighborhood": o.get("neighborhood", ""),
            "confidence": o.get("confidence", 0),
            "website": o.get("websites", [""])[0] if o.get("websites") else "",
            "instagram": "",
            "address": "",
            "accepts_consignment": "unknown",
            "accepts_submissions": "unknown",
            "notes": "",
        })

    Path("memory").mkdir(exist_ok=True)
    json.dump({
        "instructions": "Change decision to approved/rejected/skipped after review.",
        "decisions": decisions
    }, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print("Wrote", OUT)

if __name__ == "__main__":
    main()
