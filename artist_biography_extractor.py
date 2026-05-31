
import json
import re
from pathlib import Path

SRC = "memory/historical_artist_data_v2.json"
OUT_JSON = "memory/artist_biographies.json"
OUT_REPORT = "reports/artist_biographies.md"

BIO_MARKERS = [
    "生まれ", "卒業", "受賞", "入選", "著書", "作品", "個展", "展示", "制作",
    "born", "graduated", "award", "awarded", "winner", "selected", "exhibition",
    "published", "books", "illustration", "artist", "painter", "illustrator"
]

JP_ROLES = ["絵本作家", "イラストレーター", "画家", "作家", "アーティスト"]
EN_ROLES = ["artist", "illustrator", "painter", "picture book artist", "author"]

HARD_BAD_TERMS = [
    "Award", "Prize", "Exhibition", "Gallery", "Society", "Competition", "Book Fair",
    "Institute", "Association", "Open Calls", "Annual Exhibition", "Foundation",
    "Federation", "Application", "Contact", "Privacy", "Policy", "Menu", "Schedule",
    "Newsletter", "Copyright", "Event Hire", "Venue Hire", "Art Gallery", "Visual Arts"
]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def clean_name(name):
    return " ".join(str(name or "").split()).strip(" 。、:：-")

def looks_like_human_name(name, evidence=""):
    name = clean_name(name)
    if not name or len(name) < 2 or len(name) > 40:
        return False

    # Reject institutional or award names.
    if any(term.lower() in name.lower() for term in HARD_BAD_TERMS):
        return False

    # Reject English all-caps/nav fragments.
    if name.isupper():
        return False

    # Japanese names: 2-6 kanji/kana characters often enough if bio context is strong.
    if re.fullmatch(r"[一-龥ぁ-んァ-ンー・]{2,12}", name):
        return any(marker in evidence for marker in BIO_MARKERS + JP_ROLES)

    # Western-style names: usually 2 capitalized words.
    if re.fullmatch(r"[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’.-]+(?:\s+[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’.-]+){1,3}", name):
        return True

    return False

def extract_jp_name_from_bio(text):
    if not text:
        return None

    # Common Japanese bio opening: 千葉智江 1984年岩手県生まれ。
    m = re.match(r"^([一-龥ぁ-んァ-ンー・]{2,12})\s*[0-9０-９]{4}年", text)
    if m:
        return m.group(1)

    # Common: 飯野和好（いいの・かずよし）絵本作家。
    m = re.match(r"^([一-龥ぁ-んァ-ンー・]{2,12})[（(]", text)
    if m:
        return m.group(1)

    # Common: つじにぬき 京都生まれ
    m = re.match(r"^([一-龥ぁ-んァ-ンー・]{2,12})\s*(?:京都|東京|大阪|岩手|埼玉|神奈川|千葉|北海道|沖縄|福岡|兵庫|愛知|長野|新潟|静岡|広島|宮城|奈良|滋賀|岐阜|三重|山形|秋田|青森|福島|茨城|栃木|群馬|山梨|富山|石川|福井|和歌山|鳥取|島根|岡山|山口|徳島|香川|愛媛|高知|佐賀|長崎|熊本|大分|宮崎|鹿児島)", text)
    if m:
        return m.group(1)

    return None

def extract_birth_year(text):
    m = re.search(r"(19[0-9]{2}|20[0-9]{2})年[^。]{0,20}生まれ", text or "")
    if m:
        return m.group(1)
    m = re.search(r"born[^0-9]{0,20}(19[0-9]{2}|20[0-9]{2})", text or "", flags=re.I)
    if m:
        return m.group(1)
    return "unknown"

def split_clauses(text):
    parts = re.split(r"[。．.!?\n]", text or "")
    return [" ".join(p.split()) for p in parts if len(p.strip()) > 8]

def extract_awards(text):
    out = []
    for part in split_clauses(text):
        if any(k in part for k in ["受賞", "入選", "award", "winner", "selected", "prize"]):
            out.append(part[:220])
    return out[:8]

def extract_publishers_books(text):
    publishers = []
    books = []

    # Japanese book titles often appear as 『...』
    books.extend(re.findall(r"『([^』]{1,60})』", text or ""))

    # Publisher-ish terms.
    for part in split_clauses(text):
        if any(k in part for k in ["出版社", "PHP研究所", "小学館", "福音館", "理論社", "偕成社", "ブロンズ新社", "小峰書店", "publisher", "published"]):
            publishers.append(part[:220])

    return list(dict.fromkeys(publishers))[:8], list(dict.fromkeys(books))[:12]

def infer_roles(text):
    roles = []
    low = (text or "").lower()
    for role in JP_ROLES:
        if role in text:
            roles.append(role)
    for role in EN_ROLES:
        if role in low:
            roles.append(role)
    return list(dict.fromkeys(roles)) or ["artist"]

def is_bio_text(text):
    if not text:
        return False
    if len(text) < 40:
        return False
    return any(marker.lower() in text.lower() for marker in BIO_MARKERS)

def main():
    data = load(SRC, [])

    biographies = []
    seen = set()

    for opp in data:
        title = opp.get("title")
        for ent in opp.get("historical_entities", []):
            evidence = ent.get("evidence", "") or ""
            name = clean_name(ent.get("name"))

            # Prefer extracting the name from the actual bio evidence.
            jp_name = extract_jp_name_from_bio(evidence)
            if jp_name:
                name = jp_name

            if not is_bio_text(evidence):
                continue
            if not looks_like_human_name(name, evidence):
                continue

            key = (name, title, evidence[:80])
            if key in seen:
                continue
            seen.add(key)

            publishers, books = extract_publishers_books(evidence)

            biographies.append({
                "artist_name": name,
                "source_opportunity": title,
                "roles": infer_roles(evidence),
                "birth_year": extract_birth_year(evidence),
                "awards": extract_awards(evidence),
                "publishers_or_publication_clues": publishers,
                "books_or_work_titles": books,
                "source_url": ent.get("source_url"),
                "source_label": ent.get("source_label"),
                "bio_text": evidence,
                "confidence": 0.85 if jp_name else 0.65,
            })

    biographies.sort(key=lambda x: (x["confidence"], len(x["awards"]), len(x["books_or_work_titles"])), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(biographies, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Artist Biographies",
        "",
        "Extracted from biography-like evidence blocks. This report should contain real people, not awards or navigation fragments.",
        "",
        f"Total biographies: {len(biographies)}",
        "",
    ]

    for b in biographies:
        lines.append(f"## {b['artist_name']}")
        lines.append(f"- Source opportunity: {b['source_opportunity']}")
        lines.append(f"- Roles: {', '.join(b['roles'])}")
        lines.append(f"- Birth year: {b['birth_year']}")
        lines.append(f"- Confidence: {b['confidence']}")
        if b.get("source_url"):
            lines.append(f"- Source: {b['source_url']}")
        lines.append("")
        lines.append("### Bio")
        lines.append(b["bio_text"])
        if b["awards"]:
            lines.append("")
            lines.append("### Awards / selections")
            for a in b["awards"][:5]:
                lines.append(f"- {a}")
        if b["books_or_work_titles"]:
            lines.append("")
            lines.append("### Books / works")
            for book in b["books_or_work_titles"][:8]:
                lines.append(f"- {book}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Biographies:", len(biographies))

if __name__ == "__main__":
    main()
