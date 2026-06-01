
import json
from pathlib import Path

ART_FAIRS = Path("memory/art_fair_candidates.json")
CANONICAL = Path("memory/canonical_opportunities.json")
VERIFIED = Path("memory/verified_opportunity_fields.json")
OUT_JSON = Path("memory/fair_ecosystem.json")
OUT_REPORT = Path("reports/fair_ecosystem.md")

KNOWN_NAMES = {
    "tokyo art book fair": "Tokyo Art Book Fair",
    "fukuoka art book fair": "Fukuoka Art Book Fair",
    "design festa": "Design Festa",
    "comitia": "COMITIA",
    "independent tokyo": "Independent Tokyo",
    "sicf": "SICF",
    "spiral independent creators festival": "SICF",
    "handmade in japan": "HandMade In Japan Fes",
    "creators market": "Creators Market",
    "tokyo international art fair": "Tokyo International Art Fair",
    "art fair asia fukuoka": "Art Fair Asia Fukuoka",
    "kyotographie": "Kyotographie Photobook Fair",
    "jimbocho zine fair": "Jimbocho Zine Fair",
    "zines fair at cp": "Zines Fair at CP+",
    "zineフェス": "ZINEフェス東京",
}

def load(path, fallback):
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback

def canonical_name(title, url=""):
    blob = f"{title} {url}".lower()
    for pat, name in KNOWN_NAMES.items():
        if pat in blob:
            return name
    return str(title or "").strip()[:120]

def fair_type(name, group):
    low = name.lower()
    if "zine" in low or "book" in low or "photobook" in low:
        return "zine / art-book fair"
    if "design festa" in low or "comitia" in low or "handmade" in low or "creators" in low or "sicf" in low:
        return "creator market / illustration fair"
    if "art fair" in low or "independent" in low:
        return "art fair"
    return group.replace("_", " ")

def beginner_friendliness(name):
    low = name.lower()
    if any(x in low for x in ["design festa", "comitia", "handmade", "creators", "zine"]):
        return "high"
    if any(x in low for x in ["independent tokyo", "tokyo art book fair", "sicf"]):
        return "medium"
    return "unknown"

def prestige(name):
    low = name.lower()
    if any(x in low for x in ["tokyo art book fair", "independent tokyo", "sicf", "art fair tokyo", "tokyo international art fair"]):
        return "high"
    if any(x in low for x in ["design festa", "comitia", "kyotographie", "fukuoka"]):
        return "medium"
    return "unknown"

def verified_lookup():
    data = load(VERIFIED, {"records": []})
    out = {}
    for r in data.get("records", []):
        out[r.get("canonical_name", "").lower()] = r
    return out

def main():
    art = load(ART_FAIRS, {"candidates": []}).get("candidates", [])
    canonical = load(CANONICAL, {"opportunities": []}).get("opportunities", [])
    verified = verified_lookup()

    rows = []

    for c in art:
        name = canonical_name(c.get("title"), c.get("url"))
        rows.append({
            "name": name,
            "url": c.get("url", ""),
            "source_title": c.get("title", ""),
            "score": c.get("score", 0),
            "group": c.get("fair_group", "fair"),
            "source": "art_fair_expansion",
        })

    for o in canonical:
        if o.get("career_category") == "zines":
            name = canonical_name(o.get("canonical_name"), o.get("best_url"))
            rows.append({
                "name": name,
                "url": o.get("best_url", ""),
                "source_title": o.get("canonical_name", ""),
                "score": o.get("score", 0),
                "group": "zine_art_book",
                "source": "canonical_zines",
            })

    grouped = {}
    for r in rows:
        grouped.setdefault(r["name"], []).append(r)

    targets = []
    for name, items in grouped.items():
        items = sorted(items, key=lambda x: x["score"], reverse=True)
        best = items[0]
        ver = verified.get(name.lower(), {})
        urls = []
        seen = set()
        for i in items:
            if i["url"] and i["url"] not in seen:
                urls.append(i["url"])
                seen.add(i["url"])

        target = {
            "name": name,
            "score": min(100, max(i["score"] for i in items) + min(10, len(items))),
            "fair_type": fair_type(name, best["group"]),
            "beginner_friendliness": beginner_friendliness(name),
            "prestige": prestige(name),
            "application_url": ver.get("url") or best["url"],
            "deadline": ver.get("deadline_extracted", ""),
            "fee": ver.get("fee_extracted", ""),
            "application_route": ver.get("application_route", "check_source"),
            "source_count": len(items),
            "sources": urls[:8],
            "status": "research_next",
        }
        targets.append(target)

    targets.sort(key=lambda x: x["score"], reverse=True)

    data = {
        "category": "fairs_events",
        "target_count": len(targets),
        "targets": targets,
    }

    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Fair / Event Ecosystem", "", f"- Targets: {len(targets)}", ""]
    for t in targets[:80]:
        lines.append(f"### {t['name']}")
        lines.append(f"- Score: {t['score']}")
        lines.append(f"- Type: {t['fair_type']}")
        lines.append(f"- Beginner friendliness: {t['beginner_friendliness']}")
        lines.append(f"- Prestige: {t['prestige']}")
        lines.append(f"- Deadline: {t['deadline'] or 'Check source'}")
        lines.append(f"- Fee: {t['fee'] or 'Check source'}")
        lines.append(f"- Application: {t['application_url']}")
        lines.append(f"- Sources: {t['source_count']}")
        lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
