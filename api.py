import re
import sys
import json
import hmac
import hashlib
import os
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
from recommendation_readiness import assess_actionability

sys.stdout.reconfigure(encoding="utf-8")

app = FastAPI(title="Mochi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:5174", "http://127.0.0.1:5174",
        "http://localhost:5177", "http://127.0.0.1:5177",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Compress responses — the opportunities payload is large (multi-language email
# drafts + scoring metadata); gzip cuts the first-load transfer ~80%.
app.add_middleware(GZipMiddleware, minimum_size=600)

DATA_DIR        = Path(__file__).parent / "memory"
DEPLOY_DIR      = Path(__file__).parent / "deploy_data"
SUPPRESSED_PATH  = DATA_DIR / "suppressed_opportunities.json"
SUBMISSIONS_PATH = DATA_DIR / "submission_log.json"
CONTACTS_PATH    = DATA_DIR / "contact_memory.json"

# ── In-memory cache for the 2.7MB opportunities dataset ──────────────────────
_OPP_CACHE = None  # type: list
_OPP_CACHE_MTIME: float = 0.0


FOLLOWUP_STALE_DAYS = 30


def is_overdue_followup(last_contacted, now: datetime | None = None,
                        threshold_days: int = FOLLOWUP_STALE_DAYS) -> bool:
    """Decide whether a contact is a *stale* follow-up purely from its date.

    Pure and network-free. Returns True only when ``last_contacted`` parses to
    a real ISO datetime that is at least ``threshold_days`` old.

    A missing, empty, or unparseable ``last_contacted`` is *unknown*, not
    *stale*: we return False so a malformed date never spams the Quick Win
    slot on the strength of a parse failure alone. (Whether a contact that was
    *never* contacted should be surfaced is a separate decision made by the
    caller; this function only judges an actual elapsed-time staleness.)
    """
    if now is None:
        now = datetime.now(timezone.utc)
    if not last_contacted:
        return False
    try:
        lc_dt = datetime.fromisoformat(str(last_contacted).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        # Unparseable date → unknown, not overdue. Do not surface.
        return False
    if lc_dt.tzinfo is None:
        lc_dt = lc_dt.replace(tzinfo=timezone.utc)
    return (now - lc_dt).days >= threshold_days


def _load_suppressed() -> set:
    if SUPPRESSED_PATH.exists():
        return set(json.loads(SUPPRESSED_PATH.read_text(encoding="utf-8")))
    return set()


def _load_suppressed_categories() -> set:
    p = DATA_DIR / "learned_preferences.json"
    if p.exists():
        return set(json.loads(p.read_text(encoding="utf-8")).get("suppressed_categories", []))
    return set()


def _load_submission_states():
    """Return (pending_names, rejected_names, recent_accepted) from submission_log.json."""
    if not SUBMISSIONS_PATH.exists():
        return set(), set(), []
    try:
        subs = json.loads(SUBMISSIONS_PATH.read_text(encoding="utf-8"))
        if not isinstance(subs, list):
            subs = subs.get("submissions", [])
    except Exception:
        return set(), set(), []

    pending, rejected, accepted = set(), set(), []
    from datetime import date as _dt, timedelta as _td
    cutoff = (_dt.today() - _td(days=90)).isoformat()

    for s in subs:
        venue = (s.get("venue") or "").strip().lower()
        outcome = (s.get("outcome") or "pending").lower()
        date = s.get("date", "") or ""
        if not venue:
            continue
        if outcome in ("pending", "applied", "submitted"):
            pending.add(venue)
        elif outcome == "rejected":
            rejected.add(venue)
        elif outcome == "accepted" and date >= cutoff:
            accepted.append({"venue": s.get("venue"), "what": s.get("what"), "date": date})

    return pending, rejected, accepted

# Category → section mapping (covers all categories present in compact_opportunities)
SECTION_CATEGORIES = {
    "open_calls": {
        "fair_popup", "institutional",
        "global_open_call", "global_watercolor_open_call", "japan_watercolor_open_call",
        "japan_watercolor_institution", "zine_fair_booth", "global_art_book_fair",
        "global_book_arts", "group_publication_open_call",
    },
    "publication_editorial": {
        "editorial_illustration", "magazine_call", "book_cover_call",
        "publication_editorial", "editorial_commission",
    },
    "competitions_awards": {
        "competition_award", "illustration_prize", "watercolor_competition",
        "emerging_artist_award",
    },
    "zines_and_print": {
        "zine_print", "bookstore_gallery", "bookstore_event", "zine_shop_consignment",
        "book_publishing", "global_artist_book_platform",
    },
    "relationship_targets": {
        "gallery", "gallery_small", "cafe_gallery", "artist_space",
        "event_space", "gallery_event", "market_event",
    },
    "watch_list": {
        "residency", "global_residency", "global_grant_fellowship", "residency_beijing",
    },
}

SECTION_META = {
    "immediate_best_moves": {
        "label": "Immediate Best Moves",
        "description": "Confirmed deadline, known submission path, or verified contact. Act on these first.",
    },
    "open_calls": {
        "label": "Open Calls by Deadline",
        "description": "Spaces that run periodic open submissions. Confirm deadlines before applying.",
    },
    "publication_editorial": {
        "label": "Publications & Editorial",
        "description": "Magazine illustration calls, book cover submissions, and editorial commissions. Build print presence alongside gallery work.",
    },
    "competitions_awards": {
        "label": "Competitions & Awards",
        "description": "Watercolor competitions, illustration prizes, and emerging artist awards. Win records strengthen your CV and raise your profile.",
    },
    "zines_and_print": {
        "label": "Zines & Print",
        "description": "Bookstores, art book fairs, and zine spaces. Low-barrier entry — work circulates without a formal pitch.",
    },
    "relationship_targets": {
        "label": "Relationship Targets",
        "description": "Galleries, cafés, and spaces worth approaching. Long-game relationship building — attend openings, be present.",
    },
    "watch_list": {
        "label": "Watch List",
        "description": "Residencies, institutions, and items needing more research before action.",
    },
}

# ── IBM eligibility ────────────────────────────────────────────────────────────

_DEADLINE_PLACEHOLDERS = frozenset({
    "", "unknown", "n/a", "tbd", "check current schedule",
    "varies", "check site", "see website", "none",
})

_SUBMISSION_KEYWORDS = {"submit", "apply", "application", "entry", "entries", "prospectus", "open-call"}

_RELATIONSHIP_CATS = {
    "gallery", "gallery_small", "cafe_gallery", "artist_space",
    "event_space", "gallery_event", "market_event",
    "zine_shop_consignment", "bookstore_gallery", "bookstore_event",
}


def _confirmed_deadline(opp: dict) -> bool:
    d = str(opp.get("deadline", "")).strip().lower()
    if d in _DEADLINE_PLACEHOLDERS or len(d) <= 4:
        return False
    # Truth-pass rule 2: a deadline with no year ("May 15th") can never expire,
    # so it can never be confirmed. Require a parseable date or a 4-digit year.
    if _parse_deadline_date(opp) is None and not re.search(r"(19|20)\d{2}|\d{4}年", d):
        return False
    return True


_ISO_DATE_RE  = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
_JP_DATE_RE   = re.compile(r'(\d{4})年(\d{1,2})月(\d{1,2})日')
_EN_MONTH_RE  = re.compile(
    r'(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|'
    r'jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)'
    r'\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})',
    re.IGNORECASE,
)
_EN_DAY_MON_RE = re.compile(
    r'(\d{1,2})\s+'
    r'(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|'
    r'jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)'
    r'\s+(\d{4})',
    re.IGNORECASE,
)
_MONTH_NUM = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
}


def _parse_deadline_date(opp: dict):
    """Return a date object if the deadline can be parsed, else None."""
    d = str(opp.get("deadline", "")).strip()
    if not d:
        return None
    m = _ISO_DATE_RE.search(d)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
        except ValueError:
            pass
    m = _JP_DATE_RE.search(d)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
        except ValueError:
            pass
    m = _EN_MONTH_RE.search(d)
    if m:
        mon_str = d[m.start():m.start() + 3].lower()
        mon_num = _MONTH_NUM.get(mon_str)
        if mon_num:
            try:
                return datetime(int(m.group(2)), mon_num, int(m.group(1)), tzinfo=timezone.utc)
            except ValueError:
                pass
    m = _EN_DAY_MON_RE.search(d)
    if m:
        mon_str = m.group(2)[:3].lower()
        mon_num = _MONTH_NUM.get(mon_str)
        if mon_num:
            try:
                return datetime(int(m.group(3)), mon_num, int(m.group(1)), tzinfo=timezone.utc)
            except ValueError:
                pass
    return None


def _deadline_past(opp: dict) -> bool:
    """Return True if a parseable deadline is more than 7 days in the past."""
    dt = _parse_deadline_date(opp)
    if dt is None:
        return False
    return (datetime.now(timezone.utc) - dt).days > 7


def _url_field(opp: dict, key: str) -> str:
    """URL fields occasionally arrive as lists from older enrichment runs."""
    v = opp.get(key) or ""
    if isinstance(v, list):
        v = v[0] if v else ""
    return str(v).strip()


def _real_submission_page(opp: dict) -> bool:
    sp  = _url_field(opp, "submission_page")
    ow  = _url_field(opp, "official_website")
    if not sp or sp == ow:
        return False
    return any(kw in sp.lower() for kw in _SUBMISSION_KEYWORDS)


def _ibm_eligible(opp: dict) -> bool:
    if opp.get("status") in ("permanently_closed", "closed_this_cycle"):
        return False
    # Relationship/proposal venues are evergreen — stale deadline fields don't close them
    if opp.get("category") in _RELATIONSHIP_CATS and opp.get("contact_verified"):
        return True
    if _deadline_past(opp):
        return False
    if _confirmed_deadline(opp):
        return True
    if _real_submission_page(opp):
        return True
    return False


# ── Helpers ───────────────────────────────────────────────────────────────────

def _opp_id(opp: dict) -> str:
    raw = opp.get("id") or opp.get("title") or opp.get("name") or ""
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def _opp_name(opp: dict) -> str:
    return opp.get("title") or opp.get("name") or ""


_CJK_RE      = re.compile(r"[一-鿿ぁ-んァ-ン々〆〇ー]")
_PAREN_EN_RE = re.compile(r"[（(]([A-Za-z0-9][^)）]{2,})[)）]")
_LEAD_LAT_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9 \-:/.&+@!,'#|_]{1,})")


def _extract_english_name(name: str, name_zh: str = "") -> str:
    """Return a Latin-script name for display in English UI, or '' if none needed."""
    if not name or not _CJK_RE.search(name):
        return ""  # already Latin — original is fine
    # 1. Parenthetical English in name: 'XX（English Title）'
    m = _PAREN_EN_RE.search(name)
    if m and not _CJK_RE.search(m.group(1)) and len(m.group(1).strip()) >= 3:
        return m.group(1).strip()
    # 2. Leading Latin prefix in name: 'TOKAS レジデンシー' → 'TOKAS'
    lead = _LEAD_LAT_RE.match(name)
    if lead:
        cand = lead.group(1).strip()
        if len(cand) >= 3 and not _CJK_RE.search(cand):
            return cand
    # 3. From name_zh
    if name_zh:
        m2 = _PAREN_EN_RE.search(name_zh)
        if m2 and not _CJK_RE.search(m2.group(1)) and len(m2.group(1).strip()) >= 3:
            return m2.group(1).strip()
        if not _CJK_RE.search(name_zh) and name_zh.strip():
            return name_zh.strip()
        lead2 = _LEAD_LAT_RE.match(name_zh)
        if lead2:
            cand2 = lead2.group(1).strip()
            if len(cand2) >= 4 and not _CJK_RE.search(cand2):
                return cand2
    return ""


def _overall_score(opp: dict) -> float:
    for key in ("truth_aligned_score", "overall_score", "differentiated_score",
                "watercolor_adjusted_score", "dna_adjusted_score"):
        v = opp.get(key)
        if v is not None:
            return float(v)
    return 0.0


def _email_category(category: str) -> str:
    ZINE = {"zine_print", "bookstore_gallery", "bookstore_event", "zine_shop_consignment",
            "global_artist_book_platform", "book_publishing", "global_art_book_fair",
            "global_book_arts", "zine_fair_booth"}
    RESIDENCY = {"residency", "global_residency", "institutional",
                 "global_grant_fellowship", "residency_beijing"}
    if category in ZINE:
        return "zine"
    if category in RESIDENCY:
        return "residency"
    return "general"


_SCORE_CAP_ZH = "来源与核实可靠性有限，评分已上调至 {}。"
_SCORE_CAP_JA = "ソース・検証の信頼性に限りがあるため、スコアは {} に調整されています。"

def _translate_warning(note: str) -> tuple[str, str]:
    """Return (zh, ja) translations for a soft_warning string, or ('','') if unknown."""
    import re
    m = re.match(r'Score capped at ([\d.]+) because source/verification strength is limited\.?', note or '')
    if m:
        score = m.group(1)
        return _SCORE_CAP_ZH.format(score), _SCORE_CAP_JA.format(score)
    return "", ""


def email_zh(organization: str, category: str) -> str:
    kind = _email_category(category)
    ask = {"zine": "艺术书籍或ZINE的寄售合作",
           "residency": "驻留项目及申请方式"}.get(kind, "展览提案或公开征集")
    return f"""主题：艺术家合作咨询

{organization} 负责人您好，

您好！我是GEGYjiji，一位旅居东京的水彩艺术家。我的创作主要关注城市风景、建筑空间、日常室内环境与光线，以及那些静谧的、承载记忆的空间氛围。

我对贵方的空间与项目很感兴趣，希望进一步了解{ask}相关的合作可能。

您可以在Instagram（@gegyjiji）上看到我的近期作品。如需作品集PDF或艺术家简介，我可以随时发送。

期待您的回复，感谢您的时间。

GEGYjiji
[portfolio link]"""


def email_ja(organization: str, category: str) -> str:
    kind = _email_category(category)
    ask = {"zine": "アーティストブックや作品のコンサインメント販売について",
           "residency": "レジデンシープログラムやご応募方法について"}.get(kind, "展覧会のご提案やオープンコールについて")
    return f"""件名：アーティストとしてのご連絡

{organization} ご担当者様

はじめまして。私はGEGYjiji（ゲジジ）と申します。東京を拠点に活動しているウォーターカラーアーティストです。都市の風景、建築、日常の静かな空間や光をテーマに透明水彩で制作しています。

貴スペースの活動に大変共感し、ご連絡いたしました。{ask}についてお伺いできればと思います。

作品はInstagram（@gegyjiji）でもご確認いただけます。ポートフォリオも添付、またはご要望があればお送りいたします。

ご多忙のところ恐れ入りますが、ご検討のほどどうぞよろしくお願いいたします。

GEGYjiji
[portfolio link]"""


def email_en(organization: str, category: str) -> str:
    kind = _email_category(category)
    ask = {"zine": "artist book or zine consignment / stocking",
           "residency": "residency programs and how to apply"}.get(kind, "exhibition proposals or open calls")
    return f"""Subject: Artist inquiry — GEGYjiji

Dear {organization} team,

My name is GEGYjiji, a watercolor artist based in Tokyo. I work with urban atmospheres, architectural spaces, domestic interiors, and the quiet accumulation of memory — mostly in watercolor on a small, intimate scale.

I came across your space and was drawn to what you do. I would love to learn more about {ask} and whether my work might be a fit.

You can see my work on Instagram (@gegyjiji). I am happy to send a portfolio PDF or artist statement on request.

Thank you for your time.

GEGYjiji
[portfolio link]"""


_DEADLINE_EMPTY = frozenset({
    "", "unknown", "n/a", "tbd", "check current schedule",
    "varies", "check site", "see website", "none", "check source",
})


_CL = {
    # label → (zh, ja)
    "Deadline":             ("截止日期",          "締め切り"),
    "Entry fee":            ("报名费",             "参加費"),
    "Submission path":      ("投稿方法",           "応募経路"),
    "Artist statement":     ("艺术家自述",         "アーティストステートメント"),
    "Portfolio images":     ("作品图集",           "ポートフォリオ画像"),
    "Japanese intro email": ("日语介绍邮件",       "日本語紹介メール"),
    "Chinese intro email":  ("中文介绍邮件",       "中国語紹介メール"),
    "Zine or artist book":  ("Zine或艺术家书",    "Zineまたはアーティストブック"),
    "Artist book or print edition": ("艺术家书或印刷版", "アーティストブックまたは印刷版"),
}
_CN = {
    # note → (zh, ja)
    "Not yet confirmed — verify on site":       ("尚未确认，请在官网核实",         "まだ確認されていません。公式サイトでご確認ください"),
    "confirm before applying":                  ("申请前请核实",                   "応募前にご確認ください"),
    "Free":                                     ("免费",                           "無料"),
    "Verify amount on site":                    ("请在官网核实金额",               "公式サイトで金額をご確認ください"),
    "Link confirmed live":                      ("链接已确认有效",                 "リンク確認済み"),
    "Email contact available":                  ("可通过邮件联系",                 "メール連絡先あり"),
    "Find submission page or contact":          ("请查找投稿页面或联系方式",       "応募ページまたは連絡先をご確認ください"),
    "On file in Peppercorn":                    ("已存于Peppercorn",               "Peppercornに保存済み"),
    "Watercolor series available":              ("水彩系列作品已备好",             "水彩シリーズ作品準備完了"),
    "Draft available in Details":               ("详情页已有草稿",                 "詳細ページに下書きあり"),
    "Physical publication needed for this opportunity": ("此机会需要实体出版物", "この機会には実物の出版物が必要です"),
}

def _ci(label: str, status: str, note) -> dict:
    note = note or ""
    lz, lj = _CL.get(label, (label, label))
    # note may have a dynamic prefix like "2025年10月1日 — confirm before applying"
    nz, nj = "", ""
    for en_note, (zh_note, ja_note) in _CN.items():
        if en_note in note:
            nz = note.replace(en_note, zh_note) if en_note != note else zh_note
            nj = note.replace(en_note, ja_note) if en_note != note else ja_note
            break
    return {"label": label, "label_zh": lz, "label_ja": lj,
            "status": status, "note": note, "note_zh": nz or note, "note_ja": nj or note}


def _build_checklist(opp: dict) -> list:
    items = []
    category = opp.get("category", "")
    city     = (opp.get("city") or "").lower()
    country  = (opp.get("country") or "").lower()

    dl = str(opp.get("deadline", "")).strip().lower()
    if dl in _DEADLINE_EMPTY:
        items.append(_ci("Deadline", "check", "Not yet confirmed — verify on site"))
    elif opp.get("deadline_verified"):
        items.append(_ci("Deadline", "ready", opp.get("deadline", "")))
    else:
        items.append(_ci("Deadline", "check", f"{opp.get('deadline','')} — confirm before applying"))

    fees_raw = str(opp.get("fees", "")).strip().lower()
    if "free" in fees_raw or "¥0" in fees_raw or fees_raw == "0":
        items.append(_ci("Entry fee", "ready", "Free"))
    elif fees_raw and fees_raw not in {"check source", "check site", "tbd", "unknown", ""}:
        items.append(_ci("Entry fee", "ready", opp.get("fees", "")))
    else:
        items.append(_ci("Entry fee", "check", "Verify amount on site"))

    sub_ok = bool(opp.get("submission_page")) and opp.get("url_verification_status") == "ok"
    if sub_ok:
        items.append(_ci("Submission path", "ready", "Link confirmed live"))
    elif opp.get("contact") and "@" in str(opp.get("contact", "")):
        items.append(_ci("Submission path", "ready", "Email contact available"))
    else:
        items.append(_ci("Submission path", "check", "Find submission page or contact"))

    items.append(_ci("Artist statement", "ready", "On file in Peppercorn"))
    items.append(_ci("Portfolio images", "ready", "Watercolor series available"))

    if "tokyo" in city or "japan" in country:
        items.append(_ci("Japanese intro email", "ready", "Draft available in Details"))
    elif "beijing" in city or "china" in country:
        items.append(_ci("Chinese intro email", "ready", "Draft available in Details"))

    bow = opp.get("recommended_body_of_work") or ""
    if "Artist Book" in bow or "Zine" in bow:
        label = "Zine or artist book" if category in {
            "zine_print", "zine_shop_consignment", "zine_fair_booth", "book_publishing"
        } else "Artist book or print edition"
        items.append(_ci(label, "missing", "Physical publication needed for this opportunity"))

    return items


def shape_card(opp: dict) -> dict:
    category = opp.get("category", "")
    org      = opp.get("organization") or _opp_name(opp)
    name     = _opp_name(opp)
    score    = _overall_score(opp)
    summary  = opp.get("one_sentence", "")

    # Truth-pass rule 3: evergreen relationship venues (consignment shops,
    # cafés, artist spaces) carry stale one-off event dates as residue.
    # A past date on such a venue is never an action date — serve "rolling".
    if category in _RELATIONSHIP_CATS and _deadline_past(opp):
        opp = {**opp, "deadline": "", "status": opp.get("status", "")}

    why = opp.get("why_this_fits_short", "")
    # why_card: shown on card face only when it adds something beyond the summary
    why_card = why if (why and why[:60] != summary[:60]) else ""
    actionability = assess_actionability(opp)

    return {
        "id":              _opp_id(opp),
        "name":            name,
        "organization":    org,
        "category":        category,
        "opportunity_type":      opp.get("opportunity_type", ""),
        "exclusive_primary_bucket": opp.get("exclusive_primary_bucket", ""),
        "city":            opp.get("city", ""),
        "country":         opp.get("country", ""),
        "deadline":        opp.get("deadline", ""),
        "fees":            opp.get("fees", ""),
        "score":           score,
        "overall_score":   score,
        "official_website": opp.get("official_website", ""),
        "source_url":      opp.get("source_url", ""),
        "submission_page": opp.get("submission_page", ""),
        "contact":         opp.get("contact") or opp.get("contact_email") or "",
        "contact_url":     opp.get("contact_url", ""),
        "contact_note":    opp.get("contact_note", ""),
        "action_type":     opp.get("action_type", ""),
        "relationship_note": opp.get("relationship_note", ""),
        "effort":          "",
        # Card text — English source + pre-translated variants
        "summary":         summary[:180],
        "summary_zh":      opp.get("one_sentence_zh") or opp.get("summary_zh", ""),
        "summary_ja":      opp.get("one_sentence_ja") or opp.get("summary_ja", ""),
        "overview":        summary,
        "overview_zh":     opp.get("one_sentence_zh", ""),
        "overview_ja":     opp.get("one_sentence_ja", ""),
        "why_card":        why_card,
        "why_card_zh":     opp.get("why_it_fits_zh", ""),
        "why_card_ja":     opp.get("why_it_fits_ja", ""),
        "why_it_fits":     why,
        "why_it_fits_zh":  opp.get("why_it_fits_zh", ""),
        "why_it_fits_ja":  opp.get("why_it_fits_ja", ""),
        "name_en":         _extract_english_name(name, opp.get("name_zh", "")),
        "name_zh":         opp.get("name_zh", ""),
        "name_ja":         opp.get("name_ja", ""),
        "next_action":     opp.get("quick_action", ""),
        "next_action_zh":  opp.get("quick_action_zh", ""),
        "next_action_ja":  opp.get("quick_action_ja", ""),
        "soft_warning":    opp.get("score_sanity_note", "") or opp.get("verification_summary", ""),
        "soft_warning_zh": _translate_warning(opp.get("score_sanity_note", "") or opp.get("verification_summary", ""))[0],
        "soft_warning_ja": _translate_warning(opp.get("score_sanity_note", "") or opp.get("verification_summary", ""))[1],
        "what_to_verify":  opp.get("missing_fields", []),
        "bullets":         opp.get("three_bullets", []) or [],
        "bullets_zh":      opp.get("three_bullets_zh", []) or [],
        "bullets_ja":      opp.get("three_bullets_ja", []) or [],
        "checklist":       _build_checklist(opp),
        "actionability_status": actionability["actionability_status"],
        "review_flags":    actionability["review_flags"],
        "recommendation_reasons": actionability["recommendation_reasons"],
        "prerequisites":   opp.get("prerequisites", []) or [],
        "student_call":    bool(opp.get("student_call")),
        "native_medium":   opp.get("native_medium", "unknown"),
        "deadline_past":   _deadline_past(opp),
        "closed_this_cycle": opp.get("status") == "closed_this_cycle",
        # Email drafts — prefer per-entry drafts from data, fall back to templates
        "email_zh": opp.get("email_zh") or email_zh(org, category),
        "email_ja": opp.get("email_ja") or email_ja(org, category),
        "email_en": opp.get("email_en") or email_en(org, category),
    }


def _ranked_score(item: dict) -> float:
    """Sort key for already-eligible opportunities."""
    score = _overall_score(item)
    return score


def _pure_photography_noise(item: dict) -> bool:
    """Exclude pure photography calls from the watercolor artist-facing app."""
    if item.get("native_medium") == "photography":
        return True
    if item.get("category") not in {"photo_open_call", "global_photobook"}:
        return False
    accepted = str(item.get("accepted_media") or item.get("recommended_body_of_work") or "").lower()
    return "watercolor" not in accepted and "painting" not in accepted and "artist book" not in accepted


def by_display_score(cards: list) -> list:
    return sorted(cards, key=_ranked_score, reverse=True)


def load_opportunities() -> list:
    global _OPP_CACHE, _OPP_CACHE_MTIME
    path = DEPLOY_DIR / "compact_opportunities.json"
    if not path.exists():
        return []
    mtime = path.stat().st_mtime
    if _OPP_CACHE is None or mtime != _OPP_CACHE_MTIME:
        raw = json.loads(path.read_text(encoding="utf-8"))
        _OPP_CACHE = raw if isinstance(raw, list) else raw.get("items", [])
        _OPP_CACHE_MTIME = mtime
    suppressed = _load_suppressed()
    suppressed_cats = _load_suppressed_categories()
    items = [
        x for x in _OPP_CACHE
        if x.get("exclusive_primary_bucket") not in {"reject", "low_priority"}
        and x.get("status") != "permanently_closed"
        and x.get("recommendation_visibility") != "hidden"
        and not _pure_photography_noise(x)
        and _opp_id(x) not in suppressed
        and x.get("category") not in suppressed_cats
    ]
    # Truth-pass rule 4: the same call can enter twice from different sources
    # (e.g. NIKA S20 listed under two titles). Dedup by normalized name,
    # keeping the higher-scored entry.
    best: dict = {}
    for x in items:
        key = re.sub(r"[\s「」『』()（）+＋・/\-]", "", _opp_name(x).lower())[:40]
        if not key:
            best[id(x)] = x
            continue
        cur = best.get(key)
        if cur is None or _overall_score(x) > _overall_score(cur):
            best[key] = x
    return list(best.values())


def opportunities_data_updated_at() -> str | None:
    """Return a quiet freshness signal for the artist-facing UI."""
    path = DEPLOY_DIR / "compact_opportunities.json"
    if not path.exists():
        return None
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()


def bucket(items: list) -> dict:
    # Sort by ranked score: photography yields 1 pt to painting at equal quality
    scored = sorted(items, key=_ranked_score, reverse=True)

    # ── Submission log suppression ────────────────────────────────────────────
    _pending_names, _rejected_names, _accepted = _load_submission_states()

    def _match_submission(opp, name_set):
        """True if this opp's venue/org name fuzzy-matches a submission in name_set."""
        if not name_set:
            return False
        opp_names = {
            (opp.get("name") or "").strip().lower(),
            (opp.get("organization") or "").strip().lower(),
            (opp.get("title") or "")[:40].strip().lower(),
        } - {""}
        return bool(opp_names & name_set)

    used: set[str] = set()
    buckets: dict[str, list] = {}

    # ── Immediate Best Moves: pipeline-flagged IBM that pass eligibility gate ──
    ibm_candidates = [
        x for x in scored
        if x.get("exclusive_primary_bucket") == "immediate_best_moves"
        and _ibm_eligible(x)
        and not _match_submission(x, _pending_names)   # suppress if already applied (pending)
        and not _match_submission(x, _rejected_names)  # suppress if rejected
    ]
    used.update(_opp_id(x) for x in ibm_candidates)
    buckets["immediate_best_moves"] = by_display_score([shape_card(x) for x in ibm_candidates])

    # Expose accepted celebrations for status bar
    buckets["__accepted_celebrations__"] = _accepted

    # ── Category sections ────────────────────────────────────────────────────
    # closed_this_cycle entries are excluded from the action sections and fall
    # through to the watch list (truth-pass rule 5: a call whose page says
    # "expired" must never be served under "Open Calls").
    for key, cats in SECTION_CATEGORIES.items():
        section = [
            x for x in scored
            if x.get("category") in cats and _opp_id(x) not in used
            and x.get("exclusive_primary_bucket") not in {"stretch_targets", "research_needed"}
            and x.get("status") != "closed_this_cycle"
        ]
        used.update(_opp_id(x) for x in section)
        buckets[key] = by_display_score([shape_card(x) for x in section])

    # ── Watch list: remainder (research_needed, stretch_targets, uncategorised) ──
    leftover = by_display_score([
        shape_card(x) for x in scored if _opp_id(x) not in used
    ])
    buckets["watch_list"] = buckets.get("watch_list", []) + leftover

    return buckets


@app.get("/api/opportunities")
def get_opportunities():
    items   = load_opportunities()
    buckets = bucket(items)
    accepted = buckets.pop("__accepted_celebrations__", [])
    return {
        "meta":                  SECTION_META,
        "sections":              buckets,
        "total":                 sum(len(v) for v in buckets.values()),
        "data_updated_at":        opportunities_data_updated_at(),
        "accepted_celebrations": accepted,
    }


VALID_ACTIONS = {"follow", "applied", "maybe_later", "not_for_me"}


class FeedbackPayload(BaseModel):
    opp_id: str
    action: str
    opp_name: str = ""      # venue name for submission log
    opp_title: str = ""     # submission title/what
    opp_website: str = ""   # official_website for reference


@app.post("/api/feedback")
def post_feedback(payload: FeedbackPayload):
    if payload.action not in VALID_ACTIONS:
        raise HTTPException(status_code=400, detail=f"Invalid action: {payload.action}")

    feedback_path = DATA_DIR / "feedback.json"
    if feedback_path.exists():
        records = json.loads(feedback_path.read_text(encoding="utf-8"))
    else:
        records = []

    records = [r for r in records if r.get("opp_id") != payload.opp_id]
    records.append({
        "opp_id":    payload.opp_id,
        "action":    payload.action,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    feedback_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    if payload.action == "not_for_me":
        suppressed = list(_load_suppressed())
        if payload.opp_id not in suppressed:
            suppressed.append(payload.opp_id)
        SUPPRESSED_PATH.write_text(json.dumps(suppressed, ensure_ascii=False, indent=2), encoding="utf-8")

    # Auto-create submission log entry when artist marks Applied
    if payload.action == "applied":
        venue_name = payload.opp_name or payload.opp_id
        what = payload.opp_title or venue_name
        # Look up opp in compact_opportunities.json for richer data if names weren't passed
        if not payload.opp_name:
            opp_data_path = DEPLOY_DIR / "compact_opportunities.json"
            if opp_data_path.exists():
                all_opps = _OPP_CACHE if _OPP_CACHE is not None else json.loads(opp_data_path.read_text(encoding="utf-8"))
                opp_id_lower = payload.opp_id.lower()
                for o in all_opps:
                    if (o.get("title", "").lower() == opp_id_lower or
                            o.get("name", "").lower() == opp_id_lower):
                        venue_name = o.get("name") or o.get("title") or payload.opp_id
                        what = o.get("title") or venue_name
                        break

        sub_records = []
        if SUBMISSIONS_PATH.exists():
            sub_records = json.loads(SUBMISSIONS_PATH.read_text(encoding="utf-8"))

        # Don't duplicate — check if same venue already logged today
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        already_logged = any(
            r.get("venue", "").lower() == venue_name.lower() and
            r.get("date", "") == today_str
            for r in sub_records
        )

        if not already_logged:
            sub_records.append({
                "id":          hashlib.md5(f"{today_str}{venue_name}".encode()).hexdigest()[:8],
                "date":        today_str,
                "venue":       venue_name,
                "what":        what,
                "outcome":     "pending",
                "notes":       "Auto-logged from Applied action",
                "logged_at":   datetime.now(timezone.utc).isoformat(),
                "auto_logged": True,
            })
            SUBMISSIONS_PATH.write_text(
                json.dumps(sub_records, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )

    return {"ok": True, "opp_id": payload.opp_id, "action": payload.action}


@app.get("/api/feedback/insights")
def get_feedback_insights():
    """Returns patterns from feedback data — dismissal counts by category, boosted categories."""
    feedback_path = DATA_DIR / "feedback.json"
    if not feedback_path.exists():
        return {"dismissals": {}, "boosts": {}, "total": 0}

    records = json.loads(feedback_path.read_text(encoding="utf-8"))

    # Load opp data for category lookup
    opp_path = Path(__file__).parent / "deploy_data" / "compact_opportunities.json"
    opp_by_id = {}
    if opp_path.exists():
        all_opps = _OPP_CACHE if _OPP_CACHE is not None else json.loads(opp_path.read_text(encoding="utf-8"))
        for o in all_opps:
            key = (o.get("title") or o.get("name") or "").lower()
            if key:
                opp_by_id[key] = o

    dismissals = {}   # category → count
    boosts = {}       # category → count (applied + follow)

    for r in records:
        opp_key = r.get("opp_id", "").lower()
        opp = opp_by_id.get(opp_key, {})
        category = opp.get("category") or opp.get("exclusive_primary_bucket") or "unknown"

        action = r.get("action", "")
        if action == "not_for_me":
            dismissals[category] = dismissals.get(category, 0) + 1
        elif action in ("applied", "follow"):
            boosts[category] = boosts.get(category, 0) + 1

    # Only return dismissals with 3+ threshold
    significant_dismissals = {k: v for k, v in dismissals.items() if v >= 3}

    return {
        "dismissals": significant_dismissals,
        "all_dismissals": dismissals,
        "boosts": boosts,
        "total": len(records),
    }


@app.post("/api/feedback/suppress-category")
def suppress_category(payload: dict):
    category = payload.get("category", "")
    if not category:
        raise HTTPException(status_code=400, detail="category required")

    prefs_path = DATA_DIR / "learned_preferences.json"
    prefs = {}
    if prefs_path.exists():
        prefs = json.loads(prefs_path.read_text(encoding="utf-8"))

    suppressed = prefs.get("suppressed_categories", [])
    if category not in suppressed:
        suppressed.append(category)
    prefs["suppressed_categories"] = suppressed
    prefs["last_updated"] = datetime.now(timezone.utc).isoformat()

    prefs_path.write_text(json.dumps(prefs, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "suppressed_categories": suppressed}


class SubmissionEntry(BaseModel):
    date: str
    venue: str
    what: str
    outcome: str = "pending"
    notes: str = ""


@app.get("/api/submissions")
def get_submissions():
    if SUBMISSIONS_PATH.exists():
        return json.loads(SUBMISSIONS_PATH.read_text(encoding="utf-8"))
    return []


class SubmissionPatch(BaseModel):
    outcome: str = ""
    followed_up: bool | None = None
    notes: str = ""


@app.patch("/api/submissions/{sub_id}")
def patch_submission(sub_id: str, patch: SubmissionPatch):
    """Update a submission: record outcome or mark followed-up.
    Marking followed_up clears the Today's Focus follow-up nudge automatically."""
    if not SUBMISSIONS_PATH.exists():
        raise HTTPException(status_code=404, detail="No submissions found")
    records = json.loads(SUBMISSIONS_PATH.read_text(encoding="utf-8"))
    idx = next((i for i, r in enumerate(records) if r.get("id") == sub_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Submission '{sub_id}' not found")
    if patch.outcome:
        records[idx]["outcome"] = patch.outcome
    if patch.followed_up is not None:
        records[idx]["followed_up"] = patch.followed_up
        if patch.followed_up:
            records[idx]["followed_up_at"] = datetime.now(timezone.utc).isoformat()
    if patch.notes:
        records[idx]["notes"] = patch.notes
    records[idx]["updated_at"] = datetime.now(timezone.utc).isoformat()
    SUBMISSIONS_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "submission": records[idx]}


@app.post("/api/submissions")
def add_submission(entry: SubmissionEntry):
    if SUBMISSIONS_PATH.exists():
        records = json.loads(SUBMISSIONS_PATH.read_text(encoding="utf-8"))
    else:
        records = []
    records.append({
        "id":        hashlib.md5(f"{entry.date}{entry.venue}".encode()).hexdigest()[:8],
        "date":      entry.date,
        "venue":     entry.venue,
        "what":      entry.what,
        "outcome":   entry.outcome,
        "notes":     entry.notes,
        "logged_at": datetime.now(timezone.utc).isoformat(),
    })
    SUBMISSIONS_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "count": len(records)}


class ContactEntry(BaseModel):
    name: str
    type: str = ""
    city: str = ""
    last_visited: str = ""
    status: str = "cold"
    notes: str = ""
    last_contacted: str = ""


# Legacy CRM data used A/B/C priority labels; the UI and engines now use
# high/medium/low. Normalising at read time makes the served data correct
# regardless of which historical seed wrote it — an engine rule, so the fix
# survives even if old A/B/C labels reappear in the source JSON.
_PRIORITY_ALIASES = {"a": "high", "b": "medium", "c": "low",
                     "high": "high", "medium": "medium", "low": "low"}


def _normalize_priority(value):
    if not isinstance(value, str):
        return value
    return _PRIORITY_ALIASES.get(value.strip().lower(), value)


def _normalize_contact_priorities(contacts: list) -> list:
    for c in contacts:
        if isinstance(c, dict):
            if "priority" in c:
                c["priority"] = _normalize_priority(c.get("priority"))
            ca = c.get("crm_analysis")
            if isinstance(ca, dict) and "priority" in ca:
                ca["priority"] = _normalize_priority(ca.get("priority"))
    return contacts


@app.get("/api/contacts")
def get_contacts():
    if not CONTACTS_PATH.exists():
        return []
    data = json.loads(CONTACTS_PATH.read_text(encoding="utf-8"))
    contacts = data.get("contacts", []) if isinstance(data, dict) else data
    contacts = _normalize_contact_priorities(contacts)
    # Sort: most-active statuses first, then alphabetically within status
    STATUS_ORDER = {
        "in_contact": 0, "sent_inquiry": 1, "ready_to_review": 2,
        "researching": 3, "cold": 4,
    }
    contacts.sort(key=lambda c: (STATUS_ORDER.get(c.get("status", "cold"), 9), c.get("name", "")))
    return contacts


@app.post("/api/contacts")
def add_contact(entry: ContactEntry):
    if CONTACTS_PATH.exists():
        data = json.loads(CONTACTS_PATH.read_text(encoding="utf-8"))
        contacts = data.get("contacts", []) if isinstance(data, dict) else data
    else:
        data = []
        contacts = []
    # Update-or-insert by case-insensitive name. Logging the same venue twice
    # must not create a duplicate — the PATCH endpoints match the first entry by
    # name, so a duplicate would become permanently uneditable.
    name_lower = (entry.name or "").strip().lower()
    existing = next(
        (c for c in contacts if (c.get("name") or "").strip().lower() == name_lower),
        None,
    )
    fields = {
        "name":           entry.name,
        "type":           entry.type,
        "city":           entry.city,
        "last_visited":   entry.last_visited,
        "status":         entry.status,
        "notes":          entry.notes,
        "last_contacted": entry.last_contacted,
    }
    if existing is not None:
        # Merge: only overwrite with non-empty incoming values
        for k, v in fields.items():
            if v:
                existing[k] = v
        existing["date_updated"] = datetime.now(timezone.utc).isoformat()
    else:
        fields["logged_at"] = datetime.now(timezone.utc).isoformat()
        contacts.append(fields)
    out = contacts if isinstance(data, list) else {"contacts": contacts}
    CONTACTS_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "count": len(contacts), "updated": existing is not None}


class ContactUpdate(BaseModel):
    name: str           # used to find the contact
    status: str = ""
    notes: str = ""
    last_contacted: str = ""
    last_visited: str = ""


@app.patch("/api/contacts/update")
def update_contact(entry: ContactUpdate):
    if not CONTACTS_PATH.exists():
        raise HTTPException(status_code=404, detail="No contacts found")
    data = json.loads(CONTACTS_PATH.read_text(encoding="utf-8"))
    contacts = data.get("contacts", []) if isinstance(data, dict) else data
    # Find by name (case-insensitive)
    idx = next((i for i, c in enumerate(contacts) if c.get("name", "").lower() == entry.name.lower()), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Contact '{entry.name}' not found")
    if entry.status:
        contacts[idx]["status"] = entry.status
    if entry.notes:
        contacts[idx]["notes"] = entry.notes
    if entry.last_contacted:
        contacts[idx]["last_contacted"] = entry.last_contacted
    if entry.last_visited:
        contacts[idx]["last_visited"] = entry.last_visited
    contacts[idx]["date_updated"] = datetime.now(timezone.utc).isoformat()
    out = contacts if isinstance(data, list) else {"contacts": contacts}
    CONTACTS_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "contact": contacts[idx]}


class ContactPatch(BaseModel):
    status: str = ""
    last_contacted: str = ""
    notes: str = ""
    personal_note: str = ""   # the artist's own note, kept separate from pipeline notes
    response_received: bool | None = None


@app.patch("/api/contacts/{contact_name}")
def patch_contact(contact_name: str, patch: ContactPatch):
    """Update status, last_contacted, notes, response_received for a contact by name."""
    if not CONTACTS_PATH.exists():
        raise HTTPException(status_code=404, detail="No contacts found")
    data = json.loads(CONTACTS_PATH.read_text(encoding="utf-8"))
    contacts = data.get("contacts", []) if isinstance(data, dict) else data
    name_lower = contact_name.lower()
    idx = next((i for i, c in enumerate(contacts) if c.get("name", "").lower() == name_lower), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Contact '{contact_name}' not found")
    if patch.status:
        contacts[idx]["status"] = patch.status
    if patch.last_contacted:
        contacts[idx]["last_contacted"] = patch.last_contacted
    if patch.notes:
        contacts[idx]["notes"] = patch.notes
    if patch.personal_note:
        contacts[idx]["personal_note"] = patch.personal_note
    if patch.response_received is not None:
        contacts[idx]["response_received"] = patch.response_received
    contacts[idx]["date_updated"] = datetime.now(timezone.utc).isoformat()
    out = contacts if isinstance(data, list) else {"contacts": contacts}
    CONTACTS_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "contact": contacts[idx]}


@app.get("/api/contacts/lookup")
def lookup_contact(name: str):
    if not CONTACTS_PATH.exists():
        return None
    data = json.loads(CONTACTS_PATH.read_text(encoding="utf-8"))
    contacts = data.get("contacts", []) if isinstance(data, dict) else data
    name_lower = name.lower()
    # Exact match first
    for c in contacts:
        if c.get("name", "").lower() == name_lower:
            return c
    # Partial match (contact name contained in search name or vice versa)
    for c in contacts:
        cn = c.get("name", "").lower()
        if cn and (cn in name_lower or name_lower in cn):
            return c
    return None


@app.get("/api/saffron")
def get_saffron():
    # ── Peppercorn answers (live data from artist) ────────────────────────────
    _pp_path = DATA_DIR / "peppercorn_profile.json"
    _pp = json.loads(_pp_path.read_text(encoding="utf-8")) if _pp_path.exists() else {}
    _answers = _pp.get("saffron_answers") or {}

    # ── Exhibition log (from Peppercorn) ──────────────────────────────────────
    _exlog_path = DATA_DIR / "exhibition_log.json"
    _logged_shows = json.loads(_exlog_path.read_text(encoding="utf-8")) if _exlog_path.exists() else []
    # Convert logged shows to career_position format
    _logged_exhibitions = [
        {
            "title": e.get("name", ""),
            "venue": e.get("venue", ""),
            "date": e.get("date", ""),
            "type": "Group show" if e.get("type") == "group" else "Solo show",
            "note": e.get("notes", "") or "",
            "from_log": True,
        }
        for e in _logged_shows
        if e.get("outcome") in ("shown", "completed", None, "")
    ]
    # Total *confirmed* group show count: 1 hardcoded base (Tide from China
    # Part1) + confirmed group exhibitions in the artist profile + group shows
    # logged via Peppercorn. Evidence over prediction (CLAUDE.md): unconfirmed
    # profile mentions (e.g. "Kinoko Kingdom" — no venue/dates, "details
    # unconfirmed") must NOT inflate the count. Mirrors
    # career_strategy_engine._count_group_shows so the live API and the career
    # report agree. Dedup the log against profile titles to avoid double-counting.
    _amp_path = DATA_DIR / "artist_master_profile.json"
    _amp = json.loads(_amp_path.read_text(encoding="utf-8")) if _amp_path.exists() else {}
    _profile_exhibitions = _amp.get("career_history", {}).get("exhibitions", [])
    _profile_titles = {(ex.get("title") or "").strip().lower() for ex in _profile_exhibitions}
    _profile_group_count = sum(
        1 for ex in _profile_exhibitions
        if "group" in (ex.get("type") or "").lower()
        and (ex.get("title") or "").strip() != "Tide from China Part1"
        and (ex.get("confidence") or "").lower().startswith("confirmed")
    )
    _logged_group_count = sum(
        1 for e in _logged_shows
        if e.get("type") == "group"
        and (e.get("name") or "").strip() != "Tide from China Part1"
        and (e.get("name") or "").strip().lower() not in _profile_titles
    )
    _total_group_shows = 1 + _profile_group_count + _logged_group_count

    # ── Career position (confirmed research, 2026-06-02) ──────────────────────
    career_position = {
        "exhibitions": [
            {
                "title": "Tide from China Part 1",
                "venue": "ACG_Labo, Harajuku, Tokyo",
                "date": "February 2023",
                "type": "Group show — 6 Chinese illustrators",
                "note": "First Japan exhibition",
            }
        ] + _logged_exhibitions,
        "publications": [
            {
                "title": "Colour Diary",
                "year": "2021",
                "type": "Solo illustration collection",
            },
            {
                "title": "defined Definition 02: A Documented Journey",
                "year": None,
                "type": "Group publication, contributor",
            },
        ],
        "social": [
            {"platform": "Instagram",   "handle": "@gegyjiji",  "followers": "26k", "posts": None},
        ],
        "education": {
            "institution": "Beijing Fashion Institute",
            "field": "Illustration & design",
            "note": "Not a classical fine arts track",
        },
        "base": "Tokyo, Japan / Beijing, China",
    }

    # ── Market landscape (computed from compact_opportunities.json) ───────────
    opps_path = DEPLOY_DIR / "compact_opportunities.json"
    if _OPP_CACHE is not None:
        opps = _OPP_CACHE
    else:
        opps = json.loads(opps_path.read_text(encoding="utf-8")) if opps_path.exists() else []

    CAT_GROUPS = {
        "Zines & Books": {
            "zine_print", "book_publishing", "bookstore_gallery", "bookstore_event",
            "zine_shop_consignment", "global_artist_book_platform", "global_art_book_fair",
        },
        "Galleries": {
            "gallery", "gallery_small", "gallery_event", "artist_space", "event_space",
        },
        "Residencies": {
            "residency", "global_residency", "global_grant_fellowship", "residency_beijing",
        },
        "Open Calls & Fairs": {
            "fair_popup", "global_open_call", "global_watercolor_open_call",
            "japan_watercolor_open_call", "japan_watercolor_institution",
            "zine_fair_booth", "group_publication_open_call", "photo_open_call",
            "global_photobook",
        },
        "Cafés & Bookshop Spaces": {"cafe_gallery"},
    }

    cat_counts = {k: 0 for k in CAT_GROUPS}
    cat_counts["Other"] = 0
    for opp in opps:
        cat = opp.get("category", "")
        placed = False
        for group, members in CAT_GROUPS.items():
            if cat in members:
                cat_counts[group] += 1
                placed = True
                break
        if not placed:
            cat_counts["Other"] += 1

    category_breakdown = sorted(
        [{"label": k, "count": v} for k, v in cat_counts.items() if v > 0],
        key=lambda x: x["count"],
        reverse=True,
    )

    TOKYO_KEYWORDS = ["tokyo", "japan", "yokohama", "shimokitazawa", "koenji",
                      "kichijoji", "nakano", "harajuku", "shinjuku", "shibuya"]
    tokyo_count = sum(
        1 for o in opps
        if any(kw in (o.get("city") or "").lower() for kw in TOKYO_KEYWORDS)
    )

    bucket_counts = Counter(o.get("exclusive_primary_bucket", "") for o in opps)
    actionability = [
        {"label": "Immediate Best Moves", "count": bucket_counts.get("immediate_best_moves", 0), "tier": "high"},
        {"label": "Publication Targets",  "count": bucket_counts.get("publication_targets", 0),  "tier": "medium"},
        {"label": "Relationship Builders","count": bucket_counts.get("relationship_builders", 0),"tier": "medium"},
        {"label": "Stretch Targets",      "count": bucket_counts.get("stretch_targets", 0),      "tier": "stretch"},
        {"label": "Needs Research",       "count": bucket_counts.get("research_needed", 0),      "tier": "low"},
    ]

    market_landscape = {
        "total": len(opps),
        "category_breakdown": category_breakdown,
        "tokyo_vs_international": {
            "tokyo":         tokyo_count,
            "international": len(opps) - tokyo_count,
        },
        "actionability": actionability,
    }

    # ── Peer artists ──────────────────────────────────────────────────────────
    peer_path = DATA_DIR / "peer_artists.json"
    raw_peers = json.loads(peer_path.read_text(encoding="utf-8")) if peer_path.exists() else []
    peer_artists = sorted(
        [
            {
                "name":         a.get("name", ""),
                "region":       a.get("region", ""),
                "fit_reason":   a.get("fit_reason", ""),
                "shared_traits":a.get("shared_traits", []),
                "use_as":       a.get("use_as", ""),
                "fit_score":    a.get("fit_score", 0),
            }
            for a in raw_peers
        ],
        key=lambda x: x["fit_score"],
        reverse=True,
    )

    # ── Strategic pathway ─────────────────────────────────────────────────────
    pathway = {
        "goal": "First Solo Show in Tokyo",
        "timeline_estimate": "18–36 months from mid-2026",
        "steps": [
            {
                "n": 1,
                "label": "First publication credit",
                "done": True,
                "blocking": False,
                "detail": "Colour Diary (2021) and contribution to defined Definition 02. Publication history established.",
            },
            {
                "n": 2,
                "label": "First group show in Japan",
                "done": True,
                "blocking": False,
                "detail": "Tide from China Part 1, ACG_Labo Harajuku, February 2023. First confirmed Japan exhibition on record.",
            },
            {
                "n": 3,
                "label": "2–3 more Tokyo group shows",
                "done": False,
                "blocking": True,
                "detail": "Artist-run spaces are the natural path: 3331 Arts Chiyoda, Design Festa Gallery, Gallery IYN. Each show builds credibility and introduces your work to gallery directors.",
            },
            {
                "n": 4,
                "label": "Bookshop gallery exhibition",
                "done": False,
                "blocking": False,
                "detail": "UTRECHT, Book and Sons, or flotsam books. Bridges illustration community into gallery context — a natural fit given your publication background.",
            },
            {
                "n": 5,
                "label": "Second publication or new zine",
                "done": False,
                "blocking": False,
                "detail": "Builds presence in the Tokyo zine and book ecosystem. Creates a natural entrypoint for bookshop gallery conversations and strengthens the publication half of your CV.",
            },
            {
                "n": 6,
                "label": "Gallery relationship building",
                "done": False,
                "blocking": False,
                "detail": "Attend openings at target venues consistently. The invitation to a solo show comes from a relationship, not a cold submission — this step runs in parallel with everything else.",
            },
            {
                "n": 7,
                "label": "Solo show application or invitation",
                "done": False,
                "blocking": False,
                "detail": "Target: an intimate Tokyo gallery with a track record of solo shows by international artists at similar career stages. Youkobo Art Space, Gallery Denn, or a bookshop gallery context are realistic first targets.",
            },
        ],
        "blocking_now": (
            f"Only {_total_group_shows} confirmed group show{'s' if _total_group_shows != 1 else ''} in Japan. "
            f"Most Tokyo galleries expect 3–4 group exhibition credits before a solo conversation "
            f"— so {max(0, 3 - _total_group_shows)}–{max(0, 4 - _total_group_shows)} more group shows needed. "
            "The next group show is the highest-leverage move right now."
        ) if _total_group_shows < 4 else (
            f"{_total_group_shows} confirmed group shows — exhibition history is established. "
            "A solo show conversation is now viable at the right venue."
        ),
        "next_move": "Apply for a second group show at a Tokyo artist-run space. 3331 Arts Chiyoda open calls, Design Festa Gallery curated shows, and Gallery IYN open submissions are the realistic near-term entries. Any of these, confirmed and attended, advances the pathway.",
    }

    # ── Instagram strategy ────────────────────────────────────────────────────
    instagram_strategy = {
        "platforms": [
            {
                "name": "Instagram",
                "handle": "@gegyjiji",
                "followers": "26k",
                "posts": None,
                "note": "Primary visual portfolio platform — 26k followers built through daily watercolor diary practice since 2020. The platform galleries, publishers, and curators use for discovery.",
            },
        ],
        "gap": {
            "instagram": 26000,
            "analysis": "Instagram is an established strength — 26k followers, already a working portfolio and the surface galleries and publishers use to discover you. Growth from here is a bonus, not a requirement.",
        },
        "known": {
            "content_type": "Urban environments, cats, domestic life, travel fragments — subjects that already do well on Instagram",
            "diary_practice": "A years-long watercolor diary since 2020. The material is already there; nothing about visibility asks you to paint more.",
        },
        "strategy": "A low-effort way to deepen your reach without painting more: short process videos — a time-lapse, or a clip of a piece coming together. They travel well on Instagram and Reels, suit a slow studio practice, and turn work you're already doing into something to share.",
        "missing": [
            {
                "field": "Posting frequency",
                "reason": "Cannot be observed from public data. Peppercorn needs to ask: how often does she post to Instagram?",
            },
            {
                "field": "Engagement rate",
                "reason": "Likes and comments are visible but unreliable without knowing reach. Peppercorn should ask for Insights access or a screenshot.",
            },
            {
                "field": "Posting goals",
                "reason": "Does she want to grow Instagram, or is it a portfolio archive? The strategy changes entirely depending on the answer.",
            },
        ],
    }

    # ── Audience geography ────────────────────────────────────────────────────
    audience_geography = {
        "available": False,
        "reason": "Instagram Insights are not accessible without the artist's credentials. Geographic audience data cannot be observed from public sources.",
        "why_it_matters": "Whether your 26k Instagram following is concentrated in China, Japan, or distributed internationally determines which geographic markets to prioritise — for exhibitions, fairs, and publishers. A primarily Chinese audience suggests a different expansion path than a globally distributed one.",
        "hypothesis": "Based on the ACG/illustration community context, the Instagram following may skew toward Chinese-language users. Whether the Tokyo-based practice has shifted that toward a Japan-leaning or globally distributed audience is unconfirmed.",
        "what_peppercorn_should_ask": "Can you share a screenshot of your Instagram Audience Insights (country/city breakdown)?",
    }

    # ── Career benchmarks ─────────────────────────────────────────────────────
    career_benchmarks = {
        "artist_record": {
            "exhibitions": _total_group_shows,
            "publications": 2,
            "instagram": "26k",
            "age_approx": 26,
            "years_active": "~6 (daily practice from 2020, first publication 2021)",
        },
        "peer_range": [
            {
                "dimension": "Group exhibitions",
                "artist_value": f"{_total_group_shows} confirmed" if _total_group_shows > 1 else "1 confirmed",
                "peer_low": 1,
                "peer_typical": "3–5",
                "peer_high": "8+",
                "assessment": "below_typical",
                "note": "Expected at this stage — but the gap needs closing before gallery conversations are realistic",
            },
            {
                "dimension": "Publications",
                "artist_value": "2 (1 solo, 1 group)",
                "peer_low": 1,
                "peer_typical": "1–3",
                "peer_high": "5+",
                "assessment": "on_track",
                "note": "Solid for this stage, especially with a solo collection at 21",
            },
            {
                "dimension": "Instagram followers",
                "artist_value": "26k",
                "peer_low": "5k",
                "peer_typical": "15–50k",
                "peer_high": "100k+",
                "assessment": "on_track",
                "note": "Right in the typical band for illustrators at this stage — a solid, real audience for print and zine discovery, with room to grow toward the 50k market-viability signal",
            },
        ],
        "summary": "Exhibition history is the weakest dimension. The 26k Instagram following is a solid, real asset at this career stage but not yet a standout — it sits in the typical peer range. The near-term work is converting audience into exhibition and publication credits.",
    }

    # ── Seasonal opportunity calendar ─────────────────────────────────────────
    MONTH_NAMES = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December",
    ]

    def _parse_month(dl_str):
        if not dl_str:
            return None
        # Try structured parse first (ISO / JP / EN formats)
        dt = _parse_deadline_date({"deadline": dl_str})
        if dt:
            return MONTH_NAMES[dt.month - 1]
        # Fall back to month-name text scan
        for m in MONTH_NAMES:
            if m.lower() in dl_str.lower():
                return m
        return None

    monthly: dict[str, list] = {m: [] for m in MONTH_NAMES}
    rolling_opps = []
    unknown_dl_count = 0

    for opp in opps:
        dl = (opp.get("deadline") or "").strip()
        if re.search(r"rolling|ongoing|open|anytime", dl, re.IGNORECASE):
            rolling_opps.append({
                "name": opp.get("name", ""),
                "category": opp.get("category", ""),
            })
            continue
        month = _parse_month(dl)
        if month:
            monthly[month].append({
                "name": opp.get("name", ""),
                "deadline": dl,
                "category": opp.get("category", ""),
            })
        else:
            unknown_dl_count += 1

    _current_month_idx = datetime.now(timezone.utc).month  # 1-based
    calendar_months = [
        {"month": m, "opportunities": monthly[m]}
        for i, m in enumerate(MONTH_NAMES, start=1)
        if monthly[m] and i >= _current_month_idx
    ]

    seasonal_calendar = {
        "months": calendar_months,
        "rolling": rolling_opps,
        "unknown_deadline_count": unknown_dl_count,
        "total_opportunities": len(opps),
        "coverage_note": f"{unknown_dl_count} of {len(opps)} opportunities have no confirmed deadline — the calendar is partial and reflects only verified dates.",
        "preparation_lead_times": {
            "open_calls": "2–4 weeks before deadline for portfolio selection and statement",
            "residencies": "4–8 weeks for full application (proposal, references, CV)",
            "book_fairs": "2–3 months for production of zines or publications to sell",
            "gallery_submissions": "Varies — research the specific venue's submission window first",
        },
    }

    # ── Press & features ──────────────────────────────────────────────────────
    press_features = {
        "confirmed": [
            {
                "outlet": "Bored Panda",
                "type": "Work feature",
                "url": "https://www.boredpanda.com/watercolor-paintings-cats-nature-city-gegyjiji/",
                "note": "Visual feature of watercolor work — large general audience, no biographical depth",
            },
            {
                "outlet": "Bored Panda",
                "type": "Work feature (part 2)",
                "url": "https://www.boredpanda.com/watercolor-paintings-cats-nature-city-gegyjiji-part-2/",
                "note": "Follow-up feature of the same body of work",
            },
        ],
        "art_press": {
            "available": False,
            "reason": "No features found in art-specific publications. Bored Panda reaches a general audience; art press — Bijutsu Techo, Pen Magazine, It's Nice That — is a different circuit.",
        },
        "japan_coverage": {
            "available": False,
            "reason": "No confirmed features in Japanese-language media. Coverage in Japanese art and design media would meaningfully support gallery and venue relationships in Tokyo.",
        },
        "pitch_targets": [
            {"outlet": "Bijutsu Techo (美術手帖)", "why": "Japan's most significant contemporary art publication"},
            {"outlet": "Pen Magazine", "why": "Design and art, illustration-friendly, Tokyo readership"},
            {"outlet": "It's Nice That", "why": "Primary English-language illustrator discovery platform globally"},
            {"outlet": "Apartamento", "why": "Domestic interiors and everyday life — directly aligned with your subject matter"},
            {"outlet": "BOOOOOOOM", "why": "Large illustration/photography community; annual book prize you could enter"},
        ],
    }

    # ── Collector ecosystem ───────────────────────────────────────────────────
    collector_ecosystem = {
        "available": False,
        "reason": "The pipeline tracks opportunities and venues, not buyers. No collector-specific data exists in the system.",
        "why_it_matters": "Knowing who buys illustration and watercolor work at your price point determines which fairs, platforms, and venues are commercially worthwhile — not just aesthetically aligned.",
        "fairs_in_pipeline": [
            "Tokyo Art Book Fair",
            "Design Festa",
            "Comitia",
            "HandMade In Japan Fes",
            "ZINEフェス東京",
        ],
        "known_gap": "No data on what price points, formats (print vs. original), or collector profiles actually convert at these events.",
        "what_peppercorn_should_ask": "Have you sold work? At what price points? Through which channels? Which formats (prints, originals, zines) have sold vs. remained unsold?",
    }

    # ── Collaboration map ─────────────────────────────────────────────────────
    collaboration_map = {
        "known_co_exhibitors": [
            {"name": "富大貴",            "context": "Tide from China Part 1, Tokyo 2023", "current_status": "unknown"},
            {"name": "邦乔彦 (Bang Joy)", "context": "Tide from China Part 1, Tokyo 2023", "current_status": "unknown"},
            {"name": "TUOER",            "context": "Tide from China Part 1, Tokyo 2023", "current_status": "unknown"},
            {"name": "HJL",              "context": "Tide from China Part 1, Tokyo 2023", "current_status": "unknown"},
            {"name": "Doakmoon",         "context": "Tide from China Part 1, Tokyo 2023", "current_status": "unknown"},
        ],
        "peer_network": {
            "available": False,
            "reason": "No Tokyo-based peer artist data in the pipeline. The system tracks venues and open calls, not individual artists.",
            "why_it_matters": "Group show invitations at artist-run spaces typically come from peer networks, not cold submissions. 3–5 Tokyo-based illustrators at a similar stage are the most direct path to group show opportunities.",
        },
        "note": "The 5 co-exhibitors from Tide from China are your strongest existing collaboration seeds. Their current Tokyo presence and active practice is unconfirmed — tell Saffron whether you've stayed in contact with any of them.",
    }

    # ── Geographic expansion ──────────────────────────────────────────────────
    country_counts: Counter = Counter()
    for opp in opps:
        c = (opp.get("country") or "").strip()
        if c and c.lower() not in ("unknown", ""):
            country_counts[c] += 1

    uk_count  = sum(v for k, v in country_counts.items() if "uk" in k.lower() or "france" in k.lower() or "germany" in k.lower() or "netherlands" in k.lower())
    us_count  = sum(v for k, v in country_counts.items() if "usa" in k.lower() or "canada" in k.lower() or "us /" in k.lower())
    jp_count  = sum(v for k, v in country_counts.items() if k.lower() in ("japan", "tokyo", "yokohama"))
    global_ct = country_counts.get("Global", 0)

    geographic_expansion = {
        "current_base": "Tokyo, Japan / Beijing, China",
        "pipeline_by_country": [
            {"country": k, "count": v}
            for k, v in sorted(country_counts.items(), key=lambda x: x[1], reverse=True)
            if k not in ("unknown",)
        ],
        "regions": [
            {
                "name": "Japan / Tokyo",
                "pipeline_count": jp_count,
                "status": "primary_base",
                "note": "Core operating territory. The question here is depth, not entry.",
                "entry_point": None,
            },
            {
                "name": "Europe (UK, France, etc.)",
                "pipeline_count": uk_count,
                "status": "medium_term",
                "note": "Strong art book and zine fair ecosystem — Offprint Paris and London are the natural entry points.",
                "entry_point": "Offprint Paris or London — low barrier, direct access to European curators and collectors who buy artist books",
            },
            {
                "name": "North America",
                "pipeline_count": us_count,
                "status": "medium_term",
                "note": "NYC zine culture (Printed Matter) and LA illustration scene. Already in pipeline.",
                "entry_point": "Printed Matter NY Art Book Fair — the highest-profile artist book platform in North America",
            },
            {
                "name": "Global / International (open calls)",
                "pipeline_count": global_ct,
                "status": "active",
                "note": "International open calls and online platforms that accept globally. Actionable now without travel.",
                "entry_point": None,
            },
        ],
    }

    # ── Publication landscape ─────────────────────────────────────────────────
    PUB_CATS = {
        "book_publishing", "zine_print", "bookstore_gallery", "global_artist_book_platform",
        "global_art_book_fair", "zine_shop_consignment", "group_publication_open_call",
        "global_book_arts",
    }
    pub_opps = [o for o in opps if o.get("category", "") in PUB_CATS]
    top_pub_opps = sorted(pub_opps, key=lambda x: x.get("watercolor_adjusted_score", 0), reverse=True)[:10]
    pub_sample = [
        {
            "name": o.get("name", ""),
            "category": o.get("category", ""),
            "country": o.get("country", ""),
            "score": round(o.get("watercolor_adjusted_score", 0), 1),
        }
        for o in top_pub_opps
    ]

    publication_landscape = {
        "artist_publications": [
            {
                "title": "Colour Diary (色彩日記)",
                "year": "2021",
                "type": "Solo illustration collection",
                "note": "First solo published work, grew from daily diary practice",
            },
            {
                "title": "defined Definition 02: A Documented Journey",
                "year": "unknown",
                "type": "Group publication, contributor",
                "note": "Participation confirmed, publication details unverified",
            },
        ],
        "pipeline_count": len(pub_opps),
        "top_targets": pub_sample,
        "tiers": [
            {
                "tier": "Self-publish / zine",
                "barrier": "low",
                "examples": ["Tacoche", "Dig A Hole Zines", "MOUNT ZINE", "ZINEフェス東京"],
                "note": "Tokyo zine culture is active and illustrator-friendly. Fastest route to a new publication credit.",
            },
            {
                "tier": "Bookshop gallery",
                "barrier": "medium",
                "examples": ["UTRECHT", "Book and Sons", "flotsam books", "日記屋 月日"],
                "note": "Accept work from illustrators without gallery representation. Bridges publication and gallery worlds.",
            },
            {
                "tier": "Art book fairs",
                "barrier": "medium",
                "examples": ["Tokyo Art Book Fair", "Fukuoka Art Book Fair", "Offprint"],
                "note": "Table fees required but direct access to collectors and curators who buy artist books.",
            },
            {
                "tier": "Major publishers",
                "barrier": "high",
                "examples": ["torch press", "twelvebooks", "Clavis Publishing"],
                "note": "Relationship-first. Cold submissions rarely land at this level — build toward these over 2–3 years.",
            },
        ],
    }

    # ── Long-term scenarios ───────────────────────────────────────────────────
    long_term_scenarios = {
        "horizon": "Age 30 (approximately 4 years from now)",
        "scenarios": [
            {
                "name": "Gallery Track",
                "tagline": "Primary identity as a gallery artist.",
                "description": "Solo shows, institutional open calls, gallery representation by 30.",
                "requires_now": [
                    "3–5 Tokyo group shows by 2027 — artist-run spaces first (3331, Design Festa Gallery, Gallery IYN)",
                    "One institutional open call (TOKAS, Youkobo, BankART) by 2028",
                    "Consistent gallery attendance — build relationships before cold submissions",
                    "Artist statement developed and refined",
                ],
                "probability": "moderate",
                "bottleneck": "Exhibition history is thin. 2–3 more group shows are required before any gallery will discuss a solo show.",
                "best_fit_signal": "Right if you're primarily motivated by the physical exhibition experience and gallery community.",
            },
            {
                "name": "Publication Track",
                "tagline": "Primary identity as an illustrator and artist-book maker.",
                "description": "Second solo book, international distribution, major book fairs by 30.",
                "requires_now": [
                    "New self-published zine or small book within 12 months — the daily diary content already exists",
                    "Table at Tokyo Art Book Fair 2026 or 2027",
                    "Submission to Offprint or NY Art Book Fair by 2028",
                    "Publisher relationship with torch press or equivalent — start with introduction, not submission",
                ],
                "probability": "high",
                "bottleneck": "No new publication since 2021. The content exists — it needs packaging.",
                "best_fit_signal": "Right if you're motivated by the book as object and the publishing community. Your formation already points here.",
            },
            {
                "name": "Hybrid Track",
                "tagline": "Artist-publisher: books and gallery shows running in parallel.",
                "description": "The book practice feeds the gallery presence and vice versa. Bookshop gallery shows bridge both worlds.",
                "requires_now": [
                    "All Publication Track steps",
                    "2–3 Tokyo group shows in parallel",
                    "Bookshop gallery show as the bridge (UTRECHT or Book and Sons) — satisfies both tracks simultaneously",
                ],
                "probability": "high",
                "bottleneck": "Requires more energy and time management than either single track.",
                "best_fit_signal": "The most natural fit given your existing practice. The daily diary is simultaneously publication material and gallery-worthy work.",
            },
        ],
        "saffron_view": "The Hybrid Track is the best structural fit. The bookshop gallery show is the single highest-leverage action — it advances both tracks with one move.",
    }

    # ── Venue relationship tracker ────────────────────────────────────────────
    crm_path = DATA_DIR / "contact_memory.json"
    crm_raw  = json.loads(crm_path.read_text(encoding="utf-8")) if crm_path.exists() else {}
    crm_list = crm_raw.get("contacts", []) if isinstance(crm_raw, dict) else crm_raw
    crm_list = _normalize_contact_priorities(crm_list)

    venue_tracker = {
        "tracked": [
            {
                "name":           c.get("name", ""),
                "type":           c.get("type", ""),
                "city":           c.get("city", ""),
                "status":         c.get("status", ""),
                "last_contacted": c.get("last_contacted"),
                "priority":       (c.get("crm_analysis") or {}).get("priority", ""),
                "next_action":    (c.get("crm_analysis") or {}).get("next_action", ""),
            }
            for c in crm_list
        ],
        "total": len(crm_list),
        # An "active relationship" is a venue we've actually engaged: contacted at
        # least once, or that has replied. Avoids the misleading hardcoded "0".
        "active": sum(
            1 for c in crm_list
            if c.get("last_contacted") or c.get("response_received")
            or str(c.get("status", "")).lower() in ("contacted", "in_conversation", "active", "responded")
        ),
        "gap_note": (
            f"Only {len(crm_list)} venue{'s' if len(crm_list) != 1 else ''} tracked. "
            "A working relationship map needs 15–20 entries — galleries, bookshops, cafés, and artist spaces. "
            "Each group show, fair, and bookshop visit is a relationship seed that should land here."
        ) if len(crm_list) < 15 else None,
    }

    # ── Open questions ────────────────────────────────────────────────────────
    open_questions = {
        "questions": [
            {
                "question": "What's your current Instagram posting frequency?",
                "why_it_matters": "With a 26k Instagram following, the account is established and growing. Cadence is the most controllable variable for maximising reach on the platform galleries, publishers, and curators actually use for discovery. Without knowing current frequency, no posting strategy can be recommended.",
                "routed_to": "Peppercorn",
            },
            {
                "question": "Where is your audience located geographically?",
                "why_it_matters": "A primarily Chinese-language following changes the geographic expansion strategy entirely — it suggests China reentry before European expansion.",
                "routed_to": "Peppercorn",
            },
            {
                "question": "Have you sold work, and through which channels?",
                "why_it_matters": "Sales history reveals which formats and price points convert — this shapes which fairs and platforms are worth prioritising.",
                "routed_to": "Peppercorn",
            },
            {
                "question": "Is a new publication or zine in progress?",
                "why_it_matters": "If you're already planning one, this should support it — not pitch it as a new idea.",
                "routed_to": "Peppercorn",
            },
            {
                "question": "Do you have a current artist statement in any language?",
                "why_it_matters": "Most open calls and gallery submissions require one. If none exists, this is the most urgent gap before any submissions.",
                "routed_to": "Peppercorn",
            },
            {
                "question": "Are you still in contact with your Tide from China co-exhibitors?",
                "why_it_matters": "If those 5 artists are Tokyo-based and active, they are the most natural group show partners. If they've dispersed, that network is dormant.",
                "routed_to": "Peppercorn",
            },
            {
                "question": "Do you have a second Japan exhibition in progress?",
                "why_it_matters": "There's one show on record, so the read assumes 2–3 more group shows would help — but you may already have one underway. If so, tell me here.",
                "routed_to": "Peppercorn",
            },
            {
                "question": "What price points do you use for originals and prints?",
                "why_it_matters": "Pricing determines which collector tier and which fairs are appropriate. Under-pricing is common at this stage and affects how galleries perceive the work.",
                "routed_to": "Peppercorn",
            },
        ],
        "count": 8,
        "note": "These cannot be answered by observation — only by asking directly. They are flagged for Peppercorn.",
    }
    open_questions["count"] = len(open_questions["questions"])

    # ── Career Momentum Tracker ───────────────────────────────────────────────
    submission_log_path = DATA_DIR / "submission_log.json"
    raw_submissions = []
    if submission_log_path.exists():
        try:
            raw_submissions = json.loads(submission_log_path.read_text(encoding="utf-8"))
            if not isinstance(raw_submissions, list):
                raw_submissions = raw_submissions.get("submissions", [])
        except Exception:
            raw_submissions = []

    contact_mem_path = DATA_DIR / "contact_memory.json"
    raw_contacts = []
    if contact_mem_path.exists():
        try:
            _crm_raw = json.loads(contact_mem_path.read_text(encoding="utf-8"))
            raw_contacts = _crm_raw if isinstance(_crm_raw, list) else _crm_raw.get("contacts", [])
        except Exception:
            raw_contacts = []

    career_events_path = DATA_DIR / "career_events.json"
    raw_career_events = []
    if career_events_path.exists():
        try:
            raw_career_events = json.loads(career_events_path.read_text(encoding="utf-8"))
            if not isinstance(raw_career_events, list):
                raw_career_events = []
        except Exception:
            raw_career_events = []

    from datetime import date as _date, datetime as _datetime
    _today = _date.today()
    _this_ym = _today.strftime("%Y-%m")

    def _parse_ym(s):
        """Return 'YYYY-MM' prefix from a date string, or empty string."""
        s = str(s or "")
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y-%m"):
            try:
                return _datetime.strptime(s[:len(fmt)], fmt).strftime("%Y-%m")
            except ValueError:
                pass
        return s[:7] if len(s) >= 7 else ""

    # Monthly activity buckets — last 6 months
    months_back = 6
    monthly = {}
    for i in range(months_back - 1, -1, -1):
        from datetime import timedelta as _td
        ref = _date(_today.year, _today.month, 1)
        m = ref.month - i
        y = ref.year
        while m <= 0:
            m += 12
            y -= 1
        key = f"{y}-{m:02d}"
        monthly[key] = {"submissions": 0, "contacts": 0, "events": 0}

    for s in raw_submissions:
        ym = _parse_ym(s.get("date") or s.get("submitted_at") or s.get("date_added") or "")
        if ym in monthly:
            monthly[ym]["submissions"] += 1

    for c in raw_contacts:
        ym = _parse_ym(c.get("date_added") or "")
        if ym in monthly:
            monthly[ym]["contacts"] += 1

    for ev in raw_career_events:
        ym = _parse_ym(ev.get("date") or ev.get("timestamp") or "")
        if ym in monthly:
            monthly[ym]["events"] += 1

    this_month_subs = sum(1 for s in raw_submissions if _parse_ym(s.get("date") or s.get("submitted_at") or s.get("date_added") or "").startswith(_this_ym))
    this_month_contacts = monthly.get(_this_ym, {}).get("contacts", 0)
    this_month_events = monthly.get(_this_ym, {}).get("events", 0)

    responses = sum(1 for c in raw_contacts if c.get("response_received") is True)
    contacted = sum(1 for c in raw_contacts if c.get("status") not in ("cold", None, ""))
    response_rate = round((responses / contacted * 100) if contacted else 0)

    # Trajectory: simple heuristic on recent vs prior months
    recent_acts = sum(monthly[k]["submissions"] + monthly[k]["contacts"] + monthly[k]["events"] for k in list(monthly)[-2:])
    prior_acts  = sum(monthly[k]["submissions"] + monthly[k]["contacts"] + monthly[k]["events"] for k in list(monthly)[:4])
    if not raw_submissions and len(raw_contacts) < 5:
        trajectory = "early"
    elif recent_acts > prior_acts * 1.3:
        trajectory = "accelerating"
    elif recent_acts < prior_acts * 0.5:
        trajectory = "stalling"
    else:
        trajectory = "steady"

    # Recent activity — merge submissions + contacts, sort desc
    activity_items = []
    for s in raw_submissions:
        activity_items.append({
            "type": "submission",
            "name": s.get("title") or s.get("opp_title") or s.get("opp_name") or "Submission",
            "date": s.get("date") or s.get("submitted_at") or s.get("date_added") or "",
            "status": s.get("status") or s.get("action") or "submitted",
        })
    # Only contacts she's actually engaged count as activity — a cold venue
    # sitting in the CRM isn't something that "happened".
    _ENGAGED = {"in_contact", "sent_inquiry", "contacted", "responded",
                "ready_to_review", "relationship"}
    for c in raw_contacts:
        if (c.get("status") or "cold") not in _ENGAGED:
            continue
        activity_items.append({
            "type": "contact",
            "name": c.get("name") or "",
            "date": c.get("date_added") or "",
            "status": c.get("status") or "cold",
        })
    for ev in raw_career_events[:20]:
        activity_items.append({
            "type": "career_event",
            "id": ev.get("id"),
            "event_type": ev.get("type", "event"),
            "name": ev.get("note") or ev.get("type", "").replace("_", " ").title(),
            "date": ev.get("date") or (ev.get("timestamp") or "")[:10],
            "status": ev.get("type", "event"),
        })
    activity_items.sort(key=lambda x: x["date"], reverse=True)

    career_momentum = {
        "this_month": {"submissions": this_month_subs, "contacts": this_month_contacts, "events": this_month_events},
        "totals": {
            "submissions": len(raw_submissions),
            "venues_in_crm": len(raw_contacts),
            "career_events": len(raw_career_events),
            "responses_received": responses,
        },
        "response_rate": response_rate,
        "trajectory": trajectory,
        "monthly_chart": [
            {"month": k, "submissions": v["submissions"], "contacts": v["contacts"], "events": v["events"]}
            for k, v in monthly.items()
        ],
        "recent_activity": activity_items[:10],
        "recent_career_events": raw_career_events[:5],
    }

    # ── Timing Intelligence ───────────────────────────────────────────────────
    _MONTH_MAP_TI = {
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12,
        "jan": 1, "feb": 2, "mar": 3, "apr": 4,
        "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }
    _MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]
    _ROLLING_TI = frozenset({"rolling", "ongoing", "year-round", "open submission", "anytime", "proposal-based"})

    def _extract_deadline_months(dl_str):
        s = str(dl_str or "").lower()
        if any(t in s for t in _ROLLING_TI):
            return None, True   # (month_num, is_rolling)
        s_clean = re.sub(r'(\d+)(st|nd|rd|th)\b', r'\1', s)
        found = []
        # ISO / YYYY-MM-DD
        for m in re.finditer(r'20\d{2}[-/](\d{1,2})[-/]\d{1,2}', s_clean):
            try:
                found.append(int(m.group(1)))
            except ValueError:
                pass
        # "Month DD, YYYY" or "DD Month YYYY"
        for word, num in _MONTH_MAP_TI.items():
            if word in s_clean:
                found.append(num)
        if found:
            return max(found), False
        return None, False

    month_buckets = {i: [] for i in range(1, 13)}
    rolling_opps = []
    no_deadline = 0

    for opp in opps:
        dl = opp.get("deadline") or ""
        if not dl or str(dl).strip().lower() in ("", "none", "null", "unknown", "tbd", "n/a"):
            no_deadline += 1
            continue
        month_num, is_rolling = _extract_deadline_months(dl)
        name = opp.get("name") or opp.get("title") or ""
        cat = opp.get("category") or ""
        entry = {"name": name[:60], "category": cat, "deadline": str(dl)[:80]}
        if is_rolling:
            rolling_opps.append(entry)
        elif month_num:
            month_buckets[month_num].append(entry)
        else:
            no_deadline += 1

    monthly_counts = [
        {"month": _MONTH_NAMES[i - 1], "month_num": i,
         "count": len(month_buckets[i]), "top": month_buckets[i][:5]}
        for i in range(1, 13)
    ]
    sorted_by_count = sorted(monthly_counts, key=lambda x: x["count"], reverse=True)
    peak_months   = [m["month"] for m in sorted_by_count[:3] if m["count"] > 0]
    quiet_months  = [m["month"] for m in sorted_by_count if m["count"] == 0][:3]

    timing_intelligence = {
        "total_analyzed":       len(opps),
        "with_parsed_deadline": sum(len(v) for v in month_buckets.values()),
        "rolling_count":        len(rolling_opps),
        "no_deadline_count":    no_deadline,
        "monthly_counts":       monthly_counts,
        "rolling":              rolling_opps[:10],
        "peak_months":          peak_months,
        "quiet_months":         quiet_months,
        "key_insight":          (
            f"{', '.join(peak_months[:2])} {'are' if len(peak_months) >= 2 else 'is'} peak application season "
            "in this pipeline. Prepare materials 4–6 weeks before deadlines cluster."
            if peak_months else
            "Most opportunities have rolling or unspecified deadlines — check each one individually."
        ),
    }

    # ── Opportunity Gap Analysis ──────────────────────────────────────────────
    cat_counter = Counter(o.get("category", "unknown") for o in opps)
    total_opps = len(opps)

    # Expected distribution for a watercolor/illustration artist at Tier 1-2
    # based on what comparable artists' opportunity portfolios look like
    EXPECTED = {
        "gallery":                    {"label": "Galleries",            "expected_pct": 18, "note": "Core relationship-building venues for a Tokyo-based painter."},
        "cafe_gallery":               {"label": "Café Galleries",       "expected_pct": 8,  "note": "Low-barrier first exhibition venues; common for emerging Tokyo artists."},
        "residency":                  {"label": "Residencies",          "expected_pct": 8,  "note": "Production time + institutional credibility; peers typically track 5–10."},
        "editorial_illustration":     {"label": "Editorial / Magazines","expected_pct": 5,  "note": "Most watercolor illustrators this stage have 5–15 editorial leads tracked."},
        "competition_award":          {"label": "Competitions & Awards","expected_pct": 5,  "note": "Competition wins appear on every peer's early CV."},
        "global_watercolor_open_call":{"label": "Watercolor Open Calls","expected_pct": 6,  "note": "Juried watercolor calls are the fastest route to international credibility."},
        "zine_print":                 {"label": "Zines & Print",        "expected_pct": 10, "note": "The most accessible first-presence format for illustration-adjacent artists."},
        "global_grant_fellowship":    {"label": "Grants & Fellowships", "expected_pct": 4,  "note": "Most peers at this stage track 3–8 grants even when not yet eligible."},
    }

    gaps = []
    strengths = []
    for cat_key, meta in EXPECTED.items():
        actual_count = cat_counter.get(cat_key, 0)
        actual_pct   = round(actual_count / total_opps * 100, 1) if total_opps else 0
        expected_count = round(meta["expected_pct"] / 100 * total_opps)
        ratio = actual_count / expected_count if expected_count else 0
        entry = {
            "category":       cat_key,
            "label":          meta["label"],
            "actual_count":   actual_count,
            "expected_count": expected_count,
            "actual_pct":     actual_pct,
            "expected_pct":   meta["expected_pct"],
            "note":           meta["note"],
        }
        if ratio < 0.4:
            entry["status"] = "gap"
            gaps.append(entry)
        elif ratio > 1.5:
            entry["status"] = "strength"
            strengths.append(entry)
        else:
            entry["status"] = "on_track"

    gaps.sort(key=lambda x: x["expected_pct"], reverse=True)
    strengths.sort(key=lambda x: x["actual_count"], reverse=True)

    # Top non-expected categories (where portfolio is actually concentrated)
    top_cats = [
        {"category": k, "count": v}
        for k, v in cat_counter.most_common(8)
        if k not in EXPECTED and k not in ("unknown", "")
    ]

    opportunity_gap = {
        "total":     total_opps,
        "gaps":      gaps,
        "strengths": strengths,
        "top_actual_categories": top_cats,
        "summary":   (
            f"{len(gaps)} category gap{'s' if len(gaps) != 1 else ''} identified. "
            f"{'Editorial illustration and competitions are most underrepresented — both appear on every peer watercolor artist CV at this stage.' if len(gaps) >= 2 else 'Portfolio coverage is broadly on track.'}"
        ),
    }

    # ── Market Stats (computed from full compact_opportunities.json dataset) ──
    # Use cached data (load_opportunities populates _OPP_CACHE from the same file)
    _all_opps_path = DEPLOY_DIR / "compact_opportunities.json"
    if _OPP_CACHE is not None:
        _all_opps = _OPP_CACHE
    else:
        _all_opps_raw = json.loads(_all_opps_path.read_text(encoding="utf-8")) if _all_opps_path.exists() else []
        _all_opps = _all_opps_raw if isinstance(_all_opps_raw, list) else _all_opps_raw.get("items", [])

    _MS_CAT_GROUPS = {
        "Open Calls & Fairs": {
            "fair_popup", "global_open_call", "global_watercolor_open_call",
            "japan_watercolor_open_call", "japan_watercolor_institution",
            "zine_fair_booth", "group_publication_open_call", "photo_open_call",
            "global_photobook", "global_book_arts",
        },
        "Galleries": {
            "gallery", "gallery_small", "gallery_event", "artist_space", "event_space",
        },
        "Zines & Books": {
            "zine_print", "book_publishing", "bookstore_gallery", "bookstore_event",
            "zine_shop_consignment", "global_artist_book_platform", "global_art_book_fair",
        },
        "Residencies & Grants": {
            "residency", "global_residency", "global_grant_fellowship", "residency_beijing",
        },
        "Competitions & Awards": {
            "competition_award", "watercolor_competition", "illustration_prize",
            "emerging_artist_award",
        },
        "Cafes & Bookshop Spaces": {"cafe_gallery"},
    }

    _ms_cat_counts: dict[str, int] = {k: 0 for k in _MS_CAT_GROUPS}
    _ms_cat_counts["Other"] = 0
    for _o in _all_opps:
        _cat = _o.get("category", "")
        _placed = False
        for _grp, _members in _MS_CAT_GROUPS.items():
            if _cat in _members:
                _ms_cat_counts[_grp] += 1
                _placed = True
                break
        if not _placed:
            _ms_cat_counts["Other"] += 1

    _by_category = {k: v for k, v in sorted(_ms_cat_counts.items(), key=lambda x: x[1], reverse=True) if v > 0}

    _medium_counter = Counter(_o.get("native_medium", "unknown") for _o in _all_opps)
    _by_medium = {k: v for k, v in _medium_counter.most_common(8)}

    _country_counter_ms: Counter = Counter()
    for _o in _all_opps:
        _c = (_o.get("country") or "").strip()
        if _c and _c.lower() not in ("unknown", ""):
            _country_counter_ms[_c] += 1
    _by_country = {k: v for k, v in _country_counter_ms.most_common(5)}

    _today2 = datetime.now(timezone.utc).date()
    _within_30 = 0
    _within_90 = 0
    _open_ongoing = 0
    _EMPTY_DL   = frozenset({"", "none", "null", "unknown", "tbd", "n/a", "check site", "varies"})
    _ROLLING_DL = frozenset({"rolling", "ongoing", "year-round", "open submission", "anytime"})
    for _o in _all_opps:
        _dl = str(_o.get("deadline") or "").strip().lower()
        if not _dl or _dl in _EMPTY_DL:
            continue
        if any(_r in _dl for _r in _ROLLING_DL):
            _open_ongoing += 1
            continue
        _parsed_dl = None
        for _fmt in ("%Y-%m-%d", "%B %d, %Y", "%d %B %Y", "%B %Y"):
            try:
                _parsed_dl = datetime.strptime(_dl[:20], _fmt).date()
                break
            except ValueError:
                pass
        if _parsed_dl:
            _diff = (_parsed_dl - _today2).days
            if 0 <= _diff <= 30:
                _within_30 += 1
            if 0 <= _diff <= 90:
                _within_90 += 1

    def _ms_score(o):
        return float(
            o.get("overall_score") or o.get("differentiated_score") or
            o.get("watercolor_adjusted_score") or o.get("dna_adjusted_score") or 0
        )
    _top_tier  = sum(1 for _o in _all_opps if _ms_score(_o) > 8)
    _mid_tier  = sum(1 for _o in _all_opps if 5 <= _ms_score(_o) <= 8)
    _low_tier  = sum(1 for _o in _all_opps if _ms_score(_o) < 5)
    _wc_count  = sum(1 for _o in _all_opps if _o.get("native_medium") in ("painting", "watercolor"))
    _top5      = sorted(_all_opps, key=_ms_score, reverse=True)[:5]
    _top_scored = [
        {
            "name":     (_o.get("name") or _o.get("title") or "")[:60],
            "score":    round(_ms_score(_o), 1),
            "category": _o.get("category", ""),
        }
        for _o in _top5
    ]

    market_stats = {
        "total_opportunities": len(_all_opps),
        "by_category":         _by_category,
        "by_medium":           _by_medium,
        "by_country":          _by_country,
        "deadline_pressure": {
            "this_month":    _within_30,
            "next_3_months": _within_90,
            "open_ongoing":  _open_ongoing,
        },
        "score_distribution": {
            "top_tier":   _top_tier,
            "mid_tier":   _mid_tier,
            "lower_tier": _low_tier,
        },
        "watercolor_specific": _wc_count,
        "top_scored":          _top_scored,
    }

    # ── Patch Instagram strategy with Peppercorn answers ─────────────────────
    _posting = _answers.get("posting_frequency")
    if _posting:
        # Remove the "Posting frequency" item from missing list (answered)
        instagram_strategy["missing"] = [
            m for m in instagram_strategy.get("missing", [])
            if "posting" not in m.get("field", "").lower()
        ]
        instagram_strategy["known"]["posting_frequency"] = _posting

    # A planned new publication is publication intent, not an Instagram posting goal —
    # surface it in the publication landscape where it belongs.
    _pub_answer = _answers.get("new_publication_planned")
    if _pub_answer:
        publication_landscape["artist_intent"] = _pub_answer

    # ── Patch audience geography with Peppercorn answers ─────────────────────
    _geo_answer = _answers.get("audience_geography")
    if _geo_answer:
        audience_geography["available"] = True
        audience_geography["artist_report"] = _geo_answer
        audience_geography["reason"] = None  # no longer unknown

    # ── Live i18n: opportunities already carry translations (name_zh, etc.) ───
    # Build an English -> zh/ja lookup from the opportunity data itself, so the
    # dynamic content (names, one-liners, fit reasons) is translated from the
    # same source the pipeline regenerates each run — no map to hand-maintain.
    _opp_i18n: dict[str, dict] = {"zh": {}, "ja": {}}
    for _o in _all_opps:
        for _en_k, _zh_k, _ja_k in (
            ("name",                "name_zh",        "name_ja"),
            ("one_sentence",        "one_sentence_zh","one_sentence_ja"),
            ("why_this_fits_short", "why_it_fits_zh", "why_it_fits_ja"),
        ):
            _en = (_o.get(_en_k) or "").strip()
            if not _en:
                continue
            if _o.get(_zh_k):
                _opp_i18n["zh"][_en] = _o[_zh_k]
            if _o.get(_ja_k):
                _opp_i18n["ja"][_en] = _o[_ja_k]

    # Merge the engine-generated Saffron string cache (zh for the page's static
    # report text). Opportunity translations above take precedence on overlap.
    _cache_path = DATA_DIR / "translation_cache.json"
    if _cache_path.exists():
        try:
            _cache = json.loads(_cache_path.read_text(encoding="utf-8"))
            for _en, _zh in (_cache.get("zh") or {}).items():
                _opp_i18n["zh"].setdefault(_en, _zh)
        except Exception:
            pass

    return {
        "_i18n":                 _opp_i18n,
        "career_position":       career_position,
        "market_landscape":      market_landscape,
        "peer_artists":          peer_artists,
        "pathway":               pathway,
        "instagram_strategy":    instagram_strategy,
        "audience_geography":    audience_geography,
        "peppercorn_answers":    _answers,
        "career_benchmarks":     career_benchmarks,
        "seasonal_calendar":     seasonal_calendar,
        "press_features":        press_features,
        "collector_ecosystem":   collector_ecosystem,
        "collaboration_map":     collaboration_map,
        "geographic_expansion":  geographic_expansion,
        "publication_landscape": publication_landscape,
        "long_term_scenarios":   long_term_scenarios,
        "venue_tracker":         venue_tracker,
        "open_questions":        open_questions,
        "career_momentum":       career_momentum,
        "timing_intelligence":   timing_intelligence,
        "opportunity_gap":       opportunity_gap,
        "market_stats":          market_stats,
    }


def _live_career_counts() -> dict:
    """Live counts for the Peppercorn progress carousel — no hardcoded numbers.

    - group_shows: confirmed group exhibitions in the artist profile (Tide from
      China) + group_show entries logged via submission_log.json. Evidence-first:
      unconfirmed profile mentions don't count.
    - publications: publications recorded in artist_master_profile career_history.
    - instagram: follower figure from the profile's social_presence block.
    """
    amp_path = DATA_DIR / "artist_master_profile.json"
    amp = json.loads(amp_path.read_text(encoding="utf-8")) if amp_path.exists() else {}
    ch = amp.get("career_history", {})

    confirmed_groups = sum(
        1 for ex in ch.get("exhibitions", [])
        if "group" in (ex.get("type") or "").lower()
        and (ex.get("confidence") or "").lower().startswith("confirmed")
    )
    sub_path = DATA_DIR / "submission_log.json"
    logged_groups = 0
    if sub_path.exists():
        try:
            subs = json.loads(sub_path.read_text(encoding="utf-8"))
            if isinstance(subs, dict):
                subs = subs.get("submissions", [])
            logged_groups = sum(1 for s in subs if (s.get("type") or "") == "group_show")
        except Exception:
            logged_groups = 0

    publications = len(ch.get("publications", []))

    ig = (amp.get("social_presence", {}) or {}).get("instagram", {}) or {}
    return {
        "group_shows":          confirmed_groups + logged_groups,
        "group_shows_target":   3,
        "publications":         publications,
        "publications_target":  3,
        "instagram_followers":  ig.get("followers") or "—",
        "instagram_approx":     ig.get("followers_approx"),
        "instagram_target":     ig.get("next_milestone") or 50000,
    }


@app.get("/api/peppercorn")
def get_peppercorn():
    ppath = DATA_DIR / "peppercorn_profile.json"
    if ppath.exists():
        prof = json.loads(ppath.read_text(encoding="utf-8"))
        prof["live_counts"] = _live_career_counts()
        return prof
    # Build defaults from artist_master_profile
    mpath = DATA_DIR / "artist_master_profile.json"
    master = json.loads(mpath.read_text(encoding="utf-8")) if mpath.exists() else {}
    vp = master.get("visual_profile", {})
    return {
        "last_updated": None,
        "live_counts": _live_career_counts(),
        "priorities": {
            "active_tiers": [1, 2],
            "primary_track": "hybrid",
            "avoid": [],
        },
        "artist_statement": (
            "My work is about stillness as subject — the atmosphere of ordinary places, "
            "interior light and the texture of daily life. "
            "I return to memory held in domestic space, to the city seen through quiet attention. "
            "Watercolor as a medium of slow observation. "
            "Cross-cultural seeing: a Chinese artist in Tokyo."
        ),
        "goals": [],
        "preferences": {
            "geo_focus": ["tokyo", "international"],
            "fee_tolerance": "low",
            "surface_more": ["zines_books", "open_calls"],
            "surface_less": [],
        },
        "saffron_answers": {
            "posting_frequency":       None,
            "audience_geography":      None,
            "has_sold_work":           None,
            "new_publication_planned": None,
            "has_artist_statement":    None,
            "tide_china_contact":      None,
            "second_exhibition_planned": None,
            "price_points":            None,
        },
    }


@app.post("/api/peppercorn")
async def save_peppercorn(request: Request):
    payload = await request.json()
    payload["last_updated"] = datetime.now(timezone.utc).isoformat()
    ppath = DATA_DIR / "peppercorn_profile.json"
    ppath.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "last_updated": payload["last_updated"]}


@app.post("/api/saffron_answer")
async def save_saffron_answer(request: Request):
    """Inline answer to one of Saffron's open questions — writes a single
    saffron_answers field into peppercorn_profile.json (the real store)."""
    payload = await request.json()
    key = (payload.get("key") or "").strip()
    value = payload.get("value")
    if not key:
        return {"ok": False, "error": "missing key"}
    ppath = DATA_DIR / "peppercorn_profile.json"
    profile = json.loads(ppath.read_text(encoding="utf-8")) if ppath.exists() else {}
    answers = profile.get("saffron_answers") or {}
    answers[key] = value
    profile["saffron_answers"] = answers
    profile["last_updated"] = datetime.now(timezone.utc).isoformat()
    ppath.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True}


@app.get("/api/career_events")
def get_career_events():
    path = DATA_DIR / "career_events.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


@app.post("/api/career_events")
async def add_career_event(request: Request):
    entry = await request.json()
    path = DATA_DIR / "career_events.json"
    log = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    entry["id"] = f"{entry.get('type','event')}-{len(log)}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    entry.setdefault("date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    log.insert(0, entry)  # newest first
    path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "entry": entry}


@app.patch("/api/career_events/{event_id}")
async def update_career_event(event_id: str, request: Request):
    """Attach or edit the note on an already-logged event."""
    payload = await request.json()
    path = DATA_DIR / "career_events.json"
    if not path.exists():
        return {"ok": False, "error": "no log"}
    log = json.loads(path.read_text(encoding="utf-8"))
    for ev in log:
        if ev.get("id") == event_id:
            if "note" in payload:
                ev["note"] = (payload.get("note") or "").strip()
            path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
            return {"ok": True, "entry": ev}
    return {"ok": False, "error": "not found"}


@app.delete("/api/career_events/{event_id}")
def delete_career_event(event_id: str):
    """Remove a logged event (e.g. a test entry) by id."""
    path = DATA_DIR / "career_events.json"
    if not path.exists():
        return {"ok": False, "error": "no log"}
    log = json.loads(path.read_text(encoding="utf-8"))
    kept = [ev for ev in log if ev.get("id") != event_id]
    path.write_text(json.dumps(kept, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "removed": len(log) - len(kept)}


@app.get("/api/exhibition_log")
def get_exhibition_log():
    path = DATA_DIR / "exhibition_log.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


@app.post("/api/exhibition_log")
async def add_exhibition(request: Request):
    entry = await request.json()
    path = DATA_DIR / "exhibition_log.json"
    log = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    entry["id"] = entry.get("id") or f"{entry.get('date','')}-{entry.get('venue','').replace(' ','_')[:20]}-{len(log)}"
    entry["logged_at"] = datetime.now(timezone.utc).isoformat()
    log.append(entry)
    path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "entry": entry}


@app.delete("/api/exhibition_log/{entry_id}")
def delete_exhibition(entry_id: str):
    path = DATA_DIR / "exhibition_log.json"
    if not path.exists():
        return {"ok": True}
    log = json.loads(path.read_text(encoding="utf-8"))
    log = [e for e in log if e.get("id") != entry_id]
    path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True}


