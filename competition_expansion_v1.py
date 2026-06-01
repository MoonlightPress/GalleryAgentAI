import json
from pathlib import Path
from urllib.parse import quote_plus, urlparse, parse_qs, unquote
import requests
from bs4 import BeautifulSoup
OUT_JSON=Path("memory/competition_candidates.json"); OUT_REPORT=Path("reports/competition_candidates.md")
HEADERS={"User-Agent":"Mozilla/5.0 (MochiCompetitionExpansion/1.0)"}
QUERIES={
"visual_art_awards":["Japan contemporary art award 2026 open call","Tokyo emerging artist award 2026 application","Japan painting competition 2026 open call","日本 現代アート 公募 賞 2026","若手アーティスト 公募 賞 2026","絵画 公募 賞 2026"],
"illustration_awards":["Japan illustration award 2026 open call","Tokyo illustration competition 2026","イラスト 公募 コンテスト 2026","イラストレーター 公募 賞 2026","JIA Illustration Award 2026","TIS competition illustrator open call"],
"known_awards":["Brillia Art Award 2026 application","Belladonna Art competition 2026 application","Shoto Museum open call 2026","Art Olympia 2026 application","FACE art award 2026 application","Tokyo Midtown Award 2026 art competition","SICF 2026 application artist"]}
BAD=["youtube","facebook","pinterest","tripadvisor","navitime","wikipedia","amazon"]
def unwrap(url):
    if url.startswith("//"): url="https:"+url
    q=parse_qs(urlparse(url).query)
    return unquote(q["uddg"][0]) if "uddg" in q and q["uddg"] else url
def search(q):
    try:
        r=requests.get("https://duckduckgo.com/html/?q="+quote_plus(q),headers=HEADERS,timeout=15); r.encoding=r.apparent_encoding or r.encoding
    except Exception: return []
    soup=BeautifulSoup(r.text,"html.parser"); rows=[]
    for a in soup.select("a.result__a"):
        title=" ".join(a.get_text(" ",strip=True).split()); href=unwrap(a.get("href",""))
        if title and href and not any(b in href.lower() for b in BAD): rows.append({"title":title[:140],"url":href,"query":q})
    return rows[:8]
def score(r):
    blob=f"{r['title']} {r['url']} {r['query']}".lower(); s=35
    if any(x in blob for x in ["award","competition","contest","公募","賞","コンテスト"]): s+=25
    if any(x in blob for x in ["application","apply","応募","募集","要項"]): s+=20
    if any(x in blob for x in ["deadline","締切","応募期間"]): s+=8
    if any(x in blob for x in ["art","painting","illustration","アート","絵画","イラスト"]): s+=8
    if any(x in blob for x in ["children","kids","小学生","幼児"]): s-=30
    if any(x in blob for x in ["guide","まとめ","一覧"]): s-=10
    return max(0,min(100,s))
def main():
    cand=[]; seen=set()
    for group, qs in QUERIES.items():
        for q in qs:
            print("SEARCH:",group,q)
            for r in search(q):
                key=(r["title"].lower(),r["url"].lower())
                if key in seen: continue
                seen.add(key)
                row={"candidate_id":f"COMP-{len(cand)+1:04d}","title":r["title"],"url":r["url"],"query":q,"competition_group":group,"career_category":"competitions","category":"competition","status":"research_next"}
                row["score"]=score(row); cand.append(row)
    cand.sort(key=lambda x:x["score"], reverse=True)
    OUT_JSON.parent.mkdir(exist_ok=True); OUT_REPORT.parent.mkdir(exist_ok=True)
    OUT_JSON.write_text(json.dumps({"candidate_count":len(cand),"candidates":cand},ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# Competition Candidates","",f"- Candidates: {len(cand)}",""]
    for group in QUERIES:
        rows=[c for c in cand if c["competition_group"]==group]; lines += [f"## {group} ({len(rows)})",""]
        for c in rows[:35]: lines += [f"### {c['candidate_id']} — {c['title']}",f"- Score: {c['score']}",f"- URL: {c['url']}",f"- Query: {c['query']}",""]
    OUT_REPORT.write_text("\n".join(lines),encoding="utf-8")
if __name__=="__main__": main()
