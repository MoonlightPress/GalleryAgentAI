
import json
import os
from pathlib import Path

PROFILE = "memory/visual_language_profile.json"
OUT = "reports/dataset_readiness.md"

def load(path,fallback):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():

    profile = load(PROFILE,{})

    score = 0

    score += len(profile.get("visual_language",[]))
    score += len(profile.get("recurring_subjects",[]))
    score += len(profile.get("composition_patterns",[]))

    readiness = min(10, round(score / 3,1))

    lines = [
        "# Dataset Readiness",
        "",
        f"Readiness Score: {readiness}/10",
        "",
        "Goal:",
        "- 50-100 images",
        "- recurring motifs",
        "- composition patterns",
        "- emotional register",
        "- portfolio clusters"
    ]

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines),encoding="utf-8")

    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
