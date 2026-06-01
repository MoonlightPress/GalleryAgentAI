
import json
from pathlib import Path
from datetime import date

ZINE_TARGETS_PATHS = [
    Path("memory/zine_category_targets.json"),
    Path("Memory/zine_category_targets.json"),
    Path("deploy_data/zine_category_targets.json"),
]

COMPACT_PATHS = [
    Path("memory/compact_opportunities.json"),
    Path("Memory/compact_opportunities.json"),
    Path("deploy_data/compact_opportunities.json"),
]

OUT_MEMORY = Path("memory/compact_opportunities.json")
OUT_DEPLOY = Path("deploy_data/compact_opportunities.json")
OUT_REPORT = Path("reports/zine_opportunities_added.md")

CATEGORY = "zine_print"
SOURCE_TAG = "zine_category_import_v1"

def load_json(path, fallback):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return fallback

def find_existing(path_list, fallback):
    for p in path_list:
        if p.exists():
            return p, load_json(p, fallback)
    return None, fallback

def clean_unknown(value):
    if value is None:
        return ""
    value = str(value).strip()
    if value.lower() in {"unknown", "none", "null", "n/a"}:
        return ""
    return value

def title_key(opp):
    return (opp.get("title") or opp.get("name") or opp.get("organization") or "").strip().lower()

def score_from_confidence(confidence, tier):
    try:
        conf = float(confidence)
    except Exception:
        conf = 60

    # Existing app expects 0-10-ish scores.
    base = max(5.5, min(9.5, conf / 10))
    if tier == 1:
        base += 0.3
    elif tier == 3:
        base -= 0.4
    return round(max(5.0, min(9.8, base)), 1)

def source_from_target(t):
    websites = t.get("websites") or []
    if websites:
        return websites[0]
    return t.get("website") or t.get("source_url") or ""

def zine_target_to_opportunity(t):
    name = t.get("display_name") or t.get("canonical_name") or "Untitled zine target"
    neighborhood = clean_unknown(t.get("neighborhood"))
    opp_type = clean_unknown(t.get("opportunity_type"))
    confidence = t.get("confidence", 65)
    tier = t.get("tier", 2)
    source = source_from_target(t)

    why = clean_unknown(t.get("why_it_matters"))
    first_action = clean_unknown(t.get("first_action"))

    city = f"{neighborhood}, Tokyo" if neighborhood else "Tokyo"

    bullets = [
        f"Type: {opp_type.replace('_', ' ') if opp_type else 'zine / artist-book opportunity'}.",
        f"Location: {city}.",
        f"First action: {first_action or 'Confirm current contact, location, and whether zines are accepted.'}",
    ]

    return {
        "title": name,
        "name": name,
        "organization": name,
        "category": CATEGORY,
        "city": city,
        "overall_score": score_from_confidence(confidence, tier),
        "one_sentence": why or f"{name} is a zine / artist-book target worth checking for placement, consignment, or research.",
        "suggested_display_summary": why,
        "why_this_fits_short": (
            why or
            "Possible fit for small printed works, zines, artist books, and quiet works-on-paper presentation."
        ),
        "quick_action": first_action or "Verify current contact, location, and zine/artist-book policy.",
        "source_url": source,
        "source_link": source,
        "official_website": source,
        "submission_page": "",
        "deadline": "",
        "fees": "",
        "difficulty": "low",
        "three_bullets": bullets,
        "career_category": "zines",
        "opportunity_type": opp_type,
        "neighborhood": neighborhood,
        "tier": tier,
        "confidence": confidence,
        "status": "needs_confirmation",
        "import_source": SOURCE_TAG,
        "imported_at": str(date.today()),
    }

