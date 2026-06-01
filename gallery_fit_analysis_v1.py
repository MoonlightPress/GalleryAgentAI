import json
from pathlib import Path
SRC=Path("memory/gallery_tiers.json"); OUT_JSON=Path("memory/gallery_fit_analysis.json"); OUT_REPORT=Path("reports/gallery_fit_analysis.md")
def load(p,f): return json.load(open(p,encoding="utf-8")) if p.exists() else f
def fit(r):
    t=set(r.get("tags",[])); s=55
    if "emerging friendly" in t: s+=18
    if "submission route" in t: s+=14
    if "local west Tokyo" in t: s+=8
    if "prestige" in t: s+=8
    if "gallery cafe" in t: s+=4
    if "rental" in t: s-=12
    s+=min(6,(r.get("profile_score") or 0)/20)
    return max(0,min(100,round(s)))
def risk(r):
    t=set(r.get("tags",[])); x=45
    if "submission route" in t: x-=12
    if "emerging friendly" in t: x-=10
    if "rental" in t: x+=18
    if not r.get("emails") and not r.get("submission_signal"): x+=10
    if "prestige" in t: x+=8
    return max(0,min(100,round(x)))
def reason(r):
    t=set(r.get("tags",[])); parts=[]
    if "emerging friendly" in t: parts.append("has an emerging-artist signal")
    if "submission route" in t: parts.append("has a submission/open-call route")
    if "local west Tokyo" in t: parts.append("belongs to the local west-Tokyo ecosystem")
    if "rental" in t: parts.append("may be rental-based, so cost/quality must be checked")
    return "Good candidate because " + "; ".join(parts or ["it needs review of past artists and fit"]) + "."
def main():
    rows=load(SRC,{"records":[]}).get("records",[])
    out=[]
    for r in rows:
        out.append({**r,"fit_score":fit(r),"risk_score":risk(r),"reason_for_nin":reason(r),"recommended_next_action":"Review past artists, confirm curated vs rental, then contact only if fit is clear."})
    out.sort(key=lambda x:(x["fit_score"],-x["risk_score"]), reverse=True)
    OUT_JSON.parent.mkdir(exist_ok=True); OUT_REPORT.parent.mkdir(exist_ok=True)
    OUT_JSON.write_text(json.dumps({"analysis_count":len(out),"records":out},ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# Gallery Fit Analysis",""]
    for r in out[:60]:
        lines += [f"### {r['name']}",f"- Fit: {r['fit_score']}",f"- Risk: {r['risk_score']}",f"- Tier: {r['tier']}",f"- Tags: {', '.join(r['tags'])}",f"- Reason: {r['reason_for_nin']}",f"- URL: {r.get('url','')}",""]
    OUT_REPORT.write_text("\n".join(lines),encoding="utf-8")
if __name__=="__main__": main()
