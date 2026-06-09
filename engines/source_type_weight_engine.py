
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

OPP_PATH = "deploy_data/compact_opportunities.json"

# ── Type-based multipliers ────────────────────────────────────────────────────
# Applied multiplicatively to overall_score, then clamped to 9.4.
# Entries not in this table receive a multiplier of 1.0 (no change).
TYPE_WEIGHTS = {
    # Rewarded — curated, direct, artist-book ecosystem
    "photobook_publisher": 1.15,
    "artist_book_fair":    1.10,
    "manual_research":     1.05,
    "global_seed":         1.00,  # quality-controlled seeds; neutral boost
    # Neutral
    "discovery_search":    1.00,
    # Mild penalty
    "art_bookstore":       0.95,
    "photo_publication":   0.85,
    # Photography ecosystem — wrong professional context for a painter
    "photo_open_call":     0.75,
    "photo_festival":      0.75,
    # Aggregator listing pages — near-zero signal
    "event_listing":       0.40,
}

# ── URL / title signal adjustments ───────────────────────────────────────────
# Penalties are checked first; if one fires, rewards are skipped.
# Each entry: (field, [markers], factor)
PENALTY_PATTERNS = [
    # Aggregator / listicle titles
    ("title", ["一覧", "アートイベント一覧", "公募展の展覧会",
               "list of", "best of", "top 10",
               "all events", "event calendar"],       0.55),
    # Archive / past-event URLs or titles
    # NOTE: quality domains (tokyoartsandspace etc.) use /archive/ as their
    # application listing path — they are exempted via QUALITY_DOMAINS_URL below.
    ("url",   ["archive", "past", "アーカイブ"],      0.60),
    ("title", ["archive", "past", "アーカイブ"],      0.60),
    # Past-year references in title (system is 2026+)
    ("title", ["2023", "2024"],                       0.65),
    # Social media aggregator link pages
    ("url",   ["linktr.ee", "linktree", "campsite.bio"], 0.50),
]

# Known quality domains that use /archive/ as a URL path for live opportunities.
# If the source URL contains one of these, the archive URL penalty is skipped.
QUALITY_DOMAINS_URL = [
    "tokyoartsandspace.jp",
    "japanfoundation",
    "asianculturalcouncil",
    "agcj.or.jp",
]

REWARD_PATTERNS = [
    # Direct submission / application pages
    ("url", ["apply", "entry", "submit", "募集", "応募", "公募"], 1.15),
    # Known quality institutional domains
    ("url", ["japanfoundation", "asianculturalcouncil",
             "tokyoartsandspace", "agcj.or.jp"],              1.15),
    # Deadline visible in URL
    ("url", ["deadline"],                                      1.10),
]


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def _text(opp, field):
    """Return lower-case text for a field, handling None."""
    return (opp.get(field) or "").lower()


def compute_source_multiplier(opp):
    """
    Return (multiplier, reason) for the opportunity.
    Penalties are checked first; rewards only applied if no penalty fired.
    """
    title = _text(opp, "title")
    url   = _text(opp, "source_url")

    # 1. Type-weight base
    stype = opp.get("source_type") or opp.get("category") or ""
    base  = TYPE_WEIGHTS.get(stype, 1.0)

    # Is this URL from a quality domain? Used to exempt archive-URL penalty.
    is_quality_domain = any(d in url for d in QUALITY_DOMAINS_URL)

    # 2. Check penalties (first match wins)
    for field_key, markers, factor in PENALTY_PATTERNS:
        text = title if field_key == "title" else url
        # Skip archive/past URL penalty for known quality domains whose site
        # structure legitimately uses /archive/ paths for live calls.
        if field_key == "url" and is_quality_domain and any(
            m in ["archive", "past", "アーカイブ"] for m in markers
        ):
            continue

        fired = None
        for m in markers:
            ml = m.lower()
            if ml not in text:
                continue
            # Word-boundary check for short English words that are substrings
            # of common legitimate words ("past" inside "pastel", "past" inside
            # "pastoral", etc.). Require that the match is preceded and followed
            # by a non-alpha character or string boundary.
            if ml in ("past", "archive"):
                import re as _re
                if not _re.search(r'(?<![a-z])' + _re.escape(ml) + r'(?![a-z])', text):
                    continue
            fired = m
            break

        if fired:
            return base * factor, f"penalty:{field_key}:{fired}"

    # 3. Check rewards (first match wins)
    for field_key, markers, factor in REWARD_PATTERNS:
        text = title if field_key == "title" else url
        if any(m.lower() in text for m in markers):
            fired = next(m for m in markers if m.lower() in text)
            return base * factor, f"reward:{field_key}:{fired}"

    return base, f"type:{stype or 'unknown'}"


def main():
    opps = load_json(OPP_PATH, [])

    changed = 0
    for opp in opps:
        raw_score  = float(opp.get("overall_score", 0) or 0)
        multiplier, reason = compute_source_multiplier(opp)

        opp["source_type_weight"]   = round(multiplier, 4)
        opp["source_weight_reason"] = reason

        new_score = round(min(9.4, raw_score * multiplier), 2)
        if new_score != raw_score:
            opp["overall_score"] = new_score
            changed += 1

    opps.sort(key=lambda x: float(x.get("overall_score", 0) or 0), reverse=True)

    with open(OPP_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, indent=2, ensure_ascii=False)

    print(f"Applied source type weights to {len(opps)} opportunities ({changed} scores changed).")


if __name__ == "__main__":
    main()
