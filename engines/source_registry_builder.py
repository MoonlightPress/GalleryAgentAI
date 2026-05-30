
import json
from pathlib import Path

src=json.load(open("global_photo_source_pack.json",encoding="utf-8"))
out={"seed_sources":[]}

for name in src["sources"]:
    out["seed_sources"].append({
        "name":name,
        "priority":"high",
        "category":"photography_ecosystem"
    })

Path("memory").mkdir(exist_ok=True)
json.dump(out,open("memory/source_registry.json","w",encoding="utf-8"),indent=2)
print("Built source registry:",len(out["seed_sources"]))
