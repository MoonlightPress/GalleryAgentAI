
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "deploy_data/verified_opportunities.json"
REPORT_PATH = "reports/opportunity_verification_report.md"

def load(path,fallback):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save(path,data):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False)

def verify(opp):
    score = 0
    reasons = []

    title = str(opp.get("title","")).lower()

    bad = ["facebook","instagram","pinterest","tiktok","continue reading","www."]
    if any(x in title for x in bad):
        return "reject",0,["junk source"]

    if opp.get("submission_page"):
        score += 3; reasons.append("submission page")
    if opp.get("deadline"):
        score += 2; reasons.append("deadline")
    if opp.get("contact") or opp.get("email"):
        score += 2; reasons.append("contact")
    if opp.get("organization"):
        score += 1; reasons.append("organization")
    if opp.get("verification_status") == "verified":
        score += 3; reasons.append("verified")

    if score >= 7:
        return "verified",score,reasons
    if score >= 4:
        return "likely",score,reasons
    return "research_needed",score,reasons

opps = load(OPP_PATH,[])
out=[]

lines=["# Opportunity Verification Report","","## Summary",""]

counts={"verified":0,"likely":0,"research_needed":0,"reject":0}

for o in opps:
    status,score,reasons = verify(o)
    o["verification_bucket"]=status
    o["verification_score"]=score
    counts[status]+=1
    out.append(o)

for k,v in counts.items():
    lines.append(f"- {k}: {v}")

lines.append("\n## Verified Opportunities\n")
for o in sorted(out,key=lambda x:x.get("verification_score",0),reverse=True):
    if o["verification_bucket"]=="verified":
        lines.append(f"- {o.get('title','Unknown')}")

save(OUT_PATH,out)
Path(REPORT_PATH).write_text("\n".join(lines),encoding="utf-8")
print("Verification complete.")
