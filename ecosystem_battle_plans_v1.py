
import json
from pathlib import Path

GALLERIES = Path("memory/gallery_ecosystem.json")
FAIRS = Path("memory/fair_ecosystem.json")
OPEN_CALLS = Path("memory/verified_open_calls.json")
RANKINGS = Path("memory/opportunity_rankings.json")
OUT_REPORT = Path("reports/ecosystem_battle_plans.md")
OUT_JSON = Path("memory/ecosystem_battle_plans.json")
OUT_DEPLOY = Path("deploy_data/ecosystem_battle_plans.json")

def load(path, fallback):
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback

def main():
    galleries = load(GALLERIES, {"targets": []}).get("targets", [])
    fairs = load(FAIRS, {"targets": []}).get("targets", [])
    calls = load(OPEN_CALLS, {"records": []}).get("records", [])
    rankings = load(RANKINGS, {"rankings": {}}).get("rankings", {})

    actionable_calls = [c for c in calls if c.get("status") == "actionable"]
    local_galleries = [g for g in galleries if g.get("neighborhood") in {"Koenji", "Nakano", "Kichijoji", "Shimokitazawa"}]
    zine_fairs = [f for f in fairs if "zine" in f.get("fair_type", "") or "book" in f.get("fair_type", "")]
    creator_fairs = [f for f in fairs if "creator" in f.get("fair_type", "") or "illustration" in f.get("fair_type", "")]

    plans = {
        "zines": {
            "title": "Zines / Art Books",
            "summary": f"{len(zine_fairs)} fair/event targets plus existing shop targets. Best used after two small zines exist.",
            "strongest": [f["name"] for f in zine_fairs[:5]],
            "plan": [
                "Finish two small zines.",
                "Confirm Tokyo Art Book Fair deadline/fee.",
                "Use shop placement as proof before fair applications.",
                "Apply to one realistic fair and visit one major fair.",
            ],
        },
        "galleries": {
            "title": "Galleries",
            "summary": f"{len(galleries)} gallery targets identified; {len(local_galleries)} are in local-west Tokyo neighborhoods.",
            "strongest": [g["name"] for g in galleries[:10]],
            "plan": [
                "Review top 10 gallery targets for past artists and fit.",
                "Reject rental-only or poor-fit spaces.",
                "Build a small portfolio PDF and one short statement.",
                "Contact only the top 3 after review.",
            ],
        },
        "open_calls": {
            "title": "Open Calls / Competitions",
            "summary": f"{len(calls)} verified call/application records; {len(actionable_calls)} currently look actionable.",
            "strongest": [c["name"] for c in actionable_calls[:8]],
            "plan": [
                "Open the actionable list.",
                "Confirm deadline and fee manually.",
                "Pick two clear-fit applications.",
                "Prepare reusable package: 10 images, statement, CV, short bio.",
            ],
        },
        "fairs_events": {
            "title": "Fairs / Creator Events",
            "summary": f"{len(fairs)} fair/event targets mapped, including art fairs, creator markets, and illustration events.",
            "strongest": [f["name"] for f in fairs[:10]],
            "plan": [
                "Separate prestige fairs from beginner-friendly fairs.",
                "Prioritize Design Festa / COMITIA / SICF-type creator events for practical first participation.",
                "Track booth fee and application window.",
                "Use zines/prints as table-ready products.",
            ],
        },
    }

    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_DEPLOY.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    OUT_JSON.write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_DEPLOY.write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Ecosystem Battle Plans", ""]
    for key, p in plans.items():
        lines += [f"## {p['title']}", "", p["summary"], "", "### Strongest", ""]
        for s in p["strongest"]:
            lines.append(f"- {s}")
        lines += ["", "### Plan", ""]
        for step in p["plan"]:
            lines.append(f"- {step}")
        lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_DEPLOY)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
