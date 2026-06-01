
import json
from pathlib import Path
from collections import defaultdict

SRC = "memory/submission_intelligence.json"
OUT = "memory/actionable_target_shortlist.json"
REPORT = "reports/actionable_target_shortlist.md"

def score_page(p):
    score = 0

    if p.get("fetch_status") == "ok":
        score += 2

    if p.get("emails"):
        score += 2
    elif p.get("source_contact") not in [None, "", "unknown"]:
        score += 1

    if p.get("best_deadline") not in [None, "", "unknown"]:
        score += 2

    if p.get("best_fee") not in [None, "", "unknown"]:
        score += 1

    reqs = p.get("requirements_detected", [])
    if reqs and "manual_review_needed" not in reqs:
        score += min(3, len(reqs))

    if "exhibition" in (p.get("submission_page_url", "") or "").lower():
        score += 1

    if "archive" in (p.get("submission_page_url", "") or "").lower():
        score -= 2

    return max(0, score)

def main():
    if not Path(SRC).exists():
        raise SystemExit("Missing memory/submission_intelligence.json. Run run_submission_intelligence.py first.")

    pages = json.loads(Path(SRC).read_text(encoding="utf-8"))

    grouped = defaultdict(list)
    for p in pages:
        p["actionability_score"] = score_page(p)
        grouped[p.get("source_title", "Unknown")].append(p)

    shortlist = []
    for title, items in grouped.items():
        best = sorted(items, key=lambda x: x.get("actionability_score", 0), reverse=True)[0]
        shortlist.append(best)

    shortlist.sort(key=lambda x: x.get("actionability_score", 0), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    Path(OUT).write_text(json.dumps(shortlist, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Actionable Target Shortlist",
        "",
        "This ranks targets by whether they have usable contact, deadline, fee, requirement, or submission-page information.",
        "",
    ]

    for p in shortlist:
        lines.append(f"## {p.get('source_title')}")
        lines.append(f"- Actionability score: {p.get('actionability_score')}")
        lines.append(f"- Best page: {p.get('submission_page_url')}")
        lines.append(f"- Contact: {', '.join(p.get('emails', [])[:2]) or p.get('source_contact', 'unknown')}")
        lines.append(f"- Deadline: {p.get('best_deadline', 'unknown')}")
        lines.append(f"- Fee: {p.get('best_fee', 'unknown')}")
        lines.append(f"- Requirements: {', '.join(p.get('requirements_detected', []))}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Wrote {REPORT}")

if __name__ == "__main__":
    main()
