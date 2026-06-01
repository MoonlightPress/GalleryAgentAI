
import json
from pathlib import Path

CANDIDATES = "memory/extracted_business_candidates.json"
OUT = "memory/extracted_business_decisions.json"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    data = load(CANDIDATES, {"candidates": []})
    sample = []

    for c in data.get("candidates", [])[:10]:
        sample.append({
            "candidate_id": c["candidate_id"],
            "decision": "skipped",
            "name": c["name"],
            "address": "",
            "website": c.get("website", ""),
            "instagram": "",
            "email": "",
            "phone": "",
            "category": c.get("category", ""),
            "neighborhood": c.get("neighborhood", ""),
            "accepts_consignment": "unknown",
            "accepts_submissions": "unknown",
            "notes": ""
        })

    template = {
        "instructions": "Change decision to approved/rejected/skipped. Approved records with names are ingested into verified_zine_businesses.json.",
        "decisions": sample
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(template, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
