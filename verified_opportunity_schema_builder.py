
import json
from pathlib import Path

schema={
 "title":"",
 "url":"",
 "verified":False,
 "submission_open":"unknown",
 "deadline":"unknown",
 "contact_email":"unknown",
 "contact_name":"unknown",
 "fee":"unknown",
 "country":"unknown",
 "last_checked":"",
 "notes":""
}

Path("memory").mkdir(exist_ok=True)
json.dump(schema,open("memory/verified_opportunity_template.json","w",encoding="utf-8"),indent=2)
print("Template written")
