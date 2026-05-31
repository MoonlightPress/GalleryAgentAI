
import json
import re
from pathlib import Path
from collections import Counter, defaultdict

SRC = "memory/tabf_exhibitor_data.json"
OUT_JSON = "memory/tabf_clean_entities.json"
OUT_REPORT = "reports/tabf_clean_entities.md"

BAD_EXACT = {
    "Press", "Italy", "Italian", "Zine", "Studio", "Yukiko", "Franz", "Walther",
    "und", "der", "nig", "Buchhandlung", "Revolutionary", "Museum", "New",
    "BOOK", "EN", "JP", "HOME", "ABOUT", "ARCHIVES", "CONTACT", "ACCESS",
    "THE", "TOKYO", "ART", "BOOK", "FAIR", "Guest Country", "Country",
}

BAD_CONTAINS = [
    "年に一度", "開催", "来場者", "直接交流", "多様な表現", "価格帯",
    "出版社が一同", "アジアで最大", "イベントです", "紹介する企画",
    "魅力を", "開催いたします", "に向けて", "として", "による展示",
    "となっています", "を予定しています", "いたします", "おり",
    "出版文化を紹介", "ブックフェアです", "集結", "出展者は",
]

KNOWN_GOOD = {
    "Steidl": "publisher_or_press",
    "MISS READ": "art_book_fair",
    "Studio Yukiko": "publisher_or_press",
    "Verlag der Buchhandlung Walther und Franz König": "publisher_or_press",
    "Pace Gallery": "gallery",
    "Corraini": "publisher_or_press",
    "MACK": "publisher_or_press",
    "Book Works": "publisher_or_press",
}

MERGE_PATTERNS = [
    ("Verlag der Buchhandlung Walther und Franz König", ["Verlag", "Buchhandlung Walther", "Walther", "Franz", "König", "nig"]),
    ("Studio Yukiko", ["Studio", "Yukiko"]),
    ("YES YES YES Revolutionary Press", ["YES YES YES Revolutionary Press", "Revolutionary Press"]),
    ("OUT OF THE GRID: Italian Zine 1978–2006", ["OUT OF THE GRID", "Italian Zine"]),
    ("Pace Gallery", ["Pace"]),
]

TYPE_PRIORITY = {
    "publisher_or_press": 5,
    "artist_or_collective": 4,
    "bookstore_gallery": 3,
    "zine_or_book": 2,
    "unknown": 0,
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def normalize_name(name):
    name = " ".join(str(name or "").replace("\u3000", " ").split()).strip(" ・,。:：-")
    name = name.replace("’", "'")
    return name

def too_sentence_like(name):
    if len(name) > 55:
        return True
    if len(name.split()) > 6:
        return True
    if re.search(r"[。！？]", name):
        return True
    if any(x in name for x in ["する", "です", "ます", "ました", "いただ", "ください"]):
        return True
    return False

def is_bad(name):
    n = normalize_name(name)
    if not n:
        return True
    if n in KNOWN_GOOD:
        return False
    if n in BAD_EXACT:
        return True
    if len(n) < 3:
        return True
    if too_sentence_like(n):
        return True
    if any(b in n for b in BAD_CONTAINS):
        return True
    if re.fullmatch(r"[A-Za-z]{1,4}", n) and n not in {"MACK"}:
        return True
    if re.fullmatch(r"[0-9０-９]+", n):
        return True
    return False

def merged_name(name, context=""):
    blob = f"{name} {context}"
    for merged, parts in MERGE_PATTERNS:
        if any(p in blob for p in parts):
            # Only merge if the context supports the full phrase or several fragments.
            hits = sum(1 for p in parts if p in blob)
            if hits >= 2 or merged in blob:
                return merged
    return normalize_name(name)

def best_type(types):
    if not types:
        return "unknown"
    return sorted(types, key=lambda t: TYPE_PRIORITY.get(t, 0), reverse=True)[0]

def main():
    raw = load(SRC, {})
    raw_entities = raw.get("entities", [])

    grouped = {}

    rejected = []

    for ent in raw_entities:
        original = normalize_name(ent.get("name"))
        context = ent.get("context", "")
        name = merged_name(original, context)

        if is_bad(name):
            rejected.append({
                "name": original,
                "reason": "bad_or_sentence_fragment",
                "context": context[:180],
            })
            continue

        typ = KNOWN_GOOD.get(name) or best_type(ent.get("types", []))

        if name not in grouped:
            grouped[name] = {
                "name": name,
                "entity_type": typ,
                "types_seen": set(),
                "mentions": 0,
                "contexts": [],
                "source_urls": set(),
                "source_labels": set(),
            }

        g = grouped[name]
        g["mentions"] += 1
        g["types_seen"].update(ent.get("types", []))
        if context and context not in g["contexts"]:
            g["contexts"].append(context[:260])
        if ent.get("source_url"):
            g["source_urls"].add(ent["source_url"])
        if ent.get("source_label"):
            g["source_labels"].add(ent["source_label"])

    cleaned = []
    for g in grouped.values():
        row = dict(g)
        row["types_seen"] = sorted(row["types_seen"])
        row["contexts"] = row["contexts"][:5]
        row["source_urls"] = sorted(row["source_urls"])[:5]
        row["source_labels"] = sorted(row["source_labels"])[:5]
        cleaned.append(row)

    cleaned.sort(key=lambda x: (TYPE_PRIORITY.get(x["entity_type"], 0), x["mentions"], len(x["contexts"])), reverse=True)

    result = {
        "title": "TOKYO ART BOOK FAIR",
        "raw_entity_count": len(raw_entities),
        "clean_entity_count": len(cleaned),
        "rejected_count": len(rejected),
        "clean_entities": cleaned,
        "rejected_samples": rejected[:120],
        "publishers_or_presses": [e for e in cleaned if e["entity_type"] == "publisher_or_press"],
        "artists_or_collectives": [e for e in cleaned if e["entity_type"] == "artist_or_collective"],
        "bookstores_or_galleries": [e for e in cleaned if e["entity_type"] in {"bookstore_gallery", "gallery"}],
        "zines_or_books": [e for e in cleaned if e["entity_type"] == "zine_or_book"],
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# TABF Clean Entities",
        "",
        "Cleans raw TABF ecosystem extraction by removing sentence fragments, generic words, and broken name pieces.",
        "",
        f"- Raw entities: {result['raw_entity_count']}",
        f"- Clean entities: {result['clean_entity_count']}",
        f"- Rejected: {result['rejected_count']}",
        f"- Publishers / presses: {len(result['publishers_or_presses'])}",
        f"- Artists / collectives: {len(result['artists_or_collectives'])}",
        f"- Bookstores / galleries: {len(result['bookstores_or_galleries'])}",
        f"- Zines / books: {len(result['zines_or_books'])}",
        "",
    ]

    for title, key in [
        ("Publishers / Presses", "publishers_or_presses"),
        ("Artists / Collectives", "artists_or_collectives"),
        ("Bookstores / Galleries", "bookstores_or_galleries"),
        ("Zines / Books", "zines_or_books"),
    ]:
        lines.append(f"## {title}")
        if not result[key]:
            lines.append("_None after cleanup._")
        for e in result[key][:40]:
            lines.append(f"- {e['name']} — mentions {e['mentions']} — {', '.join(e['types_seen'])}")
            if e["contexts"]:
                lines.append(f"  - {e['contexts'][0]}")
        lines.append("")

    lines.append("## Rejected Samples")
    for r in rejected[:60]:
        lines.append(f"- {r['name']}")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Clean entities:", len(cleaned))

if __name__ == "__main__":
    main()
