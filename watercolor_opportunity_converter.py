
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
REPORT_PATH = "reports/watercolor_opportunity_conversion.md"

PHOTO_WORDS = {
    "photographer": "watercolor artist",
    "photographic": "painterly",
    "photography": "watercolor / works on paper",
    "photobook": "artist book / watercolor sequence",
    "street photography": "urban observational painting",
    "portfolio review": "portfolio review for works on paper"
}

WATERCOLOR_POSITIVE_TERMS = [
    "watercolor", "watercolour", "works on paper", "drawing", "painting",
    "small works", "artist-run gallery", "gallery", "residency", "grant",
    "bookstore", "artist book", "zine", "illustration", "paper", "contemporary art"
]

PHOTOGRAPHY_ONLY_TERMS = [
    "street photography", "photography award", "photo contest", "lensculture",
    "camera", "photojournalism"
]

def load(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def blob(opp):
    parts = []
    for k in ["title", "name", "organization", "category", "one_sentence", "why_this_fits_short"]:
        if opp.get(k):
            parts.append(str(opp[k]))
    return " ".join(parts).lower()

def convert_text(value):
    if not isinstance(value, str):
        return value
    text = value
    for old, new in PHOTO_WORDS.items():
        text = text.replace(old, new).replace(old.title(), new.title())
    return text

def main():
    opps = load(OPP_PATH, [])
    converted = boosted = demoted = 0

    for opp in opps:
        text = blob(opp)

        for field in ["one_sentence", "why_this_fits_short", "quick_action", "submission_strategy", "submission_tone"]:
            if field in opp:
                old = opp[field]
                opp[field] = convert_text(old)
                if opp[field] != old:
                    converted += 1

        if isinstance(opp.get("three_bullets"), list):
            old = opp["three_bullets"]
            opp["three_bullets"] = [convert_text(x) for x in old]
            if opp["three_bullets"] != old:
                converted += 1

        watercolor_hits = [t for t in WATERCOLOR_POSITIVE_TERMS if t in text]
        photo_only_hits = [t for t in PHOTOGRAPHY_ONLY_TERMS if t in text]

        opp["watercolor_fit_hits"] = watercolor_hits
        opp["photo_only_risk_hits"] = photo_only_hits

        score = float(opp.get("dna_adjusted_score", opp.get("differentiated_score", opp.get("overall_score", 0))) or 0)

        if watercolor_hits:
            score += min(1.4, len(watercolor_hits) * 0.28)
            boosted += 1

        if photo_only_hits and not any(x in text for x in ["artist book", "zine", "printed matter", "bookstore"]):
            score -= min(3.0, len(photo_only_hits) * 1.0)
            opp["watercolor_warning"] = "Photography-only context. Low priority unless translated into a painted sequence or artist book."
            demoted += 1

        if any(x in text for x in ["lensculture", "street photography award", "photo contest"]):
            opp["exclusive_primary_bucket"] = "low_priority"
            opp["watercolor_warning"] = "Likely wrong-medium opportunity."
            score = min(score, 5.2)
            demoted += 1

        opp["watercolor_adjusted_score"] = round(max(0, min(10, score)), 2)

    opps.sort(key=lambda x: float(x.get("watercolor_adjusted_score", x.get("overall_score", 0)) or 0), reverse=True)
    save(OPP_PATH, opps)

    lines = [
        "# Watercolor Opportunity Conversion Report",
        "",
        f"Converted text fields: {converted}",
        f"Boosted watercolor/works-on-paper matches: {boosted}",
        f"Demoted photography-only matches: {demoted}",
        "",
        "## Top Watercolor-Adjusted Opportunities",
        ""
    ]

    for opp in opps[:25]:
        lines.append(f"- **{opp.get('title') or opp.get('name')}** — watercolor score {opp.get('watercolor_adjusted_score')}; hits: {', '.join(opp.get('watercolor_fit_hits', [])[:6])}")
        if opp.get("watercolor_warning"):
            lines.append(f"  - Warning: {opp['watercolor_warning']}")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")
    print(f"Converted fields: {converted}")
    print(f"Boosted: {boosted}")
    print(f"Demoted: {demoted}")
    print(f"Wrote {REPORT_PATH}")

if __name__ == "__main__":
    main()
