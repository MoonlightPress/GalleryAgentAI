
import json
from collections import defaultdict
from pathlib import Path

SRC = "memory/submission_intelligence.json"
REPORT1 = "reports/submission_intelligence_report.md"
REPORT2 = "reports/artist_readiness_report.md"

CORE_REQUIREMENTS = ["portfolio", "artist_statement", "images"]

def readiness(requirements):
    found = set(requirements or [])
    score = 0
    missing = []

    for req in CORE_REQUIREMENTS:
        if req in found:
            score += 2
        else:
            missing.append(req)

    if "bio" in found:
        score += 1
    if "cv" in found:
        score += 1
    if "pdf" in found:
        score += 1
    if "application_form" in found:
        score += 1

    return min(10, score), missing

def main():
    pages = json.loads(Path(SRC).read_text(encoding="utf-8"))

    grouped = defaultdict(list)
    for p in pages:
        score, missing = readiness(p.get("requirements_detected", []))
        p["artist_readiness_score"] = score
        p["artist_missing_materials"] = missing
        grouped[p.get("source_title", "Unknown")].append(p)

    lines = ["# Submission Intelligence Report", ""]
    ready_lines = ["# Artist Readiness Report", ""]

    for title, items in grouped.items():
        best = sorted(items, key=lambda x: (
            x.get("artist_readiness_score", 0),
            x.get("deadline_confidence", 0),
            len(x.get("emails", []))
        ), reverse=True)[0]

        lines.append(f"## {title}")
        lines.append(f"- Best page: {best.get('submission_page_url')}")
        lines.append(f"- Page title: {best.get('page_title')}")
        lines.append(f"- Fetch: {best.get('fetch_status')}")
        lines.append(f"- Deadline: {best.get('best_deadline')} (confidence {best.get('deadline_confidence')})")
        lines.append(f"- Fee: {best.get('best_fee')}")
        lines.append(f"- Emails: {', '.join(best.get('emails', [])[:3]) or best.get('source_contact', 'unknown')}")
        lines.append(f"- Requirements: {', '.join(best.get('requirements_detected', []))}")
        lines.append("")

        ready_lines.append(f"## {title}")
        ready_lines.append(f"- Readiness score: {best.get('artist_readiness_score')}/10")
        ready_lines.append(f"- Missing: {', '.join(best.get('artist_missing_materials', [])) or 'none detected'}")
        ready_lines.append(f"- Prepare: portfolio PDF, 80–120 word artist statement, 8–12 work images, short bio")
        ready_lines.append(f"- Best page: {best.get('submission_page_url')}")
        ready_lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT1).write_text("\n".join(lines), encoding="utf-8")
    Path(REPORT2).write_text("\n".join(ready_lines), encoding="utf-8")

    Path(SRC).write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote {REPORT1}")
    print(f"Wrote {REPORT2}")

if __name__ == "__main__":
    main()
