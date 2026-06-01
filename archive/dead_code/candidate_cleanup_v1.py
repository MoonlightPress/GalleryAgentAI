
import json, re
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

SRC="memory/extracted_business_candidates.json"
OUT_JSON="memory/clean_business_candidates.json"
OUT_REPORT="reports/clean_business_candidates.md"
OUT_DECISIONS="memory/clean_business_decisions.json"

BAD_TITLE_TERMS=[
 "wikipedia","guide","best shops","top ","ranking","recommended","まとめ","紹介","ランキング","観光",
 "walking guide","perfect day","shopping map","official site","公式サイト","parco","kirarina","大型書店",
 "イベント開催一覧","開催日程一覧","準備","レポ"
]
ARTICLE_TERMS=[
 "blog","note.com","article","articles","collects","spots","san-tatsu","brutus","japantimes",
 "tokyoweekender","timeout","matcha","navitime","readyfor","散歩の達人","中央線が好きだ","週刊","さんたつ"
]
BAD_DOMAINS=[
 "wikipedia.org","timeout.com","matcha-jp.com","navitime.com","tripmate.news","hattiefoundthis.com",
 "hinomaru.one","maxonthemove.com","japanwondertravel.com","tokyochuko.com","japaninsides.com",
 "savvytokyo.com","tokyopocketguide.com","themeupgo.com","seitai-school.com"
]
PROMOTE_DOMAINS=[
 "stores.jp","base.shop","thebase.in","bookandsons.com","bookobscura.com","localgallerybooks.com",
 "tata-books.com","honnonagaya-honten.com","sozoroshobou","tacoche.com","mount.co.jp","utrecht.jp",
 "nadiff.com","post-books.info","flotsambooks.com","books-ruhe.co.jp","instagram.com"
]
PROMOTE_NAME_TERMS=[
 "書房","本屋","書店","Books","Bookshop","bookshop","gallery","Gallery","Zines","ZINE FARM",
 "Book Culture Club","タコシェ","Tacoche","Dig A Hole","LOCAL","tata","そぞろ","本店","Book Obscura","Books Ruhe"
]
EVENT_TERMS=["フェス","festival","fair","販売会","イベント","出店","Zine通り"]

def load(path, fallback):
    p=Path(path)
    return json.load(open(p,encoding="utf-8")) if p.exists() else fallback

def unwrap(url):
    if not url: return ""
    if url.startswith("//"): url="https:"+url
    parsed=urlparse(url); qs=parse_qs(parsed.query)
    return unquote(qs["uddg"][0]) if "uddg" in qs and qs["uddg"] else url

def domain(url):
    try: return urlparse(unwrap(url)).netloc.lower().replace("www.","")
    except Exception: return ""

def clean_name(name):
    raw=str(name or "").strip()
    patterns=[
        r"(Dig A Hole Zines?)", r"(ZINE FARM TOKYO)", r"(Book Culture Club)",
        r"(タコシェ|TACO ché|Tacoche)", r"(そぞろ書房)", r"(本店・本屋の実験室)",
        r"(tata bookshop/gallery)", r"(LOCAL Gallery・Books|LOCAL)", r"(Book Obscura)",
        r"(Books Ruhe|ブックス ルーエ)", r"(Nuts Book Stand)"
    ]
    for pat in patterns:
        m=re.search(pat, raw, flags=re.I)
        if m: return m.group(1).strip()
    name=re.sub(r"｜.*$","",raw)
    name=re.sub(r"\s+-\s+.*$","",name)
    name=re.sub(r"\s+\|\s+.*$","",name)
    name=re.sub(r"（.*?(本屋|書店|吉祥寺|高円寺|中野|下北沢).*?）","",name)
    name=re.sub(r"\(.*?(bookstore|tokyo|koenji|nakano|kichijoji).*?\)","",name,flags=re.I)
    return name.strip(" 　-—–｜|")[:80]

