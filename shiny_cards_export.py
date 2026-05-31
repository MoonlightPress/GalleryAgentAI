
import json
from pathlib import Path

SRC = "memory/opportunity_pitches.json"
OUT = "deploy_data/opportunity_pitches.json"
REPORT = "reports/shiny_opportunity_cards.md"

def main():
    data = json.load(open(SRC, encoding="utf-8"))

    Path("deploy_data").mkdir(exist_ok=True)
    json.dump(data, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = ["# Shiny Opportunity Cards", "", "Short versions for dashboard display.", ""]

    for p in data:
        lines.append(f"## {p['title']}")
        lines.append(f"**Why this one:** {p['fit_paragraph']}")
        lines.append("")
        lines.append(f"**Effort:** {p['effort']}")
        lines.append(f"**Impact:** {p['impact']}")
        lines.append(f"**Next:** {p['next_steps'][0] if p.get('next_steps') else 'Open the opportunity page.'}")
        lines.append(f"**Link:** {p['recommended_url']}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT)
    print("Wrote", REPORT)

if __name__ == "__main__":
    main()
