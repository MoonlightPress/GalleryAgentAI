import sys
import json
import hashlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.stdout.reconfigure(encoding="utf-8")

app = FastAPI(title="Mochi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:5174", "http://127.0.0.1:5174",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

DATA_DIR   = Path(__file__).parent / "memory"
DEPLOY_DIR = Path(__file__).parent / "deploy_data"

# Category → section mapping (covers all categories present in compact_opportunities)
SECTION_CATEGORIES = {
    "open_calls": {
        "fair_popup", "institutional",
        "global_open_call", "global_watercolor_open_call", "japan_watercolor_open_call",
        "japan_watercolor_institution", "zine_fair_booth", "global_art_book_fair",
        "global_book_arts", "group_publication_open_call", "global_photobook",
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
    return d not in _DEADLINE_PLACEHOLDERS and len(d) > 4


def _real_submission_page(opp: dict) -> bool:
    sp  = (opp.get("submission_page") or "").strip()
    ow  = (opp.get("official_website") or "").strip()
    if not sp or sp == ow:
        return False
    return any(kw in sp.lower() for kw in _SUBMISSION_KEYWORDS)


def _ibm_eligible(opp: dict) -> bool:
    if opp.get("status") == "permanently_closed":
        return False
    if _confirmed_deadline(opp):
        return True
    if _real_submission_page(opp):
        return True
    if opp.get("category") in _RELATIONSHIP_CATS and opp.get("contact_verified"):
        return True
    return False


# ── Helpers ───────────────────────────────────────────────────────────────────

def _opp_id(opp: dict) -> str:
    raw = opp.get("id") or opp.get("title") or opp.get("name") or ""
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def _opp_name(opp: dict) -> str:
    return opp.get("title") or opp.get("name") or ""


def _overall_score(opp: dict) -> float:
    return float(
        opp.get("overall_score")
        or opp.get("differentiated_score")
        or opp.get("watercolor_adjusted_score")
        or opp.get("dna_adjusted_score")
        or 0
    )


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


def email_zh(organization: str, category: str) -> str:
    kind = _email_category(category)
    ask = {"zine": "艺术书籍或ZINE的寄售合作",
           "residency": "驻留项目及申请方式"}.get(kind, "展览提案或公开征集")
    return f"""主题：艺术家合作咨询

{organization} 负责人您好，

您好！我是GEGYjiji，一位旅居东京的水彩艺术家。我的创作主要关注城市风景、建筑空间、日常室内环境与光线，以及那些静谧的、承载记忆的空间氛围。

我对贵方的空间与项目很感兴趣，希望进一步了解{ask}相关的合作可能。

您可以在Twitter（@GEGYjiji）上看到我的近期作品。如需作品集PDF或艺术家简介，我可以随时发送。

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

作品はSNSでもご確認いただけます（Twitter: @GEGYjiji）。ポートフォリオも添付、またはご要望があればお送りいたします。

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

You can see my work on Twitter (@GEGYjiji). I am happy to send a portfolio PDF or artist statement on request.

Thank you for your time.

GEGYjiji
[portfolio link]"""


def shape_card(opp: dict) -> dict:
    category = opp.get("category", "")
    org      = opp.get("organization") or _opp_name(opp)
    name     = _opp_name(opp)
    score    = _overall_score(opp)

    return {
        "id":              _opp_id(opp),
        "name":            name,
        "organization":    org,
        "category":        category,
        "city":            opp.get("city", ""),
        "country":         opp.get("country", ""),
        "deadline":        opp.get("deadline", ""),
        "fees":            opp.get("fees", ""),
        "score":           score,
        "overall_score":   score,
        "official_website": opp.get("official_website", ""),
        "submission_page": opp.get("submission_page", ""),
        "effort":          "",   # compact_opportunities doesn't carry effort
        # Card text
        "summary":         opp.get("one_sentence", "")[:180],
        "overview":        opp.get("one_sentence", ""),
        "why_it_fits":     opp.get("why_this_fits_short", ""),
        "next_action":     opp.get("quick_action", ""),
        "soft_warning":    opp.get("verification_summary", ""),
        "what_to_verify":  opp.get("missing_fields", []),
        "bullets":         [],
        # Email drafts
        "email_zh": email_zh(org, category),
        "email_ja": email_ja(org, category),
        "email_en": email_en(org, category),
    }


def by_display_score(cards: list) -> list:
    return sorted(cards, key=lambda c: float(c.get("overall_score") or 0), reverse=True)


def load_opportunities() -> list:
    path = DEPLOY_DIR / "compact_opportunities.json"
    raw  = json.loads(path.read_text(encoding="utf-8"))
    items = raw if isinstance(raw, list) else raw.get("items", [])
    # Exclude permanently closed and reject-bucketed items
    return [
        x for x in items
        if x.get("exclusive_primary_bucket") not in {"reject", "low_priority"}
        and x.get("status") != "permanently_closed"
    ]


def bucket(items: list) -> dict:
    # Sort by overall score descending as base order
    scored = sorted(items, key=_overall_score, reverse=True)

    used: set[str] = set()
    buckets: dict[str, list] = {}

    # ── Immediate Best Moves: pipeline-flagged IBM that pass eligibility gate ──
    ibm_candidates = [
        x for x in scored
        if x.get("exclusive_primary_bucket") == "immediate_best_moves"
        and _ibm_eligible(x)
    ]
    used.update(_opp_id(x) for x in ibm_candidates)
    buckets["immediate_best_moves"] = by_display_score([shape_card(x) for x in ibm_candidates])

    # ── Category sections ────────────────────────────────────────────────────
    for key, cats in SECTION_CATEGORIES.items():
        section = [
            x for x in scored
            if x.get("category") in cats and _opp_id(x) not in used
            and x.get("exclusive_primary_bucket") not in {"stretch_targets"}
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
    return {
        "meta":     SECTION_META,
        "sections": buckets,
        "total":    sum(len(v) for v in buckets.values()),
    }


VALID_ACTIONS = {"follow", "applied", "maybe_later", "not_for_me"}


class FeedbackPayload(BaseModel):
    opp_id: str
    action: str


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
    return {"ok": True, "opp_id": payload.opp_id, "action": payload.action}


@app.get("/api/saffron")
def get_saffron():
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
        ],
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
            {"platform": "Twitter / X", "handle": "@GegYjiji", "followers": "~90k", "posts": None},
            {"platform": "Instagram",   "handle": "@gegyjiji",  "followers": "21k",  "posts": 35},
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
                "detail": "Artist-run spaces are the natural path: 3331 Arts Chiyoda, Design Festa Gallery, Gallery IYN. Each show builds credibility and introduces her work to gallery directors.",
            },
            {
                "n": 4,
                "label": "Bookshop gallery exhibition",
                "done": False,
                "blocking": False,
                "detail": "UTRECHT, Book and Sons, or flotsam books. Bridges illustration community into gallery context — a natural fit given her publication background.",
            },
            {
                "n": 5,
                "label": "Second publication or new zine",
                "done": False,
                "blocking": False,
                "detail": "Builds presence in the Tokyo zine and book ecosystem. Creates a natural entrypoint for bookshop gallery conversations and strengthens the publication half of her CV.",
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
        "blocking_now": "Only 1 confirmed group show in Japan. Most Tokyo galleries consider 2–3 group exhibition credits a minimum before a solo conversation. The next group show is the highest-leverage move right now.",
        "next_move": "Apply for a second group show at a Tokyo artist-run space. 3331 Arts Chiyoda open calls, Design Festa Gallery curated shows, and Gallery IYN open submissions are the realistic near-term entries. Any of these, confirmed and attended, advances the pathway.",
    }

    return {
        "career_position": career_position,
        "market_landscape": market_landscape,
        "peer_artists": peer_artists,
        "pathway": pathway,
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
