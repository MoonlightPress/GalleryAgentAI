"""
Reads memory/peppercorn_profile.json and applies the artist's stated
preferences as score adjustments and IBM suppression.

Runs after exclusive_strategy_bucket_engine.py.

Adjustments:
  - primary_track == 'publication': ×1.2 boost for publication/zine categories
  - primary_track == 'gallery': ×1.2 boost for gallery/exhibition categories
  - fee_tolerance 'low'/'free': suppress high-entry-fee opps from IBM
  - geo_focus without 'international': suppress non-Japan entries from IBM
  - active_tiers: suppress tiers outside active set from IBM
"""
import sys
import json
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

OPP_PATH = Path("deploy_data/compact_opportunities.json")
PROFILE_PATH = Path("memory/peppercorn_profile.json")

PUBLICATION_CATS = {
    "zine", "book_fair", "bookshop_consignment", "fair_popup",
    "publication_editorial", "editorial_illustration", "magazine_call",
    "book_cover_call", "editorial_commission", "press_target",
    "self_publishing", "zine_shop",
}
GALLERY_CATS = {
    "open_call", "group_show", "solo_show", "gallery_rental",
    "gallery_consignment", "residency", "institutional",
    "competitions_awards", "emerging_artist_award", "watercolor_competition",
    "illustration_prize", "competition_award",
}

IBM_BUCKET = "immediate_best_moves"
SUPPRESSED_BUCKET = "research_needed"
HIGH_FEE_THRESHOLD = 5000  # ¥5,000+

# Category-keyword groups shared by surface_more / surface_less and by the
# category-based avoid ids. Matching is substring against opp["category"].
SURFACE_GROUP_KEYWORDS = {
    "zines_books":     ("zine", "book", "publica", "self_publish", "press", "editorial"),
    "gallery_shows":   ("open_call", "group_show", "solo_show", "gallery",
                        "exhibition", "competition", "award", "prize"),
    "residencies":     ("residency", "residencies", "residence"),
    "cafes_bookshops": ("cafe", "café", "bookshop", "bookstore", "consignment"),
    "art_fairs":       ("fair", "popup", "pop_up", "market", "booth"),
    # Legacy ids still present in saved profiles (the UI now writes the keys above).
    "open_calls":      ("open_call", "open call", "competition", "award",
                        "prize", "group_show", "exhibition"),
    "bookstore_gallery": ("bookstore", "bookshop", "consignment", "book"),
}
SURFACE_MORE_FACTOR = 1.1   # gentle boost for categories she asked to see more of
SURFACE_LESS_FACTOR = 0.9   # gentle damping for categories she asked to see less of
# Best-effort title/category keywords for the "large_group" avoid id. Deliberately
# narrow so it never suppresses her core Tier-2 group shows by accident.
LARGE_GROUP_KEYWORDS = ("large group", "100 artists", "hundreds", "mega", "mass open")
DIGITAL_ONLY_KEYWORDS = ("digital", "online", "virtual", "nft")


def _category_text(opp):
    return (opp.get("category", "") or "").lower()


def _matches_surface_group(opp, group_id):
    return any(kw in _category_text(opp) for kw in SURFACE_GROUP_KEYWORDS.get(group_id, ()))


def parse_fee_amount(fees_str):
    if not fees_str:
        return None
    lower = fees_str.lower().strip()
    if lower in ("free", "無料", "0", ""):
        return 0.0
    matches = re.findall(r"[¥￥]?[\d,]+(?:円)?", fees_str)
    amounts = []
    for m in matches:
        clean = re.sub(r"[¥￥円,]", "", m)
        if clean.isdigit():
            amounts.append(int(clean))
    return max(amounts) if amounts else None


