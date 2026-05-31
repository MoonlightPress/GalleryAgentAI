
import json
import re
from pathlib import Path
from urllib.parse import urlparse

SRC = "memory/tabf_clean_entities.json"
OUT_JSON = "memory/tabf_validated_entities.json"
OUT_REPORT = "reports/tabf_validated_entities.md"

REJECT_EXACT = {
    "Guest", "Country", "BOOK", "ART", "TOKYO", "FAIR", "Ginza Edition",
    "VIRTUAL ART BOOK FAIR", "SUBSCRIBE TO TOKYO ART BOOK", "BUY TICKET TOKYO ART BOOK",
    "BOOK SIGNING SPECIAL BOOTHS OUTDOOR", "LIVE BOOK SIGNING ART BOOK",
    "BOOK SIGNING PARTNERS NEIGHBOURS FLOORMAP", "BOOK FAIR THE TOKYO ART",
    "ART BOOK FAIR THE TOKYO", "tokyoartbookfair", "Threads, Say",
}

REJECT_CONTAINS = [
    "開催", "紹介", "企画", "展示", "予定", "魅力", "来場者", "国内外",
    "同国", "作家による", "出版社", "アーティストら", "集結", "開催いたします",
    "に向けて", "ました", "ます", "です", "します", "しています",
    "ブックフェア", "アート出版", "出版文化", "豊かな", "多角的",
    "コーナー", "コンテンツ", "予定です", "感染拡大", "観点から",
]

PROMOTE_CONTAINS = [
    "Press", "Gallery", "Books", "Book", "Studio", "Verlag", "Steidl",
    "MACK", "Corraini", "Feira", "Plana", "MISS READ", "Shiseido",
    "Hand Saw", "Pace", "Yukiko", "König", "Book Works"
]

