
import json
from pathlib import Path

OUT = "memory/candidate_business_decisions.json"

TEMPLATE = {
    "decisions": [
        {
            "candidate_id": "CAND-0001",
            "decision": "approved",
            "name": "",
            "address": "",
            "website": "",
            "instagram": "",
            "email": "",
            "phone": "",
            "category": "",
            "neighborhood": "",
            "accepts_consignment": "unknown",
            "accepts_submissions": "unknown",
            "notes": ""
        }
    ]
}

def main():
    Path("memory").mkdir(exist_ok=True)
    if not Path(OUT).exists():
        json.dump(TEMPLATE, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print("Wrote", OUT)
    else:
        print("Already exists:", OUT)

if __name__ == "__main__":
    main()
