
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
EVIDENCE_PATH = "memory/evidence_records.json"
OUT_PATH = "reports/evidence_score_guard.md"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def title_of(opp):
    return opp.get("title") or opp.get("name") or "Unknown"

def cap_for_quality(quality):
    if quality == "strong":
        return 9.6
    if quality == "moderate":
        return 8.8
    if quality == "weak":
        return 8.0
    return 7.2

def main():
    opps = load_json(OPP_PATH, [])
    evidence = load_json(EVIDENCE_PATH, {})

    lines = [
        "# Evidence Score Guard",
        "",
        "Scores are capped when evidence is weak or missing.",
        "",
    ]

    changed = 0

    for opp in opps:
        title = title_of(opp)
        ev = evidence.get(title, {})
        quality = ev.get("evidence_quality", "none")
        cap = cap_for_quality(quality)
        score = float(opp.get("overall_score", 0) or 0)

        opp["evidence_quality"] = quality
        opp["evidence_count"] = ev.get("evidence_count", 0)

        if score > cap:
            opp["pre_evidence_guard_score"] = score
            opp["overall_score"] = cap
            opp["evidence_guard_note"] = f"Score capped at {cap} because evidence quality is {quality}."
            changed += 1
            lines.append(f"- {title}: {score} → {cap} ({quality})")

    opps.sort(key=lambda x: float(x.get("overall_score", 0) or 0), reverse=True)

    with open(OPP_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, indent=2, ensure_ascii=False)

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Capped {changed} opportunities based on evidence.")
    print(f"Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
