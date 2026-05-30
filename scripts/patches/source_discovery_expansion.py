
import json, os
from pathlib import Path

registry=json.load(open("memory/source_registry.json",encoding="utf-8"))
out=[]

for s in registry["seed_sources"]:
    out.append({
        "title":s["name"],
        "organization":s["name"],
        "overall_score":7.0,
        "discovery_status":"needs_research",
        "source_type":s["category"]
    })

Path("ingestion").mkdir(exist_ok=True)
json.dump(out,open("ingestion/discovery_expansion_candidates.json","w",encoding="utf-8"),indent=2)
print("Generated",len(out),"expanded candidates")
