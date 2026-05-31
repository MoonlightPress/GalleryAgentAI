
import json
from pathlib import Path

RECS = "memory/nin_opportunity_recommendations.json"
OUT_JSON = "memory/opportunity_briefs.json"
OUT_REPORT = "reports/opportunity_briefs.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

briefs = []

for r in load(RECS, []):
    title = r.get("title")
    brief = {
        "title": title,
        "why_it_fits": r.get("fit_summary"),
        "recommendation_score": r.get("recommendation_score"),
        "next_step": "Review requirements and prepare submission materials.",
        "estimated_effort": "2-4 hours"
    }
    briefs.append(brief)

Path("memory").mkdir(exist_ok=True)
json.dump(briefs, open(OUT_JSON,"w",encoding="utf-8"), indent=2, ensure_ascii=False)

lines = ["# Opportunity Briefs",""]
for b in briefs:
    lines += [
        f"## {b['title']}",
        f"- Score: {b['recommendation_score']}",
        f"- Why it fits: {b['why_it_fits']}",
        f"- Next step: {b['next_step']}",
        f"- Effort: {b['estimated_effort']}",
        ""
    ]

Path("reports").mkdir(exist_ok=True)
Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")
