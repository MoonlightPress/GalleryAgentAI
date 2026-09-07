"""
career_strategy_engine.py

Produces a Career Readiness Report for GEGYjiji grounded in her actual
confirmed career history and the live opportunity pipeline.

Output: memory/career_strategy_report.json
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

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


def _is_group_type(etype: str) -> bool:
    """True for a genuine group show. Like _is_solo_type, this guards against the
    source disclaimer 'exhibition (group/solo not specified on source)', where
    'group' appears only inside "group/solo not specified" — an UNKNOWN type."""
    t = (etype or "").lower()
    if "not specified" in t or "group/solo" in t:
        return False
    return "group" in t


def _count_group_shows(profile: dict, ex_log: list) -> int:
    """Count *confirmed* group shows from research + exhibition log.

    Evidence over prediction (CLAUDE.md): an exhibition only counts if its
    confidence is confirmed. The "Kinoko Kingdom" profile entry, for example,
    is "mentioned in ACG bio, details unconfirmed" (no venue, no dates) and
    must not inflate the count — that's exactly the score-inflation the project
    warns against.
    """
    base = 1  # Tide from China Part1, Feb 2023 (confirmed: venue, dates, source)

    for ex in profile.get("career_history", {}).get("exhibitions", []):
        confidence = (ex.get("confidence") or "").lower()
        if (_is_group_type(ex.get("type"))
                and ex.get("title") != "Tide from China Part1"
                and confidence.startswith("confirmed")):
            base += 1

    # Exclude the hardcoded base show by title so logging it via the event
    # quick-log UI doesn't double-count it against base=1.
    logged = sum(
        1 for e in ex_log
        if e.get("type") == "group"
        and e.get("outcome") in ("shown", "completed", None, "")
        and (e.get("title") or "").strip() != "Tide from China Part1"
        and _confirmed(e)
    )
    return base + logged


def _confirmed(e: dict) -> bool:
    """A logged show counts as evidence unless explicitly unconfirmed
    (e.g. confidence 'mentioned') — evidence over prediction."""
    return (e.get("confidence") or "").lower() not in ("mentioned", "unconfirmed")


def _is_solo_type(etype: str) -> bool:
    """True for a genuine solo show. Guards against the source disclaimer
    'exhibition (group/solo not specified on source)', where 'solo' appears only
    as part of "not specified" — that is an UNKNOWN type, not a solo credit."""
    t = (etype or "").lower()
    if "not specified" in t or "group/solo" in t:
        return False
    return "solo" in t


def _has_solo_show(profile: dict, ex_log: list) -> bool:
    for ex in profile.get("career_history", {}).get("exhibitions", []):
        if _is_solo_type(ex.get("type")):
            return True
    for e in ex_log:
        if (e.get("type") == "solo"
                and e.get("outcome") in ("shown", "completed", None, "")
                and _confirmed(e)):
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
        venue_match = any(kw in (e.get("venue") or "").lower() for kw in KWS)
        type_match = e.get("type") == "institutional"
        if ((venue_match or type_match)
                and e.get("outcome") in ("shown", "completed", None, "")
                and _confirmed(e)):
            return True
    return False


def _has_international_show(profile: dict, ex_log: list) -> bool:
    # International = a showing outside her two home countries (China, Japan).
    INTL = ("london", "paris", "new york", "berlin", "sydney", "amsterdam",
            "brussels", "zurich", "seoul", "hong kong")
    HOME = ("china", "japan", "tokyo", "beijing", "shanghai", "guangzhou",
            "hangzhou", "shenzhen", "nanjing", "tianjin", "taizhou", "changsha")
    for ex in profile.get("career_history", {}).get("exhibitions", []):
        venue = (ex.get("venue") or "").lower()
        title = (ex.get("title") or "").lower()
        city  = (ex.get("city") or "").lower()
        if any(kw in venue for kw in INTL) or any(kw in city for kw in INTL):
            return True
        if any(kw in title for kw in ("international", "global")):
            return True
        # A confirmed show in a city that is neither Chinese nor Japanese counts.
        if city and not any(h in city for h in HOME):
            return True
    for e in ex_log:
        country = (e.get("country") or "").lower()
        if country and country not in ("japan", "china"):
            if e.get("outcome") in ("shown", "completed", None, "") and _confirmed(e):
                return True
    return False


def _has_jws(profile: dict) -> bool:
    history = str(profile.get("career_history", {})).lower()
    return "japan watercolor society" in history or "日本水彩" in history


# ── Next-tier levers (for an artist who already has solo + institutional +
#    international credits — graduating PAST foundation-building) ──────────────

_NONE_VALUES = ("", "none", "none confirmed", "none found", "n/a", "unknown")


def _has_representation(profile: dict) -> bool:
    """Gallery representation on record. The profile records a free-text field
    (e.g. 'none confirmed') — treat any non-empty, non-'none' value as a real
    representation credit."""
    rep = profile.get("career_history", {}).get("gallery_representation")
    return isinstance(rep, str) and rep.strip().lower() not in _NONE_VALUES


def _has_residency(profile: dict, ex_log: list) -> bool:
    res = profile.get("career_history", {}).get("residencies")
    if isinstance(res, list) and res:
        return True
    if isinstance(res, str) and res.strip().lower() not in _NONE_VALUES:
        return True
    for e in ex_log:
        if (e.get("type") in ("residency", "residency_show")
                and e.get("outcome") in ("shown", "completed", None, "")
                and _confirmed(e)):
            return True
    return False


def _has_grant(profile: dict) -> bool:
    awards = profile.get("career_history", {}).get("awards")
    if isinstance(awards, list) and awards:
        return True
    return isinstance(awards, str) and awards.strip().lower() not in _NONE_VALUES


def _count_solo_shows(profile: dict, ex_log: list) -> int:
    n = 0
    for ex in profile.get("career_history", {}).get("exhibitions", []):
        if _is_solo_type(ex.get("type")):
            n += 1
    for e in ex_log:
        if (e.get("type") == "solo"
                and e.get("outcome") in ("shown", "completed", None, "")
                and _confirmed(e)):
            n += 1
    return n


def _count_publications(profile: dict) -> int:
    pubs = profile.get("career_history", {}).get("publications")
    return len(pubs) if isinstance(pubs, list) else 0


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


def _tier4_readiness(group_shows: int, has_solo: bool, has_institutional: bool,
                     has_international: bool = False, has_jws: bool = False) -> float:
    """
    Score 0.0–1.0 for Tier 4 readiness (prestige: international societies,
    residencies, fellowships). Deliberately demands MORE than Tier 3 —
    international reach and society standing — so completing the Tier-3 basics
    (group shows + institutional + solo) tops out around 0.60, not 100%.
    """
    score = 0.0
    if group_shows >= 5:
        score += 0.15
    elif group_shows >= 3:
        score += 0.10
    if has_institutional:
        score += 0.25
    if has_solo:
        score += 0.20
    if has_international:
        score += 0.25   # international reach is the Tier-4 differentiator
    if has_jws:
        score += 0.15   # society membership / standing
    return round(min(score, 1.0), 2)


# Threshold at which a tier's readiness is treated as "crossed" — she's
# operating at that level, not just building toward it.
_LEVEL_THRESHOLD = 0.60

# Single source of truth for the tier/level vocabulary. These names MUST match
# the i18n tier strings the frontend renders (`pp.tier.{n}.label`,
# `sf.cr.tier{n}`) so a level badge and a tier label never name the same tier
# differently. (Was "Networking & Foundation" here vs "Networking" in i18n.)
_LEVEL_LABELS = {
    1: "Ambient Visibility",
    2: "Networking",
    3: "Credibility",
    4: "Prestige",
}


def _career_level(tier3_ready: float, tier4_ready: float, *,
                  foundation_complete: bool,
                  has_representation: bool, has_residency: bool,
                  has_grant: bool, has_jws: bool) -> dict:
    """Her current operating level, framed as earned ground rather than a wall
    of gaps. The level is gated on ATTAINMENT, not on a readiness score: she
    only rises to a tier once she actually holds a credit at that tier.

    - Tier 3 (Credibility) is reached once the foundation is complete — she has
      solo, institutional, and multiple group-show credits on record.
    - Tier 4 (Prestige) is reached only once an actual Tier-4 credit exists:
      gallery representation, a residency, a grant/award, or watercolor-society
      membership. Readiness alone (however high) does NOT promote her to Tier 4;
      that's the difference between being *ready for* the leap and having *made*
      it. With none of those credits today she sits at Tier 3, not Tier 4.

    `progress_to_next` stays driven by tier-4 readiness — how close she is to the
    next level — so the badge says "Tier 3, 85% of the way" rather than
    overshooting to Tier 4 on readiness alone."""
    has_tier4_credit = has_representation or has_residency or has_grant or has_jws
    if not foundation_complete:
        # Still building the Tier-3 foundation: how far toward it (tier-3 ready).
        current, progress = 2, min(1.0, tier3_ready / _LEVEL_THRESHOLD)
    elif not has_tier4_credit:
        # Foundation built (Tier 3, Credibility), but no Tier-4 credit yet.
        # Progress toward Tier 4 is tier-4 readiness itself.
        current, progress = 3, min(1.0, tier4_ready)
    else:
        current, progress = 4, 1.0
    nxt = current + 1 if current < 4 else None
    return {
        "current":        current,
        "current_label":  _LEVEL_LABELS[current],
        "next":           nxt,
        "next_label":     _LEVEL_LABELS.get(nxt) if nxt else None,
        "progress_to_next": round(progress, 2),
    }


def _months_to_tier3(group_shows: int, has_institutional: bool, *,
                     foundation_complete: bool = False,
                     tier3_ready: float = 0.0) -> Optional[int]:
    """Rough months-to-Tier-3 estimate, used only while she is still building
    toward Tier 3. Once the foundation is complete (or Tier-3 readiness has
    crossed the threshold) she is already ESTABLISHED in Tier 3 — there is no
    countdown to a tier she's in, so return None and let the UI hide it. (This
    kills the "~3 months to Tier 3" contradiction on a tier she's established.)"""
    if foundation_complete or tier3_ready >= _LEVEL_THRESHOLD:
        return None
    if has_institutional:
        return 3
    if group_shows >= 3:
        return 6
    return 12


