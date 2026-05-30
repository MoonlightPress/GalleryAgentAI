
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
REPORT_PATH = "reports/translation_candidates.md"

TRANSLATION_TERMS = [
    "artist book", "zine", "printed matter", "book fair", "small press",
    "bookstore", "publication", "edition", "calendar", "poster",
    "works on paper", "illustration", "drawing"
]

BAD_PHOTO_ONLY = [
    "street photography award", "camera", "lensculture", "photo contest",
    "photography award", "photojournalism"
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
    for k in ["title","name","organization","category","one_sentence","why_this_fits_short","source_url","official_website"]:
        if opp.get(k):
            parts.append(str(opp[k]))
    for k in ["fit_keyword_hits","watercolor_fit_hits","visual_fit_hits"]:
        for x in opp.get(k, []) or []:
            parts.append(str(x))
    return " ".join(parts).lower()

def main():
    opps = load(OPP_PATH, [])

    lines = [
        "# Translation Candidates",
        "",
        "These are not native watercolor opportunities, but may be useful if watercolor work is translated into a book, zine, edition, or printed sequence.",
        "",
    ]

    count = 0

    for opp in opps:
        text = blob(opp)
        native = opp.get("native_medium", "unknown")

        hits = [t for t in TRANSLATION_TERMS if t in text]
        bad = [t for t in BAD_PHOTO_ONLY if t in text]

        translation = bool(hits) and native in {"photography", "mixed", "unknown"} and not bad

        opp["translation_candidate"] = translation
        opp["translation_candidate_hits"] = hits[:10]

        if translation:
            count += 1
            title = opp.get("title") or opp.get("name") or "Unknown"
            lines.append(f"- **{title}** — native: {native}; signals: {', '.join(hits[:6])}")

    save(OPP_PATH, opps)

    lines.insert(3, f"Total translation candidates: {count}")
    Path("reports").mkdir(exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")
    print(f"Translation candidates: {count}")
    print(f"Wrote {REPORT_PATH}")

if __name__ == "__main__":
    main()
