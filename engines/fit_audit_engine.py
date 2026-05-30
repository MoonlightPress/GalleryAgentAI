
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_JSON = "memory/fit_audit.json"
OUT_MD = "reports/fit_audit_report.md"


POSITIVE_FIELDS = [
    "deep_match_score",
    "lineage_score",
    "preference_adjustment",
    "prestige_score",
]

NEGATIVE_FIELDS = [
    "corporate_penalty",
]


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def title_of(opp):
    return opp.get("title") or opp.get("name") or "Unknown"


def num(value):
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def missing_fields(opp):
    missing = []

    checks = {
        "source": opp.get("source_link") or opp.get("source_url") or opp.get("official_website"),
        "submission": opp.get("submission_page"),
        "deadline": opp.get("deadline"),
        "fees": opp.get("fees"),
        "contact": opp.get("contact") or opp.get("email") or opp.get("contact_url") or opp.get("contact_email"),
    }

    for key, value in checks.items():
        if not value:
            missing.append(key)

    return missing


def positive_reasons(opp):
    reasons = []

    if num(opp.get("deep_match_score")) > 0:
        reasons.append(f"deep artist fit +{opp.get('deep_match_score')}")

    if num(opp.get("lineage_score")) > 0:
        reasons.append(f"aesthetic lineage +{opp.get('lineage_score')}")

    if num(opp.get("preference_adjustment")) > 0:
        reasons.append(f"learned preference +{opp.get('preference_adjustment')}")

    if num(opp.get("prestige_score")) >= 8:
        reasons.append("high prestige")

    if opp.get("source_type") == "global_seed":
        reasons.append("global/international target")

    tags = [str(t).lower() for t in opp.get("tags", [])]
    for keyword in ["photobook", "publication", "zine", "artist_book", "global"]:
        if keyword in tags:
            reasons.append(f"tag: {keyword}")

    return reasons


def risk_reasons(opp):
    risks = []

    if num(opp.get("corporate_penalty")) > 0:
        risks.append(f"corporate/poor-fit penalty -{opp.get('corporate_penalty')}")

    missing = missing_fields(opp)
    if len(missing) >= 3:
        risks.append("many missing verification fields: " + ", ".join(missing))

    if num(opp.get("difficulty_score")) >= 8:
        risks.append("high difficulty")

    if num(opp.get("overall_score")) >= 8 and len(positive_reasons(opp)) <= 1:
        risks.append("high score but few clear supporting reasons")

    if num(opp.get("overall_score")) >= 8 and missing:
        risks.append("high score but still needs verification")

    if num(opp.get("overall_score")) <= 4 and num(opp.get("lineage_score")) >= 1:
        risks.append("low score despite possible aesthetic fit")

    return risks


def confidence_grade(opp):
    score = num(opp.get("overall_score"))
    missing = len(missing_fields(opp))
    reasons = len(positive_reasons(opp))
    risks = len(risk_reasons(opp))

    if score >= 7 and reasons >= 3 and missing <= 2 and risks <= 1:
        return "solid"
    if score >= 7 and (missing >= 3 or risks >= 2):
        return "needs review"
    if score < 5 and reasons >= 2:
        return "possibly underrated"
    if score >= 8 and reasons <= 1:
        return "possibly inflated"
    return "normal"


def audit_item(opp):
    return {
        "title": title_of(opp),
        "score": opp.get("overall_score"),
        "confidence_grade": confidence_grade(opp),
        "positive_reasons": positive_reasons(opp),
        "risks": risk_reasons(opp),
        "missing_fields": missing_fields(opp),
        "category": opp.get("category_label") or opp.get("category"),
        "city": opp.get("city"),
        "country": opp.get("country"),
    }


def main():
    opps = load_json(OPP_PATH, [])

    audit = [audit_item(opp) for opp in opps]
    save_json(OUT_JSON, audit)

    lines = [
        "# Fit Audit Report",
        "",
        "This report checks whether high-scoring opportunities are actually supported by fit evidence.",
        "",
        "## Needs Review",
        "",
    ]

    needs = [x for x in audit if x["confidence_grade"] in {"needs review", "possibly inflated", "possibly underrated"}]

    for item in needs[:40]:
        lines.append(f"### {item['title']} — {item['score']}/10 — {item['confidence_grade']}")
        if item["positive_reasons"]:
            lines.append("Positive reasons:")
            for r in item["positive_reasons"]:
                lines.append(f"- {r}")
        if item["risks"]:
            lines.append("Risks:")
            for r in item["risks"]:
                lines.append(f"- {r}")
        lines.append("")

    lines += [
        "",
        "## Top Solid Matches",
        "",
    ]

    solid = [x for x in audit if x["confidence_grade"] == "solid"]

    for item in solid[:25]:
        lines.append(f"- {item['title']} — {item['score']}/10 — {', '.join(item['positive_reasons'][:4])}")

    Path(OUT_MD).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_MD).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"Audited {len(audit)} opportunities.")


if __name__ == "__main__":
    main()
