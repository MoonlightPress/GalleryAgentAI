
import json, os
from pathlib import Path

PATH="deploy_data/verified_opportunities.json"

if not os.path.exists(PATH):
    raise SystemExit("Run verification first.")

with open(PATH,"r",encoding="utf-8") as f:
    opps=json.load(f)

for o in opps:
    title=str(o.get("title","")).lower()

    if "aperture" in title:
        o["primary_bucket"]="stretch"
    elif "photobook" in title or "book" in title or "zine" in title:
        o["primary_bucket"]="publication"
    elif "tokyo" in title or "shimokitazawa" in title:
        o["primary_bucket"]="relationship"
    else:
        o["primary_bucket"]="research"

with open(PATH,"w",encoding="utf-8") as f:
    json.dump(opps,f,indent=2,ensure_ascii=False)

print("Buckets simplified.")