def main():
    if not OPP_PATH.exists():
        print("No compact_opportunities.json — skipping.")
        return

    if not PROFILE_PATH.exists():
        print("No peppercorn_profile.json found — skipping preference adjustments.")
        return

    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    if not profile:
        print("Empty peppercorn_profile.json — skipping.")
        return

    priorities = profile.get("priorities", {})
    preferences = profile.get("preferences", {})

    primary_track = priorities.get("primary_track", "hybrid")
    active_tiers = [int(t) for t in (priorities.get("active_tiers") or [1, 2])]
    fee_tolerance = preferences.get("fee_tolerance", "medium")
    geo_focus = preferences.get("geo_focus") or ["tokyo", "international"]

    # Previously-dead feedback loops: the artist's explicit avoid checklist and
    # her surface-more / surface-less category preferences. These are opt-in —
    # nothing happens unless she selected it — so honoring them never contradicts
    # the "don't auto-penalize photography" rule.
    avoid = set(priorities.get("avoid") or [])
    surface_more = set(preferences.get("surface_more") or [])
    surface_less = set(preferences.get("surface_less") or [])

    suppress_high_fee = fee_tolerance in ("free", "low") or "high_fees" in avoid
    suppress_international = "international" not in geo_focus or "international_travel" in avoid
    avoid_photography = "photography_calls" in avoid
    avoid_digital = "digital_only" in avoid
    avoid_large_group = "large_group" in avoid

    # Build allowed country set from geo_focus tokens
    geo_country_map = {
        "tokyo": "japan",
        "japan": "japan",
        "beijing": "china",
        "international": None,
    }
    allowed_countries = set()
    for g in geo_focus:
        mapped = geo_country_map.get(g)
        if mapped:
            allowed_countries.add(mapped)
    # Always allow Japan
    allowed_countries.add("japan")

    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))

    boosted = suppressed_tier = suppressed_fee = suppressed_geo = 0
    nudged = suppressed_avoid = 0

    for opp in opps:
        category = opp.get("category", "") or ""
        score = float(opp.get("overall_score", 0) or 0)
        bucket = opp.get("exclusive_primary_bucket", "")

        # ── Track-based score boost ──
        if primary_track == "publication" and category in PUBLICATION_CATS:
            new_score = round(min(10.0, score * 1.2), 2)
            opp["overall_score"] = new_score
            opp["peppercorn_track_boost"] = round(new_score - score, 2)
            boosted += 1
        elif primary_track == "gallery" and category in GALLERY_CATS:
            new_score = round(min(10.0, score * 1.2), 2)
            opp["overall_score"] = new_score
            opp["peppercorn_track_boost"] = round(new_score - score, 2)
            boosted += 1

        # ── Surface more / less nudge (small, reflects stated category interest) ──
        factor = 1.0
        if any(_matches_surface_group(opp, g) for g in surface_more):
            factor *= SURFACE_MORE_FACTOR
        if any(_matches_surface_group(opp, g) for g in surface_less):
            factor *= SURFACE_LESS_FACTOR
        if factor != 1.0:
            cur = float(opp.get("overall_score", 0) or 0)
            new_score = round(min(10.0, cur * factor), 2)
            if new_score != cur:
                opp["overall_score"] = new_score
                opp["peppercorn_surface_nudge"] = round(new_score - cur, 2)
                nudged += 1

        # ── IBM suppression (only from IBM bucket) ──
        if bucket != IBM_BUCKET:
            continue

        # Avoid checklist — explicit, opt-in category suppression
        if avoid_photography and (opp.get("native_medium") == "photography"
                                  or "photograph" in category.lower()):
            opp["exclusive_primary_bucket"] = SUPPRESSED_BUCKET
            opp["peppercorn_suppressed"] = "avoid_photography_calls"
            suppressed_avoid += 1
            continue
        if avoid_digital and any(kw in category.lower() for kw in DIGITAL_ONLY_KEYWORDS):
            opp["exclusive_primary_bucket"] = SUPPRESSED_BUCKET
            opp["peppercorn_suppressed"] = "avoid_digital_only"
            suppressed_avoid += 1
            continue
        if avoid_large_group:
            _hay = f"{category} {opp.get('name','')} {opp.get('title','')}".lower()
            if any(kw in _hay for kw in LARGE_GROUP_KEYWORDS):
                opp["exclusive_primary_bucket"] = SUPPRESSED_BUCKET
                opp["peppercorn_suppressed"] = "avoid_large_group"
                suppressed_avoid += 1
                continue

        # Tier gating
        tier = opp.get("career_tier")
        if tier is not None:
            try:
                if int(tier) not in active_tiers:
                    opp["exclusive_primary_bucket"] = SUPPRESSED_BUCKET
                    opp["peppercorn_suppressed"] = f"tier_{tier}_not_active"
                    suppressed_tier += 1
                    continue
            except (ValueError, TypeError):
                pass

        # Fee suppression
        if suppress_high_fee:
            amount = parse_fee_amount(opp.get("fees", "") or "")
            if amount is not None and amount >= HIGH_FEE_THRESHOLD:
                opp["exclusive_primary_bucket"] = SUPPRESSED_BUCKET
                opp["peppercorn_suppressed"] = f"high_fee_{int(amount)}"
                suppressed_fee += 1
                continue

        # Geographic suppression
        if suppress_international:
            country = (opp.get("country", "") or "").strip().lower()
            if country and country not in allowed_countries:
                opp["exclusive_primary_bucket"] = SUPPRESSED_BUCKET
                opp["peppercorn_suppressed"] = f"geo_suppressed_{country}"
                suppressed_geo += 1

    OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Peppercorn preferences applied:")
    print(f"  Track boost ({primary_track}): {boosted}")
    print(f"  Surface more/less nudged: {nudged}")
    print(f"  IBM suppressed - wrong tier: {suppressed_tier}")
    print(f"  IBM suppressed - high fee (>¥{HIGH_FEE_THRESHOLD}): {suppressed_fee}")
    print(f"  IBM suppressed - geography: {suppressed_geo}")
    print(f"  IBM suppressed - avoid checklist: {suppressed_avoid}")


if __name__ == "__main__":
    main()
