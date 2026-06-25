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

_LEVEL_LABELS = {
    1: "Ambient Visibility",
    2: "Networking & Foundation",
    3: "Credibility",
    4: "Prestige",
}


def _career_level(tier3_ready: float, tier4_ready: float) -> dict:
    """Her current operating level, framed as earned ground rather than a wall
    of gaps. Tiers 1–2 are the foundation she has already built; she rises to
    Tier 3 once tier-3 readiness crosses the threshold, and Tier 4 after that.
    `progress` is how far she is toward the NEXT level (0–1)."""
    if tier3_ready < _LEVEL_THRESHOLD:
        current, progress = 2, min(1.0, tier3_ready / _LEVEL_THRESHOLD)
    elif tier4_ready < _LEVEL_THRESHOLD:
        current, progress = 3, min(1.0, tier4_ready / _LEVEL_THRESHOLD)
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


def _months_to_tier3(group_shows: int, has_institutional: bool) -> int:
    if has_institutional:
        return 3
    if group_shows >= 3:
        return 6
    return 12


def _next_tier_levers(solo_shows: int, has_international: bool, has_jws: bool,
                      has_representation: bool, has_residency: bool,
                      has_grant: bool, publications: int) -> list:
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
            "gap":      "Gallery representation is the next structural step",
            "gap_zh":   "画廊代理，是下一个关键的结构性跃升",
            "detail":   (
                "You already have solo shows and museum-group credits — the next structural "
                "leap is a gallery that represents you: one that sells on your behalf, places "
                "you in art fairs, and builds a collector base over time. This is the single "
                "biggest move available at your stage."
            ),
            "detail_zh": (
                "你已经拥有个展与美术馆联展的履历——下一个结构性的跃升，是找到一家代理你的画廊："
                "由它替你销售、带你进入艺术博览会、并长期为你积累藏家。"
                "这是你现阶段最重要的一步。"
            ),
            "priority": "high",
            "action":   "Build relationships with commercial galleries whose roster and program fit your work; let representation grow from shows you already have.",
            "action_zh": "与作品调性契合、项目方向相符的商业画廊建立关系；让代理关系从你已有的展览中自然生长。",
        })

    if solo_shows < 3:
        levers.append({
            "gap_id":   "solo_venue_quality",
            "gap":      "Stepping up to larger, more established solo venues",
            "gap_zh":   "迈向更大、更具分量的个展场地",
            "detail":   (
                "You have solo shows on record — the next move is the quality of the venue: "
                "graduating from artist-run and independent spaces toward established commercial "
                "galleries and institutional solo exhibitions. Each stronger solo deepens the CV "
                "more than another group show would."
            ),
            "detail_zh": (
                "你已有个展履历——下一步在于场地的分量：从艺术家自营空间与独立空间，"
                "迈向更成熟的商业画廊与机构个展。每一次更高规格的个展，"
                "对履历的加成都胜过再办一次联展。"
            ),
            "priority": "high",
            "action":   "Target established commercial galleries and institutional spaces for your next solo, building on the venues you've already shown with.",
            "action_zh": "以更成熟的商业画廊与机构空间为下一次个展的目标，在你已合作过的场地基础上更进一步。",
        })

    levers.append({
        "gap_id":   "art_fairs",
        "gap":      "Art fairs open collector access",
        "gap_zh":   "艺术博览会，打开通向藏家的通道",
        "detail":   (
            "Art fairs (Art Fair Tokyo, Tokyo Gendai and their international peers) are where "
            "collectors gather — usually reached through a representing gallery. As representation "
            "comes together, fairs become the natural place your work meets buyers at scale."
        ),
        "detail_zh": (
            "艺术博览会（Art Fair Tokyo、Tokyo Gendai 及其国际同侪）是藏家汇聚之地——"
            "通常通过代理画廊进入。随着代理关系成形，博览会会成为你的作品规模化触达藏家的天然舞台。"
        ),
        "priority": "medium",
        "action":   "Note the fairs your target galleries exhibit at; fair access typically follows representation.",
        "action_zh": "留意你的目标画廊参与的博览会；博览会的入口通常随代理关系而来。",
    })

    if not has_residency:
        levers.append({
            "gap_id":   "residency",
            "gap":      "A residency is a genuine open door on your CV",
            "gap_zh":   "驻地项目，是履历上一扇真正待开的门",
            "detail":   (
                "Residencies carry real institutional weight and are a natural fit for a "
                "cross-cultural practice between Tokyo and Beijing — and they're one of the few "
                "credits not yet on your record. A residency abroad would also deepen the "
                "international record you've already begun."
            ),
            "detail_zh": (
                "驻地项目具备真正的机构分量，也非常契合你往返东京与北京的跨文化创作——"
                "而且这是你履历上尚未拥有的少数credit之一。一次海外驻地，"
                "还能让你已经开启的国际履历更进一层。"
            ),
            "priority": "medium",
            "action":   "Research residencies that suit a watercolor/works-on-paper practice and a Tokyo–Beijing artist.",
            "action_zh": "了解适合水彩／纸上作品创作、以及往返东京—北京的艺术家的驻地项目。",
        })

    if not has_grant:
        levers.append({
            "gap_id":   "grant",
            "gap":      "Grants and fellowships add institutional standing",
            "gap_zh":   "奖助与奖学金，为你增添机构层面的分量",
            "detail":   (
                "A grant or fellowship is institutional recognition that funds the work and "
                "strengthens every future application. It's a CV dimension you haven't tapped "
                "yet — and your exhibition record now supports a competitive application."
            ),
            "detail_zh": (
                "一笔奖助或奖学金，是来自机构的认可——既为创作提供资金，也让你日后的每一份申请更有底气。"
                "这是你尚未触及的履历维度——而你如今的展览履历，已经足以支撑一份有竞争力的申请。"
            ),
            "priority": "medium",
            "action":   "Track arts grants and fellowships open to your nationality and medium; your record now reads as competitive.",
            "action_zh": "持续关注向你的国籍与媒介开放的艺术奖助与奖学金；你的履历如今已具竞争力。",
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
        "detail":   (
            "Your work has been featured — the next step is critical press: a writer or art "
            "publication engaging with the practice itself, not just reproducing the images. "
            "Criticism builds the discourse around your work that galleries and institutions read."
        ),
        "detail_zh": (
            "你的作品已被展示报道——下一步是评论性的关注：让写作者或艺术刊物真正进入你的创作本身，"
            "而不只是复制图像。评论会围绕你的作品建立起话语，而画廊与机构正是这话语的读者。"
        ),
        "priority": "low",
        "action":   "Cultivate art writers and publications who engage critically with painting and works on paper.",
        "action_zh": "结识真正以评论视角关注绘画与纸上作品的艺术写作者与刊物。",
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
        levers.append({
            "gap_id":   "monograph",
            "gap":      "A new book or monograph beyond Colour Diary (2021)",
            "gap_zh":   "在 Colour Diary（2021）之后，出一本新书或个人画册",
            "detail":   (
                "Colour Diary (2021) was your first solo collection — five years and a great deal "
                "of work later, a new book or monograph would gather the recent practice and give "
                "galleries, fairs, and press a single object to engage with."
            ),
            "detail_zh": (
                "Colour Diary（2021）是你的首部个人作品集——五年过去，作品已积累许多，"
                "一本新书或个人画册能把近期的创作汇聚起来，"
                "也为画廊、博览会与媒体提供一个可以共同关注的整体。"
            ),
            "priority": "low",
            "action":   "Gather the work made since Colour Diary toward a second book or monograph.",
            "action_zh": "把 Colour Diary 之后的创作汇整起来，朝第二本书或个人画册推进。",
        })

    return levers


def _blocking_gaps(group_shows: int, has_solo: bool, has_institutional: bool,
                   has_international: bool, has_jws: bool,
                   *, solo_shows: int = 0, has_representation: bool = False,
                   has_residency: bool = False, has_grant: bool = False,
                   publications: int = 0) -> list:
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
            has_residency, has_grant, publications,
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
            "action":   "Apply to open calls at 3331 Arts Chiyoda, Design Festa Gallery, Gallery IYN",
            "action_zh": "向 3331 Arts Chiyoda、Design Festa Gallery、Gallery IYN 的公开征集投递",
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
                "TOKAS, BankART1929, and Youkobo are realistic near-term entries for where you are now."
            ),
            "detail_zh": (
                "在艺术委员会或公立画廊办展，是下一扇值得推开的公信力之门。"
                "TOKAS、BankART1929 与 Youkobo，都是以你现在的位置切实可及的近期入口。"
            ),
            "priority": "medium",
            "action":   "Watch TOKAS open calls and Youkobo artist-in-residence programs",
            "action_zh": "关注 TOKAS 公开征集与 Youkobo 驻地项目",
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
    )

    # ── Level + single next unlock (Saffron hybrid reframe) ───────────────────
    # The hybrid framing: show ONE thing to cross next, not a wall of gaps. The
    # next unlock is the highest-priority blocking gap; when every gap is closed
    # she's at the ceiling, so the "unlock" becomes a positive advanced-state
    # line instead of going blank.
    level = _career_level(tier3_ready, tier4_ready)
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
            "~26k Instagram. The foundation is built. The next levers are structural — gallery "
            "representation, stronger solo venues, art fairs, residencies, grants, critical press, "
            "and a second book — not more entry-level group shows."
        )
        phase_note_zh = (
            "一位活跃的、跨国展出的艺术家：个展、美术馆联展与国际展出均已在册，"
            "另有首部个人出版物与约 2.6 万 Instagram 粉丝。根基已成。"
            "接下来的杠杆是结构性的——画廊代理、更高规格的个展场地、艺术博览会、驻地、奖助、"
            "评论性媒体，以及第二本书——而非更多入门级的联展。"
        )
    else:
        current_phase = "Tier 1-2 foundation building"
        phase_note = (
            "Age 26, planning a deep-work year around 30. The next 3–4 years are for accumulation: "
            "exhibition history, publishing relationships, peer network, and body of work depth. "
            "Tier 1-2 opportunities build this foundation. Tier 4 targets are tracked now, "
            "not acted on until the foundation is solid."
        )
        phase_note_zh = (
            "26 岁，计划在 30 岁前后投入一年的深耕。未来 3–4 年用于积累："
            "展览履历、出版关系、同侪网络与作品体系的深度。第一、二级的机会构筑这一根基。"
            "第四级目标现在持续追踪，待根基扎实后再行动。"
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