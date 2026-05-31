
import json
import re
from pathlib import Path
from collections import defaultdict

BIO_SRC = "memory/artist_biographies.json"
PROFILE_SRC = "memory/real_artist_profiles.json"

OUT_BIOS = "memory/validated_artist_biographies.json"
OUT_PROFILES = "memory/validated_artist_profiles.json"
OUT_REPORT = "reports/artist_name_validation_report.md"

REJECT_CONTAINS = [
    "Award", "Prize", "Gallery", "Society", "Institute", "Competition", "Exhibition",
    "Artist of the Year", "Scholarship", "Book Fair", "Open Exhibition",
    "Federation", "Foundation", "Association", "University", "Annual Exhibition",
    "Art Consultancy", "Art Commissions", "Arts Education", "Visual Arts",
    "Central London", "Great Britain", "Fire Horse", "Chinese Year",
    "Privacy", "Policy", "Application", "Contact", "Menu", "Schedule",
    "Newsletter", "Copyright", "Venue Hire", "Event Hire", "Book Fair",
]

REJECT_STARTS = [
    "The ", "For ", "Including ", "Located ", "Founded ", "To ", "Royal ",
    "British Artists", "Marine Artists", "Open Calls", "Young Artist",
    "NEAC Artist", "Society", "Art ", "Arts ",
]

REJECT_EXACT = {
    "アマ問わず",
    "ピンポイント絵本コンペの",
    "回日本絵本賞",
    "回おひさま大賞優秀賞",
    "Bristol. The",
    "Robert. Value",
    "Simon. Value",
    "Baltic Exchange. Including",
    "NCI. The Baltic",
    "The RSMA",
    "The RBA",
    "The Artist September",
    "The Natural Eye",
    "The Birdwatch",
    "Swarovski Optik Artist",
    "British Artists. Charity",
    "British Artists",
    "Queen Elizabeth II",
    "Her Royal Highness The",
    "British Artists CEO Tom",
    "Portrait Painters President Anthony",
    "British Artists. Join",
    "Great Britain",
    "Central London",
    "Fire Horse",
    "Chinese Year",
    "Shengxinyu Art",
    "NEAC Artist Scholarships",
}

KNOWN_GOOD = {
    "千葉智江",
    "飯野和好",
    "つじにぬき",
    "Grahame Booth",
    "Andrew Graham-Dixon",
    "Michael Harrison",
    "Zhang Hongbin",
    "Charles Pears",
    "Ronald Benham RBA NEAC",
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def clean_name(name):
    return " ".join(str(name or "").replace("\u3000", " ").split()).strip(" 。、:：-")

def looks_japanese_person(name):
    # Accept compact kanji/kana names. Reject phrases with particles or obvious non-name terms.
    if not re.fullmatch(r"[一-龥ぁ-んァ-ンー・]{2,12}", name):
        return False
    bad_bits = ["コンペ", "問わず", "受賞", "入賞", "作品", "絵本賞", "大賞", "展示", "審査", "現役"]
    return not any(b in name for b in bad_bits)

def looks_english_person(name):
    # Strict-ish Western person pattern.
    if not re.fullmatch(r"[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’.-]+(?:\s+[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’.-]+){1,4}", name):
        return False

    parts = name.split()
    if len(parts) < 2:
        return False

    bad_words = {
        "Award", "Prize", "Gallery", "Society", "Institute", "Competition",
        "Exhibition", "Foundation", "Federation", "Association", "Annual",
        "Artist", "Artists", "British", "Marine", "Central", "London",
        "Chinese", "Fire", "Horse", "Visual", "Arts", "Art", "Education",
        "Commissions", "Consultancy", "Venue", "Event", "Hire", "Scholarships",
        "Natural", "Eye", "Birdwatch", "Swarovski", "Optik", "Application",
    }
    if any(p in bad_words for p in parts):
        return False

    # Reject sentence fragments ending with weird clipped connector words.
    if parts[-1] in {"The", "Including", "Value", "Join"}:
        return False

    return True

def validate_name(name, evidence=""):
    name = clean_name(name)
    if not name:
        return False, "empty"

    if name in KNOWN_GOOD:
        return True, "known_good"

    if name in REJECT_EXACT:
        return False, "reject_exact"

    if len(name) < 2 or len(name) > 50:
        return False, "length"

    if name.isupper():
        return False, "all_caps"

    for term in REJECT_CONTAINS:
        if term.lower() in name.lower():
            return False, f"contains:{term}"

    for term in REJECT_STARTS:
        if name.startswith(term):
            return False, f"starts:{term.strip()}"

    if "." in name and not re.search(r"\b[A-Z]\.", name):
        return False, "sentence_fragment_period"

    if looks_japanese_person(name):
        return True, "jp_person_pattern"

    if looks_english_person(name):
        return True, "en_person_pattern"

    return False, "no_person_pattern"

def main():
    bios = load(BIO_SRC, [])
    profiles = load(PROFILE_SRC, [])

    valid_bios = []
    rejected_bios = []

    for b in bios:
        ok, reason = validate_name(b.get("artist_name"), b.get("bio_text", ""))
        row = dict(b)
        row["validation_reason"] = reason
        if ok:
            valid_bios.append(row)
        else:
            rejected_bios.append(row)

    valid_profile_names = {b["artist_name"] for b in valid_bios}
    valid_profiles = []
    rejected_profiles = []

    for p in profiles:
        ok, reason = validate_name(p.get("name"), " ".join(p.get("evidence", [])) if isinstance(p.get("evidence"), list) else "")
        row = dict(p)
        row["validation_reason"] = reason

        # Allow profiles confirmed by a valid biography even if the profile name validator is strict.
        if p.get("name") in valid_profile_names:
            row["validation_reason"] = "matched_valid_biography"
            valid_profiles.append(row)
        elif ok:
            valid_profiles.append(row)
        else:
            rejected_profiles.append(row)

    Path("memory").mkdir(exist_ok=True)
    json.dump(valid_bios, open(OUT_BIOS, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(valid_profiles, open(OUT_PROFILES, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    reject_counts = defaultdict(int)
    for r in rejected_bios + rejected_profiles:
        reject_counts[r.get("validation_reason", "unknown")] += 1

    lines = [
        "# Artist Name Validation Report",
        "",
        "Rejects awards, institutions, locations, sentence fragments, and navigation text.",
        "",
        f"- Input biographies: {len(bios)}",
        f"- Valid biographies: {len(valid_bios)}",
        f"- Rejected biographies: {len(rejected_bios)}",
        f"- Input profiles: {len(profiles)}",
        f"- Valid profiles: {len(valid_profiles)}",
        f"- Rejected profiles: {len(rejected_profiles)}",
        "",
        "## Valid Biographies",
        "",
    ]

    for b in valid_bios[:50]:
        lines.append(f"- {b.get('artist_name')} — {b.get('source_opportunity')} — {b.get('validation_reason')}")

    lines.append("")
    lines.append("## Rejection Reasons")
    lines.append("")
    for reason, count in sorted(reject_counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"- {reason}: {count}")

    lines.append("")
    lines.append("## Sample Rejections")
    lines.append("")
    for r in rejected_bios[:40]:
        lines.append(f"- {r.get('artist_name')} — {r.get('validation_reason')}")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_BIOS)
    print("Wrote", OUT_PROFILES)
    print("Wrote", OUT_REPORT)
    print("Valid biographies:", len(valid_bios))
    print("Valid profiles:", len(valid_profiles))

if __name__ == "__main__":
    main()
