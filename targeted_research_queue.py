
import json
from pathlib import Path

SRC = "memory/opportunity_gaps.json"
OUT = "reports/targeted_research_queue.md"

def main():
    rows = json.load(open(SRC, encoding="utf-8"))

    lines = [
        "# Targeted Research Queue",
        "",
        "Do these in order. Each task is chosen because it should improve the usefulness of the opportunity record.",
        "",
    ]

    n = 1
    for r in rows:
        gaps = r.get("gaps", [])
        if not gaps:
            continue

        lines.append(f"## {r['title']}")
        lines.append(f"- Current quality: {r['current_quality']}/100")
        lines.append(f"- Best projected score: {r['projected_score_if_fixed']}/100")
        lines.append("")

        for g in gaps[:3]:
            lines.append(f"{n}. {g['description']}")
            n += 1

        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
