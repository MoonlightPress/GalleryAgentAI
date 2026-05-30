
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_DIR = "reports/curator_dossiers"

def load_json(path,fallback):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():
    opps = load_json(OPP_PATH,[])

    Path(OUT_DIR).mkdir(parents=True,exist_ok=True)

    for opp in opps[:100]:

        org = opp.get("organization","Unknown")
        title = opp.get("title","Unknown")

        lines = [
            f"# {org}",
            "",
            f"Opportunity: {title}",
            "",
            "## Research Checklist",
            "",
            "- Who runs this organization?",
            "- What artists do they regularly support?",
            "- Do they publish photobooks?",
            "- Do they support emerging artists?",
            "- Is there an open submission path?",
            "",
            "## Why It Matters",
            "",
            opp.get("why_this_fits_short",""),
            "",
            "## Next Action",
            "",
            opp.get("quick_action","Research further"),
        ]

        safe = title.replace("/","_")[:80]

        Path(
            OUT_DIR,
            f"{safe}.md"
        ).write_text(
            "\n".join(lines),
            encoding="utf-8"
        )

    print("Generated curator dossiers.")
