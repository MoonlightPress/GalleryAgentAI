import json
import os
from opportunity_report_engine import load_json, upgraded_score, confidence_level, verification_summary

OPP_PATH = "deploy_data/compact_opportunities.json"
PROFILE_PATH = "memory/artist_master_profile.json"

def main():
    opps = load_json(OPP_PATH, [])
    profile = load_json(PROFILE_PATH, {})
    upgraded = []
    for opp in opps:
        new = dict(opp)
        new["original_score"] = opp.get("overall_score")
        new["overall_score"] = upgraded_score(opp, profile)
        new["confidence_level"] = confidence_level(opp)
        new["verification_summary"] = verification_summary(opp)
        upgraded.append(new)
    upgraded.sort(key=lambda x: float(x.get("overall_score") or 0), reverse=True)
    os.makedirs("deploy_data", exist_ok=True)
    with open(OPP_PATH, "w", encoding="utf-8") as f:
        json.dump(upgraded, f, indent=2, ensure_ascii=False)
    print(f"Upgraded and sorted {len(upgraded)} opportunities.")

if __name__ == "__main__":
    main()
