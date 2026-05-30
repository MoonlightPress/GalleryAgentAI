
import json
import os
from pathlib import Path

VISUAL_PATH = "memory/visual_language_profile.json"
OPP_PATH = "deploy_data/compact_opportunities.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save_json(path,data):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False)

def main():
    visual = load_json(VISUAL_PATH,{})
    opps = load_json(OPP_PATH,[])

    themes = [str(x).lower() for x in visual.get("visual_language",[])]

    for opp in opps:
        text = " ".join([
            str(opp.get("title","")),
            str(opp.get("one_sentence","")),
            str(opp.get("why_this_fits_short",""))
        ]).lower()

        hits = [t for t in themes if t and t in text]

        opp["artist_profile_hits"] = hits
        opp["artist_profile_score"] = len(hits)

    save_json(OPP_PATH, opps)
    print("Artist profile scores added.")

if __name__ == "__main__":
    main()
