
import json
from pathlib import Path

SRC = "memory/application_packets.json"
OUT = "reports/artist_daily_tasks.md"

def main():
    packets = json.load(open(SRC, encoding="utf-8"))

    lines = [
        "# Artist Daily Tasks",
        "",
        "Small, practical tasks derived from the application packets.",
        "",
    ]

    task_id = 1
    for p in packets:
        lines.append(f"## {p['title']}")
        lines.append("")

        # Always propose a tiny first task.
        for task in p.get("must_do_first", [])[:2]:
            lines.append(f"{task_id}. {task}")
            task_id += 1

        # Add preparation tasks.
        for item in p.get("packet_items", [])[:5]:
            if not item.get("confirmed"):
                lines.append(f"{task_id}. Prepare: {item.get('item')}")
                task_id += 1

        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
