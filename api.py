import sys
import json
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.stdout.reconfigure(encoding="utf-8")

app = FastAPI(title="Mochi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).parent / "memory"

SECTION_CATEGORIES = {
    "open_calls":          {"fair_popup", "institutional"},
    "zines_and_print":     {"zine_print", "bookstore_gallery", "bookstore_event"},
    "relationship_targets": {"gallery", "cafe_gallery", "artist_space", "event_space", "gallery_event", "market_event"},
    "watch_list":          {"residency"},
}

SECTION_META = {
    "immediate_best_moves": {
        "label": "Immediate Best Moves",
        "description": "Mochi's highest-signal picks for your current stage. Act on these before anything else.",
    },
    "open_calls": {
        "label": "Open Calls by Deadline",
        "description": "Spaces that run periodic open submissions. Deadlines are unverified — confirm before applying.",
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
        "description": "Residencies and institutions to prepare for. Tier 3 — not yet, but worth tracking.",
    },
}


def effort_label(raw: str) -> str:
    d = str(raw).lower()
    if "low" in d or "easy" in d:
        return "Easy"
    if "medium" in d or "moderate" in d:
        return "Medium"
    if "high" in d or "demand" in d:
        return "Heavy"
    return "Check"


def email_zh(organization: str, category: str) -> str:
    is_zine = category in {"zine_print", "bookstore_gallery", "bookstore_event"}
    is_residency = category in {"residency", "institutional"}

    if is_zine:
        ask = "艺术书籍或ZINE的寄售合作"
    elif is_residency:
        ask = "驻留项目及申请方式"
    else:
        ask = "展览提案或公开征集"

    return f"""主题：艺术家合作咨询

{organization} 负责人您好，

您好！我是GEGYjiji，一位旅居东京的水彩艺术家。我的创作主要关注城市风景、建筑空间、日常室内环境与光线，以及那些静谧的、承载记忆的空间氛围。

我对贵方的空间与项目很感兴趣，希望进一步了解{ask}相关的合作可能。

您可以在Twitter（@GEGYjiji）上看到我的近期作品。如需作品集PDF或艺术家简介，我可以随时发送。

期待您的回复，感谢您的时间。

GEGYjiji
[portfolio link]"""


def email_ja(organization: str, category: str) -> str:
    is_zine = category in {"zine_print", "bookstore_gallery", "bookstore_event"}
    is_residency = category in {"residency", "institutional"}

    if is_zine:
        ask = "アーティストブックや作品のコンサインメント販売について"
    elif is_residency:
        ask = "レジデンシープログラムやご応募方法について"
    else:
        ask = "展覧会のご提案やオープンコールについて"

    return f"""件名：アーティストとしてのご連絡

{organization} ご担当者様

はじめまして。私はGEGYjiji（ゲジジ）と申します。東京を拠点に活動しているウォーターカラーアーティストです。都市の風景、建築、日常の静かな空間や光をテーマに透明水彩で制作しています。

貴スペースの活動に大変共感し、ご連絡いたしました。{ask}についてお伺いできればと思います。

作品はSNSでもご確認いただけます（Twitter: @GEGYjiji）。ポートフォリオも添付、またはご要望があればお送りいたします。

ご多忙のところ恐れ入りますが、ご検討のほどどうぞよろしくお願いいたします。

GEGYjiji
[portfolio link]"""


def email_en(organization: str, category: str) -> str:
    is_zine = category in {"zine_print", "bookstore_gallery", "bookstore_event"}
    is_residency = category in {"residency", "institutional"}

    if is_zine:
        ask = "artist book or zine consignment / stocking"
    elif is_residency:
        ask = "residency programs and how to apply"
    else:
        ask = "exhibition proposals or open calls"

    return f"""Subject: Artist inquiry — GEGYjiji

Dear {organization} team,

My name is GEGYjiji, a watercolor artist based in Tokyo. I work with urban atmospheres, architectural spaces, domestic interiors, and the quiet accumulation of memory — mostly in watercolor on a small, intimate scale.

I came across your space and was drawn to what you do. I would love to learn more about {ask} and whether my work might be a fit.

You can see my work on Twitter (@GEGYjiji). I am happy to send a portfolio PDF or artist statement on request.

Thank you for your time.

GEGYjiji
[portfolio link]"""


def shape_card(opp: dict) -> dict:
    cr = opp.get("council_review", {})
    cc = cr.get("compact_card", {})
    aim = opp.get("artist_intelligence_match", {})
    pv = cr.get("protective_voice", {})
    category = opp.get("category", "")

    return {
        "id": opp.get("id", ""),
        "name": opp.get("name", ""),
        "organization": opp.get("organization", ""),
        "category": category,
        "city": opp.get("city", ""),
        "country": opp.get("country", ""),
        "deadline": opp.get("deadline", ""),
        "fees": opp.get("fees", ""),
        "score": opp.get("compound_career_score", 0),
        "overall_score": cr.get("overall_score", 0),
        "friction_level": opp.get("friction_level", ""),
        "effort": effort_label(cr.get("difficulty", "")),
        "source_status": opp.get("source_status", ""),
        "official_website": opp.get("official_website", ""),
        "submission_page": opp.get("submission_page", ""),
        # Collapsed summary (one line)
        "summary": cc.get("one_sentence") or aim.get("suggested_display_summary", "")[:160],
        # Expanded body
        "overview": cc.get("one_sentence", ""),
        "why_it_fits": cc.get("why_this_fits_short") or aim.get("why_this_might_fit", ""),
        "what_to_verify": aim.get("what_to_verify_first", []),
        "next_action": aim.get("suggested_next_action", ""),
        "soft_warning": pv.get("softer_summary", ""),
        "bullets": cc.get("three_bullets", []),
        # Email drafts (Chinese first — artist's primary language)
        "email_zh": email_zh(opp.get("organization") or opp.get("name", ""), category),
        "email_ja": email_ja(opp.get("organization") or opp.get("name", ""), category),
        "email_en": email_en(opp.get("organization") or opp.get("name", ""), category),
    }


def load_opportunities() -> list:
    path = DATA_DIR / "opportunities.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    items = raw if isinstance(raw, list) else raw.get("opportunities", raw.get("items", []))
    return [x for x in items if x.get("visibility") != "hidden"]


def bucket(items: list) -> dict:
    scored = sorted(items, key=lambda x: float(x.get("compound_career_score") or 0), reverse=True)

    used: set[str] = set()

    # Immediate best moves: top 5 by score, any category
    best = scored[:5]
    used.update(x["id"] for x in best)

    buckets: dict[str, list] = {"immediate_best_moves": [shape_card(x) for x in best]}

    for key, cats in SECTION_CATEGORIES.items():
        section = [x for x in scored if x.get("category") in cats and x["id"] not in used]
        used.update(x["id"] for x in section)
        buckets[key] = [shape_card(x) for x in section]

    # Anything not bucketed → watch list too
    leftover = [shape_card(x) for x in scored if x["id"] not in used]
    buckets["watch_list"] = buckets.get("watch_list", []) + leftover

    return buckets


@app.get("/api/opportunities")
def get_opportunities():
    items = load_opportunities()
    buckets = bucket(items)
    return {
        "meta": SECTION_META,
        "sections": buckets,
        "total": sum(len(v) for v in buckets.values()),
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

    # Remove any prior entry for the same opp so state is always current
    records = [r for r in records if r.get("opp_id") != payload.opp_id]
    records.append({
        "opp_id":    payload.opp_id,
        "action":    payload.action,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    feedback_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "opp_id": payload.opp_id, "action": payload.action}


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
