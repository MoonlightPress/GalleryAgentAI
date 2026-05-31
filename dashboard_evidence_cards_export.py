
import json
from pathlib import Path

SOURCES = [
    ("memory/relevance_scores.json", "deploy_data/relevance_scores.json"),
    ("memory/opportunity_evidence_cards.json", "deploy_data/opportunity_evidence_cards.json"),
]

def main():
    Path("deploy_data").mkdir(exist_ok=True)
    for src, out in SOURCES:
        if Path(src).exists():
            data = json.load(open(src, encoding="utf-8"))
            json.dump(data, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            print("Wrote", out)
        else:
            print("Missing", src)

if __name__ == "__main__":
    main()
