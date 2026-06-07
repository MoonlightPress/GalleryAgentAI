
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
REPORT_PATH = "reports/final_score_guard_report.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


JUNK_VALUES = {"unknown", "n/a", "none", "null", "not publicly listed", "unverified", ""}


def is_real(value):
    return bool(value) and str(value).strip().lower() not in JUNK_VALUES


def has_distinct_submission_page(opp):
    raw_sub = opp.get("submission_page") or ""
    sub = (raw_sub[0] if isinstance(raw_sub, list) else raw_sub).strip().rstrip("/")
    src = (opp.get("source_url") or "").strip().rstrip("/")
    official = (opp.get("official_website") or "").strip().rstrip("/")
    return is_real(sub) and sub != src and sub != official


def verification_points(opp):
    points = 0
    if opp.get("url_verification_status") == "ok":
        points += 2
    if has_distinct_submission_page(opp):
        points += 2
    if is_real(opp.get("deadline")):
        points += 1
    if is_real(opp.get("fees")):
        points += 1
    if is_real(opp.get("contact") or opp.get("email") or opp.get("contact_url") or opp.get("contact_email")):
        points += 1
    return points


# Tier ceilings: verified entries earn higher max scores.
TIER_CEILINGS = {0: 6.5, 1: 6.5, 2: 7.6, 3: 8.2, 4: 8.8, 5: 9.2, 6: 9.6, 7: 9.6}

# Verification weight: how much to trust raw scores at each verification level.
# Calibrated so a quality composite of ~9.5 hits the tier ceiling.
V_WEIGHTS = {0: 0.68, 1: 0.74, 2: 0.80, 3: 0.86, 4: 0.93, 5: 0.97, 6: 1.0, 7: 1.0}


def quality_composite(opp):
    """Weighted blend of quality signals. Uses fallback chain so missing fields don't zero-out."""
    d = float(opp.get("differentiated_score") or opp.get("overall_score") or 0)
    t = float(opp.get("truth_aligned_score") or d)
    p = float(opp.get("source_purity_score") or d)
    pp = float(opp.get("painting_priority_score") or d)
    return 0.40 * d + 0.30 * t + 0.20 * p + 0.10 * pp


def guarded_score(opp):
    pts = min(verification_points(opp), 7)
    ceiling = TIER_CEILINGS[pts]
    weight = V_WEIGHTS[pts]
    composite = quality_composite(opp)
    raw = composite * weight
    return round(min(raw, ceiling), 1)


def main():
    opps = load_json(OPP_PATH, [])

    lines = [
        "# Final Score Guard Report",
        "",
        "Scores now reflect BOTH verification strength AND quality signals,",
        "eliminating the hard-cap clustering problem.",
        "",
    ]

    changed = 0

    for opp in opps:
        old = float(opp.get("overall_score", 0) or 0)
        new = guarded_score(opp)

        if abs(old - new) >= 0.05:
            opp["pre_final_guard_score"] = old
            opp["overall_score"] = new
            opp["final_score_guard_note"] = (
                f"Rescored {old} → {new} "
                f"(verification_points={verification_points(opp)}, "
                f"composite={round(quality_composite(opp), 2)})"
            )
            changed += 1
            name = opp.get("title") or opp.get("name") or "?"
            lines.append(f"- {name}: {old} → {new}")
        else:
            opp["overall_score"] = new  # apply minor rounding fix even if same

    opps.sort(key=lambda x: float(x.get("overall_score", 0) or 0), reverse=True)

    with open(OPP_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, indent=2, ensure_ascii=False)

    Path(REPORT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Rescored {changed} opportunities.")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