KNOWN_VALID = {
    "YES YES YES Revolutionary Press": "publisher_or_press",
    "Verlag der Buchhandlung Walther und Franz König": "publisher_or_press",
    "Studio Yukiko": "publisher_or_press",
    "Hand Saw Press": "publisher_or_press",
    "Steidl": "publisher_or_press",
    "Pace Gallery": "gallery",
    "Feira Plana": "art_book_fair",
    "Shiseido Gallery": "gallery",
    "MISS READ": "art_book_fair",
    "Book Works": "publisher_or_press",
    "The Thing Quarterly": "publisher_or_press",
    "American Zines": "zine_or_book",
    "Japanese Artists' Books": "zine_or_book",
    "Steidl Book Award Japan": "award_or_program",
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def clean_name(name):
    return " ".join(str(name or "").replace("\u3000", " ").split()).strip(" ・,。:：-")

def has_sentence_ending(name):
    return any(x in name for x in ["です", "ます", "ました", "いたします", "しています", "でしょう"])

def starts_bad_japanese(name):
    return bool(re.match(r"^(で|に|を|が|は|と|の|へ|も|や|から|まで|そして|また|今年|今回|同国|国内外|昨今)", name))

def too_fragmenty(name):
    if len(name) > 70:
        return True
    if len(name.split()) >= 7:
        return True
    if len(name) > 30 and re.search(r"[ぁ-ん]", name) and not any(k in name for k in ["Press", "Gallery", "Studio", "Books", "Zine"]):
        return True
    return False

def proper_noun_score(entity):
    name = entity.get("name", "")
    contexts = " ".join(entity.get("contexts", []))
    mentions = entity.get("mentions", 0)
    score = 0

    if name in KNOWN_VALID:
        score += 60
    if any(p in name for p in PROMOTE_CONTAINS):
        score += 25
    if mentions >= 2:
        score += 15
    if mentions >= 5:
        score += 20
    if len(entity.get("source_urls", [])) >= 2:
        score += 15
    if "「" in contexts or "『" in contexts or "'" in contexts or '"' in contexts:
        score += 5
    if re.fullmatch(r"[A-Z][A-Za-z&'’.\-]+(?:\s+[A-Z][A-Za-z&'’.\-]+){0,5}", name):
        score += 15
    if re.search(r"[一-龥ァ-ンぁ-ん]", name) and len(name) <= 24 and not has_sentence_ending(name):
        score += 10

    return min(100, score)

def classify(entity):
    name = entity.get("name", "")
    if name in KNOWN_VALID:
        return KNOWN_VALID[name]
    current = entity.get("entity_type", "unknown")
    if "Gallery" in name or "ギャラリー" in name:
        return "gallery"
    if any(x in name for x in ["Press", "Verlag", "Steidl", "MACK", "Corraini", "Books", "Book Works"]):
        return "publisher_or_press"
    if any(x in name for x in ["Feira", "MISS READ", "Book Fair"]):
        return "art_book_fair"
    return current

def validate(entity):
    name = clean_name(entity.get("name"))

    if not name:
        return False, "empty", 0
    if name in KNOWN_VALID:
        return True, "known_valid", proper_noun_score(entity)
    if name in REJECT_EXACT:
        return False, "reject_exact", 0
    if any(x in name for x in REJECT_CONTAINS):
        return False, "sentence_or_description_fragment", 0
    if starts_bad_japanese(name):
        return False, "starts_like_japanese_fragment", 0
    if has_sentence_ending(name):
        return False, "verb_sentence", 0
    if too_fragmenty(name):
        return False, "too_fragmenty", 0

    score = proper_noun_score(entity)

    if score >= 30:
        return True, "proper_noun_score", score

    if entity.get("mentions", 0) >= 2 and len(name) >= 5:
        return True, "repeat_mention", score

    return False, "low_confidence", score

def main():
    data = load(SRC, {})
    entities = data.get("clean_entities", [])

    valid = []
    rejected = []

    for e in entities:
        e = dict(e)
        e["name"] = clean_name(e.get("name"))
        ok, reason, score = validate(e)
        e["validation_reason"] = reason
        e["validation_score"] = score
        e["validated_type"] = classify(e)

        if ok:
            valid.append(e)
        else:
            rejected.append(e)

    valid.sort(key=lambda x: (x["validation_score"], x.get("mentions", 0)), reverse=True)

    result = {
        "title": "TOKYO ART BOOK FAIR",
        "input_clean_entities": len(entities),
        "validated_count": len(valid),
        "rejected_count": len(rejected),
        "validated_entities": valid,
        "rejected_entities": rejected[:150],
        "publishers_or_presses": [e for e in valid if e["validated_type"] == "publisher_or_press"],
        "galleries": [e for e in valid if e["validated_type"] == "gallery"],
        "art_book_fairs": [e for e in valid if e["validated_type"] == "art_book_fair"],
        "zines_or_books": [e for e in valid if e["validated_type"] == "zine_or_book"],
        "artists_or_collectives": [e for e in valid if e["validated_type"] == "artist_or_collective"],
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# TABF Validated Entities",
        "",
        "Validates cleaned TABF entities into a tighter shortlist of real organizations, publishers, galleries, fairs, books, and artist-book signals.",
        "",
        f"- Input clean entities: {result['input_clean_entities']}",
        f"- Validated entities: {result['validated_count']}",
        f"- Rejected entities: {result['rejected_count']}",
        f"- Publishers / presses: {len(result['publishers_or_presses'])}",
        f"- Galleries: {len(result['galleries'])}",
        f"- Art book fairs: {len(result['art_book_fairs'])}",
        f"- Zines / books: {len(result['zines_or_books'])}",
        f"- Artists / collectives: {len(result['artists_or_collectives'])}",
        "",
    ]

    for title, key in [
        ("Publishers / Presses", "publishers_or_presses"),
        ("Galleries", "galleries"),
        ("Art Book Fairs", "art_book_fairs"),
        ("Zines / Books", "zines_or_books"),
        ("Artists / Collectives", "artists_or_collectives"),
    ]:
        lines.append(f"## {title}")
        if not result[key]:
            lines.append("_None validated._")
        for e in result[key][:40]:
            lines.append(f"- {e['name']} — score {e['validation_score']} — mentions {e.get('mentions')} — {e['validation_reason']}")
            if e.get("contexts"):
                lines.append(f"  - {e['contexts'][0]}")
        lines.append("")

    lines.append("## Rejected Samples")
    for e in rejected[:60]:
        lines.append(f"- {e['name']} — {e['validation_reason']}")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Validated:", len(valid))

if __name__ == "__main__":
    main()
