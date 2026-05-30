
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/artist_gap_analysis.md"

def load_json(path,fallback):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():
    opps = load_json(OPP_PATH,[])

    top = sorted(
        opps,
        key=lambda x: float(x.get("artist_profile_score",0)),
        reverse=True
    )[:20]

    lines = [
        "# Artist Gap Analysis",
        "",
        "These are the opportunities most aligned with the current visual profile.",
        ""
    ]

    for opp in top:
        lines.append(f"## {opp.get('title','Unknown')}")
        lines.append(f"- Visual score: {opp.get('artist_profile_score',0)}")
        lines.append(f"- Hits: {', '.join(opp.get('artist_profile_hits',[]))}")
        lines.append("")

    Path(OUT_PATH).parent.mkdir(parents=True,exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines),encoding="utf-8")
    print(f"Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
