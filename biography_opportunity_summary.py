
import json
from pathlib import Path
from collections import defaultdict

SRC = "memory/artist_biographies.json"
OUT = "reports/biography_opportunity_summary.md"

def main():
    bios = json.load(open(SRC, encoding="utf-8")) if Path(SRC).exists() else []
    by_opp = defaultdict(list)

    for b in bios:
        by_opp[b["source_opportunity"]].append(b)

    lines = [
        "# Biography Opportunity Summary",
        "",
        "Shows which opportunities have real artist biography evidence.",
        "",
    ]

    for opp, rows in sorted(by_opp.items(), key=lambda x: len(x[1]), reverse=True):
        lines.append(f"## {opp}")
        lines.append(f"- Biography count: {len(rows)}")
        lines.append("")
        for b in rows[:10]:
            lines.append(f"- {b['artist_name']} — {', '.join(b['roles'])}")
        lines.append("")

    if not by_opp:
        lines.append("_No biography evidence found yet._")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
