
import json
import re
from pathlib import Path
from urllib.parse import urlparse

RAW = Path("memory/multi_ingress_raw_candidates.json")
OUT_JSON = Path("memory/canonical_opportunities.json")
OUT_DEPLOY = Path("deploy_data/canonical_opportunities.json")
OUT_REPORT = Path("reports/canonical_opportunities.md")

CANONICAL_RULES = [
    ("Tokyo Art Book Fair", ["tokyoartbookfair.com", "tokyo art book fair", "tokio art book fair", "tabf"]),
    ("Fukuoka Art Book Fair", ["fukuokaartbookfair.com", "fukuoka art book fair"]),
    ("Jimbocho Zine Fair", ["jimbocho zine fair", "jimbocho.site/zinefair", "ひじりばし博覧会"]),
    ("ZINEフェス東京", ["zineフェス東京", "zine fest tokyo", "zine farm tokyo/status"]),
    ("Zines Fair at CP+", ["zines fair at cp", "cpplus.jp/zinesfair", "cp+ 2026"]),
    ("Kyotographie Photobook Fair", ["kyotographie", "photobook_fair"]),
    ("TOKAS Open Call", ["tokyoartsandspace.jp/en/application", "tokyoartsandspace.jp/application/index", "about open call programs"]),
    ("TOKAS Residency", ["tokyoartsandspace.jp/static/file/open call/residency", "international creator residency", "tokas residency", "2026年度 リサーチ・レジデンス"]),
    ("Jinny Street Gallery Open Call", ["jinnystreetgallery.com/open-call", "jinny street gallery"]),
    ("Belladonna Art Competition", ["art-belladonna.jp", "ベラドンナ"]),
    ("Shoto Museum Open Call", ["shoto-museum.jp", "松濤美術館"]),
    ("AIR_J Open Calls", ["air-j.info/en/program", "air-j.info/en/", "air_j"]),
    ("Hayama Artist Residency", ["hayamaartistresidency", "hayamaresidency"]),
    ("Kyoto Art Center Residency", ["kiac.jp", "kyoto art center", "kac.or.jp"]),
    ("NEW AIR", ["artcenter-new.jp", "new air"]),
    ("ARCUS Project Open Call", ["arcus-project.com"]),
    ("SCCP Guest Artist", ["sccp.jp/air-en"]),
    ("Clavis Publishing Submissions", ["clavis-publishing.com/submit"]),
    ("Case Publishing", ["case-publishing.jp"]),
    ("SEIGENSHA Art Publishing", ["seigensha.com"]),
    ("ARTE VENT Press", ["arte-vent.com"]),
    ("shashasha Publishers", ["shashasha.co/jp/publishers"]),
]

ARTICLE_NOISE = [
    "top 10", "complete guide", "huge list", "worth visiting", "hidden gems",
    "list of", "directory", "blog", "recommended", "ghostwriting",
    "まとめ", "一覧", "紹介", "ランキング"
]

def load(path, fallback):
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback

def domain(url):
    try:
        return urlparse(url or "").netloc.lower().replace("www.", "")
    except Exception:
        return ""

def canonical_name(row):
    blob = " ".join([
        row.get("title", ""),
        row.get("source_url", ""),
        domain(row.get("source_url", "")),
    ]).lower()

    for name, patterns in CANONICAL_RULES:
        if any(p.lower() in blob for p in patterns):
            return name

    title = row.get("title", "").strip()
    title = re.sub(r"\s+[|｜]\s+.*$", "", title)
    title = re.sub(r"\s+[-–—]\s+(Official|公式|Home|トップ).*$", "", title, flags=re.I)
    return title[:120] or "Untitled Opportunity"

def is_noise(row):
    blob = f"{row.get('title','')} {row.get('source_url','')}".lower()
    return any(x in blob for x in ARTICLE_NOISE)

