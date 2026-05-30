
import json
import os
from pathlib import Path

DNA_PATH = "memory/artist_dna.json"
OPP_PATH = "deploy_data/compact_opportunities.json"
REPORT_PATH = "reports/dna_recommendation_boost_report.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def blob(opp):
    parts = []
    for key in ["title", "name", "organization", "category", "one_sentence", "why_this_fits_short"]:
        if opp.get(key):
            parts.append(str(opp[key]))

    for key in ["visual_fit_hits", "fit_keyword_hits", "tags"]:
        for x in opp.get(key, []) or []:
            parts.append(str(x))

    return " ".join(parts).lower()


def main():
    dna = load_json(DNA_PATH, {})
    opps = load_json(OPP_PATH, [])

    if not dna:
        print("No artist DNA found. Run visual_dna_extractor.py first.")
        return

    inferred = dna.get("inferred_artist_dna", {})

    positive_terms = []
    for key in ["core_subject_likelihoods", "visual_behavior", "best_project_formats"]:
        positive_terms.extend(inferred.get(key, []))

    negative_terms = inferred.get("anti_patterns", [])

    changed = 0
    lines = [
        "# DNA Recommendation Boost Report",
        "",
    ]

    for opp in opps:
        text = blob(opp)
        old = float(opp.get("differentiated_score", opp.get("overall_score", 0)) or 0)
        delta = 0.0
        hits = []

        for term in positive_terms:
            words = term.lower().replace("/", " ").split()
            if any(w in text for w in words if len(w) > 4):
                delta += 0.12
                hits.append(term)

        for term in negative_terms:
            words = term.lower().replace("/", " ").split()
            if any(w in text for w in words if len(w) > 4):
                delta -= 0.35
                hits.append("anti:" + term)

        if delta:
            new = round(max(0, min(10, old + delta)), 2)
            opp["dna_adjusted_score"] = new
            opp["dna_score_delta"] = round(delta, 2)
            opp["dna_match_hits"] = hits[:10]
            changed += 1
            lines.append(f"- {opp.get('title') or opp.get('name')}: {old} → {new}; {', '.join(hits[:5])}")
        else:
            opp.setdefault("dna_adjusted_score", old)

    opps.sort(key=lambda x: float(x.get("dna_adjusted_score", x.get("differentiated_score", x.get("overall_score", 0))) or 0), reverse=True)

    save_json(OPP_PATH, opps)

    Path(REPORT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"DNA-adjusted opportunities: {changed}")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
