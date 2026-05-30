
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/priority_research_queue.md"

def load_json(path,fallback):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():
    opps = load_json(OPP_PATH,[])

    ranked = sorted(
        opps,
        key=lambda x: (
            float(x.get("overall_score",0)),
            float(x.get("artist_profile_score",0))
        ),
        reverse=True
    )

    lines = [
        "# Priority Research Queue",
        "",
        "Research these first.",
        ""
    ]

    for opp in ranked[:30]:
        lines.append(
            f"- {opp.get('title')} ({opp.get('overall_score')}/10)"
        )

    Path(OUT_PATH).parent.mkdir(parents=True,exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines),encoding="utf-8")

if __name__ == "__main__":
    main()