# Arts Council Tokyo's emerging-artist grant is the one hard, near date in the
# whole ladder. A near date has to *sound* near — read flat, it lands in the same
# register as a 2027 call and the one moment of urgency on the page is lost
# (prose review, 2026-09-04). Recomputed on every regeneration so it can't stale
# into claiming urgency after the date has gone by.
_ACT_GRANT_CLOSE = datetime(2026, 9, 24, tzinfo=timezone.utc)


def _act_grant_urgency() -> dict:
    """How close the Arts Council Tokyo deadline is, in prose. Empty when past."""
    days = (_ACT_GRANT_CLOSE - datetime.now(timezone.utc)).days
    if days < 0:
        return {}                # closed — the copy simply won't mention it
    if days <= 7:
        return {"en": "closes this week, on September 24", "zh": "这周就截止了，9月24日",
                "en_short": "closes this week", "zh_short": "这周就截止了"}
    if days <= 31:
        return {"en": f"closes on September 24, {days} days from today",
                "zh": f"9月24日截止，从今天算起还有 {days} 天",
                "en_short": f"has {days} days left", "zh_short": f"只剩 {days} 天"}
    return {"en": "closes on September 24", "zh": "9月24日截止",
            "en_short": "closes September 24", "zh_short": "9月24日截止"}


def _first_publication(profile: dict) -> tuple:
    """(title, year, years_since) for her first published book, from the profile.

    Both the title and the year used to be typed into the copy below, along with
    "five years and a great deal of work later" — correct in 2026 and wrong every
    year after, which is the same staleness that once had a 2023 group show
    described as her latest news. All three are derived now.
    """
    pubs = (profile.get("career_history", {}) or {}).get("publications") or []
    for pub in pubs:
        m = re.search(r"(19|20)\d{2}", str(pub.get("date", "")))
        if m:
            year = int(m.group(0))
            title = str(pub.get("title", "")).split(" (")[0].strip()
            return title or "the first book", year, max(0, datetime.now(timezone.utc).year - year)
    return "", 0, 0


