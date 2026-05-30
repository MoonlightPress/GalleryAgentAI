
from pathlib import Path
import json, os

PATH="memory/artist_visual_profile.json"

if not os.path.exists(PATH):
    print("No profile found.")
    raise SystemExit()

with open(PATH,"r",encoding="utf-8") as f:
    data=json.load(f)

banned=["illustrator","illustration","painter","painting"]

text=json.dumps(data)

for b in banned:
    text=text.replace(b,"")

Path(PATH).write_text(text,encoding="utf-8")
print("Removed legacy illustrator/painter contamination.")
