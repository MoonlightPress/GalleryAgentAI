"""
why_hook.py — what makes a "why this fits you" line actually about her.

One source of truth, shared by the generator (engines/why_it_fits_engine.py)
and the serve-time guard (api.py shape_card). The rule, from the 2026-09-04
prose review's top finding:

    Every why-line must contain at least one clause that could only have
    been written about HER.

"A Tokyo gallery showing emerging artists" is a catalog sentence — true of
any painter alive. "Your daily watercolor diary" is not. So a line earns
its place on the card face when it carries either

  * a STRONG anchor — something unique to her record or situation
    (Colour Diary, the diary practice, her Instagram audience, N2 Japanese,
    Beijing/Shanghai/Changsha, her solo shows, being a student), or

  * a possessive anchor — a second-person marker sitting next to one of her
    practice words ("your watercolor", "你的日记", "あなたの水彩").

Bare category words fail on purpose: 水彩 inside "a competition suitable for
watercolor and illustration artists" is describing the contest, not her.

Detection works in English, Simplified Chinese and Japanese because her page
is Chinese by default — a hook that survives only in the English source is a
hook she never reads.
"""
import re

# ── Strong anchors: true of her and effectively no one else ────────────────
# Kept lowercase; matching is case-insensitive on a lowercased string.
STRONG_ANCHORS = (
    # the book and the practice it grew from
    "colour diary", "color diary", "色彩日记", "色彩日記",
    "daily diary", "diary practice", "日记", "日記",
    # audience
    "instagram", "followers", "粉丝", "关注者", "フォロワー", "インスタ",
    # languages
    "jlpt", "n2", "日语", "日本語能力", "中文",
    # citizenship — eligibility that turns on who she is, not what she makes.
    # The bare word "chinese" is too broad (any Chinese-art venue trips it);
    # these phrases only appear when the line is about her passport.
    "chinese national", "chinese citizen", "mainland china",
    "中国国籍", "中国大陆", "中国籍",
    # where she comes from and where she has shown
    "beijing", "shanghai", "changsha", "harajuku", "hunan",
    "北京", "上海", "长沙", "原宿", "湖南",
    "beijing institute of fashion", "bift", "北京服装学院",
    # her record
    "solo show", "solo shows", "solo exhibition", "个展", "個展",
    "group shows", "museum group", "美术馆", "美術館",
    # her situation
    "student", "学生", "在读",
    # the cats that run through the work
    "cats", "猫",
)

# ── Practice words: only count when a second-person marker is beside them ──
PRACTICE_WORDS = (
    "watercolor", "watercolour", "水彩",
    "diary", "日记", "日記",
    "painting", "paintings", "绘画", "画作", "絵画",
    "illustration", "插画", "イラスト",
    "works on paper", "纸本", "紙もの",
    "zine", "artist book", "artist's book", "艺术家书", "アーティストブック",
    "sketch", "速写",
    "tokyo", "东京", "東京",
    "japanese", "日语", "日本語",
    "book", "书", "画集",
)

SECOND_PERSON = ("your", "you've", "you have", "你", "您", "あなた", "ご自身")

# How far apart the possessive and the practice word may sit and still read as
# one clause. Chinese and Japanese pack more meaning per character, so the same
# character window is generous for English and tight for CJK — which is what we
# want.
NEAR_WINDOW = 30

# ── Catalog phrases: generic even when they happen to contain an anchor ────
BOILERPLATE = (
    "relevant for watercolor and illustration artists",
    "suitable for watercolor artists",
    "适合水彩及插画艺术家",
    "适合水彩和插画艺术家",
    "面向国际视觉艺术家",
    "面向所有艺术家",
    "open to artists of all",
    "open to all artists",
    "good fit for emerging artists",
    "a good opportunity for artists",
    "适合新兴艺术家",
    "potential fit because it belongs to a structured opportunity category",
)


def _positions(text: str, needles) -> list:
    out = []
    for n in needles:
        out.extend(m.start() for m in re.finditer(re.escape(n), text))
    return out


def has_personal_hook(text: str) -> bool:
    """True when the line says something that could only be about her."""
    if not text:
        return False
    low = text.lower()
    if any(a in low for a in STRONG_ANCHORS):
        return True
    people = _positions(low, SECOND_PERSON)
    if not people:
        return False
    practice = _positions(low, PRACTICE_WORDS)
    return any(abs(p - q) <= NEAR_WINDOW for p in people for q in practice)


def is_boilerplate(text: str) -> bool:
    """True when the line is a catalog phrase any artist could be handed."""
    if not text:
        return False
    low = text.lower()
    return any(b in low for b in BOILERPLATE)


def why_line_problem(why: str, summary: str = "") -> str:
    """'' when the line earns its place, else the reason it does not."""
    if not (why or "").strip():
        return "empty"
    if is_boilerplate(why):
        return "boilerplate"
    if not has_personal_hook(why):
        return "no her-specific clause"
    return ""
