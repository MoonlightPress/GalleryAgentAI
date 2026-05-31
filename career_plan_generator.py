
import json
from pathlib import Path

RECS = "memory/nin_opportunity_recommendations.json"
OUT_JSON = "memory/monthly_career_plan.json"
OUT_REPORT = "reports/monthly_career_plan.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

recs = sorted(load(RECS, []), key=lambda x: x.get("recommendation_score", 0), reverse=True)

plan = {
    "apply": [],
    "research": [],
    "portfolio": [
        "Select strongest 10 works",
        "Create 1 PDF portfolio",
        "Prepare artist statement"
    ],
    "networking": [
        "Identify 5 artists with similar practice",
        "Follow 5 publishers/galleries"
    ]
}

for r in recs[:2]:
    plan["apply"].append(r.get("title"))

for r in recs[2:7]:
    plan["research"].append(r.get("title"))

Path("memory").mkdir(exist_ok=True)
json.dump(plan, open(OUT_JSON,"w",encoding="utf-8"), indent=2, ensure_ascii=False)

Path("reports").mkdir(exist_ok=True)
Path(OUT_REPORT).write_text(
f"""# Monthly Career Plan

## Apply
{chr(10).join('- '+x for x in plan['apply'])}

## Research
{chr(10).join('- '+x for x in plan['research'])}

## Portfolio
{chr(10).join('- '+x for x in plan['portfolio'])}

## Networking
{chr(10).join('- '+x for x in plan['networking'])}
""", encoding="utf-8")
