"""
generate_fallback_bullets.py

Rule-based fallback bullet generator for opportunities missing three_bullets.
Uses category, city, deadline, and submission fields to produce 2-3 actionable
bullets without AI API calls.

Only touches entries where three_bullets is empty/missing.
"""
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

OPP_PATH = Path(__file__).parent.parent.parent / "deploy_data" / "compact_opportunities.json"


def _location(opp):
    city = (opp.get("city") or "").strip()
    country = (opp.get("country") or "").strip()
    if city and country and city.lower() not in country.lower():
        return f"{city}, {country}"
    return city or country or ""


def _deadline_bullet(opp):
    dl = (opp.get("deadline") or "").strip()
    if not dl or dl.lower() in ("unknown", "none", "tbd", "n/a", "varies", "check site", "rolling", "ongoing"):
        return None
    return f"Deadline: {dl} — confirm on the official site before submitting"


def fallback_bullets(opp):
    cat = opp.get("category", "")
    loc = _location(opp)
    loc_str = f" in {loc}" if loc else ""
    dl = _deadline_bullet(opp)
    contact = (opp.get("contact") or "").strip()
    url = (opp.get("url") or opp.get("submission_url") or "").strip()
    sub_strategy = (opp.get("submission_strategy") or "").strip()

    bullets = []

    # Category-specific first bullet
    if cat in ("bookstore_gallery", "bookstore_event", "zine_shop_consignment"):
        bullets.append(f"Email{' '+contact if contact else ''} to discuss consignment or exhibition terms — these venues work by relationship, not open calls")
    elif cat in ("cafe_gallery",):
        bullets.append(f"Visit{loc_str} to see the space and speak with the manager about upcoming exhibition slots")
    elif cat in ("gallery", "gallery_small", "gallery_event", "artist_space"):
        bullets.append(f"Attend an opening or event{loc_str} first — gallery relationships start with presence, not cold submissions")
    elif cat in ("zine_print", "zine_fair_booth"):
        bullets.append("Bring or send a physical sample — zine culture is tactile and curators decide based on the object")
    elif cat in ("residency", "global_residency", "residency_beijing"):
        bullets.append("Review residency requirements carefully — most want a project proposal, CV, and portfolio PDF in one package")
    elif cat in ("global_grant_fellowship",):
        bullets.append("Read the full eligibility criteria before investing time in an application — grants have specific career-stage requirements")
    elif cat in ("global_open_call", "japan_watercolor_open_call", "global_watercolor_open_call"):
        bullets.append("Submit your strongest 3-5 works — open calls are judged quickly and first impressions matter")
    elif cat in ("book_publishing", "global_artist_book_platform", "global_art_book_fair"):
        bullets.append("Prepare a clear project description alongside images — publishers want to understand intent, not just see pretty work")
    elif cat in ("fair_popup", "market_event"):
        bullets.append("Consider table/booth cost and minimum inventory needed — these require physical preparation and stock")
    elif cat in ("global_photobook",):
        bullets.append("Photography-focused context — suitable for your photographic practice alongside or separately from watercolor work")
    else:
        if sub_strategy:
            bullets.append(sub_strategy[:120])
        else:
            bullets.append("Check the official website for current submission guidelines and open call status")

    # Second bullet: location or URL check
    if url:
        bullets.append(f"Verify current status at the official site before investing time — websites change and open calls close early")
    elif loc:
        bullets.append(f"Based{loc_str} — confirm this matches your geographic focus before investing preparation time")

    # Third bullet: deadline if available
    if dl:
        bullets.append(dl)
    elif len(bullets) < 3:
        bullets.append("Contact information or submission guidelines may require direct research")

    return bullets[:3]


def main():
    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))
    updated = 0
    for opp in opps:
        existing = opp.get("three_bullets")
        if existing and len(existing) > 0:
            continue
        bullets = fallback_bullets(opp)
        if bullets:
            opp["three_bullets"] = bullets
            updated += 1

    OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Added fallback bullets to {updated} entries.")


if __name__ == "__main__":
    main()
