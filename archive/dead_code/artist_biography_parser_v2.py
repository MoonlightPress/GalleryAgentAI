
import json
import re
from pathlib import Path

SRC = "memory/validated_artist_biographies.json"
OUT_JSON = "memory/parsed_artist_biographies.json"
OUT_REPORT = "reports/parsed_artist_biographies.md"

PUBLISHER_TERMS = [
    "小学館", "福音館書店", "偕成社", "理論社", "ブロンズ新社", "小峰書店",
    "PHP研究所", "大日本図書", "学研", "NHK", "ひかりのくに", "地湧社",
    "クレヨンハウス", "publisher", "published by", "press"
]

ROLE_TERMS = {
    "picture_book_artist": ["絵本作家", "picture book artist"],
    "illustrator": ["イラストレーター", "イラスト", "illustrator", "illustration"],
    "painter": ["画家", "painter", "painting"],
    "artist": ["作家", "アーティスト", "artist"],
    "author": ["著書", "author"],
}

AWARD_TERMS = ["受賞", "入選", "優秀賞", "賞", "award", "prize", "winner", "selected"]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def split_sentences(text):
    parts = re.split(r"[。．.!?\n]", text or "")
    return [" ".join(p.split()) for p in parts if p.strip()]

def extract_books(text):
    # Japanese book titles in 『...』
    titles = re.findall(r"『([^』]{1,80})』", text or "")
    # quoted Japanese series sometimes in 「...」
    titles += re.findall(r"「([^」]{1,80})」", text or "")
    out = []
    for t in titles:
        t = t.strip()
        if t and t not in out:
            out.append(t)
    return out[:20]

def extract_publishers(text):
    found = []
    for term in PUBLISHER_TERMS:
        if term in (text or "") and term not in found:
            found.append(term)

    # Find publisher-like parenthetical chunks: （小学館） / (publisher)
    for m in re.findall(r"[（(]([^）)]{2,40})[）)]", text or ""):
        if any(k in m for k in ["社", "書店", "図書", "研究所", "館", "press", "publisher"]):
            if m not in found:
                found.append(m)

    return found[:20]

def extract_awards(text):
    out = []
    for s in split_sentences(text):
        if any(term.lower() in s.lower() for term in AWARD_TERMS):
            # Break long biography sentence into smaller award-ish clauses where possible.
            clauses = re.split(r"[、,]", s)
            for c in clauses:
                if any(term.lower() in c.lower() for term in AWARD_TERMS):
                    c = c.strip()
                    if 5 <= len(c) <= 180 and c not in out:
                        out.append(c)
    return out[:20]

def extract_education(text):
    out = []
    for s in split_sentences(text):
        if any(k in s for k in ["卒業", "大学", "学校", "セミナー", "workshop", "ワークショップ", "graduated", "University", "School"]):
            if s not in out:
                out.append(s[:220])
    return out[:10]

def extract_roles(text, existing_roles):
    roles = set(existing_roles or [])
    low = (text or "").lower()
    for role, terms in ROLE_TERMS.items():
        if any(t.lower() in low for t in terms):
            roles.add(role)
    return sorted(roles) or ["artist"]

def extract_birth_place(text):
    # Common JP pattern: 1984年岩手県生まれ
    m = re.search(r"(?:19|20)[0-9]{2}年([^。、\s]{2,12})生まれ", text or "")
    if m:
        return m.group(1)

    # Common: 京都生まれ
    m = re.search(r"([^。、\s]{2,12})生まれ", text or "")
    if m:
        return m.group(1)

    return "unknown"

def extract_key_career_clues(text):
    clues = []
    for s in split_sentences(text):
        if any(k in s for k in ["制作", "依頼", "出版", "新聞", "雑誌", "展示", "個展", "受賞", "入選", "著書", "work", "published", "exhibition"]):
            if s not in clues:
                clues.append(s[:240])
    return clues[:12]

def main():
    bios = load(SRC, [])
    parsed = []

    for b in bios:
        text = b.get("bio_text", "")
        record = {
            "artist_name": b.get("artist_name"),
            "source_opportunity": b.get("source_opportunity"),
            "source_url": b.get("source_url"),
            "roles": extract_roles(text, b.get("roles", [])),
            "birth_year": b.get("birth_year", "unknown"),
            "birth_place": extract_birth_place(text),
            "education": extract_education(text),
            "books_or_works": extract_books(text),
            "publishers_or_clients": extract_publishers(text),
            "awards_or_selections": extract_awards(text),
            "career_clues": extract_key_career_clues(text),
            "bio_text": text,
            "confidence": b.get("confidence", 0),
        }
        parsed.append(record)

    parsed.sort(key=lambda x: (len(x["books_or_works"]), len(x["awards_or_selections"]), x["confidence"]), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(parsed, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Parsed Artist Biographies",
        "",
        "Structured career evidence extracted from validated artist biographies.",
        "",
        f"Parsed biographies: {len(parsed)}",
        "",
    ]

    for p in parsed:
        lines.append(f"## {p['artist_name']}")
        lines.append(f"- Source opportunity: {p['source_opportunity']}")
        lines.append(f"- Roles: {', '.join(p['roles'])}")
        lines.append(f"- Birth: {p['birth_year']} / {p['birth_place']}")
        lines.append(f"- Source: {p.get('source_url')}")
        if p["education"]:
            lines.append("")
            lines.append("### Education / training")
            for e in p["education"][:5]:
                lines.append(f"- {e}")
        if p["books_or_works"]:
            lines.append("")
            lines.append("### Books / works")
            for x in p["books_or_works"][:10]:
                lines.append(f"- {x}")
        if p["publishers_or_clients"]:
            lines.append("")
            lines.append("### Publishers / clients")
            for x in p["publishers_or_clients"][:10]:
                lines.append(f"- {x}")
        if p["awards_or_selections"]:
            lines.append("")
            lines.append("### Awards / selections")
            for x in p["awards_or_selections"][:10]:
                lines.append(f"- {x}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Parsed:", len(parsed))

if __name__ == "__main__":
    main()
