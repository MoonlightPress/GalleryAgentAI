
import json
import re
from pathlib import Path
from collections import Counter, defaultdict

SRC = "memory/historical_artist_data_v2.json"
OUT_JSON = "memory/artist_profiles.json"
OUT_REPORT = "reports/artist_profiles.md"

ROLE_KEYWORDS = {
    "illustrator": ["illustrator", "illustration", "イラストレーター", "イラスト"],
    "picture_book_artist": ["picture book", "絵本", "絵本作家"],
    "painter": ["painter", "painting", "画家", "絵画"],
    "watercolor_artist": ["watercolor", "watercolour", "水彩"],
    "zine_maker": ["zine", "ZINE", "ジン"],
    "publisher": ["publisher", "press", "出版", "出版社"],
    "gallery_artist": ["gallery", "exhibition", "exhibitor", "ギャラリー", "展示", "出展"],
    "award_winner": ["winner", "award", "selected", "受賞", "入賞", "selected artist"],
    "judge": ["judge", "juror", "審査員"],
}

MATERIAL_KEYWORDS = {
    "watercolor": ["watercolor", "watercolour", "水彩"],
    "works_on_paper": ["paper", "紙", "作品画像", "drawing", "ドローイング"],
    "books": ["book", "books", "絵本", "artist book", "publication", "出版"],
    "zines": ["zine", "ZINE", "ジン"],
    "illustration": ["illustration", "illustrator", "イラスト"],
    "painting": ["painting", "painter", "画家", "絵画"],
    "children_books": ["children", "絵本", "児童", "children's book"],
}

BAD_NAMES = {
    "Open Calls", "Mall Galleries", "Tokyo Art Book Fair", "Pinpoint Gallery",
    "Contact Jackson", "Past Competitions", "Selected Artist", "Mini Print International"
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def clean_name(name):
    name = " ".join(str(name or "").split()).strip()
    name = re.sub(r"\s+", " ", name)
    return name

def is_usable_name(name):
    if not name:
        return False
    if name in BAD_NAMES:
        return False
    if len(name) < 4 or len(name) > 60:
        return False
    upper = name.upper()
    if upper == name and not re.search(r"[一-龥ぁ-んァ-ン]", name):
        return False
    nav = ["HOME", "ABOUT", "CONTACT", "MENU", "PRIVACY", "APPLICATION", "OPEN CALL", "NEWS", "RSS", "COPYRIGHT"]
    if any(x in upper for x in nav):
        return False
    return True

def infer_roles(text, entity_type):
    roles = set()
    blob = text or ""

    for role, keywords in ROLE_KEYWORDS.items():
        if any(k.lower() in blob.lower() for k in keywords):
            roles.add(role)

    if entity_type == "judge":
        roles.add("judge")
    if entity_type == "publisher_or_bookstore":
        roles.add("publisher_or_bookstore")
    if entity_type in {"winner_or_selected_artist", "exhibitor"}:
        roles.add(entity_type)

    return sorted(roles) or ["artist_or_related"]

def infer_keywords(text):
    out = set()
    blob = text or ""
    for key, words in MATERIAL_KEYWORDS.items():
        if any(w.lower() in blob.lower() for w in words):
            out.add(key)
    return sorted(out)

def confidence_for(profile):
    score = 0.25

    if profile["evidence_count"] >= 2:
        score += 0.2
    if profile["roles"] and profile["roles"] != ["artist_or_related"]:
        score += 0.2
    if profile["keywords"]:
        score += 0.15
    if profile["source_opportunities"]:
        score += 0.1
    if any("winner" in r or "selected" in r or "exhibitor" in r for r in profile["roles"]):
        score += 0.1

    return round(min(0.95, score), 2)

def main():
    data = load(SRC, [])
    grouped = {}

    for opp in data:
        title = opp.get("title")
        for ent in opp.get("historical_entities", []):
            name = clean_name(ent.get("name"))
            if not is_usable_name(name):
                continue

            if name not in grouped:
                grouped[name] = {
                    "name": name,
                    "source_opportunities": [],
                    "source_urls": [],
                    "raw_evidence": [],
                    "entity_types": [],
                }

            g = grouped[name]
            if title and title not in g["source_opportunities"]:
                g["source_opportunities"].append(title)
            if ent.get("source_url") and ent["source_url"] not in g["source_urls"]:
                g["source_urls"].append(ent["source_url"])
            if ent.get("evidence"):
                g["raw_evidence"].append(ent["evidence"])
            if ent.get("entity_type"):
                g["entity_types"].append(ent["entity_type"])

    profiles = []
    for name, g in grouped.items():
        evidence_text = "\n".join(g["raw_evidence"])
        entity_type_text = " ".join(g["entity_types"])

        profile = {
            "name": name,
            "source_opportunities": g["source_opportunities"],
            "source_urls": g["source_urls"][:5],
            "roles": infer_roles(evidence_text + " " + entity_type_text, entity_type_text),
            "keywords": infer_keywords(evidence_text),
            "evidence_count": len(g["raw_evidence"]),
            "evidence": g["raw_evidence"][:5],
        }
        profile["confidence"] = confidence_for(profile)
        profiles.append(profile)

    profiles.sort(key=lambda x: (x["confidence"], x["evidence_count"], len(x["source_opportunities"])), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(profiles, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Artist Profiles",
        "",
        "Profiles inferred from historical opportunity/entity extraction.",
        "",
        f"Total usable profiles: {len(profiles)}",
        "",
    ]

    for p in profiles:
        lines.append(f"## {p['name']}")
        lines.append(f"- Confidence: {p['confidence']}")
        lines.append(f"- Roles: {', '.join(p['roles'])}")
        lines.append(f"- Keywords: {', '.join(p['keywords']) or 'none'}")
        lines.append(f"- Source opportunities: {', '.join(p['source_opportunities'])}")
        if p["source_urls"]:
            lines.append(f"- Source URL: {p['source_urls'][0]}")
        if p["evidence"]:
            lines.append("")
            lines.append("### Evidence")
            for e in p["evidence"][:3]:
                lines.append(f"- {e}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Profiles:", len(profiles))

if __name__ == "__main__":
    main()
