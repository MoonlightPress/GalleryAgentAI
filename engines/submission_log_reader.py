"""
submission_log_reader.py — marks already_submitted, boosts accepted venues, flags prior_rejection.

Reads memory/submission_log.json and memory/contact_memory.json.
Writes back to deploy_data/compact_opportunities.json with new fields:
  - already_submitted: bool
  - submission_outcome: str (last outcome, e.g. "accepted"/"rejected"/"pending")
  - prior_rejection: bool
  - venue_accepted: bool (accepted at least once)
  Score boost of +0.6 if venue_accepted, -0.3 penalty if prior_rejection.
"""

import sys
import json
import re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT       = Path(__file__).parent.parent
OPP_PATH   = ROOT / "deploy_data" / "compact_opportunities.json"
LOG_PATH   = ROOT / "Memory" / "submission_log.json"
CRM_PATH   = ROOT / "Memory" / "contact_memory.json"
REPORT_PATH = ROOT / "reports" / "submission_log_reader_report.md"


def _normalise(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def _matches(venue_str, opp):
    """True if venue_str token-matches any name field on the opportunity."""
    vn = _normalise(venue_str)
    if len(vn) < 4:
        return False
    for field in ("name", "title", "organization", "official_website", "source_url"):
        fn = _normalise(opp.get(field) or "")
        if vn in fn or fn in vn:
            return True
    return False


def load_submissions():
    if not LOG_PATH.exists():
        return []
    data = json.loads(LOG_PATH.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def load_crm_contacts():
    if not CRM_PATH.exists():
        return []
    data = json.loads(CRM_PATH.read_text(encoding="utf-8"))
    contacts = data.get("contacts", []) if isinstance(data, dict) else data
    return contacts


def main():
    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))
    submissions = load_submissions()
    crm_contacts = load_crm_contacts()

    if not submissions:
        print("No submissions on record — nothing to mark.")
        return

    # Build lookup: {normalised_venue: [submission, ...]}
    sub_index: dict[str, list] = {}
    for s in submissions:
        key = _normalise(s.get("venue", ""))
        if key:
            sub_index.setdefault(key, []).append(s)

    marked = accepted = rejected = 0

    for opp in opps:
        # Find any submissions that match this opportunity
        matched_subs = [s for s in submissions if _matches(s.get("venue", ""), opp)]

        if not matched_subs:
            opp.setdefault("already_submitted", False)
            opp.setdefault("prior_rejection", False)
            opp.setdefault("venue_accepted", False)
            continue

        outcomes = [s.get("outcome", "pending") for s in matched_subs]
        last = matched_subs[-1]

        opp["already_submitted"]    = True
        opp["submission_outcome"]   = last.get("outcome", "pending")
        opp["prior_rejection"]      = "rejected" in outcomes
        opp["venue_accepted"]       = "accepted" in outcomes

        base = float(opp.get("overall_score", 0) or 0)
        if opp["venue_accepted"]:
            opp["overall_score"] = round(min(base + 0.6, 9.8), 1)
            accepted += 1
        elif opp["prior_rejection"]:
            opp["overall_score"] = round(max(base - 0.3, 1.0), 1)
            rejected += 1

        marked += 1

    # Also mark CRM contacts that have "applied" or "ongoing" status
    crm_applied = {_normalise(c.get("name", "")) for c in crm_contacts if c.get("status") in ("applied", "ongoing")}
    if crm_applied:
        for opp in opps:
            if not opp.get("already_submitted"):
                for field in ("name", "title", "organization"):
                    fn = _normalise(opp.get(field) or "")
                    if any(ca in fn or fn in ca for ca in crm_applied if ca):
                        opp["already_submitted"] = True
                        opp.setdefault("submission_outcome", "crm_tracked")
                        break

    OPP_PATH.write_text(json.dumps(opps, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Submission Log Reader Report",
        "",
        f"- Submissions on record: {len(submissions)}",
        f"- Opportunities marked already_submitted: {marked}",
        f"- Score boosted (accepted venue): {accepted}",
        f"- Score penalised (prior rejection): {rejected}",
        "",
    ]
    if marked:
        lines.append("## Matched opportunities")
        for opp in opps:
            if opp.get("already_submitted"):
                name = opp.get("title") or opp.get("name") or "?"
                outcome = opp.get("submission_outcome", "?")
                lines.append(f"- {name}: {outcome}")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Marked {marked} opportunities. Boosted {accepted}, penalised {rejected}.")


if __name__ == "__main__":
    main()
