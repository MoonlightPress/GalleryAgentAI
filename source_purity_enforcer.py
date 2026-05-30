
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
REPORT_PATH = "reports/source_purity_enforcer_report.md"

def load(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def current_score(opp):
    for k in ["truth_aligned_score", "watercolor_adjusted_score", "dna_adjusted_score", "differentiated_score", "overall_score"]:
        if opp.get(k) is not None:
            try:
                return float(opp.get(k) or 0)
            except Exception:
                pass
    return 0.0

def main():
    opps = load(OPP_PATH, [])

    changed = []

    for opp in opps:
        native = opp.get("native_medium", "unknown")
        translation = bool(opp.get("translation_candidate"))
        score = current_score(opp)
        old = score
        reason = None

        if opp.get("recommendation_visibility") == "hidden" or opp.get("verification_bucket") == "reject":
            score = min(score, 2.5)
            reason = "hidden/rejected"
        elif native == "painting":
            score = min(10, score + 0.7)
            reason = "native painting/works-on-paper boost"
        elif native == "mixed":
            score = min(9.0, score + (0.35 if translation else 0.0))
            reason = "mixed medium / possible translation"
        elif native == "photography":
            if translation:
                score = min(score, 7.2)
                reason = "photography source capped as translation candidate"
            else:
                score = min(score, 5.4)
                reason = "photography-only source demoted"
        elif native == "unknown":
            score = min(score, 7.0)
            reason = "unknown native medium capped"

        opp["source_purity_score"] = round(max(0, min(10, score)), 2)
        opp["source_purity_reason"] = reason or "no change"

        if round(old, 2) != opp["source_purity_score"]:
            changed.append({
                "title": opp.get("title") or opp.get("name") or "Unknown",
                "native": native,
                "translation": translation,
                "old": round(old, 2),
                "new": opp["source_purity_score"],
                "reason": opp["source_purity_reason"],
            })

    opps.sort(key=lambda x: float(x.get("source_purity_score", 0) or 0), reverse=True)
    save(OPP_PATH, opps)

    lines = [
        "# Source Purity Enforcer Report",
        "",
        "This report adjusts scores based on the original/native medium of the opportunity, not rewritten prose.",
        "",
        "## Changes",
        "",
    ]

    for c in changed[:100]:
        lines.append(f"- **{c['title']}** — {c['old']} → {c['new']} — native: {c['native']} — translation: {c['translation']} — {c['reason']}")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")
    print(f"Source purity changes: {len(changed)}")
    print(f"Wrote {REPORT_PATH}")

if __name__ == "__main__":
    main()
