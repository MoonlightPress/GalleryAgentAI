
import json
from pathlib import Path
from collections import defaultdict

BIOS = "memory/validated_artist_biographies.json"
PROFILES = "memory/validated_artist_profiles.json"
QUALITY = "memory/opportunity_quality_board.json"

OUT_JSON = "memory/validated_opportunity_credibility.json"
OUT_REPORT = "reports/validated_opportunity_credibility.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    bios = load(BIOS, [])
    profiles = load(PROFILES, [])
    quality = {q.get("title"): q for q in load(QUALITY, [])}

    by_opp = defaultdict(lambda: {
        "biographies": [],
        "profiles": [],
    })

    for b in bios:
        by_opp[b.get("source_opportunity")]["biographies"].append(b)

    for p in profiles:
        for opp in p.get("source_opportunities", []):
            by_opp[opp]["profiles"].append(p)

    rows = []
    for opp, data in by_opp.items():
        bio_count = len(data["biographies"])
        profile_count = len(data["profiles"])
        q = quality.get(opp, {})
        match_score = q.get("match_score", 0) or 0
        evidence_strength = q.get("evidence_strength", 0) or 0

        # Conservative credibility: real bios matter more than raw profile count.
        score = min(100, round((bio_count * 12) + (profile_count * 2) + (float(match_score) * 3) + (float(evidence_strength) * 0.15), 1))

        if score >= 80:
            label = "strong"
        elif score >= 50:
            label = "promising"
        elif score >= 25:
            label = "thin but usable"
        else:
            label = "weak"

        rows.append({
            "title": opp,
            "credibility_score": score,
            "credibility_label": label,
            "validated_biography_count": bio_count,
            "validated_profile_count": profile_count,
            "validated_biographies": data["biographies"][:20],
            "validated_profiles": data["profiles"][:20],
        })

    rows.sort(key=lambda x: x["credibility_score"], reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(rows, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Validated Opportunity Credibility",
        "",
        "Scores opportunities using only validated human artist/profile evidence.",
        "",
    ]

    for r in rows:
        lines.append(f"## {r['title']}")
        lines.append(f"- Credibility: {r['credibility_score']}/100 ({r['credibility_label']})")
        lines.append(f"- Validated biographies: {r['validated_biography_count']}")
        lines.append(f"- Validated profiles: {r['validated_profile_count']}")
        lines.append("")
        if r["validated_biographies"]:
            lines.append("### Validated biography examples")
            for b in r["validated_biographies"][:8]:
                lines.append(f"- {b.get('artist_name')} — birth year {b.get('birth_year')} — roles: {', '.join(b.get('roles', []))}")
        else:
            lines.append("_No validated biographies yet._")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
