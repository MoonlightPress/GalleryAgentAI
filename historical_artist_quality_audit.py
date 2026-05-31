
import json
from pathlib import Path

SRC = "memory/historical_artist_data_v2.json"
OUT = "reports/historical_artist_quality_audit.md"

def main():
    data = json.load(open(SRC, encoding="utf-8"))
    total = sum(x.get("real_entity_count", 0) for x in data)

    lines = [
        "# Historical Artist Quality Audit",
        "",
        f"- Total entities found: {total}",
        "",
    ]

    for item in data:
        count = item.get("real_entity_count", 0)
        status = "good" if count >= 10 else "partial" if count >= 3 else "weak"
        lines.append(f"## {item.get('title')}")
        lines.append(f"- Status: {status}")
        lines.append(f"- Entity count: {count}")
        if status == "weak":
            lines.append("- Next: find better archive/winner/exhibitor pages.")
        elif status == "partial":
            lines.append("- Next: improve extraction from found pages.")
        else:
            lines.append("- Next: run similarity scoring against artist DNA.")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
