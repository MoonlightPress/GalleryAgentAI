
import json
from pathlib import Path

BRIEFS="memory/opportunity_briefs.json"
PLAN="memory/monthly_career_plan.json"

Path("deploy_data").mkdir(exist_ok=True)

for src,name in [(BRIEFS,"opportunity_briefs.json"),(PLAN,"monthly_career_plan.json")]:
    p=Path(src)
    if p.exists():
        data=json.load(open(p,encoding="utf-8"))
        json.dump(data, open(Path("deploy_data")/name,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
