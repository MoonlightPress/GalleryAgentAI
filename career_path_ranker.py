
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/watercolor_career_path_rankings.md"

PATHS = {
    "gallery_relationship": {
        "label": "Gallery Relationship",
        "terms": ["gallery", "artist-run gallery", "works on paper", "painting", "small works", "open exhibition"],
        "avoid": ["photography award", "photo contest", "street photography", "craft fair"],
    },
    "works_on_paper_open_calls": {
        "label": "Works on Paper Open Calls",
        "terms": ["works on paper", "drawing", "painting", "watercolor", "open call", "open exhibition", "paper"],
        "avoid": ["photobook-only", "camera", "photojournalism"],
    },
    "bookstore_artist_book": {
        "label": "Bookstore / Artist Book Translation",
        "terms": ["bookstore", "artist book", "zine", "printed matter", "book fair", "small press"],
        "avoid": ["street photography award", "photo contest"],
    },
    "low_pressure_local": {
        "label": "Low-Pressure Local Visibility",
        "terms": ["cafe", "bookstore", "shimokitazawa", "local", "small works", "gallery"],
        "avoid": ["prestige", "major institution"],
    },
    "stretch": {
        "label": "Stretch / Benchmark",
        "terms": ["residency", "grant", "contemporary art", "institution", "portfolio review", "open exhibition"],
        "avoid": ["wrong medium", "doesn't fit"],
    },
}

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def blob(opp):
    parts = []
    for k in ["title", "name", "organization", "category", "one_sentence", "why_this_fits_short", "watercolor_warning"]:
        if opp.get(k):
            parts.append(str(opp[k]))
    for k in ["watercolor_fit_hits", "photo_only_risk_hits", "visual_fit_hits", "fit_keyword_hits"]:
        for x in opp.get(k, []) or []:
            parts.append(str(x))
    return " ".join(parts).lower()

def rank_for_path(opp, config):
    text = blob(opp)

    if opp.get("recommendation_visibility") == "hidden":
        return -999, []

    base = float(opp.get("truth_aligned_score", opp.get("watercolor_adjusted_score", opp.get("overall_score", 0))) or 0)
    hits = []

    for t in config["terms"]:
        if t in text:
            base += 0.6
            hits.append(t)

    for t in config["avoid"]:
        if t in text:
            base -= 1.2
            hits.append("avoid:" + t)

    return round(base, 2), hits

def main():
    opps = load_json(OPP_PATH, [])

    lines = [
        "# Watercolor Career Path Rankings",
        "",
        "This ranks opportunities by practical career path instead of one universal score.",
        "",
    ]

    for key, config in PATHS.items():
        ranked = []
        for opp in opps:
            score, hits = rank_for_path(opp, config)
            if score > 0 and hits:
                ranked.append((score, hits, opp))

        ranked.sort(key=lambda x: x[0], reverse=True)

        lines.append(f"## {config['label']}")
        lines.append("")

        if not ranked:
            lines.append("_No matches._")
            lines.append("")
            continue

        for score, hits, opp in ranked[:10]:
            title = opp.get("title") or opp.get("name") or "Unknown"
            why = opp.get("why_this_fits_short") or opp.get("one_sentence") or ""
            lines.append(f"- **{title}** — path score {score}; signals: {', '.join(hits[:6])}. {why}")

        lines.append("")

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
