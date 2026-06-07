"""
seed_grant_opportunities.py

Adds 5 known real grant opportunities to compact_opportunities.json
if they don't already exist (checked by title, case-insensitive).

Run once: python scripts/patches/seed_grant_opportunities.py
"""

import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

import json
import re
from pathlib import Path

ROOT     = Path(__file__).parent.parent.parent
OPP_PATH = ROOT / "deploy_data" / "compact_opportunities.json"

SEED_GRANTS = [
    {
        "title": "Asian Cultural Council Fellowship",
        "name": "Asian Cultural Council Fellowship",
        "organization": "Asian Cultural Council",
        "category": "grant",
        "opportunity_type": "grant",
        "city": "New York",
        "country": "USA",
        "source_url": "https://www.accgrants.org/",
        "official_website": "https://www.accgrants.org/",
        "deadline": "March 2027 (check accgrants.org for 2027 cycle)",
        "fees": "Free to apply",
        "overall_score": 9.0,
        "differentiated_score": 9.5,
        "one_sentence": "Fellowship grant for Asian artists doing arts exchange with the USA. Chinese nationals fully eligible. Travel + $3k/month stipend for 1-6 months.",
        "why_this_fits_short": "She's Chinese — fully eligible. ACC alumni network is one of the most valuable in Asian contemporary art. Lower competition than Western equivalents.",
        "quick_action": "Research current eligibility requirements at accgrants.org. Prepare: project proposal, portfolio, 2 recommendation letters.",
        "native_medium": "all",
        "action_type": "apply",
        "verification_status": "verified",
        "verification_bucket": "stretch_targets",
        "tags": ["grant", "fellowship", "chinese_national", "arts_exchange", "acc"],
        "discovery_group": "GRANT",
        "added_by": "grant_discovery_engine",
        "research_priority": "high",
        "relationship_note": "Annual program. Previous Asian watercolor/painting artists have received ACC fellowships. Strong application narrative: Chinese artist in Tokyo documenting urban disappearance for US arts exchange.",
    },
    {
        "title": "Japan Foundation Cultural Exchange Grant",
        "name": "Japan Foundation Cultural Exchange Grant",
        "organization": "Japan Foundation (国際交流基金)",
        "category": "grant",
        "opportunity_type": "grant",
        "city": "Tokyo",
        "country": "Japan",
        "source_url": "https://www.jpf.go.jp/j/program/grant.html",
        "official_website": "https://www.jpf.go.jp/",
        "deadline": "September–October annually (check jpf.go.jp for current cycle)",
        "fees": "Free to apply",
        "overall_score": 8.5,
        "differentiated_score": 9.0,
        "one_sentence": "Japanese government cultural exchange grants for artists resident in Japan. ¥500k–3M depending on program track. Watercolor/painting has track record.",
        "why_this_fits_short": "Japan-based artist. Urban documentation of Tokyo is a strong cultural exchange narrative. Multiple program tracks — individual artists, collaborative projects.",
        "quick_action": "Visit jpf.go.jp for current programs. Application in Japanese required. Start 4 months before deadline.",
        "native_medium": "all",
        "action_type": "apply",
        "verification_status": "verified",
        "verification_bucket": "stretch_targets",
        "tags": ["grant", "japan_foundation", "cultural_exchange", "japanese_government"],
        "discovery_group": "GRANT",
        "added_by": "grant_discovery_engine",
        "research_priority": "high",
    },
    {
        "title": "Bunka-cho 新進芸術家海外研修制度",
        "name": "Bunka-cho Overseas Study Grant for Emerging Artists",
        "organization": "文化庁 (Agency for Cultural Affairs, Japan)",
        "category": "grant",
        "opportunity_type": "grant",
        "city": "Tokyo",
        "country": "Japan",
        "source_url": "https://www.bunka.go.jp/seisaku/geijutsubunka/shinkokusai/kaigai_kenshu/",
        "official_website": "https://www.bunka.go.jp/",
        "deadline": "Check bunka.go.jp annually — typically spring deadline",
        "fees": "Free to apply",
        "overall_score": 8.5,
        "differentiated_score": 9.0,
        "one_sentence": "Bunka-cho overseas residency grant for emerging artists in Japan. Monthly allowance + airfare for 6–12 months abroad. Painting/visual arts category.",
        "why_this_fits_short": "Funds a full year of overseas artistic development. Applying for residency at Cité Internationale des Arts (Paris) strengthens the application significantly.",
        "quick_action": "Research eligibility at bunka.go.jp. Application in Japanese. Start 4–6 months before deadline with a specific overseas residency target named.",
        "native_medium": "painting",
        "action_type": "apply",
        "verification_status": "strong_partial",
        "verification_bucket": "stretch_targets",
        "tags": ["grant", "bunka_cho", "overseas_residency", "japanese_government", "emerging_artist"],
        "discovery_group": "GRANT",
        "added_by": "grant_discovery_engine",
        "research_priority": "high",
    },
    {
        "title": "Tokyo Arts and Space (TOKAS) Residency + Grant",
        "name": "TOKAS Residency Program",
        "organization": "Tokyo Arts and Space (東京都現代美術館)",
        "category": "grant",
        "opportunity_type": "grant",
        "city": "Tokyo",
        "country": "Japan",
        "source_url": "https://www.tokyoartsandspace.jp/en/programs/residency/",
        "official_website": "https://www.tokyoartsandspace.jp/",
        "deadline": "Check tokyoartsandspace.jp — typically annual open call",
        "fees": "Free to apply",
        "overall_score": 8.0,
        "differentiated_score": 8.5,
        "one_sentence": "Tokyo Metropolitan arts residency with stipend. Studio space + ¥100k–500k grant support. Institutional credibility from Tokyo Metro government.",
        "why_this_fits_short": "Tokyo-based artist — strong eligibility. TOKAS residency on CV is a significant credibility marker for Tier 3 advancement.",
        "quick_action": "Check tokyoartsandspace.jp for current open call. Requires project proposal + portfolio.",
        "native_medium": "all",
        "action_type": "apply",
        "verification_status": "strong_partial",
        "verification_bucket": "research_needed",
        "tags": ["grant", "residency", "tokyo_metro", "institutional", "tokas"],
        "discovery_group": "GRANT",
        "added_by": "grant_discovery_engine",
        "research_priority": "high",
    },
    {
        "title": "Pola Art Foundation Grant",
        "name": "Pola Art Foundation Grant for Overseas Study",
        "organization": "Pola Art Foundation (公益財団法人ポーラ美術振興財団)",
        "category": "grant",
        "opportunity_type": "grant",
        "city": "Tokyo",
        "country": "Japan",
        "source_url": "https://www.pola-art-foundation.jp/grant/",
        "official_website": "https://www.pola-art-foundation.jp/",
        "deadline": "Typically September–November annually",
        "fees": "Free to apply",
        "overall_score": 8.0,
        "differentiated_score": 8.5,
        "one_sentence": "Private Japanese foundation grant for overseas art study. Painters and print artists. ¥1–2M for 6–12 months abroad. Lower competition than government grants.",
        "why_this_fits_short": "Painting category is core Pola focus. Private foundation = faster decisions and less bureaucracy than government grants.",
        "quick_action": "Check pola-art-foundation.jp for current cycle. Japanese application required.",
        "native_medium": "painting",
        "action_type": "apply",
        "verification_status": "strong_partial",
        "verification_bucket": "stretch_targets",
        "tags": ["grant", "private_foundation", "overseas_study", "painting", "pola"],
        "discovery_group": "GRANT",
        "added_by": "grant_discovery_engine",
        "research_priority": "medium",
    },
]


def name_key(item: dict) -> str:
    n = (item.get("title") or item.get("name") or "").lower().strip()
    return re.sub(r"\s+", " ", n)


def load_json(path: Path, fallback):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return fallback


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    print("=== Seed Grant Opportunities ===")
    print(f"File: {OPP_PATH}\n")

    opps = load_json(OPP_PATH, [])
    existing_keys = {name_key(o) for o in opps}

    added = []
    for grant in SEED_GRANTS:
        key = name_key(grant)
        if key in existing_keys:
            print(f"  SKIP (exists): {grant['title']}")
        else:
            existing_keys.add(key)
            opps.append(grant)
            added.append(grant)
            print(f"  ADD: {grant['title']} [score={grant['overall_score']}]")

    if added:
        opps.sort(
            key=lambda x: float(x.get("overall_score", 0) or 0),
            reverse=True,
        )
        save_json(OPP_PATH, opps)
        print(f"\nAdded {len(added)} grant(s). Total opportunities: {len(opps)}")
        print(f"Saved: {OPP_PATH}")
    else:
        print("\nAll grants already present — nothing to add.")

    print("\nDone.")


if __name__ == "__main__":
    main()
