
import json
from pathlib import Path

SRC = "memory/dna_matches.json"
OUT = "reports/top_10_because.md"

def main():
    data = json.load(open(SRC, encoding="utf-8"))
    top = [x for x in data if x.get("verdict") in {"strong_match", "promising_match"}][:10]

    lines = [
        "# Top 10 Opportunities Because...",
        "",
        "Short advisor-style explanation of the best current targets.",
        "",
    ]

    for i, item in enumerate(top, 1):
        lines.append(f"## {i}. {item['title']}")
        lines.append(f"- Score: {item['dna_match_score']}/10")
        lines.append(f"- Type: {item['opportunity_type']}")
        lines.append(f"- Best link: {item.get('best_link')}")
        lines.append("")
        lines.append("**Because:**")
        for r in item.get("reasons", [])[:4]:
            lines.append(f"- {r}")
        if item.get("risks"):
            lines.append("")
            lines.append("**But first:**")
            for r in item.get("risks", [])[:3]:
                lines.append(f"- {r}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
