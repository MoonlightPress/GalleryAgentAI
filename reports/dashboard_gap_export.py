
import json
from pathlib import Path

SRC = "memory/opportunity_gaps.json"
OUT = "deploy_data/opportunity_gaps.json"

def main():
    data = json.load(open(SRC, encoding="utf-8"))
    Path("deploy_data").mkdir(exist_ok=True)
    json.dump(data, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
