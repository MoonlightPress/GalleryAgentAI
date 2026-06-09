"""
seed_crm_from_relationship_builders.py

Seeds the CRM with relationship_builder opportunities not yet in contacts.
Only adds entries scoring >= 7.0 and not already present (case-insensitive name match).
Sets status='cold' and generates rule-based next_action.
"""
import sys
import json
from pathlib import Path
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8")

OPP_PATH      = Path(__file__).parent.parent.parent / "deploy_data" / "compact_opportunities.json"
CONTACTS_PATH = Path(__file__).parent.parent.parent / "memory" / "contact_memory.json"

TYPE_MAP = {
    "cafe_gallery":      "cafe_gallery",
    "bookstore_gallery": "bookstore_gallery",
    "gallery":           "gallery",
    "gallery_small":     "gallery",
    "artist_space":      "artist_space",
    "magazine":          "magazine",
    "publication":       "magazine",
    "global_open_call":  "open_call",
    "zine_print":        "zine_shop",
    "zine_fair_booth":   "fair",
    "book_publishing":   "book_publisher",
}


def _next_action(opp: dict) -> str:
    cat = opp.get("category", "")
    name = opp.get("name", "this venue")
    city = opp.get("city", "")
    loc = f" in {city}" if city else ""
    if cat in ("cafe_gallery", "cafe"):
        return f"Visit {name}{loc} to see the display space and speak with the manager about upcoming exhibition availability."
    if cat in ("bookstore_gallery", "bookshop", "bookstore"):
        return f"Visit {name}{loc} in person to confirm the aesthetic fit, then draft a brief consignment inquiry."
    if cat in ("gallery", "gallery_small", "artist_space"):
        return f"Attend an opening or event at {name}{loc} to observe their curation style before any formal approach."
    if cat in ("magazine", "publication"):
        return f"Research {name}'s submission guidelines and pitch format before initiating contact."
    return f"Research {name}'s current program and submission policy before reaching out."


def _risk_notes(opp: dict) -> str:
    cat = opp.get("category", "")
    if cat in ("gallery", "gallery_small", "artist_space"):
        return "Many galleries do not accept unsolicited submissions — verify their policy before sending work."
    if cat in ("bookstore_gallery", "bookshop"):
        return "Confirm consignment terms (commission rate, minimum stock, return policy) before committing inventory."
    if cat in ("cafe_gallery",):
        return "Café exhibition slots are often booked months in advance. Verify current availability first."
    if cat in ("magazine",):
        return "Editorial submissions often go through specific channels — research the correct contact before pitching."
    return ""


def main():
    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))
    raw = json.loads(CONTACTS_PATH.read_text(encoding="utf-8"))
    is_list = isinstance(raw, list)
    contacts = raw if is_list else raw.get("contacts", [])

    existing_names = {c.get("name", "").lower().strip() for c in contacts}

    added = 0
    now = datetime.now(timezone.utc).isoformat()

    for opp in opps:
        if opp.get("exclusive_primary_bucket") != "relationship_builders":
            continue
        score = float(opp.get("truth_aligned_score") or opp.get("overall_score") or 0)
        if score < 7.0:
            continue
        name = opp.get("name", "").strip()
        if not name or name.lower() in existing_names:
            continue

        cat = opp.get("category", "")
        contact_type = TYPE_MAP.get(cat, cat or "venue")

        new_contact = {
            "name":            name,
            "type":            contact_type,
            "city":            opp.get("city", "Tokyo"),
            "country":         opp.get("country", "Japan"),
            "contact_email":   opp.get("contact") if opp.get("contact") and "@" in str(opp.get("contact", "")) else None,
            "contact_page":    opp.get("contact_page") or opp.get("contact_url") or None,
            "official_website": opp.get("official_website") or opp.get("source_url") or None,
            "submission_page": opp.get("submission_page") or None,
            "status":          "cold",
            "why_relevant":    opp.get("why_this_fits_short") or opp.get("one_sentence") or "",
            "last_contacted":  None,
            "response_received": False,
            "notes":           "",
            "date_added":      now[:16].replace("T", " "),
            "date_updated":    now[:16].replace("T", " "),
            "crm_analysis": {
                "contact_summary":      "",
                "relationship_stage":   "cold",
                "recommended_status":   "cold",
                "follow_up_timing":     "Research first; visit in person before any email outreach.",
                "next_action":          _next_action(opp),
                "risk_notes":           _risk_notes(opp),
                "priority":             "medium" if score >= 9.0 else "low",
            },
        }
        contacts.append(new_contact)
        existing_names.add(name.lower().strip())
        added += 1
        print(f"  Added: {name} [{contact_type}] score={score}")

    if is_list:
        out = contacts
    else:
        raw["contacts"] = contacts
        out = raw

    CONTACTS_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nAdded {added} new CRM contacts from relationship_builders.")


if __name__ == "__main__":
    main()
