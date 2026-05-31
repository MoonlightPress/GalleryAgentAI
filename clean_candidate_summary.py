
import json
from pathlib import Path
from collections import Counter
CLEAN="memory/clean_business_candidates.json"; VERIFIED="memory/verified_zine_businesses.json"
OUT_JSON="memory/clean_candidate_summary.json"; OUT_REPORT="reports/clean_candidate_summary.md"
def load(path,fallback):
    p=Path(path); return json.load(open(p,encoding="utf-8")) if p.exists() else fallback
def main():
    clean=load(CLEAN,{}); verified=load(VERIFIED,{"businesses":[]})
    candidates=clean.get("candidates",[]); strong=[c for c in candidates if c.get("cleanup_bucket")=="strong_lead"]
    byh=Counter(c.get("neighborhood") for c in strong); byc=Counter(c.get("category") for c in strong)
    summary={"source_candidates":clean.get("source_count",len(candidates)),"strong_leads":len(strong),"review_leads":clean.get("review_lead_count",0),"auto_rejects":clean.get("auto_reject_count",0),"verified_businesses":len(verified.get("businesses",[])),"strong_by_neighborhood":dict(byh),"strong_by_category":dict(byc),"top_strong_leads":strong[:20]}
    Path("memory").mkdir(exist_ok=True); Path("reports").mkdir(exist_ok=True)
    json.dump(summary,open(OUT_JSON,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
    lines=["# Clean Candidate Summary","",f"- Source candidates: {summary['source_candidates']}",f"- Strong leads: {summary['strong_leads']}",f"- Review leads: {summary['review_leads']}",f"- Auto-rejects: {summary['auto_rejects']}",f"- Verified businesses: {summary['verified_businesses']}","","## Strong Leads by Neighborhood"]
    for k,v in byh.most_common(): lines.append(f"- {k}: {v}")
    lines += ["","## Strong Leads by Category"]
    for k,v in byc.most_common(): lines.append(f"- {k}: {v}")
    lines += ["","## Top Strong Leads"]
    for c in strong[:30]:
        lines.append(f"- {c.get('name')} — {c.get('neighborhood')} — {c.get('category')} — {c.get('cleanup_score')}")
        lines.append(f"  - {c.get('website')}")
    Path(OUT_REPORT).write_text("\n".join(lines),encoding="utf-8")
if __name__=="__main__": main()
