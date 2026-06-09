
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
REPORT_PATH = "reports/opportunity_truth_checker_report.md"

NEGATIVE_PHRASES = [
    "it doesn't",
    "doesn't fit",
    "does not fit",
    "wrong medium",
    "low priority",
    "low impact",
    "not strategic",
    "not ideal",
    "unlikely",
    "unclear",
    "question mark",
    "poor match",
    "weak fit",
    "bad fit",
    "commercial pop-up format conflicts",
    "would pull you away",
    "undermine your positioning",
    "not actionable",
    "requires significant investigative work",
    "lack of clear",
    "complete lack",
]

PHOTOGRAPHY_ONLY_PHRASES = [
    "street photography",
    "photography award",
    "photo contest",
    "portfolio prize",
    "photographers' gallery",
    "aperture",
    "lensculture",
    "photovogue",
]

STRONG_WATERCOLOR_TERMS = [
    "watercolor",
    "watercolour",
    "works on paper",
    "drawing",
    "painting",
    "small works",
    "illustration gallery",
    "open exhibition",
    "gallery open call",
    "artist-run gallery",
]

TEXT_FIELDS = [
    "title",
    "name",
    "organization",
    "category",
    "one_sentence",
    "why_this_fits_short",
    "quick_action",
    "submission_strategy",
    "submission_tone",
    "watercolor_warning",
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


def blob(opp):
    parts = []
    for field in TEXT_FIELDS:
        if opp.get(field):
            parts.append(str(opp[field]))

    for field in ["three_bullets", "watercolor_fit_hits", "photo_only_risk_hits", "visual_fit_hits", "fit_keyword_hits"]:
        for item in opp.get(field, []) or []:
            parts.append(str(item))

    return " ".join(parts).lower()


def truth_check(opp):
    text = blob(opp)

    negative_hits = [p for p in NEGATIVE_PHRASES if p in text]
    photo_hits = [p for p in PHOTOGRAPHY_ONLY_PHRASES if p in text]
    watercolor_hits = [p for p in STRONG_WATERCOLOR_TERMS if p in text]

    current = float(
        opp.get("watercolor_adjusted_score",
        opp.get("dna_adjusted_score",
        opp.get("differentiated_score",
        opp.get("overall_score", 0)))) or 0
    )

    cap = 10.0
    verdict = "ok"
    reasons = []

    if negative_hits:
        cap = min(cap, 6.4)
        verdict = "capped_negative_explanation"
        reasons.append("negative explanation: " + ", ".join(negative_hits[:4]))

    # Photography cap exempts native_medium=photography — Nin is a photographer
    if photo_hits and not watercolor_hits and opp.get("native_medium") != "photography":
        cap = min(cap, 5.8)
        verdict = "capped_wrong_medium"
        reasons.append("photography-only risk: " + ", ".join(photo_hits[:4]))

    if opp.get("recommendation_visibility") == "hidden":
        cap = min(cap, 2.5)
        verdict = "hidden"
        reasons.append("hidden recommendation")

    if opp.get("verification_bucket") == "reject":
        cap = min(cap, 2.5)
        verdict = "reject"
        reasons.append("verification rejected")

    if "comitia" in text:
        cap = min(cap, 6.0)
        verdict = "capped_context_mismatch"
        reasons.append("self-publishing/doujinshi context may conflict with positioning")

    if "design festa" in text and "gallery" not in text:
        cap = min(cap, 5.8)
        verdict = "capped_market_format"
        reasons.append("market format risk")

    corrected = round(min(current, cap), 2)

    opp["truth_alignment_verdict"] = verdict
    opp["truth_alignment_reasons"] = reasons
    opp["truth_aligned_score"] = corrected

    if corrected < current:
        opp["score_capped_by_truth_checker"] = True
    else:
        opp["score_capped_by_truth_checker"] = False

    return current, corrected, verdict, reasons


def main():
    opps = load_json(OPP_PATH, [])

    changed = []
    counts = {}

    for opp in opps:
        old, new, verdict, reasons = truth_check(opp)
        counts[verdict] = counts.get(verdict, 0) + 1

        if new < old:
            changed.append({
                "title": opp.get("title") or opp.get("name") or "Unknown",
                "old": old,
                "new": new,
                "verdict": verdict,
                "reasons": reasons,
            })

    opps.sort(key=lambda x: float(x.get("truth_aligned_score", 0) or 0), reverse=True)
    save_json(OPP_PATH, opps)

    lines = [
        "# Opportunity Truth Checker Report",
        "",
        "This report caps scores when the explanation contradicts the ranking.",
        "",
        "## Verdict Counts",
        "",
    ]

    for k, v in sorted(counts.items()):
        lines.append(f"- {k}: {v}")

    lines += [
        "",
        "## Score Caps Applied",
        "",
    ]

    if not changed:
        lines.append("_No score caps applied._")
    else:
        for item in changed[:80]:
            lines.append(f"- **{item['title']}** — {item['old']} → {item['new']} — {item['verdict']}")
            for reason in item["reasons"]:
                lines.append(f"  - {reason}")

    Path(REPORT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Truth checker capped: {len(changed)}")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
