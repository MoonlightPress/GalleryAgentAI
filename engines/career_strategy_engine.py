"""
career_strategy_engine.py

Produces a Career Readiness Report for GEGYjiji grounded in her actual
confirmed career history and the live opportunity pipeline.

Output: memory/career_strategy_report.json
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT      = Path(__file__).parent.parent
OPP_PATH  = ROOT / "deploy_data" / "compact_opportunities.json"
PROFILE   = ROOT / "memory" / "artist_master_profile.json"
EX_LOG    = ROOT / "memory" / "exhibition_log.json"
OUT_PATH  = ROOT / "memory" / "career_strategy_report.json"


# ── Tier classification ───────────────────────────────────────────────────────

# Tier 1 = Ambient Visibility (zines, bookshops, cafes, fairs)
# Tier 2 = Networking (group shows, open calls, artist-run spaces)
# Tier 3 = Credibility (institutional, juried, watercolor societies)
# Tier 4 = Prestige (residencies abroad, major fellowships, RWS, ACC, etc.)

TIER1_CATS = {
    "zine_print",
    "zine_shop_consignment",
    "zine_fair_booth",
    "bookstore_gallery",
    "bookstore_event",
    "book_publishing",
    "global_artist_book_platform",
    "global_art_book_fair",
    "global_book_arts",
    "cafe_gallery",
    "fair_popup",
    "market_event",
}

TIER2_CATS = {
    "gallery",
    "gallery_small",
    "artist_space",
    "event_space",
    "gallery_event",
    "global_open_call",
    "group_publication_open_call",
    "editorial_illustration",
    "magazine_call",
    "book_cover_call",
    "publication_editorial",
    "editorial_commission",
    "competition_award",
    "illustration_prize",
    "emerging_artist_award",
    "watercolor_competition",
}

TIER3_CATS = {
    "institutional",
    "japan_watercolor_institution",
    "japan_watercolor_open_call",
    "global_watercolor_open_call",
    "global_photobook",
}

TIER4_CATS = {
    "residency",
    "global_residency",
    "global_grant_fellowship",
    "residency_beijing",
}

TIER4_TITLE_KEYWORDS = {
    "royal watercolour", "royal watercolor", "rws open",
    "american watercolor society", "aws annual",
    "cité internationale", "cite internationale",
    "asian cultural council", "acc fellowship",
    "printed matter", "offprint", "center for book arts",
}

TIER3_TITLE_KEYWORDS = {
    "tokas", "bankart", "youkobo", "shoto museum", "jinny street",
    "belladonna", "japan watercolor society", "日本水彩", "公益社団法人日本水彩",
}


def _classify_tier(opp: dict) -> int:
    """Return 1–4 for the career tier of an opportunity."""
    cat      = (opp.get("category") or "").lower()
    title    = (opp.get("title") or opp.get("name") or "").lower()
    org      = (opp.get("organization") or "").lower()
    combined = f"{title} {org}"

    # Explicit career_tier field wins if present and valid
    explicit = opp.get("career_tier")
    if isinstance(explicit, int) and 1 <= explicit <= 4:
        return explicit

    # Title/org keyword overrides
    if any(kw in combined for kw in TIER4_TITLE_KEYWORDS):
        return 4
    if any(kw in combined for kw in TIER3_TITLE_KEYWORDS):
        return 3

    # Category-based
    if cat in TIER4_CATS:
        return 4
    if cat in TIER3_CATS:
        return 3
    if cat in TIER2_CATS:
        return 2
    if cat in TIER1_CATS:
        return 1

    # Fallback from pipeline bucket
    bucket = (opp.get("exclusive_primary_bucket") or "").lower()
    if bucket == "stretch_targets":
        return 4
    if bucket == "publication_targets":
        return 1

    return 2  # default to Tier 2


def _score(opp: dict) -> float:
    return float(
        opp.get("overall_score")
        or opp.get("dna_adjusted_score")
        or opp.get("watercolor_adjusted_score")
        or 0
    )


def _opp_title(opp: dict) -> str:
    return opp.get("title") or opp.get("name") or "Unknown"


def _opp_summary(opp: dict) -> str:
    return (opp.get("one_sentence") or opp.get("summary") or "")[:200]


def _opp_deadline(opp: dict) -> str:
    d = str(opp.get("deadline") or "").strip()
    EMPTY = {"", "unknown", "n/a", "tbd", "check current schedule", "varies",
             "check site", "see website", "none", "check source"}
    return d if d.lower() not in EMPTY else ""


def _opp_card(opp: dict, tier: int) -> dict:
    return {
        "title":    _opp_title(opp),
        "tier":     tier,
        "score":    round(_score(opp), 2),
        "category": opp.get("category", ""),
        "city":     opp.get("city", ""),
        "deadline": _opp_deadline(opp),
        "summary":  _opp_summary(opp),
        "website":  opp.get("official_website") or opp.get("source_url") or "",
    }


# ── Career history helpers ────────────────────────────────────────────────────

def _load_json(path: Path, fallback):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return fallback


def _count_group_shows(profile: dict, ex_log: list) -> int:
    """Count confirmed group shows from research + exhibition log."""
    base = 1  # Tide from China Part1, Feb 2023 (confirmed)

    for ex in profile.get("career_history", {}).get("exhibitions", []):
        etype = (ex.get("type") or "").lower()
        if "group" in etype and ex.get("title") != "Tide from China Part1":
            base += 1

    # Exclude the hardcoded base show by title so logging it via the event
    # quick-log UI doesn't double-count it against base=1.
    logged = sum(
        1 for e in ex_log
        if e.get("type") == "group"
        and e.get("outcome") in ("shown", "completed", None, "")
        and (e.get("title") or "").strip() != "Tide from China Part1"
    )
    return base + logged


def _has_solo_show(profile: dict, ex_log: list) -> bool:
    for ex in profile.get("career_history", {}).get("exhibitions", []):
        if "solo" in (ex.get("type") or "").lower():
            return True
    for e in ex_log:
        if e.get("type") == "solo" and e.get("outcome") in ("shown", "completed", None, ""):
            return True
    return False


def _has_institutional_show(profile: dict, ex_log: list) -> bool:
    KWS = {"tokas", "bankart", "youkobo", "museum", "arts council",
           "cultural center", "cultural centre", "arts centre", "arts center",
           "公益", "財団", "国際"}
    for ex in profile.get("career_history", {}).get("exhibitions", []):
        if any(kw in (ex.get("venue") or "").lower() for kw in KWS):
            return True
    for e in ex_log:
        if any(kw in (e.get("venue") or "").lower() for kw in KWS):
            if e.get("outcome") in ("shown", "completed", None, ""):
                return True
    return False


def _has_international_show(profile: dict, ex_log: list) -> bool:
    INTL = ("london", "paris", "new york", "berlin", "sydney", "amsterdam",
            "brussels", "zurich", "seoul", "hong kong")
    for ex in profile.get("career_history", {}).get("exhibitions", []):
        venue = (ex.get("venue") or "").lower()
        title = (ex.get("title") or "").lower()
        if any(kw in venue for kw in INTL) or any(kw in title for kw in ("international", "global")):
            return True
    for e in ex_log:
        country = (e.get("country") or "").lower()
        if country and country not in ("japan", "china"):
            if e.get("outcome") in ("shown", "completed", None, ""):
                return True
    return False


def _has_jws(profile: dict) -> bool:
    history = str(profile.get("career_history", {})).lower()
    return "japan watercolor society" in history or "日本水彩" in history


# ── Readiness scores ──────────────────────────────────────────────────────────

def _tier3_readiness(group_shows: int, has_solo: bool,
                     has_institutional: bool, has_international: bool) -> float:
    """
    Score 0.0–1.0 for Tier 3 readiness.
    Group shows are the dominant factor (up to 0.45).
    Institutional: 0.25 | Solo: 0.20 | International: 0.10
    """
    score = 0.0
    if group_shows >= 5:
        score += 0.45
    elif group_shows >= 3:
        score += 0.35
    elif group_shows >= 2:
        score += 0.20
    elif group_shows == 1:
        score += 0.10
    if has_institutional:
        score += 0.25
    if has_solo:
        score += 0.20
    if has_international:
        score += 0.10
    return round(min(score, 1.0), 2)


def _tier4_readiness(group_shows: int, has_solo: bool, has_institutional: bool) -> float:
    """
    Score 0.0–1.0 for Tier 4 readiness.
    Requires solid foundation: group shows + institutional + solo.
    """
    score = 0.0
    if group_shows >= 5:
        score += 0.30
    elif group_shows >= 3:
        score += 0.20
    elif group_shows >= 2:
        score += 0.10
    if has_institutional:
        score += 0.35
    if has_solo:
        score += 0.35
    return round(min(score, 1.0), 2)


def _months_to_tier3(group_shows: int, has_institutional: bool) -> int:
    if has_institutional:
        return 3
    if group_shows >= 3:
        return 6
    return 12


def _blocking_gaps(group_shows: int, has_solo: bool, has_institutional: bool,
                   has_international: bool, has_jws: bool) -> list:
    gaps = []

    if group_shows < 3:
        needed = 3 - group_shows
        gaps.append({
            "gap":      "Insufficient group show history",
            "detail":   (
                f"Only {group_shows} confirmed group show(s). "
                f"Most Tokyo galleries consider 3+ group exhibition credits before "
                f"discussing solo work. {needed} more group show(s) needed."
            ),
            "priority": "high",
            "action":   "Apply to open calls at 3331 Arts Chiyoda, Design Festa Gallery, Gallery IYN",
        })

    if not has_solo:
        gaps.append({
            "gap":      "No solo show on CV",
            "detail":   (
                "No solo exhibition confirmed in Tokyo or elsewhere. "
                "A solo show — even in a small bookshop gallery or documented café context — "
                "provides a qualitative leap in credibility when applying to Tier 3 calls."
            ),
            "priority": "medium",
            "action":   "Target bookshop gallery solo show: UTRECHT, Book and Sons, flotsam books, 日記屋 月日",
        })

    if not has_institutional:
        gaps.append({
            "gap":      "No institutional exhibition history",
            "detail":   (
                "No show at an arts council, public gallery, or institutional space. "
                "TOKAS, BankART1929, and Youkobo are the realistic near-term institutional entries "
                "for Tokyo-based artists at this stage."
            ),
            "priority": "medium",
            "action":   "Watch TOKAS open calls and Youkobo artist-in-residence programs",
        })

    if not has_international:
        gaps.append({
            "gap":      "No international exhibition outside Japan/China",
            "detail":   (
                "All confirmed exhibition history is in Japan (and China, via Kinoko Kingdom). "
                "International reach strengthens applications for residencies and fellowships."
            ),
            "priority": "low",
            "action":   "Consider global watercolor open calls or table at Offprint Paris / London Art Book Fair",
        })

    if not has_jws:
        gaps.append({
            "gap":      "No Japan Watercolor Society membership or exhibition",
            "detail":   (
                "The Japan Watercolor Society annual exhibition is a Tier 3 credibility marker "
                "for watercolor artists in Japan. Non-members can enter juried calls; "
                "membership requires exhibition selection."
            ),
            "priority": "low",
            "action":   "Research Japan Watercolor Society (公益社団法人日本水彩画会) annual entry process",
        })

    return gaps


# ── Main engine ───────────────────────────────────────────────────────────────

def build_career_strategy_report():
    opps    = _load_json(OPP_PATH, [])
    profile = _load_json(PROFILE, {})
    ex_log  = _load_json(EX_LOG, [])

    if not opps:
        print("WARNING: No opportunities loaded — check OPP_PATH")
    if not profile:
        print("WARNING: No artist profile loaded — check PROFILE")

    # ── Career history facts ─────────────────────────────────────────────────
    group_shows       = _count_group_shows(profile, ex_log)
    has_solo          = _has_solo_show(profile, ex_log)
    has_institutional = _has_institutional_show(profile, ex_log)
    has_international = _has_international_show(profile, ex_log)
    has_jws           = _has_jws(profile)

    # ── Readiness scores ─────────────────────────────────────────────────────
    tier3_ready = _tier3_readiness(group_shows, has_solo, has_institutional, has_international)
    tier4_ready = _tier4_readiness(group_shows, has_solo, has_institutional)

    # ── Classify and tier-weight all active opportunities ────────────────────
    REJECT_BUCKETS = {"reject", "low_priority"}
    active = [
        o for o in opps
        if o.get("exclusive_primary_bucket") not in REJECT_BUCKETS
        and o.get("status") != "permanently_closed"
        and o.get("recommendation_visibility") != "hidden"
    ]

    tier1_opps: list = []
    tier2_opps: list = []
    tier3_opps: list = []
    tier4_opps: list = []

    for opp in active:
        tier = _classify_tier(opp)
        ws   = _score(opp)
        if tier == 1:
            ws *= 1.4
            tier1_opps.append((ws, opp, tier))
        elif tier == 2:
            ws *= 1.3
            tier2_opps.append((ws, opp, tier))
        elif tier == 3:
            tier3_opps.append((ws, opp, tier))
        else:
            tier4_opps.append((ws, opp, tier))

    tier1_opps.sort(key=lambda x: x[0], reverse=True)
    tier2_opps.sort(key=lambda x: x[0], reverse=True)
    tier3_opps.sort(key=lambda x: x[0], reverse=True)
    tier4_opps.sort(key=lambda x: x[0], reverse=True)

    # ── Immediate priorities: top 5 from Tier 1+2 (Tier 3/4 excluded) ───────
    combined_12       = sorted(tier1_opps + tier2_opps, key=lambda x: x[0], reverse=True)
    immediate_priorities = [_opp_card(o, t) for _, o, t in combined_12[:5]]

    # ── Build toward: top 3 Tier 3 opps (6–18 month horizon) ────────────────
    build_toward = [_opp_card(o, 3) for _, o, _ in tier3_opps[:3]]

    # ── Watch list: top Tier 4 opps (2–5 year horizon, track only) ──────────
    watch_list = [_opp_card(o, 4) for _, o, _ in tier4_opps[:6]]

    # ── Months to Tier 3 / next milestone ────────────────────────────────────
    months_to_t3 = _months_to_tier3(group_shows, has_institutional)

    if group_shows < 3:
        next_milestone = (
            f"Complete {3 - group_shows} more Tokyo group show(s) to reach the "
            "3-show minimum that opens Tier 3 conversations."
        )
    elif not has_solo:
        next_milestone = (
            "Secure a first solo show — a bookshop gallery exhibition (UTRECHT, Book and Sons) "
            "is the most achievable and strategically natural next step."
        )
    elif not has_institutional:
        next_milestone = (
            "Apply to a Tier 3 institutional open call (TOKAS, Youkobo, BankART1929) "
            "to establish the first institutional exhibition credit."
        )
    else:
        next_milestone = (
            "Begin preparing the artist statement and portfolio body for Tier 4 applications "
            "(Cité Internationale des Arts, Asian Cultural Council) in the 2–3 year window."
        )

    # ── Blocking gaps ─────────────────────────────────────────────────────────
    blocking_gaps = _blocking_gaps(
        group_shows, has_solo, has_institutional, has_international, has_jws
    )

    # ── Tier 3 note ───────────────────────────────────────────────────────────
    if tier3_ready < 0.30:
        t3_note = "Low — more group shows are the most direct path to improving this score."
    elif tier3_ready < 0.60:
        t3_note = "Building — group show count is the primary remaining gap for Tier 3 eligibility."
    else:
        t3_note = "Approaching — Tier 3 credibility work is within reach; institutional show is the key missing piece."

    # ── Write output ──────────────────────────────────────────────────────────
    report = {
        "_generated_at":   datetime.now(timezone.utc).isoformat(),
        "_engine_version": "2.0",

        "current_phase": "Tier 1-2 foundation building",
        "phase_note": (
            "Age 26, planning a deep-work year around 30. The next 3–4 years are for accumulation: "
            "exhibition history, publishing relationships, peer network, and body of work depth. "
            "Tier 1-2 opportunities build this foundation. Tier 4 targets are tracked now, "
            "not acted on until the foundation is solid."
        ),

        "career_evidence": {
            "confirmed_group_shows":  group_shows,
            "has_solo_show":          has_solo,
            "has_institutional_show": has_institutional,
            "has_international_show": has_international,
            "jws_membership":         has_jws,
            "publications_confirmed": 2,
        },

        "readiness_scores": {
            "tier_3_readiness":      tier3_ready,
            "tier_4_readiness":      tier4_ready,
            "tier_3_readiness_note": t3_note,
        },

        "immediate_priorities": immediate_priorities,
        "build_toward":         build_toward,
        "watch_list":           watch_list,

        "blocking_gaps":   blocking_gaps,
        "next_milestone":  next_milestone,
        "months_to_tier3": months_to_t3,

        "pipeline_summary": {
            "total_active": len(active),
            "tier_1_count": len(tier1_opps),
            "tier_2_count": len(tier2_opps),
            "tier_3_count": len(tier3_opps),
            "tier_4_count": len(tier4_opps),
        },
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("Career Strategy Report written to:", OUT_PATH)
    print()
    print(f"  Current phase          : {report['current_phase']}")
    print(f"  Confirmed group shows  : {group_shows}")
    print(f"  Solo show              : {'yes' if has_solo else 'no'}")
    print(f"  Institutional show     : {'yes' if has_institutional else 'no'}")
    print(f"  Tier 3 readiness       : {tier3_ready:.0%}")
    print(f"  Tier 4 readiness       : {tier4_ready:.0%}")
    print(f"  Months to Tier 3       : {months_to_t3}")
    print(f"  Immediate priorities   : {len(immediate_priorities)}")
    print(f"  Build toward (Tier 3)  : {len(build_toward)}")
    print(f"  Watch list  (Tier 4)   : {len(watch_list)}")
    print(f"  Blocking gaps          : {len(blocking_gaps)}")
    print()
    print(f"  Next milestone: {next_milestone}")
    print()
    if blocking_gaps:
        print("  Blocking gaps:")
        for g in blocking_gaps:
            print(f"    [{g['priority'].upper()}] {g['gap']}")


if __name__ == "__main__":
    build_career_strategy_report()