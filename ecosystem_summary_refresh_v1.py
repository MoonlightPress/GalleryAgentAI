import json
from pathlib import Path
def load(p,f): return json.load(open(p,encoding="utf-8")) if p.exists() else f
OUT_JSON=Path("memory/ecosystem_summary_v2.json"); OUT_DEPLOY=Path("deploy_data/ecosystem_summary_v2.json"); OUT_REPORT=Path("reports/ecosystem_summary_v2.md")
def main():
    gp=load(Path("memory/gallery_profiles.json"),{"profiles":[]}).get("profiles",[])
    gt=load(Path("memory/gallery_tiers.json"),{"records":[]}).get("records",[])
    gf=load(Path("memory/gallery_fit_analysis.json"),{"records":[]}).get("records",[])
    vc=load(Path("memory/verified_competitions.json"),{"records":[]}).get("records",[])
    fairs=load(Path("memory/fair_ecosystem.json"),{"targets":[]}).get("targets",[])
    calls=load(Path("memory/verified_open_calls.json"),{"records":[]}).get("records",[])
    summary={"galleries":{"profiles":len(gp),"direct_submission":len([g for g in gp if g.get("submission_signal")]),"emerging_friendly":len([g for g in gt if "emerging friendly" in g.get("tags",[])]),"top_fit":[g["name"] for g in gf[:10]]},"competitions":{"verified":len(vc),"actionable":len([c for c in vc if c.get("status")=="actionable"]),"top":[c["name"] for c in vc[:10]]},"fairs_events":{"targets":len(fairs),"beginner_friendly":len([f for f in fairs if f.get("beginner_friendliness")=="high"]),"high_prestige":len([f for f in fairs if f.get("prestige")=="high"]),"top":[f["name"] for f in fairs[:10]]},"open_calls":{"verified":len(calls),"actionable":len([c for c in calls if c.get("status")=="actionable"]),"top":[c["name"] for c in calls[:10]]}}
    OUT_JSON.parent.mkdir(exist_ok=True); OUT_DEPLOY.parent.mkdir(exist_ok=True); OUT_REPORT.parent.mkdir(exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8"); OUT_DEPLOY.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# Ecosystem Summary v2",""]
    for section,label in [("galleries","Galleries"),("competitions","Competitions"),("fairs_events","Fairs / Events"),("open_calls","Open Calls")]:
        lines += [f"## {label}"]
        for k,v in summary[section].items():
            if isinstance(v,list): continue
            lines.append(f"- {k}: {v}")
        lines += ["","### Top"]
        for x in summary[section].get("top_fit",summary[section].get("top",[])): lines.append(f"- {x}")
        lines.append("")
    OUT_REPORT.write_text("\n".join(lines),encoding="utf-8")
if __name__=="__main__": main()