@app.get("/api/today")
def get_today():
    items = load_opportunities()

    # ── High Impact Move: highest-scoring IBM-eligible ────────────────────────
    ibm = [
        x for x in sorted(items, key=_ranked_score, reverse=True)
        if x.get("exclusive_primary_bucket") == "immediate_best_moves"
        and _ibm_eligible(x)
    ]
    high_impact_raw = ibm[0] if ibm else None

    # ── Quick Win: IBM-eligible relationship-type with confirmed contact/email ─
    qw_candidates = [
        x for x in ibm
        if x.get("category") in _RELATIONSHIP_CATS
        and (
            (x.get("contact") and "@" in str(x.get("contact", "")))
            or x.get("contact_verified")
        )
        and (high_impact_raw is None or _opp_id(x) != _opp_id(high_impact_raw))
    ]
    # If no relationship IBM, widen to any low-effort verified contact.
    # Same staleness gate as IBM: a venue whose only deadline is months past
    # must not be served as today's action (Verification > ranking).
    if not qw_candidates:
        qw_candidates = [
            x for x in items
            if x.get("category") in _RELATIONSHIP_CATS
            and x.get("contact") and "@" in str(x.get("contact", ""))
            and not _deadline_past(x)
            and (high_impact_raw is None or _opp_id(x) != _opp_id(high_impact_raw))
        ]
    qw_candidates.sort(key=_ranked_score, reverse=True)
    quick_win_raw = qw_candidates[0] if qw_candidates else None

    used_ids = {_opp_id(x) for x in [high_impact_raw, quick_win_raw] if x}

    # ── Stretch Goal: highest-scoring stretch_target that is NOT Tier 4 ─────────
    # Tier 4 items (RWS, ACC, Cité Internationale, Printed Matter…) must never appear
    # in Today's Focus. The stretch slot is for "one step toward a future target",
    # not for acting on a Tier 4 opportunity directly.
    _TIER4_KEYWORDS = frozenset({
        "royal watercolour society", "rws open", "american watercolor society",
        "cite internationale des arts", "cité internationale des arts",
        "asian cultural council", "acc 20", "printed matter", "offprint",
    })

    def _is_tier4(opp: dict) -> bool:
        name_lower = (opp.get("name") or opp.get("title") or "").lower()
        if any(kw in name_lower for kw in _TIER4_KEYWORDS):
            return True
        if opp.get("career_tier") == 4 or str(opp.get("tier", "")) == "4":
            return True
        return False

    # All stretch slots share the staleness gate: a fellowship whose deadline
    # passed seven months ago is not "one step toward a future target" — it's
    # noise that erodes trust in the whole Focus panel.
    stretch_candidates = sorted(
        [
            x for x in items
            if x.get("exclusive_primary_bucket") == "stretch_targets"
            and _opp_id(x) not in used_ids
            and not _is_tier4(x)
            and not _deadline_past(x)
        ],
        key=_overall_score, reverse=True,
    )
    # Fallback 1: Tier-4 stretch targets (better than nothing)
    if not stretch_candidates:
        stretch_candidates = sorted(
            [x for x in items if x.get("exclusive_primary_bucket") == "stretch_targets"
             and _opp_id(x) not in used_ids and not _deadline_past(x)],
            key=_overall_score, reverse=True,
        )
    # Fallback 2: highest-scoring watch-list item (non-Tier-4 preferred)
    if not stretch_candidates:
        watch_items = [
            x for x in items
            if x.get("exclusive_primary_bucket") in {"watch_list", "research_needed"}
            and _opp_id(x) not in used_ids
            and not _is_tier4(x)
            and not _deadline_past(x)
        ]
        stretch_candidates = sorted(watch_items, key=_overall_score, reverse=True)
    # Final fallback: any remaining non-Tier-4 item
    if not stretch_candidates:
        stretch_candidates = sorted(
            [x for x in items if _opp_id(x) not in used_ids and not _is_tier4(x)
             and not _deadline_past(x)],
            key=_overall_score, reverse=True,
        )
    stretch_raw = stretch_candidates[0] if stretch_candidates else None

    # ── CRM follow-up: if a contact is "in_contact" and last_contacted > 30 days, override quick_win ──
    crm_followup_raw = None
    if CONTACTS_PATH.exists():
        crm_data = json.loads(CONTACTS_PATH.read_text(encoding="utf-8"))
        crm_list = crm_data.get("contacts", []) if isinstance(crm_data, dict) else crm_data
        today_dt = datetime.now(timezone.utc)
        for contact in crm_list:
            if contact.get("status") != "in_contact":
                continue
            lc = contact.get("last_contacted", "")
            if not lc:
                # Never contacted — surface as follow-up
                crm_followup_raw = contact
                break
            # A malformed / non-ISO date is *unknown*, not overdue. Only a
            # genuinely old, parseable date surfaces as a stale follow-up —
            # otherwise a junk last_contacted value would spam the Quick Win.
            if is_overdue_followup(lc, now=today_dt):
                crm_followup_raw = contact
                break

    def _card(opp, role, label, time_est):
        if opp is None:
            return None
        c = shape_card(opp)
        # Evergreen relationship venues pass the eligibility gate on verified
        # contact alone — but a stale deadline field on such a venue is event
        # residue, not an action date. Never display it as one.
        if c.get("deadline_past") and opp.get("category") in _RELATIONSHIP_CATS:
            c["deadline"] = ""
            c["deadline_past"] = False
        c["today_role"]  = role
        c["today_label"] = label
        c["time_est"]    = time_est
        return c

    # ── Submission follow-up: pending application, 14–90 days old, not yet
    # followed up → becomes today's Quick Win. This is the systemic loop the
    # system lacked: "applied" used to be a dead end. Computed fresh from
    # submission_log.json on every request; marking followed_up (PATCH
    # /api/submissions/{id}) or recording an outcome clears it automatically.
    def _submission_followup_raw():
        if not SUBMISSIONS_PATH.exists():
            return None
        try:
            subs = json.loads(SUBMISSIONS_PATH.read_text(encoding="utf-8"))
            if not isinstance(subs, list):
                subs = subs.get("submissions", [])
        except Exception:
            return None
        now = datetime.now(timezone.utc)
        due = []
        for s in subs:
            if (s.get("outcome") or "pending").lower() not in ("pending", "applied", "submitted"):
                continue
            if s.get("followed_up"):
                continue
            try:
                d = datetime.fromisoformat(str(s.get("date", ""))[:10]).replace(tzinfo=timezone.utc)
            except Exception:
                continue
            days = (now - d).days
            if 14 <= days <= 90:
                due.append((days, s))
        if not due:
            return None
        due.sort(key=lambda x: -x[0])  # longest-waiting first
        return due[0]

    def _submission_card(days, sub):
        venue = sub.get("venue", "")
        what = sub.get("what", "")
        return {
            "id":          sub.get("id", ""),
            "name":        venue,
            "today_role":  "quick_win",
            "today_label": "Follow-up",
            "time_est":    "5 min",
            "summary": (
                f"You applied to {venue} ({what}) {days} days ago and haven't heard back. "
                "A short, polite check-in is appropriate now."
            ),
            "summary_zh": f"你在 {days} 天前向 {venue} 提交了申请（{what}），尚未收到回复。现在可以礼貌地跟进一下。",
            "summary_ja": f"{venue}（{what}）に応募してから{days}日が経ちました。丁寧なフォローアップを送るのに良いタイミングです。",
            "submission_followup": True,
            "submission_days": days,
        }

    def _crm_card(contact):
        if contact is None:
            return None
        lc = contact.get("last_contacted", "")
        days_note = ""
        if lc:
            try:
                lc_dt = datetime.fromisoformat(lc.replace("Z", "+00:00"))
                if lc_dt.tzinfo is None:
                    lc_dt = lc_dt.replace(tzinfo=timezone.utc)
                days_ago = (datetime.now(timezone.utc) - lc_dt).days
                days_note = f" — {days_ago} days since last contact"
            except Exception:
                pass
        return {
            "name": contact.get("name", ""),
            "city": contact.get("city", ""),
            "today_role": "quick_win",
            "today_label": "Follow-up",
            "time_est": "5 min",
            "summary": f"You're in contact with {contact.get('name', '')} but haven't followed up recently{days_note}. Send a short check-in.",
            "why_card": contact.get("notes", ""),
            "official_website": contact.get("official_website", ""),
            "crm_followup": True,
            "crm_status": contact.get("status", ""),
        }

    # Quick-win precedence: overdue application follow-up (most time-boxed)
    # → stale CRM relationship → regular best quick win.
    _sub_due = _submission_followup_raw()
    quick_win_card = (
        (_submission_card(*_sub_due) if _sub_due else None)
        or _crm_card(crm_followup_raw)
        or _card(quick_win_raw, "quick_win", "Quick Win", "5 min")
    )

    return {
        "quick_win":    quick_win_card,
        "high_impact":  _card(high_impact_raw,"high_impact",  "High Impact Move",   "30–60 min"),
        "stretch_goal": _card(stretch_raw,    "stretch_goal", "Stretch Goal",       "longer term"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


# ── Issue reports — the artist's direct line to the maintainer ───────────────
# Anything she reports lands here; check_attention.py turns open issues into
# reports/NEEDS_ATTENTION.md so a Claude session can be pointed at them.

ISSUES_PATH = DATA_DIR / "user_reported_issues.json"


class IssueReport(BaseModel):
    text: str
    page: str = ""
    lang: str = ""


@app.post("/api/issues")
def report_issue(issue: IssueReport):
    if not issue.text.strip():
        raise HTTPException(status_code=400, detail="empty report")
    records = []
    if ISSUES_PATH.exists():
        records = json.loads(ISSUES_PATH.read_text(encoding="utf-8"))
    records.append({
        "id":     hashlib.md5(f"{datetime.now(timezone.utc).isoformat()}{issue.text}".encode()).hexdigest()[:8],
        "ts":     datetime.now(timezone.utc).isoformat(),
        "page":   issue.page,
        "lang":   issue.lang,
        "text":   issue.text.strip()[:2000],
        "status": "open",
    })
    ISSUES_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "open": sum(1 for r in records if r.get("status") == "open")}


@app.get("/api/issues")
def list_issues():
    if ISSUES_PATH.exists():
        return json.loads(ISSUES_PATH.read_text(encoding="utf-8"))
    return []


@app.get("/api/health")
def health():
    return {"status": "ok"}


# ── GitHub webhook — auto-deploy on push to main ──────────────────────────────

WEBHOOK_SECRET   = os.environ.get("MOCHI_WEBHOOK_SECRET", "")
DEPLOY_SCRIPT    = Path(__file__).parent / "scripts" / "deploy_from_git.sh"

def _run_deploy():
    if DEPLOY_SCRIPT.exists():
        subprocess.Popen(["bash", str(DEPLOY_SCRIPT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

@app.post("/webhook/deploy")
async def webhook_deploy(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    if WEBHOOK_SECRET:
        sig = request.headers.get("X-Hub-Signature-256", "")
        expected = "sha256=" + hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            raise HTTPException(status_code=403, detail="Invalid signature")
    event = request.headers.get("X-GitHub-Event", "")
    if event == "push":
        background_tasks.add_task(_run_deploy)
    return {"status": "ok", "event": event}


@app.get("/api/career_strategy")
def get_career_strategy():
    path = DATA_DIR / "career_strategy_report.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="career_strategy_report.json not found — run engines/career_strategy_engine.py first")
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8001, reload=False)
