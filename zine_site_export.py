
import json
from pathlib import Path

SOURCES = [
    ("memory/tokyo_zine_ecosystem.json", "tokyo_zine_ecosystem.json"),
    ("memory/zine_section_summary.json", "zine_section_summary.json"),
]

def main():
    Path("deploy_data").mkdir(exist_ok=True)
    for src, out_name in SOURCES:
        p = Path(src)
        if p.exists():
            data = json.load(open(p, encoding="utf-8"))
            json.dump(data, open(Path("deploy_data") / out_name, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            print("Wrote", Path("deploy_data") / out_name)
        else:
            print("Missing", src)

if __name__ == "__main__":
    main()