def classify(c):
    raw=c.get("name",""); name=clean_name(raw); url=unwrap(c.get("website","")); dom=domain(url)
    blob=f"{raw} {name} {url} {c.get('source_title','')}".lower()
    score=c.get("confidence",0); reasons=[]
    if any(d in dom for d in PROMOTE_DOMAINS): score+=25; reasons.append("promoted domain")
    if any(t.lower() in f"{raw} {name}".lower() for t in PROMOTE_NAME_TERMS): score+=25; reasons.append("business-like name")
    if any(t.lower() in blob for t in EVENT_TERMS): score+=8; reasons.append("event/fair signal")
    if any(d in dom for d in BAD_DOMAINS): score-=45; reasons.append("bad directory/tourism domain")
    if any(t.lower() in blob for t in BAD_TITLE_TERMS): score-=35; reasons.append("article/listicle/title noise")
    if any(t.lower() in blob for t in ARTICLE_TERMS): score-=15; reasons.append("article/source page")
    if len(raw)>55 and name==raw[:80]: score-=30; reasons.append("long title likely article")
    if name!=raw: score+=10; reasons.append("cleaned name")
    score=max(0,min(100,score))
    bucket="strong_lead" if score>=75 else "review_lead" if score>=45 else "event_or_article_lead" if any(t.lower() in blob for t in EVENT_TERMS) else "auto_reject"
    out=dict(c); out.update({"original_name":raw,"name":name,"website":url,"domain":dom,"cleanup_score":score,"cleanup_bucket":bucket,"cleanup_reasons":reasons})
    return out

def main():
    data=load(SRC,{"candidates":[]})
    cleaned=[classify(c) for c in data.get("candidates",[])]
    order={"strong_lead":0,"review_lead":1,"event_or_article_lead":2,"auto_reject":3}
    cleaned.sort(key=lambda x:(order.get(x["cleanup_bucket"],9),-x["cleanup_score"]))
    buckets={k:[c for c in cleaned if c["cleanup_bucket"]==k] for k in ["strong_lead","review_lead","event_or_article_lead","auto_reject"]}
    result={"source_count":len(cleaned),"strong_lead_count":len(buckets["strong_lead"]),"review_lead_count":len(buckets["review_lead"]),"event_or_article_lead_count":len(buckets["event_or_article_lead"]),"auto_reject_count":len(buckets["auto_reject"]),"candidates":cleaned,"buckets":buckets}
    Path("memory").mkdir(exist_ok=True); Path("reports").mkdir(exist_ok=True)
    json.dump(result,open(OUT_JSON,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
    decisions=[]
    for c in buckets["strong_lead"]+buckets["review_lead"]:
        decisions.append({"candidate_id":c.get("candidate_id"),"decision":"skipped","name":c.get("name"),"address":"","website":c.get("website",""),"instagram":"","email":"","phone":"","category":c.get("category",""),"neighborhood":c.get("neighborhood",""),"accepts_consignment":"unknown","accepts_submissions":"unknown","notes":"Cleanup reasons: "+", ".join(c.get("cleanup_reasons",[]))})
    json.dump({"instructions":"Change decision to approved/rejected/skipped. Approved records are ingested by ingest_clean_business_decisions.py.","decisions":decisions},open(OUT_DECISIONS,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
    lines=["# Clean Business Candidates","",f"- Source candidates: {len(cleaned)}",f"- Strong leads: {len(buckets['strong_lead'])}",f"- Review leads: {len(buckets['review_lead'])}",f"- Event/article leads: {len(buckets['event_or_article_lead'])}",f"- Auto-rejects: {len(buckets['auto_reject'])}",""]
    for bn in ["strong_lead","review_lead","event_or_article_lead","auto_reject"]:
        lines += [f"## {bn}",""]
        for c in buckets[bn][:80]:
            lines += [f"### {c.get('candidate_id')} — {c.get('name')}",f"- Original: {c.get('original_name')}",f"- Score: {c.get('cleanup_score')}",f"- Category: {c.get('category')}",f"- Neighborhood: {c.get('neighborhood')}",f"- Domain: {c.get('domain')}",f"- Website: {c.get('website')}",f"- Reasons: {', '.join(c.get('cleanup_reasons', []))}",f"- Maps: {c.get('google_maps_url')}",""]
    Path(OUT_REPORT).write_text("\n".join(lines),encoding="utf-8")
    print("Wrote cleanup files. Strong leads:",len(buckets["strong_lead"]))
if __name__=="__main__": main()
