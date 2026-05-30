
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


def verification_points(opp):
    points = 0

    if opp.get("url_verification_status") == "ok":
        points += 2

    if opp.get("submission_page"):
        points += 2

    if opp.get("deadline"):
        points += 1

    if opp.get("fees"):
        points += 1

    if opp.get("contact") or opp.get("email") or opp.get("contact_url") or opp.get("contact_email"):
        points += 1

    return points


def cap_for(opp):
    points = verification_points(opp)

    if points <= 1:
        return 6.5

    if points == 2:
        return 7.6

    if points == 3:
        return 8.2

    if points == 4:
        return 8.8

    if points == 5:
        return 9.2

    return 9.6


def main():
    opps = load_json(OPP_PATH, [])

    lines = [
        "# Final Score Guard Report",
        "",
        "This runs at the end of the pipeline so later scoring scripts cannot inflate weakly verified opportunities.",
        "",
    ]

    changed = 0

    for opp in opps:
        old = float(opp.get("overall_score", 0) or 0)
        cap = cap_for(opp)

        if old > cap:
            opp["pre_final_guard_score"] = old
            opp["overall_score"] = cap
            opp["final_score_guard_note"] = f"Capped at {cap} due to verification strength."
            changed += 1
            lines.append(f"- {opp.get('title')}: {old} → {cap}")

    opps.sort(key=lambda x: float(x.get("overall_score", 0) or 0), reverse=True)

    with open(OPP_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, indent=2, ensure_ascii=False)

    Path(REPORT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Final score guard capped {changed} opportunities.")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
