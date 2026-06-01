
import json
from pathlib import Path

SOURCES = [
    ("memory/category_metrics.json", "category_metrics.json"),
    ("memory/zine_battle_plan_metrics.json", "zine_battle_plan_metrics.json"),
    ("memory/zine_website_section_final.json", "zine_website_section_final.json"),
]

def main():
    Path("deploy_data").mkdir(exist_ok=True)
    for src, name in SOURCES:
        p = Path(src)
        if p.exists():
            data = json.load(open(p, encoding="utf-8"))
            json.dump(data, open(Path("deploy_data") / name, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            print("Wrote", Path("deploy_data") / name)
        else:
            print("Missing", src)

if __name__ == "__main__":
    main()
