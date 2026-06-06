import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
from datetime import date
from pathlib import Path

COMPACT_PATH = Path("deploy_data/compact_opportunities.json")
SUMMARY_PATH = Path("memory/verification_summary.json")
REPORT_PATH  = Path("reports/verification_status_report.md")

SCORE_RULES = [
    ("url_verification_status", lambda v: v == "ok",   2),
    ("deadline_verified",        lambda v: v is True,  2),
    ("contact_verified",         lambda v: v is True,  2),
    ("fees_verified",            lambda v: v is True,  1),
    ("submission_process_known", lambda v: v is True,  2),
    ("confirmation_gate_status", lambda v: v == "confirmed", 1),
]

MAX_SCORE = sum(w for _, _, w in SCORE_RULES)  # 10


def compute_score(opp: dict) -> int:
    score = 0
    for field, test, weight in SCORE_RULES:
        if test(opp.get(field)):
            score += weight
    return score


def score_to_status(score: int) -> str:
    if score >= 8:
        return "verified"
    if score >= 5:
        return "strong_partial"
    if score >= 3:
        return "partial"
    return "research_needed"


def what_confirmed(opp: dict) -> list[str]:
    labels = {
        "url_verification_status": ("url_verification_status", lambda v: v == "ok",   "URL ok"),
        "deadline_verified":        ("deadline_verified",        lambda v: v is True,  "deadline"),
        "contact_verified":         ("contact_verified",         lambda v: v is True,  "contact"),
        "fees_verified":            ("fees_verified",            lambda v: v is True,  "fees"),
        "submission_process_known": ("submission_process_known", lambda v: v is True,  "submission process"),
        "confirmation_gate_status": ("confirmation_gate_status", lambda v: v == "confirmed", "confirmed"),
    }
    confirmed = []
    for label_key, (field, test, label) in labels.items():
        if test(opp.get(field)):
            confirmed.append(label)
    return confirmed


def what_missing(opp: dict) -> list[str]:
    labels = {
        "url_verification_status": ("url_verification_status", lambda v: v == "ok",   "URL"),
        "deadline_verified":        ("deadline_verified",        lambda v: v is True,  "deadline"),
        "contact_verified":         ("contact_verified",         lambda v: v is True,  "contact"),
        "fees_verified":            ("fees_verified",            lambda v: v is True,  "fees"),
        "submission_process_known": ("submission_process_known", lambda v: v is True,  "submission process"),
        "confirmation_gate_status": ("confirmation_gate_status", lambda v: v == "confirmed", "medium confirmation"),
    }
    missing = []
    for label_key, (field, test, label) in labels.items():
        if not test(opp.get(field)):
            missing.append(label)
    return missing


