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


def build_pref_context(profile: dict) -> dict | None:
    """Precompute all preference flags/sets from a profile. Returns None when
    there's nothing to apply, so callers can cheaply skip."""
    if not profile:
        return None
    priorities = profile.get("priorities", {})
    preferences = profile.get("preferences", {})
    ctx = {
        "primary_track":  priorities.get("primary_track", "hybrid"),
        "active_tiers":   [int(t) for t in (priorities.get("active_tiers") or [1, 2])],
        "avoid":          set(priorities.get("avoid") or []),
        "surface_more":   set(preferences.get("surface_more") or []),
        "surface_less":   set(preferences.get("surface_less") or []),
    }
    fee_tolerance = preferences.get("fee_tolerance", "medium")
    geo_focus = preferences.get("geo_focus") or ["tokyo", "international"]
    ctx["suppress_high_fee"]     = fee_tolerance in ("free", "low") or "high_fees" in ctx["avoid"]
    ctx["suppress_international"] = "international" not in geo_focus or "international_travel" in ctx["avoid"]
    ctx["avoid_photography"]     = "photography_calls" in ctx["avoid"]
    ctx["avoid_digital"]         = "digital_only" in ctx["avoid"]
    ctx["avoid_large_group"]     = "large_group" in ctx["avoid"]
    geo_country_map = {"tokyo": "japan", "japan": "japan", "beijing": "china", "international": None}
    allowed = {m for g in geo_focus if (m := geo_country_map.get(g))}
    allowed.add("japan")  # always allow Japan
    ctx["allowed_countries"] = allowed
    return ctx


def restore_baseline(opp: dict) -> dict:
    """Return a copy of `opp` with every preference effect undone — original
    score and bucket restored, markers cleared. Makes application idempotent
    AND bidirectional: re-applying a changed profile both adds and REMOVES
    effects, instead of leaving stale suppression baked in.

    Handles both new markers (peppercorn_base_score / _base_bucket) and the
    older delta-only markers, so it works on data from any prior pipeline run."""
    o = dict(opp)
    # Score: prefer the recorded base; otherwise reverse the recorded deltas.
    if "peppercorn_base_score" in o:
        o["overall_score"] = o["peppercorn_base_score"]
    else:
        delta = float(o.get("peppercorn_track_boost", 0) or 0) + \
                float(o.get("peppercorn_surface_nudge", 0) or 0)
        if delta:
            o["overall_score"] = round(float(o.get("overall_score", 0) or 0) - delta, 2)
    # Bucket: restore the recorded base, or (older data) infer IBM — the engine
    # only ever suppressed opps that started in the IBM bucket.
    if "peppercorn_base_bucket" in o:
        o["exclusive_primary_bucket"] = o["peppercorn_base_bucket"]
    elif o.get("peppercorn_suppressed"):
        o["exclusive_primary_bucket"] = IBM_BUCKET
    for k in ("peppercorn_base_score", "peppercorn_base_bucket", "peppercorn_track_boost",
              "peppercorn_surface_nudge", "peppercorn_suppressed"):
        o.pop(k, None)
    return o


def apply_to_opp(opp: dict, ctx: dict) -> dict:
    """Apply the preference context to a single opportunity. Always restores the
    baseline first, so the result depends only on the CURRENT profile — never on
    what a previous run happened to bake in. Returns a new dict; never mutates
    the input."""
    o = restore_baseline(opp)
    category = o.get("category", "") or ""
    base_score = float(o.get("overall_score", 0) or 0)
    base_bucket = o.get("exclusive_primary_bucket", "")
    score = base_score

    # ── Track-based score boost ──
    if ctx["primary_track"] == "publication" and category in PUBLICATION_CATS:
        score = round(min(10.0, base_score * 1.2), 2)
        o["peppercorn_track_boost"] = round(score - base_score, 2)
    elif ctx["primary_track"] == "gallery" and category in GALLERY_CATS:
        score = round(min(10.0, base_score * 1.2), 2)
        o["peppercorn_track_boost"] = round(score - base_score, 2)

    # ── Surface more / less nudge ──
    factor = 1.0
    if any(_matches_surface_group(o, g) for g in ctx["surface_more"]):
        factor *= SURFACE_MORE_FACTOR
    if any(_matches_surface_group(o, g) for g in ctx["surface_less"]):
        factor *= SURFACE_LESS_FACTOR
    if factor != 1.0:
        nudged_score = round(min(10.0, score * factor), 2)
        if nudged_score != score:
            o["peppercorn_surface_nudge"] = round(nudged_score - score, 2)
            score = nudged_score

    if score != base_score:
        o["peppercorn_base_score"] = base_score
        o["overall_score"] = score

    # ── IBM suppression (only from the IBM bucket) ──
    if base_bucket != IBM_BUCKET:
        return o

    def _suppress(reason):
        o["peppercorn_base_bucket"] = base_bucket
        o["exclusive_primary_bucket"] = SUPPRESSED_BUCKET
        o["peppercorn_suppressed"] = reason
        return o

    if ctx["avoid_photography"] and (o.get("native_medium") == "photography"
                                     or "photograph" in category.lower()):
        return _suppress("avoid_photography_calls")
    if ctx["avoid_digital"] and any(kw in category.lower() for kw in DIGITAL_ONLY_KEYWORDS):
        return _suppress("avoid_digital_only")
    if ctx["avoid_large_group"]:
        _hay = f"{category} {o.get('name','')} {o.get('title','')}".lower()
        if any(kw in _hay for kw in LARGE_GROUP_KEYWORDS):
            return _suppress("avoid_large_group")

    tier = o.get("career_tier")
    if tier is not None:
        try:
            if int(tier) not in ctx["active_tiers"]:
                return _suppress(f"tier_{tier}_not_active")
        except (ValueError, TypeError):
            pass

    if ctx["suppress_high_fee"]:
        amount = parse_fee_amount(o.get("fees", "") or "")
        if amount is not None and amount >= HIGH_FEE_THRESHOLD:
            return _suppress(f"high_fee_{int(amount)}")

    if ctx["suppress_international"]:
        country = (o.get("country", "") or "").strip().lower()
        if country and country not in ctx["allowed_countries"]:
            return _suppress(f"geo_suppressed_{country}")

    return o


def apply_preferences(opps: list, profile: dict) -> list:
    """Apply a profile's preferences to a list of opportunities, returning a new
    list of new dicts. A no-op (returns the input list unchanged) when there are
    no preferences to apply. Safe to call at serve time on cached data."""
    ctx = build_pref_context(profile)
    if ctx is None:
        return opps
    return [apply_to_opp(o, ctx) for o in opps]


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

    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))
    adjusted = apply_preferences(opps, profile)
    OPP_PATH.write_text(json.dumps(adjusted, ensure_ascii=False, indent=2), encoding="utf-8")

    suppressed = sum(1 for o in adjusted if o.get("peppercorn_suppressed"))
    boosted    = sum(1 for o in adjusted if o.get("peppercorn_track_boost"))
    nudged     = sum(1 for o in adjusted if o.get("peppercorn_surface_nudge"))
    print("Peppercorn preferences applied (idempotent):")
    print(f"  Track boosted     : {boosted}")
    print(f"  Surface nudged    : {nudged}")
    print(f"  IBM suppressed    : {suppressed}")


if __name__ == "__main__":
    main()
