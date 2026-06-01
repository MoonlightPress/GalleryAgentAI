
import json
from pathlib import Path

SRC = "memory/actionable_targets.json"
OUT = "deploy_data/actionable_targets.json"
REPORT = "reports/actionable_targets_export_report.md"

def main():
    p = Path(SRC)
    if not p.exists():
        raise SystemExit("Run actionable_target_builder.py first.")

    data = json.load(open(SRC, encoding="utf-8"))

    Path("deploy_data").mkdir(exist_ok=True)
    json.dump(data, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Actionable Targets Export",
        "",
        f"Exported records: {len(data)}",
        "",
        f"Output: `{OUT}`",
        "",
    ]

    for item in data:
        lines.append(f"- {item.get('title')} — {item.get('status')} — confidence {item.get('confidence')}")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT)
    print("Wrote", REPORT)

if __name__ == "__main__":
    main()