def main():
    if not COMPACT_PATH.exists():
        print(f"ERROR: {COMPACT_PATH} not found — nothing to process.")
        return

    with COMPACT_PATH.open(encoding="utf-8") as f:
        opportunities = json.load(f)

    if not isinstance(opportunities, list):
        print("ERROR: compact_opportunities.json is not a list.")
        return

    # --- Recompute scores ---
    status_counts = {"verified": 0, "strong_partial": 0, "partial": 0, "research_needed": 0}
    field_counts = {
        "url_ok": 0,
        "deadline_verified": 0,
        "contact_verified": 0,
        "fees_verified": 0,
        "submission_process_known": 0,
        "medium_confirmed": 0,
    }

    for opp in opportunities:
        if not isinstance(opp, dict):
            continue

        score = compute_score(opp)
        status = score_to_status(score)
        opp["verification_score"] = score
        opp["verification_status"] = status
        status_counts[status] += 1

        # Field counts
        if opp.get("url_verification_status") == "ok":
            field_counts["url_ok"] += 1
        if opp.get("deadline_verified") is True:
            field_counts["deadline_verified"] += 1
        if opp.get("contact_verified") is True:
            field_counts["contact_verified"] += 1
        if opp.get("fees_verified") is True:
            field_counts["fees_verified"] += 1
        if opp.get("submission_process_known") is True:
            field_counts["submission_process_known"] += 1
        if opp.get("confirmation_gate_status") == "confirmed":
            field_counts["medium_confirmed"] += 1

    # Write back
    COMPACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with COMPACT_PATH.open("w", encoding="utf-8") as f:
        json.dump(opportunities, f, ensure_ascii=False, indent=2)

    total = len([o for o in opportunities if isinstance(o, dict)])

    # --- Summary JSON ---
    summary = {
        "total": total,
        "verified": status_counts["verified"],
        "strong_partial": status_counts["strong_partial"],
        "partial": status_counts["partial"],
        "research_needed": status_counts["research_needed"],
        **field_counts,
        "generated_at": date.today().isoformat(),
    }

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY_PATH.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # --- Markdown report ---
    sorted_opps = sorted(
        [o for o in opportunities if isinstance(o, dict)],
        key=lambda o: o.get("verification_score", 0),
        reverse=True,
    )
    top20 = sorted_opps[:20]

    # "Still needs work": high overall_score but not fully verified
    high_score_unverified = [
        o for o in opportunities
        if isinstance(o, dict)
        and (o.get("overall_score") or 0) >= 8
        and o.get("verification_status") != "verified"
    ]
    high_score_unverified.sort(key=lambda o: o.get("overall_score", 0), reverse=True)
    bottom10 = high_score_unverified[:10]

    lines = [
        "# Verification Status Report",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Summary",
        "",
        "| Status | Count |",
        "|--------|-------|",
        f"| Verified (score 8-10) | {status_counts['verified']} |",
        f"| Strong partial (5-7) | {status_counts['strong_partial']} |",
        f"| Partial (3-4) | {status_counts['partial']} |",
        f"| Research needed (<3) | {status_counts['research_needed']} |",
        f"| **Total** | **{total}** |",
        "",
        "### Field Coverage",
        "",
        "| Field | Verified count |",
        "|-------|----------------|",
        f"| URL ok | {field_counts['url_ok']} |",
        f"| Deadline verified | {field_counts['deadline_verified']} |",
        f"| Contact verified | {field_counts['contact_verified']} |",
        f"| Fees verified | {field_counts['fees_verified']} |",
        f"| Submission process known | {field_counts['submission_process_known']} |",
        f"| Medium confirmed | {field_counts['medium_confirmed']} |",
        "",
        "---",
        "",
        "## Top 20 Highest-Verification Opportunities",
        "",
    ]

    for i, opp in enumerate(top20, 1):
        name = opp.get("title") or opp.get("name") or f"Opportunity #{i}"
        score = opp.get("verification_score", 0)
        confirmed = what_confirmed(opp)
        missing = what_missing(opp)
        confirmed_str = ", ".join(confirmed) if confirmed else "none"
        missing_str = ", ".join(missing) if missing else "none"
        lines.append(f"### {i}. {name}")
        lines.append(f"- **Verification score:** {score}/{MAX_SCORE}")
        lines.append(f"- **Confirmed:** {confirmed_str}")
        lines.append(f"- **Missing:** {missing_str}")
        lines.append("")

    lines += [
        "---",
        "",
        "## Still Needs Work",
        "",
        "High-scored opportunities (overall_score >= 8) that are not yet fully verified.",
        "",
    ]

    if bottom10:
        for i, opp in enumerate(bottom10, 1):
            name = opp.get("title") or opp.get("name") or f"Opportunity #{i}"
            overall = opp.get("overall_score", "?")
            vscore = opp.get("verification_score", 0)
            vstatus = opp.get("verification_status", "unknown")
            missing = what_missing(opp)
            missing_str = ", ".join(missing) if missing else "none"
            lines.append(f"### {i}. {name}")
            lines.append(f"- **Overall score:** {overall}  |  **Verification score:** {vscore}/{MAX_SCORE}  |  **Status:** {vstatus}")
            lines.append(f"- **Missing verification:** {missing_str}")
            lines.append("")
    else:
        lines.append("_No high-scored opportunities with incomplete verification found._")
        lines.append("")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # --- Stdout summary ---
    print("Verification report complete.")
    print(f"  Total opportunities     : {total}")
    print(f"  Verified (8-10)         : {status_counts['verified']}")
    print(f"  Strong partial (5-7)    : {status_counts['strong_partial']}")
    print(f"  Partial (3-4)           : {status_counts['partial']}")
    print(f"  Research needed (<3)    : {status_counts['research_needed']}")
    print(f"  URL ok                  : {field_counts['url_ok']}")
    print(f"  Deadline verified       : {field_counts['deadline_verified']}")
    print(f"  Fees verified           : {field_counts['fees_verified']}")
    print(f"  Medium confirmed        : {field_counts['medium_confirmed']}")
    print(f"  Summary written to      : {SUMMARY_PATH}")
    print(f"  Report written to       : {REPORT_PATH}")
    print(f"  High-scored unverified  : {len(high_score_unverified)} (top 10 in report)")


if __name__ == "__main__":
    main()
