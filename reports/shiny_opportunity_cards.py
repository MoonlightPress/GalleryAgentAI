
import json
from pathlib import Path

SRC = "memory/opportunity_pitches.json"
OUT = "reports/shiny_opportunity_cards.md"
DEPLOY = "deploy_data/shiny_opportunity_cards.json"

def main():
    pitches = json.load(open(SRC, encoding="utf-8"))

    cards = []
    for p in pitches:
        cards.append({
            "title": p["title"],
            "score": p.get("dna_match_score"),
            "readiness": p.get("readiness"),
            "effort": p.get("estimated_effort"),
            "deadline": p.get("deadline"),
            "url": p.get("recommended_url"),
            "headline": p.get("headline"),
            "why_it_matters": p.get("why_this_matters"),
            "why_it_fits": p.get("why_it_fits_her"),
            "first_step": p.get("first_step"),
            "confirm_first": p.get("missing_details", []),
        })

    Path("deploy_data").mkdir(exist_ok=True)
    json.dump(cards, open(DEPLOY, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Shiny Opportunity Cards",
        "",
        "Short version for the site. These should feel like recommendations, not database records.",
        "",
    ]

    for c in cards:
        lines.append(f"## {c['title']}")
        if c.get("score") is not None:
            lines.append(f"**Match:** {c['score']}/10  ")
        lines.append(f"**Readiness:** {c['readiness']}  ")
        lines.append(f"**Effort:** {c['effort']}  ")
        lines.append(f"**Deadline:** {c['deadline']}  ")
        lines.append("")
        lines.append(c["headline"])
        lines.append("")
        lines.append(f"**Why it matters:** {c['why_it_matters']}")
        lines.append("")
        lines.append(f"**Why it fits:** {c['why_it_fits']}")
        lines.append("")
        lines.append(f"**First step:** {c['first_step']}")
        lines.append("")
        lines.append(f"**Link:** {c['url']}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT)
    print("Wrote", DEPLOY)

if __name__ == "__main__":
    main()