def _next_tier_levers(solo_shows: int, has_international: bool, has_jws: bool,
                      has_representation: bool, has_residency: bool,
                      has_grant: bool, publications: int,
                      first_pub: tuple = ("Colour Diary", 2021, 0)) -> list:
    """The graduated ladder for an artist who already has solo + institutional
    + international credits (Scott, 2026-06-25). She is past foundation-building;
    these are the real next levers, every one framed as a door to walk through —
    never a deficit. Each carries a _zh sibling so the page never leaks English.

    Order is the strategic priority Scott named: representation first (the biggest
    structural step), then venue quality, art fairs, residencies, grants, a
    deeper international record, critical press, and a second publication."""
    levers = []

    if not has_representation:
        levers.append({
            "gap_id":   "gallery_representation",
            "gap":      "The next door: a gallery that takes you on",
            "gap_zh":   "下一扇门：一家愿意长期代理你的画廊",
            # De-triplication pass (prose review, 2026-09-04): the detail tells
            # the story and names the doors; the dates, fees and eligibility live
            # once, in `targets`; the action is one thing she can do this week.
            "detail":   (
                "You already have solos and museum-group credits — what changes the picture "
                "most now is a gallery that sells on your behalf, places you in fairs, and "
                "builds a collector base over time. Tokyo galleries rarely run submission "
                "boxes; the usual path is going to a show, meeting the gallerist, being "
                "introduced. The doors below are the ones closest to your work: one gallery "
                "you can simply write to, and two open calls that have put a winner straight "
                "into a solo show."
            ),
            "detail_zh": (
                "你已经有个展和美术馆联展的履历——接下来最能改变格局的，是一家替你销售、"
                "带你去博览会、慢慢替你积累藏家的画廊。东京的画廊很少设投稿入口，"
                "通常的路是先去看展、认识画廊主、被人引荐。"
                "下面几扇门是山楂找到的、离你的作品最近的：一家可以直接写信的画廊，"
                "两个曾把获奖者直接送进个展的公开征集。"
            ),
            "priority": "high",
            "action":   "One thing this week is enough: a short note to Gallery Kogure (works@gallerykogure.com) with three diary paintings attached.",
            "action_zh": "这周做一件事就够：给 Gallery Kogure 写一封短信（works@gallerykogure.com），附三张日记系列。",
            "targets": [
                {
                    "name": "Gallery Kogure",
                    "why": "The closest roster match found — works-on-paper and illustration-to-fine-art artists close to your format.",
                    "why_zh": "目前找到与你风格最契合的画廊——展出的纸上作品与插画转纯艺术创作者，与你的形式相近。",
                    "url": "https://gallerykogure.com/artists/",
                    "window": "Cold approach any time — works@gallerykogure.com",
                    "window_zh": "随时可主动联系——works@gallerykogure.com",
                },
                {
                    "name": "biscuit gallery — \"grid next\"",
                    "why": "A free open call that has already placed a winner straight into a solo show.",
                    "why_zh": "一个免费的公开征集，曾有获奖者因此直接获得个展机会。",
                    "url": "https://biscuitgallery.com/gridnext-2026/",
                    "window": "Usually opens each December",
                    "window_zh": "通常每年12月开放",
                },
                {
                    "name": "HB Gallery — FILE competition",
                    "why": "No eligibility restriction; five grand-prize winners each get a one-week solo.",
                    "why_zh": "无资格限制；五位大奖得主可各获得一周个展。",
                    "url": "https://hbgallery.com/compe.html",
                    "window": "Open now",
                    "window_zh": "现正征集中",
                },
                {
                    "name": "Kaikai Kiki / Hidari Zingaro",
                    "why": "Their current show scouted 12 artists via Instagram — proof a following like yours can itself be the door in.",
                    "why_zh": "他们目前的展览有12位艺术家是通过 Instagram 被发掘的——证明像你这样的关注度本身也能成为一扇门。",
                    "url": "https://gallery-kaikaikiki.com/",
                    "window": "No application route found — worth watching, not applying to",
                    "window_zh": "未找到申请入口——值得关注，暂不必主动申请",
                },
            ],
        })

    # No longer gated on solo_shows < 3 — she crossed that count (3 solos) while
    # all three remained pay-to-exhibit rental venues (Moon Gallery, Galerie LE
    # MONDE, 77ART), so the raw count was measuring the wrong thing and hid the
    # lever exactly when it became most relevant (Fable research, 2026-09-04).
    # Quality-of-venue is an ongoing dimension like art_fairs/critical_press
    # below, not a one-time unlock — so it stays unconditional post-foundation.
    levers.append({
        "gap_id":   "solo_venue_quality",
        "gap":      "Stepping up to larger, more established solo venues",
        "gap_zh":   "迈向更大、更具分量的个展场地",
        # The opener honors the three solos she made happen before it names the
        # rental point (prose review, 2026-09-04) — the money and the dates now
        # live once, in `targets`.
        "detail":   (
            "Three solos, each one you made happen yourself. The next step is a venue that "
            "pays for the show instead of the other way round — Tokyo Arts and Space runs "
            "two programs built for exactly this, open to any nationality, and Kyoto Art "
            "Center's Co-program is the best-funded solo call found anywhere in Japan."
        ),
        "detail_zh": (
            "三场个展，每一场都是你自己做出来的。下一步，是让场地反过来为展览付钱——"
            "东京都现代美术空间（Tokyo Arts and Space）的两个项目正为此而设，不限国籍；"
            "京都艺术中心的 Co-program 则是目前在日本找到的、经费最充裕的个展征集。"
        ),
        "priority": "high",
        "action":   "Put one solo proposal on paper this month — the show you'd make with a real production budget — so it's ready when the next TOKAS call opens.",
        "action_zh": "这个月先把一份个展提案写下来——如果有一笔真正的制作经费，你想做的那个展——等 TOKAS 下一轮征集开放时就能直接投。",
        "targets": [
            {
                "name": "TOKAS-Emerging",
                "why": "¥150,000 production grant plus install/PR/catalogue, nationality-open — two 2026 picks were Chinese artists.",
                "why_zh": "15万日元制作经费，含布展/宣传/画册，不限国籍——2026年入选者中有两位是中国艺术家。",
                "url": "https://www.tokyoartsandspace.jp/en/archive/exhibition/2026/20260404-7535.html",
                "window": "Next call expected June–July 2027",
                "window_zh": "下一轮征集预计在2027年6-7月",
            },
            {
                "name": "TOKAS OPEN SITE",
                "why": "¥400,000 grant, no age limit, solo proposals accepted.",
                "why_zh": "40万日元经费，无年龄限制，接受个展提案。",
                "url": "https://www.tokyoartsandspace.jp/application/schedule.html",
                "window": "Next call expected Feb–Mar 2027",
                "window_zh": "下一轮征集预计在2027年2-3月",
            },
            {
                "name": "Kyoto Art Center Co-program",
                "why": "The best-funded open call found — up to ¥1,000,000 for a solo, plus 6 weeks' studio.",
                "why_zh": "目前找到经费最充裕的公开征集——最高可为个展提供100万日元经费，外加6周工作室使用。",
                "url": "https://www.kac.or.jp/open_call/",
                "window": "Expect a call each October",
                "window_zh": "预计每年10月开放征集",
            },
            {
                "name": "Shibuya Hikarie 8/CUBE",
                "why": "Committee-screened with station-direct footfall — a real step up from a rental space.",
                "why_zh": "由委员会评审，位于车站直连的高人流地段——比租赁场地更进一步。",
                "url": "https://www.hikarie8.com/cube/",
                "window": "Next call planned for autumn 2026",
                "window_zh": "下一轮征集预计在2026年秋季",
            },
        ],
    })

    levers.append({
        "gap_id":   "art_fairs",
        "gap":      "Art fairs open collector access",
        "gap_zh":   "艺术博览会，打开通向藏家的通道",
        # Open doors first, the gallery-applied fairs last and as a future rather
        # than a closed door (prose review, 2026-09-04).
        "detail":   (
            "There is a real artist-direct ladder into the fairs, and three of its rungs are "
            "open to you: SICF at Spiral in Aoyama, whose Grand Prize is a solo show in the "
            "Atrium; Independent Tokyo, where gallerists judge the floor in person; and Art "
            "Fair Beppu, free to enter with travel subsidised. As for Art Fair Tokyo and "
            "Tokyo Gendai — those are the ones a gallery applies to on your behalf. After "
            "representation, they come on their own."
        ),
        "detail_zh": (
            "通往博览会的路上，确实有一条艺术家可以自己走的阶梯，其中三级现在就对你开着："
            "青山 Spiral 的 SICF，大奖得主可在中庭办个展；Independent Tokyo，"
            "由画廊主亲自到场评审；以及免费参展、还补贴差旅的 Art Fair Beppu。"
            "至于 Art Fair Tokyo 和 Tokyo Gendai，那是画廊替你申请的——等代理之后，自然会到。"
        ),
        "priority": "medium",
        "action":   "Pick out ten paintings that would hang together as a booth — that selection is what every one of these calls asks for first.",
        "action_zh": "挑出十张能挂成一个展位的画——这几个征集，第一步问的都是这个。",
        "targets": [
            {
                "name": "SICF (Spiral Independent Creators Festival)",
                "why": "Grand Prize is a solo show in Spiral's Atrium plus ¥500,000 — the fair goal and the solo-venue goal in one.",
                "why_zh": "大奖得主可在 Spiral 中庭举办个展，并获得50万日元制作经费——同时达成博览会与个展两个目标。",
                "url": "https://www.spiral.co.jp/artcat/sicf",
                "window": "Call usually opens ~November",
                "window_zh": "征集通常约每年11月开放",
            },
            {
                "name": "Independent Tokyo",
                "why": "20–30 gallerists judge the floor directly — the recognized way galleries scout new artists.",
                "why_zh": "现场有20-30位画廊主直接担任评审——是画廊发掘新艺术家的公认渠道。",
                "url": "https://www.tagboat.com/artevent/independenttokyo2026/index.php",
                "window": "Call usually opens ~October",
                "window_zh": "征集通常约每年10月开放",
            },
            {
                "name": "Art Fair Beppu",
                "why": "Curated by HAPS, free entry, travel and accommodation subsidised.",
                "why_zh": "由 HAPS 策划，免费参展，并补贴差旅与住宿费用。",
                "url": "https://haps-kyoto.com/art-fair-beppu-spring-2027/",
                "window": "Call usually opens in summer",
                "window_zh": "征集通常在夏季开放",
            },
        ],
    })

    if not has_residency:
        levers.append({
            "gap_id":   "residency",
            "gap":      "A residency is a genuine open door on your CV",
            "gap_zh":   "驻地项目，是履历上一扇真正待开的门",
            # "尚未拥有的credit" was deficit framing with an untranslated English
            # word inside a Chinese sentence; the near date now sounds near and
            # the action is a verb, not 留意 (prose review, 2026-09-04).
            "detail":   (
                "A residency is one of the few things you haven't tried yet — and the "
                "best-fitting ones are right here in Japan. Tokyo Arts and Space runs two, "
                "both open to any Japan resident whatever their passport: months of studio "
                "time in Sumida, or a fully-funded stay in a partner city. Fukuoka Asian Art "
                "Museum runs a third, built for artists working across Asia."
            ),
            "detail_zh": (
                "驻地是少数你还没试过的事——而最适合你的几个，就在日本。"
                "东京都现代美术空间（Tokyo Arts and Space）有两个，只要住在日本就能申请、不问国籍："
                "在墨田连着几个月的工作室时间，或者全额资助去一座合作城市住上一阵。"
                "福冈亚洲美术馆还有第三个，专为在亚洲各地往返创作的人而设。"
            ),
            "priority": "high",
            "action":   "TOKAS's residency call should open within the next couple of weeks — the door most worth watching this autumn. Have your portfolio and a three-sentence residency idea ready, so you can apply the day it opens.",
            "action_zh": "TOKAS 的驻地征集大概就在这两周开放——这是今年秋天最值得盯住的一扇门。先把作品集和三句话的驻地计划准备好，开放当天就能投。",
            "targets": [
                {
                    "name": "TOKAS Local Emerging Creator Residency",
                    "why": "60–90 days at TOKAS Sumida; Japan-resident, nationality unrestricted — your exact profile.",
                    "why_zh": "在 TOKAS 墨田驻留60-90天；只要在日本居住即可申请、不限国籍——正符合你的情况。",
                    "url": "https://www.tokyoartsandspace.jp/application/index.html",
                    "window": "Next call expected mid-September 2026",
                    "window_zh": "下一轮征集预计在2026年9月中旬开放",
                },
                {
                    "name": "TOKAS Exchange Residency",
                    "why": "Fully-funded ~3 months in a partner city — Taipei, Seoul, Helsinki and others.",
                    "why_zh": "全额资助，约3个月，驻留于台北、首尔、赫尔辛基等合作城市。",
                    "url": "https://www.tokyoartsandspace.jp/application/index.html",
                    "window": "Same call, expected mid-September 2026",
                    "window_zh": "与上者同批征集，预计2026年9月中旬开放",
                },
                {
                    "name": "Fukuoka Asian Art Museum Residency",
                    "why": "Built specifically for artists working across Asia — a Tokyo/Beijing practice is exactly its audience.",
                    "why_zh": "专为在亚洲各地创作的艺术家而设——你往返东京与北京的创作实践，正是它面向的对象。",
                    "url": "https://faam.city.fukuoka.lg.jp/residence/requirement/",
                    "window": "Next call expected late Dec 2026 – late Jan 2027",
                    "window_zh": "下一轮征集预计在2026年12月底至2027年1月底",
                },
            ],
        })

    if not has_grant:
        _act = _act_grant_urgency()
        _act_line_en = (
            f"Arts Council Tokyo's grant for emerging artists, which {_act['en']}, and "
            if _act else ""
        )
        _act_line_zh = (
            f"东京艺术委员会（Arts Council Tokyo）面向新锐艺术家的扶持金，{_act['zh']}；"
            if _act else ""
        )
        _act_action_en = (
            f"The Arts Council Tokyo form {_act['en_short']} — fill it in this week, and "
            "send Greenshields the same images afterwards; theirs has no deadline at all."
            if _act else
            "Send the Elizabeth Greenshields Foundation ten diary paintings this week — "
            "their application is open all year and takes an afternoon."
        )
        _act_action_zh = (
            f"东京艺术委员会的申请{_act['zh_short']}——这周把表格填掉；"
            "同一批图片随后寄给 Greenshields 就行，那边根本没有截止日期。"
            if _act else
            "这周把十张日记寄给 Elizabeth Greenshields 基金会——他们常年开放，一个下午就能投完。"
        )
        levers.append({
            "gap_id":   "grant",
            "gap":      "Grants and fellowships add institutional standing",
            "gap_zh":   "奖助与奖学金，为你增添机构层面的分量",
            # The two most *seen* facts — the Mainland China track she qualifies
            # for by citizenship, and Greenshields explicitly taking students —
            # were buried in a six-grant list. Surfaced; the katakana-in-Chinese
            # name and 创业期 ("startup capital") are gone (prose review).
            "detail":   (
                "Your record can carry a grant application now. "
                f"{'Two doors are' if _act_line_en else 'One door is'} open this minute: "
                f"{_act_line_en}Canada's Elizabeth Greenshields Foundation, which funds "
                "representational painters at exactly your stage, students included, any time "
                "of year. Three more open in October — Nomura, Asahi Shimbun, and the Asian "
                "Cultural Council, whose Mainland China track you qualify for by citizenship, "
                "Tokyo address and all."
            ),
            "detail_zh": (
                "你的履历现在已经撑得起申请奖助了。"
                f"{'两扇门' if _act_line_zh else '有一扇门'}此刻开着："
                f"{_act_line_zh}加拿大的 Elizabeth Greenshields 基金会专门资助你这个阶段的具象绘画者，"
                "学生也可以，随时可投。10月还有三扇会开——野村财团、朝日新闻文化财团，"
                "以及亚洲文化协会：凭你的中国国籍就能走它的中国大陆通道，住在东京也没关系。"
            ),
            "priority": "high",
            "action":    _act_action_en,
            "action_zh": _act_action_zh,
            "targets": [
                {
                    "name": "Arts Council Tokyo Startup Grant",
                    "why": "Up to ¥300,000, no nationality clause — funds exactly the kind of activity you're already doing.",
                    "why_zh": "最高30万日元，无国籍限制——资助的正是你目前已经在做的事。",
                    "url": "https://www.artscouncil-tokyo.jp/grants/startup-grant-program/",
                    "window": "Closes September 24, 2026",
                    "window_zh": "截止于2026年9月24日",
                },
                {
                    "name": "Elizabeth Greenshields Foundation",
                    "why": "Built for exactly your stage — representational painting, no citizenship or residency requirement, students explicitly eligible.",
                    "why_zh": "几乎是为你现阶段量身定制——具象绘画，无国籍或居住地要求，明确接受学生申请。",
                    "url": "https://www.elizabethgreenshieldsfoundation.org/",
                    "window": "Rolling — apply any time",
                    "window_zh": "常年滚动接受申请",
                },
                {
                    "name": "Nomura Foundation",
                    "why": "Up to ¥1,000,000 for international-exchange art projects — a China–Japan show fits its own criteria exactly.",
                    "why_zh": "最高100万日元，资助国际艺术文化交流项目——一场中日交流展正符合其评选标准。",
                    "url": "https://www.nomurafoundation.or.jp/culture/art_ov01.html",
                    "window": "Opens October 1, 2026",
                    "window_zh": "2026年10月1日开放",
                },
                {
                    "name": "Asian Cultural Council",
                    "why": "You qualify for its Mainland China track by citizenship, regardless of living in Tokyo.",
                    "why_zh": "凭中国国籍即可申请其中国大陆项目，无论目前是否居住在东京。",
                    "url": "https://www.asianculturalcouncil.org/grant-opportunities",
                    "window": "Opens October 1, 2026",
                    "window_zh": "2026年10月1日开放",
                },
                {
                    "name": "Holbein Scholarship",
                    "why": "A materials grant from a watercolor manufacturer — a near-perfect medium match and a recognized CV line.",
                    "why_zh": "来自水彩画材制造商的画材资助——与你的创作媒介高度契合，也是被认可的履历一笔。",
                    "url": "https://www.holbein.co.jp/scholarship.html",
                    "window": "Expect the next round around April–July 2027",
                    "window_zh": "下一轮预计在2027年4-7月",
                },
            ],
        })

    if not has_international:
        levers.append({
            "gap_id":   "international_record",
            "gap":      "Turning one international showing into a pattern",
            "gap_zh":   "把一次国际展出，发展成一种常态",
            "detail":   (
                "Your record now reaches beyond China and Japan — the next move is to make that "
                "international presence a pattern rather than a single entry: a European gallery, "
                "the international art-book circuit, a recurring overseas showing."
            ),
            "detail_zh": (
                "你的履历如今已延伸至中国与日本之外——下一步是把这份国际存在，"
                "从单次记录发展成一种常态：欧洲的画廊、国际艺术书的流通网络、可持续的海外展出。"
            ),
            "priority": "medium",
            "action":   "Build on your first overseas showing — look toward European galleries and the international art-book circuit.",
            "action_zh": "在首次海外展出的基础上更进一步——把目光投向欧洲画廊与国际艺术书的流通网络。",
        })

    levers.append({
        "gap_id":   "critical_press",
        "gap":      "Moving from features to being written about",
        "gap_zh":   "从作品被展示，迈向作品被书写",
        # Each fact once: the story here, the specifics in `targets` (prose review).
        "detail":   (
            "Your work has been shown and reproduced — what comes next is writing that "
            "engages with the practice itself. The strongest thing you have to offer an "
            "editor is the diary: five years of it, one painting a day, a city seen at the "
            "same hour again and again. That is a story, not a portfolio. Three places below "
            "publish exactly that kind of story."
        ),
        "detail_zh": (
            "你的作品已经被展示、被转载——接下来是让文字真正走进创作本身。"
            "你手上最能打动编辑的东西就是那本日记：五年，一天一张，"
            "同一座城市在同一个时刻被看了一遍又一遍。这是一个故事，而不是一份作品集。"
            "下面三个地方，登的正是这样的故事。"
        ),
        "priority": "low",
        "action":   "Write the diary down as one paragraph — what it is, when it began, why every day — and send it to Colossal (submissions@thisiscolossal.com) with six images.",
        "action_zh": "把这本日记写成一段话——它是什么、从什么时候开始、为什么每天都画——连同六张图片寄给 Colossal（submissions@thisiscolossal.com）。",
        "targets": [
            {
                "name": "Colossal",
                "why": "Runs an active watercolor tag and takes open submissions — a years-long daily Tokyo watercolor diary is exactly its kind of story.",
                "why_zh": "设有活跃的水彩标签，并接受主动投稿——一份持续数年的东京水彩日记，正是它偏爱的故事类型。",
                "url": "https://www.thisiscolossal.com/submissions/",
                "window": "Open now — pitch any time",
                "window_zh": "常年开放投稿",
            },
            {
                "name": "Tokyo Weekender",
                "why": "Regularly covers painters from abroad showing in Tokyo — pitch three or four weeks before your next solo opens.",
                "why_zh": "常报道旅日画家在东京的展览——下一场个展开幕前3-4周投稿正合适。",
                "url": "https://www.tokyoweekender.com/contact-us/",
                "window": "Pitch 3–4 weeks before a show",
                "window_zh": "建议在展览开幕前3-4周投稿",
            },
            {
                "name": "The Choice (イラストレーション magazine)",
                "why": "The Japanese illustration industry's own quarterly competition — watercolor is explicitly among the accepted media, and a selection is a recognized CV line.",
                "why_zh": "日本插画界自身的季度大赛——水彩明确属于其接受的创作媒介，入选会成为被认可的履历一笔。",
                "url": "https://illustration-mag.jp/choice",
                "window": "Quarterly — watch for the next entry window",
                "window_zh": "每季一次——留意下一次征集窗口",
            },
        ],
    })

    if publications < 2:
        # Defensive: she has 2 on record; only fires if the record thins.
        _need = 2 - publications
        levers.append({
            "gap_id":   "second_publication",
            "gap":      "A second publication builds the written record",
            "gap_zh":   "第二本出版物，夯实你的出版履历",
            "detail":   (
                f"{_need} more publication rounds out the publishing half of your CV beyond your "
                "first solo collection."
            ),
            "detail_zh": (
                f"再有 {_need} 本出版物，就能让你在首部个人作品集之外，补全履历中出版的那一半。"
            ),
            "priority": "low",
            "action":   "Plan the next book or zine beyond Colour Diary.",
            "action_zh": "在 Colour Diary 之后，规划下一本书或zine。",
        })
    else:
        _pt, _py, _yrs = first_pub
        # Spelled out in English prose; Chinese takes the digit, as the rest of
        # the page does.
        _words = ("no", "a", "two", "three", "four", "five", "six", "seven",
                  "eight", "nine", "ten")
        _pn = ("a year" if _yrs == 1
               else f"{_words[_yrs] if _yrs < len(_words) else _yrs} years")
        _pz = f"{_yrs} 年过去" if _yrs != 1 else "一年过去"
        levers.append({
            "gap_id":   "monograph",
            "gap":      f"A new book or monograph beyond {_pt} ({_py})",
            "gap_zh":   f"在 {_pt}（{_py}）之后，出一本新书或个人画册",
            "detail":   (
                f"{_pt} ({_py}) was your first solo collection — {_pn} and a great deal "
                "of work later, a new book or monograph would gather the recent practice and give "
                "galleries, fairs, and press a single object to engage with."
            ),
            "detail_zh": (
                f"{_pt}（{_py}）是你的首部个人作品集——{_pz}，作品已积累许多，"
                "一本新书或个人画册能把近期的创作汇聚起来，"
                "也为画廊、博览会与媒体提供一个可以共同关注的整体。"
            ),
            "priority": "low",
            "action":   f"Gather the work made since {_pt} toward a second book or monograph.",
            "action_zh": f"把 {_pt} 之后的创作汇整起来，朝第二本书或个人画册推进。",
        })

    return levers


