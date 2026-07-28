
import json, os, sys
from datetime import date
from pathlib import Path
sys.path.insert(0, "engines")
from opportunity_report_engine import load_json, upgraded_score, score_bump, confidence_level, verification_summary, get_source, category_label

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
    # Every concept checks BOTH spellings of its split-field pair. rumor_mill
    # writes submission_url / fee / contact_email; this function only knew the
    # older spellings, so manual_review_needed was re-stamped True on items
    # rumor_mill had fully answered — which kept 713 entries cycling through
    # needs_research forever (measured 2026-07-28: 520 of them had every fact).
    missing = []
    if not get_source(opp): missing.append("source")
    if not bool_field(opp.get("submission_page") or opp.get("submission_url")): missing.append("submission process")
    if not bool_field(opp.get("deadline")): missing.append("deadline")
    if not bool_field(opp.get("fees") or opp.get("fee")): missing.append("fees")
    if not bool_field(opp.get("contact") or opp.get("email") or opp.get("contact_url")
                      or opp.get("contact_email")): missing.append("contact")
    return missing

def source_quality(opp):
    source = get_source(opp)
    if not source: return "missing"
    if any(domain in source.lower() for domain in ["instagram.com", "facebook.com", "x.com", "twitter.com"]): return "social"
    return "official_or_listing"

def enrich_opportunity(opp, profile):
    out = dict(opp)
    missing = missing_fields(opp)

    # Idempotency anchor (2026-07-28). upgraded_score = stored score + bumps,
    # and enrichment runs in EVERY pipeline — so each run compounded the bumps
    # onto the previous run's output (6.0 -> 6.8 -> 7.6 -> ... -> 10.0),
    # inflating every ideal-shaped entry toward the cap and flattening ranking
    # into the "endless 9.4 ties". Snapshot the pre-bump base once; every
    # enrichment after that recomputes FROM THE BASE, so enriching N times
    # equals enriching once. (Bases snapshotted before this fix are the
    # already-inflated values — historic inflation is frozen, not reversed;
    # the true originals are unrecoverable.)
    if out.get("score_base") is None:
        # Seed base = stored - bump, so this FIRST fixed run freezes the
        # stored score exactly (no fresh bump on top of historic inflation);
        # every later run recomputes from the frozen base and is stable.
        out["score_base"] = round(
            float(out.get("overall_score") or 0) - score_bump(opp, profile), 2)
    score = upgraded_score({**opp, "overall_score": out["score_base"]}, profile)

    out["overall_score"] = score
    out["confidence_level"] = confidence_level(opp)
    out["verification_summary"] = verification_summary(opp)
    out["verification_status"] = "verified" if not missing else ("partial" if get_source(opp) else "weak")
    out["last_verified"] = out.get("last_verified") or date.today().isoformat()
    out["research_priority"] = "high" if len(missing) >= 3 or score >= 7 else "medium" if missing else "low"
    out["manual_review_needed"] = bool(missing)
    out["submission_process_known"] = bool_field(opp.get("submission_page") or opp.get("submission_url"))
    out["contact_verified"] = bool_field(opp.get("contact") or opp.get("email") or opp.get("contact_url")
                                         or opp.get("contact_email"))
    out["fees_verified"] = bool_field(opp.get("fees") or opp.get("fee"))
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
