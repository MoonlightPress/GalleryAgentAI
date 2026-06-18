
import json
import os
import re
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Date-aware deadline helpers
# ---------------------------------------------------------------------------
_TODAY = date.today()

_MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

# Categories that are ONGOING VENUES — deadline field is not a submission deadline.
# All other categories (including empty/unknown) are treated as time-limited calls.
_ONGOING_VENUE_CATS = frozenset({
    "bookstore_gallery",     # ongoing bookshop / gallery space
    "bookstore_event",       # bookshop event programme (relationship target)
    "cafe_gallery",          # rotating café exhibitions
    "zine_shop_consignment", # consignment relationship — no deadline
    "zine_print",            # zine/print shops and publishers (as used here = shops)
    "market_event",          # recurring market events (BONUS TRACK etc.)
})


def _parse_deadline_date(deadline_str: str):
    """Return the latest parseable date in deadline_str, or None.
    Returns the latest date so we don't prematurely expire multi-window deadlines."""
    s = str(deadline_str or "")
    # Strip ordinal suffixes: "1st", "2nd", "3rd", "14th" → digits only
    s = re.sub(r'(\d+)(st|nd|rd|th)\b', r'\1', s, flags=re.IGNORECASE)
    found = []
    # ISO: 2026-02-11 or 2026/2/11 — use \d{1,2} to avoid greedy alternation bug
    for m in re.finditer(r'(20\d{2})[-/](\d{1,2})[-/](\d{1,2})', s):
        try:
            found.append(date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            pass
    # Japanese: 2026年3月9日
    for m in re.finditer(r'(20\d{2})年(\d{1,2})月(\d{1,2})日', s):
        try:
            found.append(date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            pass
    # English day-month-year: 6 November 2025
    for m in re.finditer(r'(\d{1,2})\s+([A-Za-z]+)\s+(20\d{2})', s):
        mon = _MONTH_MAP.get(m.group(2).lower())
        if mon:
            try:
                found.append(date(int(m.group(3)), mon, int(m.group(1))))
            except ValueError:
                pass
    # English month-day-year: March 18, 2026 / June 30, 2026
    for m in re.finditer(r'([A-Za-z]+)\s+(\d{1,2}),?\s+(20\d{2})', s):
        mon = _MONTH_MAP.get(m.group(1).lower())
        if mon:
            try:
                found.append(date(int(m.group(3)), mon, int(m.group(2))))
            except ValueError:
                pass
    # Return the latest date found — don't expire until the last deadline has passed
    return max(found) if found else None

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/exclusive_strategy_buckets.json"
SUPPRESSION_PATH = "memory/ibm_suppression.json"

BUCKET_ORDER = [
    "immediate_best_moves",
    "publication_editorial",
    "competitions_awards",
    "publication_targets",
    "japan_book_ecosystem",
    "stretch_targets",
    "relationship_builders",
    "research_needed",
    "low_priority",
    "reject",
]

LABELS = {
    "immediate_best_moves":  "Immediate Best Moves",
    "publication_editorial": "Publications & Editorial",
    "competitions_awards":   "Competitions & Awards",
    "publication_targets":   "Publication Targets",
    "japan_book_ecosystem":  "Japan Book / Zine Ecosystem",
    "stretch_targets":       "Stretch Targets",
    "relationship_builders": "Relationship Builders",
    "research_needed":       "Needs Research",
    "low_priority":          "Low Priority",
    "reject":                "Reject / Hide",
}


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def text_blob(opp):
    parts = []
    for key in [
        "title",
        "name",
        "organization",
        "category",
        "category_label",
        "opportunity_type",
        "relationship_note",
        "one_sentence",
        "why_this_fits_short",
    ]:
        if opp.get(key):
            parts.append(str(opp[key]))

    for key in ["tags", "visual_fit_hits", "fit_keyword_hits"]:
        for item in opp.get(key, []) or []:
            parts.append(str(item))

    return " ".join(parts).lower()


def num(value):
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def has(text, terms):
    return any(t in text for t in terms)


_PASSED_MARKERS = ("passed", "closed", "cycle closed", "deadline was", "deadline passed")
_RECURRING_MARKERS = ("annual", "recurring", "watch", "2027", "2028", "next cycle")


def _deadline_confirmed_passed(opp):
    deadline = str(opp.get("deadline") or "").lower()
    cycle_note = str(opp.get("cycle_note") or "").lower()
    return any(m in deadline or m in cycle_note for m in _PASSED_MARKERS)


def _is_recurring(opp):
    deadline = str(opp.get("deadline") or "").lower()
    cycle_note = str(opp.get("cycle_note") or "").lower()
    return any(m in deadline or m in cycle_note for m in _RECURRING_MARKERS)


def _call_deadline_is_past(opp) -> bool:
    """True if this entry has a parsed deadline that has already passed.
    Ongoing venue categories are exempt — their 'deadline' field is not a call deadline."""
    cat = opp.get("category") or ""
    if cat in _ONGOING_VENUE_CATS:
        return False  # ongoing venue relationship — deadline is irrelevant
    dl_date = _parse_deadline_date(str(opp.get("deadline") or ""))
    return dl_date is not None and dl_date < _TODAY


# ---------------------------------------------------------------------------
# Source-quality knowledge base + corpus-learned portal detection
# ---------------------------------------------------------------------------
_SQ_PATH = Path(__file__).parent.parent / "memory" / "source_quality.json"
try:
    _SQ = json.loads(_SQ_PATH.read_text(encoding="utf-8"))
except Exception:
    _SQ = {}
_AGG_STATIC     = tuple(_SQ.get("aggregator_domains", []))
_PLATFORM_HOSTS = tuple(_SQ.get("platform_hosts", []))
_VANITY_MILLS   = tuple(m.lower() for m in _SQ.get("vanity_mills", []))

_LEARNED_PORTALS: set = set()


def _domain(url) -> str:
    if isinstance(url, list):
        url = url[0] if url else ""
    m = re.match(r"https?://(?:www\.)?([^/]+)", str(url or ""))
    return m.group(1).lower() if m else ""


def set_corpus(opps):
    """Learn portal domains from the corpus: a domain used as official_website
    by 3+ DISTINCT organizations is a listing portal, not a venue. Builder
    platforms are exempt (each subdomain/account is one organizer)."""
    global _LEARNED_PORTALS
    by_domain: dict = {}
    for o in opps:
        d = _domain(o.get("official_website"))
        if not d or any(p in d for p in _PLATFORM_HOSTS):
            continue
        org = (o.get("organization") or o.get("title") or o.get("name") or "").strip().lower()
        by_domain.setdefault(d, set()).add(org)
    _LEARNED_PORTALS = {d for d, orgs in by_domain.items() if len(orgs) >= 3}


def _is_aggregator_url(url) -> bool:
    if isinstance(url, list):
        url = url[0] if url else ""
    u = str(url or "").lower()
    if not u:
        return False
    d = _domain(u)
    if any(p in d for p in _PLATFORM_HOSTS):
        return False
    return any(a in u for a in _AGG_STATIC) or d in _LEARNED_PORTALS


def _has_real_venue_url(opp) -> bool:
    """True if at least one action URL is a real venue (or no URLs at all —
    relationship venues without sites are handled by other rules).
    Per-entry escape hatch: official_site_confirmed=True means a human
    verified the URL is organizer-owned even though the domain looks like a
    portal (e.g. Art Olympia's listing on artkoubo.jp — the portal is run by
    the same foundation that runs the competition)."""
    if opp.get("official_site_confirmed"):
        return True
    urls = [opp.get("official_website") or "", opp.get("submission_page") or ""]
    flat = [u[0] if isinstance(u, list) and u else u for u in urls]
    flat = [str(u or "") for u in flat]
    if not any(flat):
        return True
    return any(u and not _is_aggregator_url(u) for u in flat)


def _is_vanity_mill(opp) -> bool:
    blob = " ".join(str(opp.get(k) or "") for k in
                    ("title", "name", "organization", "one_sentence")).lower()
    return any(m in blob for m in _VANITY_MILLS)


# Artist facts for eligibility (from artist_master_profile.json when present)
def _artist_age() -> int:
    try:
        prof = json.loads((Path(__file__).parent.parent / "memory" /
                           "artist_master_profile.json").read_text(encoding="utf-8"))
        age = prof.get("age") or prof.get("identity", {}).get("age")
        if age:
            return int(age)
    except Exception:
        pass
    return 26  # confirmed age as of 2026 (CLAUDE.md career framework)


_ARTIST_AGE = _artist_age()

_STUDENT_ONLY_RE = re.compile(
    r"学生限定|在学生のみ|大学生限定|在校生限定|现役学生|仅限学生|"
    r"students?\s+only|must\s+be\s+(?:currently\s+)?enrolled", re.I)
_AGE_CAP_RE = re.compile(r"(?:under|U)\s*(\d{2})\b|(\d{2})\s*歳以下|(\d{2})\s*岁以下", re.I)
_NATIONALITY_RE = re.compile(r"日本国籍(?:を有する|に限る|のみ)|japanese\s+nationals?\s+only", re.I)


def _eligibility_conflict(opp) -> str:
    """Return '' or the conflict kind. A hired assistant never shows her a
    call she cannot enter — but SHE IS A STUDENT (confirmed 2026-06-13), so
    student-only calls are eligible and get marked (student_call flag) rather
    than filtered; student fee tiers are an advantage. Note: '学生部門' (a
    student *division*) is not exclusive either way."""
    blob = " ".join(str(opp.get(k) or "") for k in
                    ("title", "name", "one_sentence", "requirements",
                     "eligibility", "why_this_fits_short"))
    if _STUDENT_ONLY_RE.search(blob):
        opp["student_call"] = True   # mark for her, never hide
    if _NATIONALITY_RE.search(blob):
        return "nationality"
    for m in _AGE_CAP_RE.finditer(blob):
        cap = next((g for g in m.groups() if g), None)
        if cap and int(cap) < _ARTIST_AGE:
            return f"age_cap_{cap}"
    return ""


def choose_bucket(opp):
    text = text_blob(opp)
    title = str(opp.get("title") or opp.get("name") or "").lower()

    score = num(opp.get("overall_score"))
    dscore = num(opp.get("differentiated_score"))
    visual = num(opp.get("visual_fit_score"))

    if opp.get("recommendation_visibility") == "hidden":
        return "reject"

    # Data-level bucket override: an entry may explicitly pin its bucket via the
    # `bucket_override` field. The engine honors it deterministically, so a
    # curated routing decision lives in the data yet stays 100% reproducible on a
    # fresh pipeline run. This is the sanctioned alternative to silently editing
    # `exclusive_primary_bucket` (which the engine would otherwise overwrite).
    override = opp.get("bucket_override")
    if override in BUCKET_ORDER:
        return override

    # Grants are never filtered by photography or deadline in the usual way.
    # Only verified/strong_partial grants with high scores → stretch_targets.
    # Discovered but unverified grants → research_needed (don't flood stretch_targets).
    if opp.get("category") in ("grant", "global_grant_fellowship") or opp.get("opportunity_type") == "grant":
        if opp.get("verification_bucket") == "stretch_targets":
            return "stretch_targets"
        v_status = opp.get("verification_status", "")
        if score >= 8.0 and v_status in ("verified", "strong_partial"):
            return "stretch_targets"
        return "research_needed"

    if opp.get("verification_bucket") == "reject":
        return "reject"

    # Data-level bucket override — lets individual records pin to a bucket
    # without requiring engine changes (e.g. invitation-only publishers → stretch_targets)
    if opp.get("verification_bucket") == "stretch_targets":
        return "stretch_targets"

    # Photography: visual similarity is not professional fit for this watercolor painter.
    # Pure photography-native opportunities are rejected instead of being routed to
    # research_needed; artist-book/print opportunities should use non-photo categories.
    if opp.get("native_medium") == "photography":
        return "reject"

    # Photography category gate — catches photo calls even when native_medium is
    # missing or marked "mixed". Only keep if explicitly painting/watercolor friendly.
    if opp.get("category") in ("photo_open_call", "global_photobook"):
        accepted = str(opp.get("accepted_media") or "").lower()
        if "watercolor" not in accepted and "painting" not in accepted:
            return "reject"

    # Generic index listing pages and non-art calls: never surface to artist.
    # open_call_index = raw listing-page URLs scraped as link text, not real opportunities.
    # Film / audio / podcast calls are not relevant to a visual painting practice.
    if opp.get("category") == "open_call_index":
        return "reject"
    _title_lc = (opp.get("title") or opp.get("name") or "").lower()
    if any(t in _title_lc for t in ("film festival", "podcast", "audio work required")):
        return "reject"

    # Publications & Editorial: magazine illustration calls, book cover submissions,
    # editorial commissions, Japanese art magazines. Never competition-style deadlines.
    _EDITORIAL_CATS = {
        "editorial_illustration", "magazine_call", "book_cover_call",
        "publication_editorial", "editorial_commission",
    }
    if opp.get("category") in _EDITORIAL_CATS:
        return "publication_editorial"

    # Competitions & Awards: illustration prizes, watercolor competitions,
    # emerging artist awards. Low score → research_needed (not worth time if score < 6).
    _COMPETITION_CATS = {
        "competition_award", "illustration_prize",
        "watercolor_competition", "emerging_artist_award",
    }
    if opp.get("category") in _COMPETITION_CATS:
        return "competitions_awards" if score >= 6.0 else "research_needed"

    # Keyword fallback for entries classified generic but clearly editorial or competition
    _editorial_kw = {"editorial illustration", "magazine illustration", "book cover call",
                     "editorial commission", "雑誌掲載", "挿絵募集", "约稿", "编辑插画"}
    _competition_kw = {"illustration prize", "watercolor prize", "illustration award",
                       "art prize", "コンクール", "大賞", "新人賞", "比赛", "大赛", "奖项"}
    if has(text, _editorial_kw):
        return "publication_editorial"
    if has(text, _competition_kw) and score >= 5.5:
        return "competitions_awards"

    # Press targets: publications to pitch for features. Never filtered by deadline.
    # Route to relationship_builders (they are relationship plays, not one-off applications).
    if opp.get("category") == "press_target" or opp.get("opportunity_type") == "press_target":
        if opp.get("exclusive_primary_bucket") == "press_target":
            return "relationship_builders"
        if score >= 7.0:
            return "relationship_builders"
        return "research_needed"

    # Confirmed passed deadline (text markers): recurring → stretch_targets, one-off → reject
    if _deadline_confirmed_passed(opp):
        return "stretch_targets" if _is_recurring(opp) else "reject"

    # Date-aware deadline check for call-type categories.
    # Past deadline = closed call; route to research_needed (may recur, not actionable now).
    # Ongoing venues (bookstores, cafes, zine shops) are exempt via _DEADLINE_SENSITIVE_CATS.
    if _call_deadline_is_past(opp):
        return "research_needed"

    # Only use dscore for low_priority check when it is actually set (>0)
    if score <= 4 or (dscore > 0 and dscore <= 4):
        return "low_priority"

    if has(title, ["facebook", "instagram", "pinterest", "tiktok", "continue reading"]):
        return "reject"

    # ── Source-quality guards (truth pass 2026-06-13, hardened) ──────────────
    # 1. Aggregator-as-venue: listing portals are sources, never venues. The
    #    domain list lives in memory/source_quality.json (data, editable) and
    #    is EXTENDED automatically: any domain serving as official_website for
    #    3+ distinct organizations in this corpus is a portal by definition
    #    (a real venue's site belongs to one organization). Site-builder
    #    platforms (jimdo/wix/note/artcall…) are exempt — there, each account
    #    IS one organizer's own site.
    if not _has_real_venue_url(opp):
        return "research_needed"

    # 2. Vanity-mill guard: pay-to-enter online-gallery competition factories
    #    (TERAVARNA etc.) have negligible career value at Tier 1-2 — a hired
    #    assistant would not show these. Tracked, never actioned.
    if _is_vanity_mill(opp):
        return "research_needed"

    # 3. Eligibility guard: never show her a call she cannot enter.
    #    (Also sets student_call=True on student-only calls — she IS a
    #    student, so those are eligible and surfaced with a mark.)
    _elig = _eligibility_conflict(opp)
    if _elig:
        opp["eligibility_conflict"] = _elig
        return "reject" if _elig == "nationality" else "research_needed"

    # Tier 4 hard guard (CLAUDE.md rule): prestige targets NEVER reach
    # immediate_best_moves, regardless of score or verification strength.
    # The structured career_tier field is authoritative and must be checked
    # BEFORE any rule that can return immediate_best_moves — the name list
    # further down is only a fallback for entries that lack the field.
    if opp.get("career_tier") == 4 or str(opp.get("tier", "")) == "4":
        return "stretch_targets"

    # Tier 4 — Prestige Targets: always stretch_targets, never immediate_best_moves.
    # These are future goals for the deep-work year at ~30, not current actions.
    tier_4_terms = [
        "royal watercolour society",
        "american watercolor society",
        "cité internationale des arts",
        "cite internationale des arts",
        "asian cultural council",
        "printed matter art book fairs",
        "center for book arts",
        "offprint",
        "aperture",
        "mack",
        # torch press: invitation-only label; no submissions; Tier 4 aspirational target
        "torch press",
    ]

    # Tier 1 — Ambient Visibility: zine/bookshop ecosystem, art book fairs.
    # Also includes currently-open watercolor open calls (NWWS etc.) that are
    # actionable right now. Route to immediate or japan_book_ecosystem.
    tier_1_terms = [
        "tokyo art book fair",
        "mount zine",
        "utrecht",
        "book and sons",
        "flotsam",
        "b&b shimokitazawa",
        "bookandbeer",
        "shashasha",
        "zine fest",
        "zine fair",
        "fugensha",
        "akaaka",
        # New Tokyo relationship targets
        "sunny boy books",
        "clouds art",
        "shimokitazawa arts",
        # Recurring Tokyo zine fairs
        "zinefes",
        "zineフェス",
        "zine fest tokyo",
        # Currently-open international watercolor calls (always immediate when verified + open)
        "northwest watercolor society",
        "cspwc",
        "canadian society of painters",
    ]

    # High-score verified global watercolor open calls get immediate_best_moves
    # even when the city is not Tokyo (they are still medium-perfect and actionable).
    # This handles nwws.org, cspwc.ca, and similar juried watercolor societies.
    if (
        opp.get("category") == "global_watercolor_open_call"
        and opp.get("native_medium") == "painting"
        and opp.get("verification_status") in ("verified", "strong_partial")
        and score >= 7.0
    ):
        return "immediate_best_moves"

    # Tier 1-2 publication / artist-book terms
    publication_terms = [
        "artist book",
        "printed matter",
        "publication",
        "small press",
        "self publish",
        "zine",
    ]

    # Tier 2 — Networking: artist-run spaces and relationship venues
    relationship_terms = [
        "cafe",
        "bookstore",
        "shimokitazawa",
        "bonus track",
        "gallery wall",
        "community",
        "artist-run",
    ]

    # Major commercial art fairs (gallery-represented, not artist-table/booth events).
    # Rule: fair_popup + international scope → stretch_targets + score capped to 6.0 by caller.
    # These require gallery backing or institutional standing the artist doesn't yet have.
    commercial_art_fair_terms = [
        "art sg", "art singapore",
        "art vancouver",
        "tokyo gendai",
        "art fair tokyo",      # gallery-represented fair; not artist booth
        "art basel", "frieze",
        "art miami", "art paris",
        "tefaf",
    ]
    if has(text, commercial_art_fair_terms) or (
        opp.get("category") == "fair_popup"
        and str(opp.get("country") or "Japan") not in ("Japan", "")
    ):
        return "stretch_targets"

    # Stale deadline guard: deadline year ≤ 2023 → research_needed (not reject — may recur).
    # Note: no \b — Japanese text like "2021年" breaks word-boundary assertions.
    deadline_str = str(opp.get("deadline") or "")
    years = re.findall(r'(20\d{2})', deadline_str)
    if years and max(int(y) for y in years) <= 2023:
        return "research_needed"

    # Confirmed watercolor-medium Tokyo events with high score → immediate_best_moves.
    # Prevents native painting opportunities from being misrouted to research_needed.
    if (
        opp.get("native_medium") == "painting"
        and str(opp.get("city") or "").lower() in ("tokyo", "")
        and score >= 7.5
        and opp.get("verification_status") in ("verified", "strong_partial")
    ):
        return "immediate_best_moves"

    # Tier 4 check is first — prestige targets never reach immediate_best_moves
    if has(text, tier_4_terms):
        return "stretch_targets"

    # Tier 1 ambient visibility — immediate or japan book ecosystem
    if has(text, tier_1_terms):
        if visual >= 3 or score >= 7.5:
            return "immediate_best_moves"
        return "japan_book_ecosystem"

    # High visual fit + publication angle → immediate
    if visual >= 5 and has(text, publication_terms):
        return "immediate_best_moves"

    # Tier 1-2 publication targets
    if has(text, publication_terms):
        return "publication_targets"

    # Tier 2 relationship / networking venues — Japan/unlocated only.
    # Non-Japan galleries and spaces can't be relationship targets for a Tokyo artist.
    if has(text, relationship_terms):
        country = str(opp.get("country") or "").strip()
        if country in ("", "Japan"):
            return "relationship_builders"
        # International venue with relationship-ish terms → research_needed
        return "research_needed"

    if opp.get("verification_bucket") in {"research_needed", None}:
        return "research_needed"

    if score >= 8 and visual >= 1:
        return "immediate_best_moves"

    return "research_needed"


def compact(opp):
    return {
        "title": opp.get("title") or opp.get("name") or "Unknown",
        "score": opp.get("overall_score"),
        "differentiated_score": opp.get("differentiated_score"),
        "visual_fit_score": opp.get("visual_fit_score"),
        "verification_bucket": opp.get("verification_bucket", ""),
        "verification_score": opp.get("verification_score", ""),
        "why": opp.get("why_this_fits_short") or opp.get("one_sentence") or "",
        "source": (
            opp.get("source_url")
            or opp.get("official_website")
            or opp.get("source_link")
            or opp.get("submission_page")
            or ""
        ),
        "visual_hits": opp.get("visual_fit_hits", []) or [],
        "opportunity_type": opp.get("opportunity_type", "open_call"),
        "action_type": opp.get("action_type", "apply"),
        "relationship_note": opp.get("relationship_note", ""),
        "draft_introduction_ja": opp.get("draft_introduction_ja", ""),
    }


def load_suppression():
    data = load_json(SUPPRESSION_PATH, {})
    return set(data.get("suppressed", {}).keys())


def main():
    opps = load_json(OPP_PATH, [])
    suppressed = load_suppression()
    set_corpus(opps)  # learn portal domains from this corpus before bucketing

    buckets = {key: [] for key in BUCKET_ORDER}

    for opp in opps:
        title = (opp.get("title") or opp.get("name") or "").strip().lower()
        org = str(opp.get("organization") or "").strip().lower()
        key = f"{title}::{org}"
        if key in suppressed:
            opp["exclusive_primary_bucket"] = "reject"
            buckets["reject"].append(compact(opp))
            continue

        bucket = choose_bucket(opp)
        opp["exclusive_primary_bucket"] = bucket

        # Score cap: international commercial art fairs should not score > 6.0
        # (they are not actionable for an emerging artist without gallery representation)
        if bucket == "stretch_targets" and opp.get("category") == "fair_popup":
            country = str(opp.get("country") or "Japan")
            if country not in ("Japan", ""):
                opp["overall_score"] = min(float(opp.get("overall_score") or 0), 6.0)

        buckets.setdefault(bucket, []).append(compact(opp))

    for key in buckets:
        buckets[key].sort(
            key=lambda x: float(x.get("differentiated_score", x.get("score", 0)) or 0),
            reverse=True,
        )

    save_json(OPP_PATH, opps)
    save_json(OUT_PATH, buckets)

    print("Built exclusive strategic buckets:")
    for key in BUCKET_ORDER:
        print(f"{LABELS[key]}: {len(buckets.get(key, []))}")


if __name__ == "__main__":
    main()
