
import json
import os
from pathlib import Path

APPROVED_PATH = "ingestion/approved_candidates.json"
REJECTED_PATH = "ingestion/rejected_candidates.json"
OUT_PATH = "reports/candidate_review_report.md"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def section(title, items):
    lines = [f"## {title}", ""]
    for item in items[:50]:
        lines.append(f"### {item.get('title')}")
        lines.append(f"- Quality score: {item.get('quality_gate_score')}")
        lines.append(f"- Source: {item.get('source_url')}")
        lines.append(f"- Fit hits: {', '.join(item.get('fit_keyword_hits', []))}")
        if item.get("reject_keyword_hits"):
            lines.append(f"- Reject hits: {', '.join(item.get('reject_keyword_hits', []))}")
        lines.append(f"- Summary: {item.get('one_sentence', '')[:300]}")
        lines.append("")
    return lines

def main():
    approved = load_json(APPROVED_PATH, [])
    rejected = load_json(REJECTED_PATH, [])

    lines = [
        "# Candidate Review Report",
        "",
        "This report shows scraped candidates before they become serious recommendations.",
        "",
        f"Approved: {len(approved)}",
        f"Rejected: {len(rejected)}",
        "",
    ]

    lines.extend(section("Approved Candidates", approved))
    lines.extend(section("Rejected / Low-Quality Candidates", rejected))

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
