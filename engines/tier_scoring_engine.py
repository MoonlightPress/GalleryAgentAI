import json
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

OPP_PATH = "deploy_data/compact_opportunities.json"

TIER1_CATEGORIES = frozenset([
    'zine_fair_booth',
    'zine_shop_consignment',
    'cafe_gallery',
    'bookstore_gallery',
    'bookstore_event',
])

TIER2_CATEGORIES = frozenset([
    'gallery',
    'artist_space',
    'event_space',
    'gallery_event',
    'fair_popup',
    'market_event',
])

TIER3_CATEGORIES = frozenset([
    'japan_watercolor_open_call',
    'global_watercolor_open_call',
    'global_open_call',
    'residency',
    'global_photobook',
    'group_publication_open_call',
    'book_publishing',
])

TIER4_CATEGORIES = frozenset([
    'global_residency',
    'global_art_book_fair',
])

TIER4_TITLE_SIGNALS = [
    'royal watercolour', 'rws', 'american watercolor society', 'aws',
    'cité internationale', 'cite internationale', 'cité',
    'asian cultural council', 'printed matter', 'offprint',
]

# Score adjustment per tier for an artist currently in Tier 1-2.
# Tier 1-2 opportunities get a strong boost; international open calls (Tier 3)
# get a modest penalty so local consignment/café venues rank above them.
# The gap between Tier 1 and Tier 3 must be large enough to overcome
# higher base scores on well-documented international open calls.
TIER_ADJUSTMENTS = {
    1: +2.5,
    2: +1.0,
    3: -0.5,
    4: -2.0,
}


def classify_tier(opp):
    category = (opp.get('category') or '').lower().strip()
    tags = [str(t).lower() for t in opp.get('tags', [])]
    title = (opp.get('title') or opp.get('name') or '').lower()

    # Tag overrides first — explicit tags trump category inference
    if 'tier_1' in tags:
        return 1
    if 'tier_2' in tags:
        return 2
    if 'prestige' in tags:
        return 4

    # Tier 4 by title signal (known prestige targets)
    for signal in TIER4_TITLE_SIGNALS:
        if signal in title:
            return 4

    if category in TIER4_CATEGORIES:
        return 4
    if category in TIER1_CATEGORIES:
        return 1
    if category in TIER2_CATEGORIES:
        return 2
    if category in TIER3_CATEGORIES:
        return 3

    # Ambiguous — default to Tier 3 (no boost, no penalty)
    return 3


def main():
    if not os.path.exists(OPP_PATH):
        print(f"Not found: {OPP_PATH}")
        return

    with open(OPP_PATH, 'r', encoding='utf-8') as f:
        opps = json.load(f)

    for opp in opps:
        tier = classify_tier(opp)
        adjustment = TIER_ADJUSTMENTS[tier]
        original = float(opp.get('overall_score') or 0)
        adjusted = round(max(0.0, min(10.0, original + adjustment)), 2)

        opp['career_tier'] = tier
        opp['tier_adjustment'] = adjustment
        opp['overall_score'] = adjusted

    opps.sort(key=lambda x: float(x.get('overall_score') or 0), reverse=True)

    with open(OPP_PATH, 'w', encoding='utf-8') as f:
        json.dump(opps, f, indent=2, ensure_ascii=False)

    tier_counts = {}
    for opp in opps:
        t = opp.get('career_tier', '?')
        tier_counts[t] = tier_counts.get(t, 0) + 1

    print(f"Tier scoring applied to {len(opps)} opportunities.")
    for t in sorted(tier_counts):
        print(f"  Tier {t}: {tier_counts[t]}")


if __name__ == "__main__":
    main()
