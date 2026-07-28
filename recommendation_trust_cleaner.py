
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/recommendation_trust_cleaner_report.md"

BAD_TITLE_BITS = [
    "facebook",
    "instagram",
    "pinterest",
    "tiktok",
    "continue reading",
    "magazine subscription",
    "magazine subscribers",
    "www.facebook.com",
    "www.instagram.com",
]

BAD_PHRASES = {
    # Remove photography framing from AI-generated descriptions.
    # GEGYjiji is a watercolor painter — these replacements correct
    # copy that mis-describes her medium as photography.
    "photographic work": "watercolor work",
    "photographer": "watercolor artist",
    "photographers": "watercolor artists",
    "photographerly": "watercolor artistly",
    "photography": "watercolor",
    "photographs": "paintings",
    "illustrator": "artist",
    "illustrators": "artists",
    "illustrative work": "watercolor work",
    "technical skill would shine": "the work could translate well",
    "decorative": "surface-level",
}

TEXT_FIELDS = [
    "one_sentence",
    "why_this_fits_short",
    "quick_action",
    "submission_strategy",
    "submission_tone",
    "score_sanity_note",
    "final_score_guard_note",
]


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def clean_text(value):
    if not isinstance(value, str):
        return value

    text = value

    for bad, replacement in BAD_PHRASES.items():
        text = text.replace(bad, replacement)
        text = text.replace(bad.title(), replacement.title())

    return text


def backfill_identity(opp):
    """Make `name` and `title` agree. 41 live entries (2026-07-28) carried only
    `title` — real calls invisible to any consumer keying on `name`. Same
    split-field class as added_at/imported_at and fee/fees: backfill both
    spellings once here rather than teaching every reader the fallback.
    Entries that already have both are left alone (they may legitimately
    differ: short name vs long formal title). Returns True if changed."""
    name = str(opp.get("name") or "").strip()
    title = str(opp.get("title") or "").strip()
    if name and not title:
        opp["title"] = name
        return True
    if title and not name:
        opp["name"] = title
        return True
    return False


def is_junk(opp):
    title = str(opp.get("title") or opp.get("name") or "").lower()
    source = str(
        opp.get("source_url")
        or opp.get("official_website")
        or opp.get("source_link")
        or ""
    ).lower()

    blob = title + " " + source

    return any(bit in blob for bit in BAD_TITLE_BITS)


def main():
    opps = load_json(OPP_PATH, [])

    cleaned = 0
    rejected = 0
    backfilled = 0

    for opp in opps:
        if backfill_identity(opp):
            backfilled += 1
        for field in TEXT_FIELDS:
            if field in opp:
                old = opp[field]
                new = clean_text(old)
                if new != old:
                    opp[field] = new
                    cleaned += 1

        bullets = opp.get("three_bullets", [])
        if isinstance(bullets, list):
            new_bullets = [clean_text(x) for x in bullets]
            if new_bullets != bullets:
                opp["three_bullets"] = new_bullets
                cleaned += 1

        if is_junk(opp):
            opp["recommendation_visibility"] = "hidden"
            opp["primary_bucket"] = "reject"
            opp["verification_bucket"] = "reject"
            opp["overall_score"] = min(float(opp.get("overall_score", 0) or 0), 2.0)
            opp["differentiated_score"] = min(float(opp.get("differentiated_score", 0) or 0), 2.0)
            rejected += 1
        else:
            opp.setdefault("recommendation_visibility", "show")

    opps.sort(
        key=lambda x: float(x.get("differentiated_score", x.get("overall_score", 0)) or 0),
        reverse=True,
    )

    save_json(OPP_PATH, opps)

    lines = [
        "# Recommendation Trust Cleaner Report",
        "",
        f"Text fields cleaned: {cleaned}",
        f"Junk opportunities hidden: {rejected}",
        "",
    ]

    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Cleaned text fields: {cleaned}")
    print(f"Hidden junk opportunities: {rejected}")
    print(f"Backfilled name/title identity: {backfilled}")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
