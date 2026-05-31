
import json
from pathlib import Path
from datetime import date

EXISTING = "memory/verified_zine_businesses.json"
DECISIONS = "memory/candidate_business_decisions.json"
OUT_JSON = "memory/verified_zine_businesses.json"
OUT_REPORT = "reports/verified_zine_businesses.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def normalize_key(row):
    return (row.get("name", "").strip().lower(), row.get("address", "").strip().lower())

def main():
    existing = load(EXISTING, {"businesses": []})
    decisions = load(DECISIONS, {"decisions": []})

    businesses = existing.get("businesses", [])
    seen = {normalize_key(b) for b in businesses}

    added = []
    rejected = []
    skipped = []

    for d in decisions.get("decisions", []):
        decision = d.get("decision", "").lower().strip()

        if decision == "approved":
            row = {
                "name": d.get("name", "").strip(),
                "address": d.get("address", "").strip(),
                "website": d.get("website", "").strip(),
                "instagram": d.get("instagram", "").strip(),
                "email": d.get("email", "").strip(),
                "phone": d.get("phone", "").strip(),
                "category": d.get("category", "").strip(),
                "neighborhood": d.get("neighborhood", "").strip(),
                "accepts_consignment": d.get("accepts_consignment", "unknown"),
                "accepts_submissions": d.get("accepts_submissions", "unknown"),
                "notes": d.get("notes", ""),
                "source_candidate_id": d.get("candidate_id"),
                "verification_status": "verified_by_user",
                "last_verified": str(date.today()),
            }
            if not row["name"]:
                skipped.append({"candidate_id": d.get("candidate_id"), "reason": "approved_missing_name"})
                continue

            key = normalize_key(row)
            if key not in seen:
                businesses.append(row)
                seen.add(key)
                added.append(row)

        elif decision == "rejected":
            rejected.append(d)
        elif decision == "skipped":
            skipped.append(d)

    result = {
        "businesses": businesses,
        "business_count": len(businesses),
        "last_ingest": str(date.today()),
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Verified Zine Businesses",
        "",
        f"- Total verified businesses: {len(businesses)}",
        f"- Added this run: {len(added)}",
        f"- Rejected in decisions: {len(rejected)}",
        f"- Skipped in decisions: {len(skipped)}",
        "",
    ]

    by_neighborhood = {}
    for b in businesses:
        by_neighborhood.setdefault(b.get("neighborhood") or "unknown", []).append(b)

    for hood, rows in sorted(by_neighborhood.items()):
        lines.append(f"## {hood}")
        for b in rows:
            lines.append(f"- {b['name']} — {b.get('category')} — {b.get('address')}")
            if b.get("website"):
                lines.append(f"  - {b['website']}")
            if b.get("instagram"):
                lines.append(f"  - Instagram: {b['instagram']}")
            lines.append(f"  - Consignment: {b.get('accepts_consignment')}; Submissions: {b.get('accepts_submissions')}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Added:", len(added))

if __name__ == "__main__":
    main()