def source_kind(row):
    title = row.get("title", "").lower()
    url = row.get("source_url", "").lower()
    if row.get("form_signal") or "application" in url or "apply" in url or "応募" in title or "申込" in title:
        return "application"
    if row.get("deadline_signal") or "open call" in title or "公募" in title:
        return "requirements"
    if any(x in url for x in ["pdf", ".pdf"]):
        return "pdf"
    if is_noise(row):
        return "article_or_directory"
    return "reference"

def merge_score(rows):
    best = max([r.get("score", 0) for r in rows] or [0])
    source_bonus = min(10, len(rows) * 2)
    form_bonus = 8 if any(r.get("form_signal") for r in rows) else 0
    deadline_bonus = 6 if any(r.get("deadline_signal") for r in rows) else 0
    noise_penalty = 8 if all(is_noise(r) for r in rows) else 0
    return max(0, min(100, best + source_bonus + form_bonus + deadline_bonus - noise_penalty))

def main():
    raw = load(RAW, {"candidates": []})
    candidates = raw.get("candidates", [])

    grouped = {}
    for row in candidates:
        name = canonical_name(row)
        grouped.setdefault(name, []).append(row)

    opportunities = []
    for name, rows in grouped.items():
        rows = sorted(rows, key=lambda r: r.get("score", 0), reverse=True)
        categories = [r.get("career_category", "other") for r in rows]
        category = max(set(categories), key=categories.count) if categories else "other"

        sources = []
        for r in rows:
            url = r.get("source_url", "")
            if not url:
                continue
            sources.append({
                "url": url,
                "title": r.get("title", ""),
                "kind": source_kind(r),
                "score": r.get("score", 0),
                "candidate_id": r.get("candidate_id"),
                "deadline_signal": r.get("deadline_signal", False),
                "fee_signal": r.get("fee_signal", False),
                "form_signal": r.get("form_signal", False),
            })

        # de-dupe URLs
        seen = set()
        clean_sources = []
        for s in sources:
            if s["url"] in seen:
                continue
            seen.add(s["url"])
            clean_sources.append(s)

        best_source = next((s for s in clean_sources if s["kind"] == "application"), None)
        if not best_source and clean_sources:
            best_source = clean_sources[0]

        opp = {
            "canonical_name": name,
            "career_category": category,
            "score": merge_score(rows),
            "source_count": len(clean_sources),
            "best_url": best_source["url"] if best_source else "",
            "best_source_kind": best_source["kind"] if best_source else "",
            "has_application": any(s["kind"] == "application" for s in clean_sources),
            "has_deadline_signal": any(s["deadline_signal"] for s in clean_sources),
            "has_fee_signal": any(s["fee_signal"] for s in clean_sources),
            "sources": clean_sources,
            "status": "canonicalized",
        }
        opportunities.append(opp)

    opportunities.sort(key=lambda x: x["score"], reverse=True)

    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_DEPLOY.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    data = {
        "source_candidate_count": len(candidates),
        "canonical_opportunity_count": len(opportunities),
        "opportunities": opportunities,
    }

    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_DEPLOY.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Canonical Opportunities",
        "",
        f"- Source candidates: {len(candidates)}",
        f"- Canonical opportunities: {len(opportunities)}",
        "",
    ]

    for cat in ["zines", "contests", "residencies", "publishing", "galleries"]:
        rows = [o for o in opportunities if o["career_category"] == cat]
        if not rows:
            continue
        lines.append(f"## {cat} ({len(rows)})")
        for o in rows[:25]:
            lines.append(f"### {o['canonical_name']}")
            lines.append(f"- Score: {o['score']}")
            lines.append(f"- Sources: {o['source_count']}")
            lines.append(f"- Best URL: {o['best_url']}")
            lines.append(f"- Has application: {o['has_application']}")
            lines.append(f"- Has deadline signal: {o['has_deadline_signal']}")
            lines.append("")
        lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_DEPLOY)
    print("Wrote", OUT_REPORT)
    print("Canonical opportunities:", len(opportunities))

if __name__ == "__main__":
    main()
