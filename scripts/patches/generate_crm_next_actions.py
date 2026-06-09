"""
generate_crm_next_actions.py

Rule-based fallback CRM next_action / risk_notes / follow_up_timing generator.
Fills in missing crm_analysis fields for contacts that lack them.
Does NOT overwrite existing values.
"""
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

CONTACTS_PATH = Path(__file__).parent.parent.parent / "memory" / "contact_memory.json"


def _next_action(c: dict) -> str:
    status = c.get("status", "cold")
    ctype = c.get("type", "")
    name = c.get("name", "this venue")

    if status == "cold":
        if ctype in ("gallery", "artist_space"):
            return f"Attend an opening or event at {name} to observe their curation style and audience before any formal approach."
        if ctype in ("bookstore_gallery", "bookshop", "bookstore"):
            return f"Visit {name} in person (or browse their online inventory) to confirm the aesthetic fit, then draft a brief consignment inquiry."
        if ctype in ("zine_shop", "zine_fair"):
            return f"Send or bring a physical copy of your work to {name} — zine culture prioritises the object over email pitches."
        if ctype in ("cafe_gallery", "cafe"):
            return f"Visit {name} to see the display space and speak with the manager about upcoming exhibition availability."
        if ctype in ("fair", "art_fair", "fair_popup"):
            return f"Research {name}'s application process and booth costs. Evaluate whether table fees align with current inventory levels."
        return f"Research {name}'s current program, submission policy, and key contact person before initiating outreach."

    if status == "researching":
        return f"Complete research on {name}: check their website for recent exhibitions, any open call announcements, and a named contact person."

    if status == "ready_to_review":
        return f"Review your research notes on {name} and decide: is this ready for a first outreach email, or do you need one more round of research?"

    if status == "in_contact":
        lc = c.get("last_contacted")
        if not lc:
            return f"You haven't logged a date for your last contact with {name}. Review your email thread and update the record."
        return f"Review your last exchange with {name} and decide whether a follow-up is appropriate — be brief and add clear new value."

    if status == "sent_inquiry":
        return f"If it has been more than 2 weeks since you wrote to {name} and no reply, a single polite follow-up is acceptable."

    return f"Review {name}'s status and determine the right next step."


def _risk_notes(c: dict) -> str:
    status = c.get("status", "cold")
    ctype = c.get("type", "")

    if ctype in ("gallery", "artist_space"):
        return "Many galleries do not accept unsolicited submissions — verify their policy before sending work."
    if ctype in ("bookstore_gallery", "bookshop"):
        return "Consignment terms vary widely — confirm commission rate, minimum stock, and return policy before committing inventory."
    if ctype in ("zine_shop",):
        return "Small zine shops often have limited space and inconsistent restocking. Confirm current capacity before sending copies."
    if ctype in ("cafe_gallery",):
        return "Café exhibition slots are often booked months in advance. Verify current availability before investing preparation time."
    if ctype in ("fair", "art_fair", "fair_popup"):
        return "Fair participation requires upfront cost and significant stock. Evaluate ROI before committing."
    if status in ("cold", "researching"):
        return "No contact established yet — research submission policy and named contact before reaching out."
    return ""


def _follow_up_timing(c: dict) -> str:
    status = c.get("status", "cold")
    ctype = c.get("type", "")

    if status == "cold":
        if ctype in ("gallery", "artist_space"):
            return "Visit in person first; follow up with email only after you have attended at least one event."
        if ctype in ("bookstore_gallery", "bookshop", "bookstore"):
            return "Reach out within the next 2-3 weeks. Bookshop relationships move slowly — don't rush."
        return "No rush — research first, then reach out when you have a clear, specific reason to."

    if status == "researching":
        return "Complete your research within 1-2 weeks and move this to ready_to_review."

    if status == "ready_to_review":
        return "Decide this week: either draft an outreach email or park this contact for 3 months."

    if status == "in_contact":
        return "Follow up only if there's a specific new reason to — a show you attended, a deadline you want to flag, or a question you need answered."

    if status == "sent_inquiry":
        return "Wait at least 2 weeks from initial contact before following up once."

    return "Review timing based on most recent interaction."


def main():
    raw = json.loads(CONTACTS_PATH.read_text(encoding="utf-8"))
    is_list = isinstance(raw, list)
    contacts = raw if is_list else raw.get("contacts", [])

    updated = 0
    for c in contacts:
        crm = c.get("crm_analysis")
        if not isinstance(crm, dict):
            crm = {}
            c["crm_analysis"] = crm

        changed = False
        if not crm.get("next_action"):
            crm["next_action"] = _next_action(c)
            changed = True
        if not crm.get("risk_notes"):
            r = _risk_notes(c)
            if r:
                crm["risk_notes"] = r
                changed = True
        if not crm.get("follow_up_timing"):
            crm["follow_up_timing"] = _follow_up_timing(c)
            changed = True

        if changed:
            updated += 1

    if is_list:
        out = contacts
    else:
        raw["contacts"] = contacts
        out = raw

    CONTACTS_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Updated CRM next_action/risk_notes/follow_up_timing for {updated} contacts.")


if __name__ == "__main__":
    main()
