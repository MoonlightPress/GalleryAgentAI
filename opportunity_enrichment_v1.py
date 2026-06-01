
import json
import re
from pathlib import Path

CANONICAL = Path("memory/canonical_opportunities.json")
GALLERIES = Path("memory/gallery_candidates.json")
OUT_JSON = Path("memory/enriched_opportunities.json")
OUT_DEPLOY = Path("deploy_data/enriched_opportunities.json")
OUT_REPORT = Path("reports/enriched_opportunities.md")

TOP_PER_CATEGORY = {
    "zines": 12,
    "contests": 12,
    "residencies": 10,
    "publishing": 8,
    "galleries": 12,
}

def load(path, fallback):
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback

def infer_action(opp):
    cat = opp.get("career_category")
    if cat == "zines":
        return "Check application window, booth/table fee, required images, and whether a finished zine is required."
    if cat == "contests":
        return "Confirm deadline, fee, eligibility, required images, and application form."
    if cat == "residencies":
        return "Confirm eligibility, duration, cost, housing, and project proposal requirements."
    if cat == "publishing":
        return "Decide whether this is a real target, benchmark, directory, or self-publishing service."
    if cat == "galleries":
        return "Review current/past artists and check whether submissions, contact email, or open calls are visible."
    return "Open source and verify current requirements."

def infer_risks(opp):
    risks = []
    if not opp.get("has_application") and opp.get("career_category") not in {"galleries", "publishing"}:
        risks.append("Application route may be unclear.")
    if not opp.get("has_deadline_signal") and opp.get("career_category") in {"contests", "residencies", "zines"}:
        risks.append("Deadline needs manual confirmation.")
    if opp.get("source_count", 0) <= 1:
        risks.append("Only one source found so far.")
    if opp.get("career_category") == "publishing":
        risks.append("Publishing results are noisy; verify that this is not only a directory or service.")
    if not risks:
        risks.append("Main risk is fit and competitiveness.")
    return risks

def fit_score(opp):
    cat = opp.get("career_category")
    base = {
        "zines": 82,
        "contests": 78,
        "residencies": 65,
        "publishing": 55,
        "galleries": 70,
    }.get(cat, 50)

    if opp.get("has_application"):
        base += 8
    if opp.get("has_deadline_signal"):
        base += 5
    if opp.get("source_count", 0) >= 3:
        base += 5

    title = opp.get("canonical_name", "").lower()
    if any(x in title for x in ["tokas", "tokyo art book fair", "jinny", "hayama", "kyoto art center", "zine"]):
        base += 5

    if cat == "publishing" and opp.get("score", 0) < 65:
        base -= 12

    return max(0, min(100, round(base)))

def actionability_score(opp):
    base = opp.get("score", 50)
    if opp.get("has_application"):
        base += 8
    if opp.get("has_deadline_signal"):
        base += 6
    if opp.get("best_url"):
        base += 4
    if opp.get("career_category") == "publishing":
        base -= 10
    return max(0, min(100, round(base)))

def enrich_opp(opp):
    fit = fit_score(opp)
    actionability = actionability_score(opp)
    risk = max(0, min(100, 100 - ((fit + actionability) / 2)))

    return {
        **opp,
        "fit_score": fit,
        "actionability_score": actionability,
        "risk_score": round(risk),
        "recommended_next_action": infer_action(opp),
        "risks": infer_risks(opp),
        "why_for_nin": why_for_nin(opp, fit),
    }

def why_for_nin(opp, fit):
    cat = opp.get("career_category")
    name = opp.get("canonical_name", "")
    if cat == "zines":
        return f"{name} fits because zines and art-book contexts suit quiet works-on-paper, small editions, atmosphere, and visual sequencing."
    if cat == "contests":
        return f"{name} is worth checking because open calls can turn existing portfolio work into a concrete application."
    if cat == "residencies":
        return f"{name} may matter later if her portfolio package and project statement become strong enough."
    if cat == "galleries":
        return f"{name} may fit if its past artists show quiet contemporary work, painting, drawing, atmosphere, or place-based themes."
    if cat == "publishing":
        return f"{name} is mainly useful as a benchmark unless it clearly accepts proposals or artist-book submissions."
    return f"{name} needs manual fit review."

def gallery_to_enriched(row):
    base = {
        "canonical_name": row["title"],
        "career_category": "galleries",
        "score": row.get("score", 50),
        "source_count": 1,
        "best_url": row.get("url", ""),
        "best_source_kind": "reference",
        "has_application": any(x in f"{row.get('title','')} {row.get('url','')}".lower() for x in ["submission", "open call", "公募", "募集"]),
        "has_deadline_signal": False,
        "has_fee_signal": False,
        "sources": [{
            "url": row.get("url", ""),
            "title": row.get("title", ""),
            "kind": "reference",
            "score": row.get("score", 50),
            "candidate_id": row.get("candidate_id"),
        }],
        "status": "gallery_candidate",
        "neighborhood": row.get("neighborhood", "Tokyo"),
    }
    return enrich_opp(base)

def main():
    canonical = load(CANONICAL, {"opportunities": []}).get("opportunities", [])
    galleries = load(GALLERIES, {"candidates": []}).get("candidates", [])

    selected = []
    for cat, limit in TOP_PER_CATEGORY.items():
        if cat == "galleries":
            rows = sorted(galleries, key=lambda x: x.get("score", 0), reverse=True)[:limit]
            selected.extend([gallery_to_enriched(r) for r in rows])
        else:
            rows = [o for o in canonical if o.get("career_category") == cat]
            rows = sorted(rows, key=lambda x: x.get("score", 0), reverse=True)[:limit]
            selected.extend([enrich_opp(o) for o in rows])

    selected.sort(key=lambda x: (x.get("fit_score", 0) + x.get("actionability_score", 0)), reverse=True)

    data = {
        "enriched_count": len(selected),
        "opportunities": selected,
    }

    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_DEPLOY.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_DEPLOY.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Enriched Opportunities", "", f"- Enriched: {len(selected)}", ""]
    for cat in ["zines", "contests", "residencies", "galleries", "publishing"]:
        rows = [o for o in selected if o.get("career_category") == cat]
        if not rows:
            continue
        lines.append(f"## {cat}")
        for o in rows:
            lines.append(f"### {o['canonical_name']}")
            lines.append(f"- Fit: {o['fit_score']}")
            lines.append(f"- Actionability: {o['actionability_score']}")
            lines.append(f"- Risk: {o['risk_score']}")
            lines.append(f"- URL: {o.get('best_url','')}")
            lines.append(f"- Next action: {o['recommended_next_action']}")
            lines.append(f"- Why for Nin: {o['why_for_nin']}")
            lines.append("")
        lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_DEPLOY)
    print("Wrote", OUT_REPORT)
    print("Enriched:", len(selected))

if __name__ == "__main__":
    main()