def build_summary_opportunity(targets):
    phase_1 = [
        "Tacoche",
        "LOCAL Gallery・Books",
        "Dig A Hole Zines",
        "本店・本屋の実験室",
        "そぞろ書房",
    ]

    known_count = len(targets)
    local_count = len([t for t in targets if t.get("neighborhood") in {"Koenji", "Nakano"}])
    high_priority = len([t for t in targets if t.get("tier") == 1])

    return {
        "title": "Zines / Artist Books — Battle Plan",
        "name": "Zines / Artist Books — Battle Plan",
        "organization": "Mochi Career System",
        "category": CATEGORY,
        "city": "Tokyo",
        "overall_score": 9.8,
        "one_sentence": (
            f"Fast, low-cost path with {known_count} curated targets, "
            f"{high_priority} high-priority targets, and {local_count} Koenji/Nakano targets."
        ),
        "suggested_display_summary": (
            "Create two small zines, print 20 copies each, and approach five strong local targets first."
        ),
        "why_this_fits_short": (
            "This path fits quiet works-on-paper and visual sequencing because one printed object can become "
            "a shop placement, fair application, portfolio proof, and publisher conversation starter."
        ),
        "quick_action": "Start with Tacoche, LOCAL Gallery・Books, Dig A Hole Zines, 本店・本屋の実験室, and そぞろ書房.",
        "source_url": "",
        "source_link": "",
        "official_website": "",
        "submission_page": "",
        "deadline": "",
        "fees": "Estimated print test: ¥10,000–¥25,000",
        "difficulty": "low",
        "three_bullets": [
            f"Known curated targets: {known_count}.",
            f"Phase 1 route: Koenji + Nakano.",
            "Success condition: two finished zines, five outreach attempts, one accepted placement.",
        ],
        "career_category": "zines",
        "opportunity_type": "category_summary",
        "neighborhood": "Tokyo",
        "tier": 0,
        "confidence": 100,
        "status": "ready",
        "phase_1_targets": phase_1,
        "import_source": SOURCE_TAG,
        "imported_at": str(date.today()),
    }

def main():
    zine_path, zine_data = find_existing(ZINE_TARGETS_PATHS, {"targets": []})
    compact_path, existing = find_existing(COMPACT_PATHS, [])

    if not zine_data.get("targets"):
        raise SystemExit("No zine targets found. Run run_zine_website_top_section_v1.py first.")

    if not isinstance(existing, list):
        raise SystemExit("compact_opportunities.json is not a list. Aborting to avoid corrupting data.")

    targets = zine_data["targets"]
    new_opps = [build_summary_opportunity(targets)] + [zine_target_to_opportunity(t) for t in targets]

    # Remove older zine imports by this script so repeated runs are safe.
    preserved = [
        o for o in existing
        if o.get("import_source") != SOURCE_TAG
    ]

    existing_keys = {title_key(o) for o in preserved}
    added = []
    skipped = []

    for opp in new_opps:
        key = title_key(opp)
        if key in existing_keys:
            skipped.append(opp["title"])
            continue
        preserved.append(opp)
        existing_keys.add(key)
        added.append(opp["title"])

    OUT_MEMORY.parent.mkdir(exist_ok=True)
    OUT_DEPLOY.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    OUT_MEMORY.write_text(json.dumps(preserved, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_DEPLOY.write_text(json.dumps(preserved, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Zine Opportunities Added To Existing Feed",
        "",
        f"- Zine source: {zine_path}",
        f"- Existing compact source: {compact_path}",
        f"- Existing preserved opportunities: {len(preserved) - len(added)}",
        f"- Added zine opportunities: {len(added)}",
        f"- Skipped duplicate titles: {len(skipped)}",
        "",
        "## Added",
    ]

    for title in added:
        lines.append(f"- {title}")

    if skipped:
        lines += ["", "## Skipped duplicates"]
        for title in skipped:
            lines.append(f"- {title}")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_MEMORY)
    print("Wrote", OUT_DEPLOY)
    print("Wrote", OUT_REPORT)
    print("Added:", len(added))

if __name__ == "__main__":
    main()
