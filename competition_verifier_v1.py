import json,re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
SRC=Path("memory/competition_candidates.json"); OUT_JSON=Path("memory/verified_competitions.json"); OUT_REPORT=Path("reports/verified_competitions.md")
HEADERS={"User-Agent":"Mozilla/5.0 (MochiCompetitionVerifier/1.0)"}
EMAIL_RE=r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
DEAD=[r"(締切|応募締切|応募期間|deadline|application deadline)[^\n。:：]{0,40}[:：]?\s*([^\n。]{0,100})",r"((20\d{2})[./年-]\s?\d{1,2}[./月-]\s?\d{1,2}日?)",r"([A-Z][a-z]+ \d{1,2}, 20\d{2})"]
FEE=[r"(応募料|出品料|参加費|entry fee|application fee|fee)[^\n。:：]{0,40}[:：]?\s*([^\n。]{0,100})",r"(¥\s?\d[\d,]*)",r"(\d[\d,]*\s?円)"]
def load(p,f): return json.load(open(p,encoding="utf-8")) if p.exists() else f
def fetch(url):
    if not url or url.endswith(".pdf"): return ""
    try:
        r=requests.get(url,headers=HEADERS,timeout=15); r.encoding=r.apparent_encoding or r.encoding
        soup=BeautifulSoup(r.text,"html.parser")
        for tag in soup(["script","style","noscript"]): tag.decompose()
        return " ".join(soup.get_text("\n",strip=True).split())
    except Exception: return ""
def ext(pats,text):
    for pat in pats:
        m=re.search(pat,text,flags=re.I)
        if m: return " ".join([g for g in m.groups() if g])[:180]
    return ""
def route(url,text):
    blob=f"{url} {text[:3000]}".lower()
    if any(x in blob for x in ["form","google","jotform","応募フォーム","申込フォーム"]): return "form"
    if "@" in text: return "email_possible"
    if any(x in blob for x in ["application","apply","応募","募集","要項"]): return "application_page"
    return "check_source"
def main():
    selected=load(SRC,{"candidates":[]}).get("candidates",[])[:40]; records=[]
    for c in selected:
        print("VERIFY COMP:",c.get("title"))
        text=fetch(c.get("url","")); r=route(c.get("url",""),text); deadline=ext(DEAD,text)
        records.append({"name":c.get("title"),"url":c.get("url"),"score":c.get("score"),"competition_group":c.get("competition_group"),"deadline":deadline,"fee":ext(FEE,text),"emails":sorted(set(re.findall(EMAIL_RE,text)))[:5],"application_route":r,"status":"actionable" if deadline and r!="check_source" else "needs_review"})
    OUT_JSON.parent.mkdir(exist_ok=True); OUT_REPORT.parent.mkdir(exist_ok=True)
    OUT_JSON.write_text(json.dumps({"verified_count":len(records),"records":records},ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# Verified Competitions","",f"- Records: {len(records)}",""]
    for status in ["actionable","needs_review"]:
        rows=[r for r in records if r["status"]==status]; lines += [f"## {status} ({len(rows)})",""]
        for r in rows: lines += [f"### {r['name']}",f"- Score: {r['score']}",f"- Deadline: {r['deadline'] or 'Check source'}",f"- Fee: {r['fee'] or 'Check source'}",f"- Route: {r['application_route']}",f"- Emails: {', '.join(r['emails']) if r['emails'] else 'None extracted'}",f"- URL: {r['url']}",""]
    OUT_REPORT.write_text("\n".join(lines),encoding="utf-8")
if __name__=="__main__": main()
