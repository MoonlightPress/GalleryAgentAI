
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
REPORT_PATH = "reports/painting_quality_gate_report.md"

BAD = ["farmers market", "raw tokyo", "handmade", "craft fair", "flea", "street photography", "lensculture", "photovogue", "camera"]
STRONG = ["watercolor", "watercolour", "works on paper", "painting", "drawing", "illustration gallery", "open exhibition", "gallery open call", "painting prize"]

def load(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def blob(o):
    parts=[]
    for k in ["title","organization","source_type","one_sentence","why_this_fits_short","source_url","official_website"]:
        if o.get(k): parts.append(str(o[k]))
    for k in ["watercolor_fit_hits","native_medium_hits"]:
        val=o.get(k,[])
        if isinstance(val,dict):
            for arr in val.values():
                parts += [str(x) for x in arr]
        elif isinstance(val,list):
            parts += [str(x) for x in val]
    return " ".join(parts).lower()

def main():
    opps=load(OPP_PATH,[])
    promoted=demoted=0

    lines=["# Painting Quality Gate Report","","## Changes",""]

    for o in opps:
        text=blob(o)
        score=float(o.get("source_purity_score", o.get("watercolor_adjusted_score", o.get("overall_score",0))) or 0)
        old=score

        strong_hits=[x for x in STRONG if x in text]
        bad_hits=[x for x in BAD if x in text]

        if o.get("native_medium")=="painting" or strong_hits:
            score=min(9.6, score + 0.8)
            o["painting_gate_status"]="promoted"
            o["painting_gate_hits"]=strong_hits
            promoted += 1

        if bad_hits and o.get("native_medium")!="painting":
            score=min(score,5.5)
            o["painting_gate_status"]="demoted"
            o["painting_gate_hits"]=bad_hits
            demoted += 1

        o["painting_priority_score"]=round(max(0,min(10,score)),2)

        if round(old,2)!=o["painting_priority_score"]:
            lines.append(f"- **{o.get('title') or o.get('name')}** — {round(old,2)} → {o['painting_priority_score']} — {o.get('painting_gate_status')}")

    opps.sort(key=lambda x: float(x.get("painting_priority_score",0) or 0), reverse=True)
    save(OPP_PATH,opps)

    lines.insert(2,f"Promoted: {promoted}")
    lines.insert(3,f"Demoted: {demoted}")
    Path("reports").mkdir(exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines),encoding="utf-8")
    print(f"Promoted: {promoted}")
    print(f"Demoted: {demoted}")
    print(f"Wrote {REPORT_PATH}")

if __name__=="__main__":
    main()
