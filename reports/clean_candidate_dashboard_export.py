
import json
from pathlib import Path
SOURCES=[("memory/clean_business_candidates.json","clean_business_candidates.json"),("memory/clean_candidate_summary.json","clean_candidate_summary.json"),("memory/verified_zine_businesses.json","verified_zine_businesses.json")]
def main():
    Path("deploy_data").mkdir(exist_ok=True)
    for src,name in SOURCES:
        p=Path(src)
        if p.exists():
            json.dump(json.load(open(p,encoding="utf-8")),open(Path("deploy_data")/name,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
            print("Wrote",Path("deploy_data")/name)
        else: print("Missing",src)
if __name__=="__main__": main()
