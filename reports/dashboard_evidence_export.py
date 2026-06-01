
import json
from pathlib import Path

SOURCES = [
    ("memory/opportunity_evidence.json", "deploy_data/opportunity_evidence.json"),
    ("memory/opportunity_quality_board.json", "deploy_data/opportunity_quality_board.json"),
]

def main():
    Path("deploy_data").mkdir(exist_ok=True)
    for src, out in SOURCES:
        data = json.load(open(src, encoding="utf-8"))
        json.dump(data, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print("Wrote", out)

if __name__ == "__main__":
    main()
