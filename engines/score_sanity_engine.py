
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/score_sanity_report.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def source_strength(opp):
    if opp.get("url_verification_status") == "ok":
        return 2
    if opp.get("source_url") or opp.get("official_website") or opp.get("source_link"):
        return 1
    return 0


JUNK_VALUES = {"unknown", "n/a", "none", "null", "not publicly listed", "unverified", ""}


def is_real(value):
    return bool(value) and str(value).strip().lower() not in JUNK_VALUES


def has_distinct_submission_page(opp):
    sub = (opp.get("submission_page") or "").strip().rstrip("/")
    src = (opp.get("source_url") or "").strip().rstrip("/")
    official = (opp.get("official_website") or "").strip().rstrip("/")
    return is_real(sub) and sub != src and sub != official


def verification_strength(opp):
    points = 0
    if has_distinct_submission_page(opp):
        points += 1
    for key in ["deadline", "fees", "contact", "email", "contact_url"]:
        if is_real(opp.get(key)):
            points += 1
    return points


def cap_for(opp):
    source = source_strength(opp)
    verify = verification_strength(opp)

    if source == 0:
        return 6.5
    if source == 1 and verify <= 1:
        return 8.0
    if source == 2 and verify <= 1:
        return 8.6
    if source == 2 and verify >= 3:
        return 9.4
    return 8.8


def main():
    opps = load_json(OPP_PATH, [])

    lines = [
        "# Score Sanity Report",
        "",
        "This report caps inflated scores when verification is weak.",
        "",
    ]

    changed = 0

    for opp in opps:
        old = float(opp.get("overall_score", 0) or 0)
        cap = cap_for(opp)

        if old > cap:
            opp["uncapped_score"] = old
            opp["overall_score"] = cap
            opp["score_sanity_note"] = f"Score capped at {cap} because source/verification strength is limited."
            changed += 1

            lines.append(f"- {opp.get('title')}: {old} → {cap}")

    opps.sort(key=lambda x: float(x.get("overall_score", 0) or 0), reverse=True)

    with open(OPP_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, indent=2, ensure_ascii=False)

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Capped {changed} scores.")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
