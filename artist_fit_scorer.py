
import json
from pathlib import Path

DNA = "memory/artist_dna.json"
TYPES = "memory/opportunity_type_classifications.json"
RECS = "memory/nin_opportunity_recommendations.json"
EVIDENCE_CARDS = "memory/opportunity_evidence_cards.json"

OUT_JSON = "memory/artist_fit_scores.json"
OUT_REPORT = "reports/artist_fit_scores.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def by_title(rows):
    return {r.get("title"): r for r in rows if r.get("title")}

def score(types, dna):
    strong = set(dna.get("strong_fit_opportunity_types", []))
    weak = set(dna.get("weak_fit_opportunity_types", []))
    t = set(types)

    s = 35
    reasons = []

    strong_hits = sorted(t.intersection(strong))
    weak_hits = sorted(t.intersection(weak))

    if strong_hits:
        s += min(50, len(strong_hits) * 18)
        reasons.append("strong type match: " + ", ".join(strong_hits))

    if weak_hits:
        s -= min(45, len(weak_hits) * 20)
        reasons.append("weak type warning: " + ", ".join(weak_hits))

    if "unknown" in t:
        s -= 10
        reasons.append("type unclear")

    return max(0, min(100, s)), reasons

def main():
    dna = load(DNA, {})
    type_rows = load(TYPES, [])
    recs = by_title(load(RECS, []))
    cards = by_title(load(EVIDENCE_CARDS, []))

    rows = []
    for tr in type_rows:
        title = tr["title"]
        fit, reasons = score(tr["opportunity_types"], dna)
        rec = recs.get(title, {})
        card = cards.get(title, {})

        combined = round(
            fit * 0.65
            + (rec.get("recommendation_score", 0) or 0) * 0.25
            + (20 if card else 0) * 0.10,
            1
        )

        if combined >= 75:
            label = "very strong personal fit"
        elif combined >= 55:
            label = "promising personal fit"
        elif combined >= 35:
            label = "possible but not personal"
        else:
            label = "low personal fit"

        rows.append({
            "title": title,
            "artist_fit_score": fit,
            "combined_personal_score": combined,
            "fit_label": label,
            "opportunity_types": tr["opportunity_types"],
            "fit_reasons": reasons,
            "existing_recommendation_score": rec.get("recommendation_score"),
            "evidence_card_present": bool(card),
        })

    rows.sort(key=lambda x: x["combined_personal_score"], reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(rows, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Artist Fit Scores",
        "",
        "Scores opportunities against Artist DNA, not just general opportunity quality.",
        "",
    ]

    for r in rows:
        lines.append(f"## {r['title']}")
        lines.append(f"- Personal score: {r['combined_personal_score']}/100 ({r['fit_label']})")
        lines.append(f"- Artist fit only: {r['artist_fit_score']}/100")
        lines.append(f"- Types: {', '.join(r['opportunity_types'])}")
        lines.append(f"- Reasons: {', '.join(r['fit_reasons']) or 'none'}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
