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

    suppress_high_fee = fee_tolerance in ("free", "low")
    suppress_international = "international" not in geo_focus

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

        # ── IBM suppression (only from IBM bucket) ──
        if bucket != IBM_BUCKET:
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
    print(f"  IBM suppressed - wrong tier: {suppressed_tier}")
    print(f"  IBM suppressed - high fee (>¥{HIGH_FEE_THRESHOLD}): {suppressed_fee}")
    print(f"  IBM suppressed - geography: {suppressed_geo}")


if __name__ == "__main__":
    main()
