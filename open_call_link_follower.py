
import json

INFILE="memory/deep_contact_results.json"
OUTFILE="memory/open_call_results.json"

items=json.load(open(INFILE,encoding="utf-8"))

for item in items:
    status="unknown"
    confidence=0.25

    links=item.get("relevant_links",[])

    for link in links:
        blob=(str(link.get("label",""))+" "+str(link.get("url",""))).lower()

        if any(x in blob for x in ["open call","application","submission","artist call","entry","応募","公募","募集"]):
            status="possible_open_call"
            confidence=0.8
            break

    item["submission_status"]=status
    item["submission_confidence"]=confidence

json.dump(items,open(OUTFILE,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
print("Wrote",OUTFILE)
