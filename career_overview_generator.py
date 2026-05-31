
import json
from pathlib import Path

CHANNELS = "memory/career_channels.json"
PLANS = "memory/career_battle_plans.json"
OUT_JSON = "memory/career_overview.json"
OUT_REPORT = "reports/career_overview.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    channels = load(CHANNELS, [])
    plans = load(PLANS, [])

    overview = {
        "primary_path": ["Zines", "Artist Books"],
        "secondary_path": ["Illustration Galleries", "Small Press Publishers"],
        "experimental_path": ["Print Markets", "Instagram / TikTok"],
        "current_stage": "Early distribution and positioning",
        "next_milestone": "Build one finished zine or artist-book prototype and place/research it through a small local ecosystem.",
        "recommended_focus": [
            "Do not start with big formal competitions.",
            "Build the zine / artist-book channel first.",
            "Use galleries as a secondary bridge.",
            "Use social media to document real actions rather than chase generic growth."
        ],
        "top_30_day_actions": [
            "Map 3 Koenji zine/book shops, 1 Nakano shop, and 10 nearby shops.",
            "Choose one zine or artist-book concept.",
            "Prepare 20 printed copies or one strong prototype.",
            "Research Pinpoint requirements only after portfolio materials are ready.",
            "Create a simple tracker for shops contacted, copies placed, and follow-up dates."
        ],
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(overview, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Career Overview",
        "",
        f"Current stage: {overview['current_stage']}",
        "",
        f"Next milestone: {overview['next_milestone']}",
        "",
        "## Primary Path",
    ]

    for x in overview["primary_path"]:
        lines.append(f"- {x}")

    lines += ["", "## Secondary Path"]
    for x in overview["secondary_path"]:
        lines.append(f"- {x}")

    lines += ["", "## Experimental Path"]
    for x in overview["experimental_path"]:
        lines.append(f"- {x}")

    lines += ["", "## Recommended Focus"]
    for x in overview["recommended_focus"]:
        lines.append(f"- {x}")

    lines += ["", "## Top 30-Day Actions"]
    for x in overview["top_30_day_actions"]:
        lines.append(f"- {x}")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
