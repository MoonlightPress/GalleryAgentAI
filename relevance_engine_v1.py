
import json
import re
from pathlib import Path

TABF = "memory/tabf_validated_entities.json"
PINPOINT = "memory/nin_opportunity_recommendations.json"
ECOSYSTEMS = "memory/opportunity_ecosystems.json"
DENSITY = "memory/ecosystem_density_scores.json"

OUT_JSON = "memory/relevance_scores.json"
OUT_REPORT = "reports/relevance_scores.md"

ENTITY_TYPE_WEIGHTS = {
    "publisher_or_press": 35,
    "gallery": 25,
    "art_book_fair": 30,
    "zine_or_book": 22,
    "artist_or_collective": 20,
    "award_or_program": 12,
    "unknown": 0,
}

GOOD_TERMS = {
    "zine": 12,
    "ZINE": 12,
    "artist book": 14,
    "art book": 14,
    "アートブック": 14,
    "アーティストブック": 14,
    "publisher": 12,
    "press": 12,
    "出版": 12,
    "出版社": 12,
    "gallery": 8,
    "ギャラリー": 8,
    "bookstore": 8,
    "書店": 8,
    "independent": 10,
    "インディペンデント": 10,
    "risograph": 10,
    "リソグラフ": 10,
    "print": 8,
    "prints": 8,
}

BAD_TERMS = [
    "ticket", "subscribe", "newsletter", "privacy", "policy", "contact",
    "book signing", "buy ticket", "schedule", "menu", "guest", "country",
    "感染", "中止", "開催", "いたします", "ください", "ました", "です",
    "予定", "紹介", "企画", "展示のほか", "国内外から", "同国",
]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def blob(entity):
    return " ".join([
        entity.get("name", ""),
        entity.get("validated_type", ""),
        " ".join(entity.get("contexts", [])),
        " ".join(entity.get("types_seen", [])),
    ])

def bad_penalty(entity):
    text = blob(entity).lower()
    name = entity.get("name", "").lower()
    penalty = 0

    for term in BAD_TERMS:
        if term.lower() in name:
            penalty += 35
        elif term.lower() in text:
            penalty += 10

    # Generic titles / site mechanics.
    if entity.get("name", "").isupper() and len(entity.get("name", "")) > 18:
        penalty += 25

    if len(entity.get("name", "").split()) >= 7:
        penalty += 30

    # Japanese sentence fragments.
    if re.search(r"(です|ます|ました|しています|いたします|ください)", entity.get("name", "")):
        penalty += 50

    return penalty

def good_score(entity):
    text = blob(entity)
    score = 0

    score += ENTITY_TYPE_WEIGHTS.get(entity.get("validated_type", "unknown"), 0)
    score += min(20, entity.get("mentions", 0) * 4)
    score += min(15, len(entity.get("source_urls", [])) * 5)
    score += min(10, entity.get("validation_score", 0) * 0.1)

    hits = []
    for term, value in GOOD_TERMS.items():
        if term.lower() in text.lower():
            score += value
            hits.append(term)

    if entity.get("name") in {
        "Steidl",
        "MISS READ",
        "YES YES YES Revolutionary Press",
        "Verlag der Buchhandlung Walther und Franz König",
        "Studio Yukiko",
        "Hand Saw Press",
        "Pace Gallery",
        "Feira Plana",
        "Shiseido Gallery",
        "The Thing Quarterly",
    }:
        score += 25
        hits.append("known strong ecosystem entity")

    return score, sorted(set(hits))

def entity_relevance(entity):
    raw, hits = good_score(entity)
    penalty = bad_penalty(entity)
    score = max(0, min(100, round(raw - penalty, 1)))

    if score >= 75:
        label = "high"
    elif score >= 45:
        label = "medium"
    elif score >= 20:
        label = "low"
    else:
        label = "reject_or_ignore"

    return {
        "name": entity.get("name"),
        "entity_type": entity.get("validated_type"),
        "relevance_score": score,
        "relevance_label": label,
        "positive_terms": hits,
        "penalty": penalty,
        "mentions": entity.get("mentions", 0),
        "source_urls": entity.get("source_urls", []),
        "contexts": entity.get("contexts", [])[:3],
    }

def build_tabf_scores():
    tabf = load(TABF, {})
    rows = []
    for e in tabf.get("validated_entities", []):
        rows.append(entity_relevance(e))
    rows.sort(key=lambda x: x["relevance_score"], reverse=True)
    return rows

def main():
    tabf_rows = build_tabf_scores()

    result = {
        "TOKYO ART BOOK FAIR": {
            "entities": tabf_rows,
            "high_relevance_count": len([r for r in tabf_rows if r["relevance_score"] >= 75]),
            "medium_relevance_count": len([r for r in tabf_rows if 45 <= r["relevance_score"] < 75]),
            "ignored_count": len([r for r in tabf_rows if r["relevance_score"] < 20]),
        }
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Relevance Scores",
        "",
        "Scores entities by actual career relevance, not keyword density.",
        "",
        "## TOKYO ART BOOK FAIR",
        "",
        f"- High relevance: {result['TOKYO ART BOOK FAIR']['high_relevance_count']}",
        f"- Medium relevance: {result['TOKYO ART BOOK FAIR']['medium_relevance_count']}",
        f"- Ignored / rejected: {result['TOKYO ART BOOK FAIR']['ignored_count']}",
        "",
        "## Top relevant entities",
        "",
    ]

    for r in tabf_rows[:40]:
        if r["relevance_score"] < 20:
            continue
        lines.append(f"### {r['name']}")
        lines.append(f"- Relevance: {r['relevance_score']}/100 ({r['relevance_label']})")
        lines.append(f"- Type: {r['entity_type']}")
        lines.append(f"- Positive terms: {', '.join(r['positive_terms']) or 'none'}")
        lines.append(f"- Penalty: {r['penalty']}")
        if r.get("source_urls"):
            lines.append(f"- Source: {r['source_urls'][0]}")
        if r.get("contexts"):
            lines.append("")
            lines.append("Evidence:")
            lines.append(f"- {r['contexts'][0]}")
        lines.append("")

    lines.append("## Ignored examples")
    lines.append("")
    for r in [x for x in tabf_rows if x["relevance_score"] < 20][:40]:
        lines.append(f"- {r['name']} — score {r['relevance_score']} — penalty {r['penalty']}")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
