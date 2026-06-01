
import json
from pathlib import Path

GALLERIES = Path("memory/gallery_ecosystem.json")
FAIRS = Path("memory/fair_ecosystem.json")
OPEN_CALLS = Path("memory/verified_open_calls.json")
OUT_JSON = Path("memory/opportunity_rankings.json")
OUT_DEPLOY = Path("deploy_data/opportunity_rankings.json")
OUT_REPORT = Path("reports/opportunity_rankings.md")

LOCAL_HOODS = ["Koenji", "Nakano", "Kichijoji", "Shimokitazawa"]

def load(path, fallback):
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback

def make_item(name, category, score, reason, url="", extra=None):
    return {
        "name": name,
        "category": category,
        "score": score,
        "reason": reason,
        "url": url,
        **(extra or {}),
    }

def main():
    galleries = load(GALLERIES, {"targets": []}).get("targets", [])
    fairs = load(FAIRS, {"targets": []}).get("targets", [])
    calls = load(OPEN_CALLS, {"records": []}).get("records", [])

    rankings = {}

    rankings["highest_actionability"] = sorted(
        [
            make_item(c["name"], c["category"], c.get("actionability_score") or 0, "Verified application/call data.", c.get("url", ""), c)
            for c in calls
        ],
        key=lambda x: x["score"], reverse=True
    )[:15]

    rankings["closest_to_koenji"] = sorted(
        [
            make_item(g["name"], "galleries", g["score"], f"Neighborhood: {g.get('neighborhood')}", g.get("url", ""), g)
            for g in galleries
            if g.get("neighborhood") in LOCAL_HOODS
        ],
        key=lambda x: x["score"], reverse=True
    )[:15]

    rankings["best_for_emerging_artists"] = sorted(
        [
            make_item(g["name"], "galleries", g["score"], "Emerging/submission/gallery signal.", g.get("url", ""), g)
            for g in galleries
            if g.get("submission_signal") or "emerging artists" in g.get("artist_type", [])
        ] + [
            make_item(f["name"], "fairs_events", f["score"], f"Beginner friendliness: {f.get('beginner_friendliness')}", f.get("application_url", ""), f)
            for f in fairs
            if f.get("beginner_friendliness") in {"high", "medium"}
        ],
        key=lambda x: x["score"], reverse=True
    )[:20]

    rankings["highest_prestige"] = sorted(
        [
            make_item(f["name"], "fairs_events", f["score"], "High-prestige fair/event signal.", f.get("application_url", ""), f)
            for f in fairs if f.get("prestige") == "high"
        ] + [
            make_item(c["name"], c["category"], c.get("actionability_score") or 0, "High-prestige open-call/residency candidate.", c.get("url", ""), c)
            for c in calls if any(x in c["name"].lower() for x in ["tokas", "kyoto", "hayama", "shoto"])
        ],
        key=lambda x: x["score"], reverse=True
    )[:15]

    rankings["best_for_prints_and_zines"] = sorted(
        [
            make_item(f["name"], "fairs_events", f["score"], f["fair_type"], f.get("application_url", ""), f)
            for f in fairs
            if "zine" in f.get("fair_type", "") or "book" in f.get("fair_type", "") or "creator" in f.get("fair_type", "")
        ],
        key=lambda x: x["score"], reverse=True
    )[:20]

    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_DEPLOY.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    data = {"rankings": rankings}
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_DEPLOY.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Opportunity Rankings / Heat Map", ""]
    for key, rows in rankings.items():
        lines += [f"## {key}", ""]
        for r in rows:
            lines.append(f"- {r['name']} — {r['category']} — score {r['score']}")
            lines.append(f"  - {r['reason']}")
            if r.get("url"):
                lines.append(f"  - {r['url']}")
        lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_DEPLOY)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
