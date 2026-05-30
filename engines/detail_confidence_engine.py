
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_REPORT = "reports/detail_confidence_report.md"

DETAILS = [
    "deadline",
    "fees",
    "submission_page",
    "publication_frequency",
    "contact",
    "email",
    "contact_url"
]


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def detail_score(opp):
    score = 0
    present = []
    missing = []

    for key in DETAILS:
        if opp.get(key):
            score += 1
            present.append(key)
        else:
            missing.append(key)

    evidence_bonus = 0

    if opp.get("deadline_evidence"):
        evidence_bonus += 1

    if opp.get("evidence_quality") in {"moderate", "strong"}:
        evidence_bonus += 1

    total = score + evidence_bonus

    if total >= 6:
        grade = "strong"
    elif total >= 4:
        grade = "moderate"
    elif total >= 2:
        grade = "weak"
    else:
        grade = "poor"

    return total, grade, present, missing


def main():
    opps = load_json(OPP_PATH, [])

    lines = [
        "# Detail Confidence Report",
        "",
        "This report ranks how much concrete actionable information exists for each opportunity.",
        ""
    ]

    for opp in opps:
        score, grade, present, missing = detail_score(opp)

        opp["detail_confidence_score"] = score
        opp["detail_confidence_grade"] = grade
        opp["detail_present_fields"] = present
        opp["detail_missing_fields"] = missing

        lines.append(f"## {opp.get('title') or opp.get('name')}")
        lines.append(f"- Grade: {grade}")
        lines.append(f"- Score: {score}")
        lines.append(f"- Present: {', '.join(present) or 'none'}")
        lines.append(f"- Missing: {', '.join(missing) or 'none'}")
        lines.append("")

    opps.sort(
        key=lambda x: (
            float(x.get("overall_score", 0) or 0),
            float(x.get("detail_confidence_score", 0) or 0)
        ),
        reverse=True
    )

    with open(OPP_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, indent=2, ensure_ascii=False)

    Path(OUT_REPORT).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_REPORT}")


if __name__ == "__main__":
    main()
