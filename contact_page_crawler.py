
import json,re
from pathlib import Path

INFILE="memory/verified_opportunities.json"
OUTFILE="memory/deep_contact_results.json"

items=json.load(open(INFILE,encoding="utf-8"))

for item in items:
    links=item.get("relevant_links",[])
    contacts=[]
    pages=[]

    for link in links:
        url=str(link.get("url",""))
        label=str(link.get("label","")).lower()

        if any(x in label for x in ["contact","about","submission","apply","open call","opportunity","応募","公募","募集"]):
            pages.append(url)

    item["contact_pages"]=pages[:10]
    item["contact_emails"]=contacts

json.dump(items,open(OUTFILE,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
print("Wrote",OUTFILE)
