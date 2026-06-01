
import json
from pathlib import Path

VERIFIED = Path("memory/verified_opportunity_fields.json")
ENRICHED = Path("memory/enriched_opportunities.json")
OUT_JSON = Path("memory/verified_open_calls.json")
OUT_REPORT = Path("reports/open_call_verification.md")

def load(path, fallback):
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback

def status_from_record(r):
    if r.get("deadline_extracted") and r.get("application_route") in {"form", "application_page", "email_possible"}:
        return "actionable"
    if r.get("application_route") in {"form", "application_page", "email_possible"}:
        return "needs_deadline_check"
    return "needs_manual_review"

def main():
    verified = load(VERIFIED, {"records": []}).get("records", [])
    enriched = load(ENRICHED, {"opportunities": []}).get("opportunities", [])
    by_name = {e.get("canonical_name", ""): e for e in enriched}

    records = []
    for r in verified:
        if r.get("career_category") not in {"contests", "galleries", "zines", "residencies"}:
            continue
        e = by_name.get(r.get("canonical_name", ""), {})
        records.append({
            "name": r.get("canonical_name"),
            "category": r.get("career_category"),
            "url": r.get("url"),
            "deadline": r.get("deadline_extracted", ""),
            "fee": r.get("fee_extracted", ""),
            "emails": r.get("emails", []),
            "application_route": r.get("application_route", ""),
            "fit_score": e.get("fit_score"),
            "actionability_score": e.get("actionability_score"),
            "status": status_from_record(r),
            "next_action": e.get("recommended_next_action", "Open source and verify requirements."),
        })

    records.sort(key=lambda x: (
        {"actionable": 0, "needs_deadline_check": 1, "needs_manual_review": 2}.get(x["status"], 9),
        -(x.get("actionability_score") or 0),
        -(x.get("fit_score") or 0),
    ))

    data = {
        "verified_open_call_count": len(records),
        "actionable_count": len([r for r in records if r["status"] == "actionable"]),
        "records": records,
    }

    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Open Call / Application Verification",
        "",
        f"- Records: {len(records)}",
        f"- Actionable: {data['actionable_count']}",
        "",
    ]
    for status in ["actionable", "needs_deadline_check", "needs_manual_review"]:
        rows = [r for r in records if r["status"] == status]
        lines += [f"## {status} ({len(rows)})", ""]
        for r in rows[:40]:
            lines.append(f"### {r['name']}")
            lines.append(f"- Category: {r['category']}")
            lines.append(f"- Deadline: {r['deadline'] or 'Check source'}")
            lines.append(f"- Fee: {r['fee'] or 'Check source'}")
            lines.append(f"- Route: {r['application_route']}")
            lines.append(f"- Email: {', '.join(r['emails']) if r['emails'] else 'None extracted'}")
            lines.append(f"- Fit: {r.get('fit_score')}")
            lines.append(f"- Actionability: {r.get('actionability_score')}")
            lines.append(f"- URL: {r['url']}")
            lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
