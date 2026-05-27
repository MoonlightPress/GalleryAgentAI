
import json, os
from datetime import date
from pathlib import Path
from opportunity_report_engine import load_json, upgraded_score, confidence_level, verification_summary, get_source, category_label

OPP_PATH = "deploy_data/compact_opportunities.json"
PROFILE_PATH = "memory/artist_master_profile.json"
QUEUE_PATH = "memory/research_queue.json"

def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def bool_field(value):
    return bool(value and str(value).lower() not in {"unknown", "none", "null", "n/a"})

def missing_fields(opp):
    missing = []
    if not get_source(opp): missing.append("source")
    if not bool_field(opp.get("submission_page")): missing.append("submission process")
    if not bool_field(opp.get("deadline")): missing.append("deadline")
    if not bool_field(opp.get("fees")): missing.append("fees")
    if not bool_field(opp.get("contact") or opp.get("email") or opp.get("contact_url")): missing.append("contact")
    return missing

def source_quality(opp):
    source = get_source(opp)
    if not source: return "missing"
    if any(domain in source.lower() for domain in ["instagram.com", "facebook.com", "x.com", "twitter.com"]): return "social"
    return "official_or_listing"

def enrich_opportunity(opp, profile):
    out = dict(opp)
    missing = missing_fields(opp)
    score = upgraded_score(opp, profile)

    out["overall_score"] = score
    out["confidence_level"] = confidence_level(opp)
    out["verification_summary"] = verification_summary(opp)
    out["verification_status"] = "verified" if not missing else ("partial" if get_source(opp) else "weak")
    out["last_verified"] = out.get("last_verified") or date.today().isoformat()
    out["research_priority"] = "high" if len(missing) >= 3 or score >= 7 else "medium" if missing else "low"
    out["manual_review_needed"] = bool(missing)
    out["submission_process_known"] = bool_field(opp.get("submission_page"))
    out["contact_verified"] = bool_field(opp.get("contact") or opp.get("email") or opp.get("contact_url"))
    out["fees_verified"] = bool_field(opp.get("fees"))
    out["deadline_verified"] = bool_field(opp.get("deadline"))
    out["source_quality"] = source_quality(opp)
    out["missing_fields"] = missing
    out["category_label"] = category_label(opp.get("category"))
    return out

def main():
    opps = load_json(OPP_PATH, [])
    profile = load_json(PROFILE_PATH, {})
    enriched = [enrich_opportunity(opp, profile) for opp in opps]
    enriched.sort(key=lambda x: float(x.get("overall_score") or 0), reverse=True)
    save_json(OPP_PATH, enriched)

    queue = []
    for opp in enriched:
        if opp["manual_review_needed"]:
            queue.append({
                "title": opp.get("title") or opp.get("name"),
                "organization": opp.get("organization"),
                "score": opp.get("overall_score"),
                "priority": opp.get("research_priority"),
                "missing": opp.get("missing_fields"),
                "source": get_source(opp),
                "recommended_action": "Verify missing fields or generate inquiry draft."
            })
    save_json(QUEUE_PATH, queue)
    print(f"Enriched {len(enriched)} opportunities.")
    print(f"Research queue contains {len(queue)} items.")

if __name__ == "__main__":
    main()