def _blocking_gaps(group_shows: int, has_solo: bool, has_institutional: bool,
                   has_international: bool, has_jws: bool,
                   *, solo_shows: int = 0, has_representation: bool = False,
                   has_residency: bool = False, has_grant: bool = False,
                   publications: int = 0,
                   first_pub: tuple = ("Colour Diary", 2021, 0)) -> list:
    gaps = []

    # Framed as opportunities ahead, not deficits. The whole readiness surface
    # reads "here's where you are, and here's what's in reach" — never "here's
    # what you lack." (Scott, 2026-06-25: positive reinforcement throughout.)
    #
    # Each string carries its own _zh sibling, generated with the SAME live
    # counts. The UI prefers the _zh, so it never has to match a whole baked
    # English sentence — which silently leaked English the moment a count changed.
    #
    # Two ladders, picked by where she actually is:
    #   • Foundation ladder (below) fires only while she is still BUILDING the
    #     first group/solo/institutional/international credits.
    #   • Once those foundations exist, the graduated next-tier ladder
    #     (_next_tier_levers) takes over: representation, bigger solo venues,
    #     art fairs, residencies, grants, a deeper international record, critical
    #     press, a second publication. (Scott, 2026-06-25: her real record shows
    #     solo + museum + London credits — the "needs a first solo" framing is
    #     false and must never reach her.)
    foundation_complete = (
        group_shows >= 3 and has_solo and has_institutional
    )
    if foundation_complete:
        return _next_tier_levers(
            solo_shows or (1 if has_solo else 0),
            has_international, has_jws, has_representation,
            has_residency, has_grant, publications, first_pub,
        )

    if group_shows < 3:
        needed = 3 - group_shows
        s = "s" if group_shows != 1 else ""
        gaps.append({
            "gap_id":   "group_shows",
            "gap":      "A few more group shows opens Tier 3",
            "gap_zh":   "再来几场联展，就能开启第三级",
            "detail":   (
                f"You have {group_shows} confirmed group show{s} — a real start. "
                f"{needed} more brings you to the 3 that open Tier 3 conversations with "
                f"Tokyo galleries. This is your fastest move up."
            ),
            "detail_zh": (
                f"你已经有 {group_shows} 场已确认的联展——这是实打实的起点。"
                f"再来 {needed} 场，就凑齐了与东京画廊洽谈第三级所需的 3 场。"
                "这是你当下最快的进阶之路。"
            ),
            "priority": "high",
            # 3331 Arts Chiyoda closed March 2023 — dropped (Fable research, 2026-09-04).
            # No verified open replacement found yet; don't backfill with an unresearched name.
            "action":   "Apply to open calls at Design Festa Gallery, Gallery IYN",
            "action_zh": "向 Design Festa Gallery、Gallery IYN 的公开征集投递",
        })

    if not has_solo:
        gaps.append({
            "gap_id":   "solo_show",
            "gap":      "A first solo show is within reach",
            "gap_zh":   "首次个展，已经触手可及",
            "detail":   (
                "A first solo show is a real leap in credibility for Tier 3 calls — and it's "
                "an achievable next step. Even a small bookshop-gallery or café solo counts."
            ),
            "detail_zh": (
                "首次个展会让你在第三级征集中的公信力实现真正的飞跃——而且这是可以达成的下一步。"
                "哪怕是书店画廊或咖啡馆里的小型个展，也算数。"
            ),
            "priority": "medium",
            "action":   "Target bookshop gallery solo show: UTRECHT, Book and Sons, flotsam books, 日記屋 月日",
            "action_zh": "争取书店画廊个展：UTRECHT、Book and Sons、flotsam books、日記屋 月日",
        })

    if not has_institutional:
        gaps.append({
            "gap_id":   "institutional_show",
            "gap":      "An institutional show is the next door to open",
            "gap_zh":   "机构展览，是下一扇待你推开的门",
            "detail":   (
                "An arts-council or public-gallery show is the next credibility door to open. "
                "Tokyo Arts and Space's open calls (TOKAS-Emerging, OPEN SITE) are realistic "
                "near-term entries for where you are now."
            ),
            "detail_zh": (
                "在艺术委员会或公立画廊办展，是下一扇值得推开的公信力之门。"
                "东京都现代美术空间（Tokyo Arts and Space）的公开征集"
                "（TOKAS-Emerging、OPEN SITE）都是以你现在的位置切实可及的近期入口。"
            ),
            "priority": "medium",
            # Youkobo's residency program is discontinued and BankART Station/KAIKO
            # closed March 2025 — both dropped (Fable research, 2026-09-04).
            "action":   "Watch TOKAS-Emerging and OPEN SITE open calls at tokyoartsandspace.jp",
            "action_zh": "关注 tokyoartsandspace.jp 上 TOKAS-Emerging 与 OPEN SITE 的公开征集",
        })

    if not has_international:
        gaps.append({
            "gap_id":   "international_show",
            "gap":      "International reach, whenever you want it",
            "gap_zh":   "国际舞台，随时为你敞开",
            "detail":   (
                "Your shows so far are in Japan and China — a strong base. Adding an international "
                "showing, even a remote open call, opens residencies and fellowships when you want them."
            ),
            "detail_zh": (
                "你目前的展览集中在日本与中国——这是坚实的根基。"
                "再添一次国际展出，哪怕是一次远程公开征集，就能在你想要的时候打开驻地与奖助的大门。"
            ),
            "priority": "low",
            "action":   "Consider global watercolor open calls or table at Offprint Paris / London Art Book Fair",
            "action_zh": "考虑国际水彩公开征集，或在 Offprint Paris／London Art Book Fair 设展位",
        })

    if not has_jws:
        gaps.append({
            "gap_id":   "jws",
            "gap":      "The Japan Watercolor Society is open to you",
            "gap_zh":   "日本水彩画会，正向你敞开",
            "detail":   (
                "The Japan Watercolor Society annual exhibition is a Tier 3 credibility marker for "
                "watercolor artists in Japan — and non-members can enter the juried calls. "
                "An open door whenever you're ready."
            ),
            "detail_zh": (
                "日本水彩画会的年度展览，是日本水彩艺术家第三级公信力的标志——"
                "而且非会员也可以参加评审征集。这扇门，随时为你敞开。"
            ),
            "priority": "low",
            "action":   "Research Japan Watercolor Society (公益社団法人日本水彩画会) annual entry process",
            "action_zh": "了解日本水彩画会（公益社団法人日本水彩画会）的年度参展流程",
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
    # Next-tier signals (for an artist past foundation-building):
    solo_shows        = _count_solo_shows(profile, ex_log)
    has_representation = _has_representation(profile)
    has_residency     = _has_residency(profile, ex_log)
    has_grant         = _has_grant(profile)
    publications      = _count_publications(profile)

    # She is past foundation-building once the first group/solo/institutional
    # credits exist — at that point the advice graduates to the next-tier ladder
    # (representation, bigger solo venues, fairs, residencies, grants, …).
    foundation_complete = group_shows >= 3 and has_solo and has_institutional

    # ── Readiness scores ─────────────────────────────────────────────────────
    tier3_ready = _tier3_readiness(group_shows, has_solo, has_institutional, has_international)
    tier4_ready = _tier4_readiness(group_shows, has_solo, has_institutional,
                                   has_international, has_jws)

    # ── Classify and tier-weight all active opportunities ────────────────────
    REJECT_BUCKETS = {"reject", "low_priority"}
    active = [
        o for o in opps
        if o.get("exclusive_primary_bucket") not in REJECT_BUCKETS
        and o.get("status") != "permanently_closed"
        and o.get("recommendation_visibility") != "hidden"
        and not o.get("deadline_past")
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
    months_to_t3 = _months_to_tier3(
        group_shows, has_institutional,
        foundation_complete=foundation_complete, tier3_ready=tier3_ready,
    )

    if not foundation_complete and group_shows < 3:
        _n = 3 - group_shows
        next_milestone = (
            f"Complete {_n} more Tokyo group show(s) to reach the "
            "3-show minimum that opens Tier 3 conversations."
        )
        next_milestone_zh = (
            f"再完成 {_n} 场东京联展，达到开启第三级洽谈所需的 3 场最低门槛。"
        )
    elif not foundation_complete and not has_solo:
        next_milestone = (
            "Secure a first solo show — a bookshop gallery exhibition (UTRECHT, Book and Sons) "
            "is the most achievable and strategically natural next step."
        )
        next_milestone_zh = (
            "争取一次个展——书店画廊展览（UTRECHT、Book and Sons）是最可行、也最顺理成章的下一步。"
        )
    elif not foundation_complete and not has_institutional:
        next_milestone = (
            "Apply to a Tier 3 institutional open call (TOKAS, Youkobo, BankART1929) "
            "to establish the first institutional exhibition credit."
        )
        next_milestone_zh = (
            "投递一次第三级机构公开征集（TOKAS、Youkobo、BankART1929），建立首个机构展览履历。"
        )
    elif not has_representation:
        # Foundation is complete (solo + institutional + multiple group shows).
        # The biggest structural next step is gallery representation.
        next_milestone = (
            "Build toward gallery representation — a gallery that sells on your behalf, places "
            "you in art fairs, and grows a collector base. With solo and museum-group credits "
            "already on record, this is the highest-leverage next step."
        )
        next_milestone_zh = (
            "朝画廊代理迈进——一家替你销售、带你进入博览会、并培育藏家群体的画廊。"
            "你已有个展与美术馆联展的履历，这是当下杠杆最高的下一步。"
        )
    elif not has_residency:
        next_milestone = (
            "Pursue a residency — institutional weight that suits a Tokyo–Beijing cross-cultural "
            "practice and is one of the few credits not yet on your record."
        )
        next_milestone_zh = (
            "争取一次驻地——它具备机构分量，契合你往返东京与北京的跨文化创作，"
            "也是你履历上尚未拥有的少数credit之一。"
        )
    else:
        next_milestone = (
            "Deepen the record you've built: a new book or monograph, critical press, and a "
            "more sustained international presence beyond your first overseas showing."
        )
        next_milestone_zh = (
            "在你已建立的履历上更进一步：一本新书或个人画册、评论性的关注，"
            "以及在首次海外展出之外更持续的国际存在。"
        )

    # ── Blocking gaps ─────────────────────────────────────────────────────────
    blocking_gaps = _blocking_gaps(
        group_shows, has_solo, has_institutional, has_international, has_jws,
        solo_shows=solo_shows, has_representation=has_representation,
        has_residency=has_residency, has_grant=has_grant,
        publications=publications,
        first_pub=_first_publication(profile),
    )

    # ── Level + single next unlock (Saffron hybrid reframe) ───────────────────
    # The hybrid framing: show ONE thing to cross next, not a wall of gaps. The
    # next unlock is the highest-priority blocking gap; when every gap is closed
    # she's at the ceiling, so the "unlock" becomes a positive advanced-state
    # line instead of going blank.
    level = _career_level(
        tier3_ready, tier4_ready,
        foundation_complete=foundation_complete,
        has_representation=has_representation, has_residency=has_residency,
        has_grant=has_grant, has_jws=has_jws,
    )
    if blocking_gaps:
        next_unlock = dict(blocking_gaps[0])
    else:
        next_unlock = {
            "gap_id":   "advanced",
            "gap":      "Deepening a record that already stands on its own",
            "gap_zh":   "在已然成立的履历上，继续向纵深推进",
            "detail":   (
                "Representation, residency, and grant credits are in place. The work now is "
                "depth and reach: a new book or monograph, critical press, and a sustained "
                "international presence."
            ),
            "detail_zh": (
                "代理、驻地与奖助的履历都已具备。接下来的功课是纵深与广度："
                "一本新书或个人画册、评论性的关注，以及持续的国际存在。"
            ),
            "priority": "low",
            "action":   "Gather recent work toward a second book; cultivate critical press; sustain the international record.",
            "action_zh": "把近期作品汇整成第二本书；结识评论性的媒体；让国际履历持续延展。",
        }
    level["next_unlock"] = next_unlock

    # ── Tier 3 note ───────────────────────────────────────────────────────────
    # Once the foundation is complete the Tier-3 credibility question is settled —
    # she HAS the institutional + solo credits — so the note must not keep asking
    # for "more group shows."
    if foundation_complete:
        t3_note = (
            "Established — solo, institutional, and international credits are on record. "
            "The next levers are representation, residencies, grants, and press, not more "
            "group shows."
        )
    elif tier3_ready < 0.30:
        t3_note = "Low — more group shows are the most direct path to improving this score."
    elif tier3_ready < 0.60:
        t3_note = "Building — group show count is the primary remaining gap for Tier 3 eligibility."
    else:
        t3_note = "Approaching — Tier 3 credibility work is within reach; institutional show is the key missing piece."

    # ── Write output ──────────────────────────────────────────────────────────
    if foundation_complete:
        current_phase = "Tier 3 established — building toward representation & prestige"
        phase_note = (
            "An active multi-country exhibiting artist: solo shows, museum-group exhibitions, "
            "and an international showing are on record, alongside a first solo publication and "
            "an established, growing Instagram following. The foundation is built. The next levers are structural — gallery "
            "representation, stronger solo venues, art fairs, residencies, grants, critical press, "
            "and a second book — not more entry-level group shows."
        )
        phase_note_zh = (
            "一位活跃的、跨国展出的艺术家：个展、美术馆联展与国际展出均已在册，"
            "另有首部个人出版物与稳固且持续增长的 Instagram 受众。根基已成。"
            "接下来的杠杆是结构性的——画廊代理、更高规格的个展场地、艺术博览会、驻地、奖助、"
            "评论性媒体，以及第二本书——而非更多入门级的联展。"
        )
    else:
        current_phase = "Tier 1-2 foundation building"
        phase_note = (
            "Still building the Tier 1-2 foundation: exhibition history, publishing "
            "relationships, peer network, and depth of work. Tier 1-2 opportunities build "
            "this base; Tier 4 prestige targets are tracked now and pursued once the "
            "foundation — solo, institutional, and several group-show credits — is in place."
        )
        phase_note_zh = (
            "仍在构筑第一、二级的根基：展览履历、出版关系、同侪网络与作品的深度。"
            "第一、二级的机会构筑这一基础；第四级的目标现在持续追踪，"
            "待根基——个展、机构展与若干联展履历——扎实后再行动。"
        )

    report = {
        "_generated_at":   datetime.now(timezone.utc).isoformat(),
        "_engine_version": "2.1",

        "current_phase": current_phase,
        "phase_note": phase_note,
        "phase_note_zh": phase_note_zh,

        "career_evidence": {
            "confirmed_group_shows":  group_shows,
            "solo_shows":             solo_shows,
            "has_solo_show":          has_solo,
            "has_institutional_show": has_institutional,
            "has_international_show": has_international,
            "has_representation":     has_representation,
            "has_residency":          has_residency,
            "has_grant":              has_grant,
            "jws_membership":         has_jws,
            "publications_confirmed": publications,
        },

        "readiness_scores": {
            "tier_3_readiness":      tier3_ready,
            "tier_4_readiness":      tier4_ready,
            "tier_3_readiness_note": t3_note,
        },

        "level": level,

        "immediate_priorities": immediate_priorities,
        "build_toward":         build_toward,
        "watch_list":           watch_list,

        "blocking_gaps":   blocking_gaps,
        "next_milestone":  next_milestone,
        "next_milestone_zh": next_milestone_zh,
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