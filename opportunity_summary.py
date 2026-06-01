
import json
from pathlib import Path
from collections import Counter

SRC = "memory/normalized_opportunities.json"
OUT_JSON = "memory/normalized_opportunity_summary.json"
OUT_REPORT = "reports/opportunity_summary.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    data = load(SRC, {})
    opps = data.get("opportunities", [])

    by_neighborhood = Counter(o.get("neighborhood", "unknown") for o in opps)
    by_category = Counter(o.get("category", "unknown") for o in opps)

    top = sorted(opps, key=lambda x: x.get("confidence", 0), reverse=True)[:10]

    phase1_names = []
    for o in opps:
        if o.get("neighborhood") in {"Koenji", "Nakano"} and o.get("confidence", 0) >= 70:
            phase1_names.append(o["canonical_name"])
    phase1_names = phase1_names[:8]

    summary = {
        "verified_opportunities_estimate": len(opps),
        "by_neighborhood": dict(by_neighborhood),
        "by_category": dict(by_category),
        "highest_impact_targets": top[:5],
        "phase_1_targets": phase1_names,
        "practical_recommendation": {
            "current_reach": "0 stores",
            "target": "5 stores",
            "phase_1": "Koenji + Nakano",
            "action": "Create two zines, print 20 copies each, and approach the phase 1 targets first."
        }
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(summary, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Tokyo Zine Ecosystem Summary",
        "",
        f"Normalized opportunities: {len(opps)}",
        "",
        "## By Neighborhood",
    ]

    for k, v in by_neighborhood.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## By Category"]
    for k, v in by_category.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Highest Impact Targets"]
    for i, o in enumerate(top[:10], 1):
        lines.append(f"{i}. {o['canonical_name']} — {o['neighborhood']} — {o['category']} — confidence {o['confidence']}")

    lines += [
        "",
        "## Practical Recommendation",
        "- Current reach: 0 stores",
        "- Target: 5 stores",
        "- Phase 1: Koenji + Nakano",
        "- Create two zines, print 20 copies each, and approach the phase 1 targets first.",
        "",
        "## Phase 1 Targets",
    ]

    for name in phase1_names:
        lines.append(f"- {name}")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
