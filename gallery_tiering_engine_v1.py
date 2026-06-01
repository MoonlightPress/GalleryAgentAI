import json
from pathlib import Path
SRC = Path("memory/gallery_profiles.json")
OUT_JSON = Path("memory/gallery_tiers.json")
OUT_REPORT = Path("reports/gallery_tiers.md")
PRESTIGE = ["tokyo arts and space", "tokyo gendai", "tagboat", "nca", "nichido", "tokyo gallery", "biscuit"]
EMERGING = ["emerging", "若手", "新人", "登竜門", "new power", "grid"]
LOCAL = {"Koenji", "Nakano", "Kichijoji", "Shimokitazawa"}
def load(p,f): return json.load(open(p,encoding="utf-8")) if p.exists() else f
def tags(p):
    blob = " ".join([p.get("name",""), " ".join(p.get("gallery_type",[])), " ".join(p.get("artist_type",[])), " ".join(p.get("exhibition_terms",[]))]).lower()
    out=[]
    if any(x in blob for x in PRESTIGE): out.append("prestige")
    if p.get("submission_signal"): out.append("submission route")
    if any(x.lower() in blob for x in EMERGING): out.append("emerging friendly")
    if "rental" in blob: out.append("rental")
    if "gallery cafe" in blob: out.append("gallery cafe")
    if p.get("neighborhood") in LOCAL: out.append("local west Tokyo")
    if "curated" in blob or "exhibition" in blob: out.append("curated/exhibition")
    return out or ["needs review"]
def tier(p,t):
    s=p.get("profile_score",0)
    if "submission route" in t and "emerging friendly" in t: return "A - direct emerging opportunity"
    if "prestige" in t and "submission route" in t: return "A - prestige application"
    if "local west Tokyo" in t and s>=75: return "B - local ecosystem target"
    if "rental" in t: return "C - rental / use carefully"
    if s>=85: return "B - promising target"
    return "C - research later"
def main():
    profiles=load(SRC,{"profiles":[]}).get("profiles",[])
    rec=[]
    for p in profiles:
        t=tags(p)
        rec.append({"name":p.get("name"),"url":p.get("url"),"neighborhood":p.get("neighborhood"),"profile_score":p.get("profile_score"),"tier":tier(p,t),"tags":t,"submission_signal":p.get("submission_signal"),"emails":p.get("emails",[])})
    rec.sort(key=lambda x:(x["tier"],-(x.get("profile_score") or 0)))
    OUT_JSON.parent.mkdir(exist_ok=True); OUT_REPORT.parent.mkdir(exist_ok=True)
    OUT_JSON.write_text(json.dumps({"tier_count":len(rec),"records":rec},ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# Gallery Tiers",""]
    for tr in sorted(set(r["tier"] for r in rec)):
        rows=[r for r in rec if r["tier"]==tr]; lines += [f"## {tr} ({len(rows)})",""]
        for r in rows: lines += [f"- {r['name']} — score {r['profile_score']} — {', '.join(r['tags'])}", f"  - {r.get('url','')}"]
        lines.append("")
    OUT_REPORT.write_text("\n".join(lines),encoding="utf-8")
if __name__=="__main__": main()
