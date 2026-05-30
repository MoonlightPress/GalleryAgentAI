
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_DIR = "institution_profiles"

def load_json(path,fallback):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():
    opps = load_json(OPP_PATH,[])

    Path(OUT_DIR).mkdir(parents=True,exist_ok=True)

    for opp in opps[:200]:

        profile = {
            "name": opp.get("organization","Unknown"),
            "website": opp.get("official_website",""),
            "supported_artists": [],
            "exhibited_artists": [],
            "published_artists": [],
            "curatorial_keywords": [],
            "artist_fit_notes": "",
            "research_status": "needs_research",
            "confidence": 0
        }

        safe = str(profile["name"]).replace("/","_")[:80]

        with open(
            Path(OUT_DIR,f"{safe}.json"),
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(profile,f,indent=2,ensure_ascii=False)

    print("Institution profiles generated.")
