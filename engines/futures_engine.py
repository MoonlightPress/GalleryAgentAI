"""
futures_engine.py

Five futures, replacing the three "long-term scenarios".

The old section offered a choice between Gallery, Publication, and Both — which
is not a choice: "both" is the obvious answer, and she has in fact been doing
both concurrently for years (Shanghai solo and two Chinese museum group shows in
2024-25, London, two Tokyo solos in 2026). A fork she is already on both sides
of is decoration.

These are not strategies, they are *kinds of success*. They have real tension —
licensing work is different daily work from gallery work — so choosing between
them means something, while "gallery or publishing" did not.

The names are deliberately flat: "Selling Direct", "Galleries", "Licensing",
"Publishing", "Commissions". An earlier set was written for atmosphere ("No
Gatekeepers", "The Work Goes Out Without You") and was killed on sight — a title
nobody can decode has failed, and it fails harder in translation. The atmosphere
lives in the tagline, one line down, where a reader has already agreed to spend
a second. The `id` keys still carry the old phrasing; they are internal and
stable, and renaming them would buy nothing.

Five rules, each learned the hard way:

1. **No prescribed destination.** She is self-taught, independent, and runs
   everything herself; a system that tells such a person what to want reads as
   presumptuous however good the research is. Show the range; the choice is hers.

   "Self-taught" is how SHE presents herself (Scott, 2026-09-07), and that is
   what the copy answers to. `artist_master_profile` does record illustration
   and design at Beijing Fashion Institute — a specialist design school rather
   than a fine-arts academy — so the two are not in conflict so much as
   describing different things: a qualification on one side, and on the other
   how a painter who taught herself watercolour every day for six years accounts
   for her own practice. A Chinese reader flagged a standing line that called
   this 科班 (academy-trained); she was right, and it is gone. Where her account
   of herself and a database field disagree about who she is, hers wins.
2. **Types of things to pursue, not credentials to acquire.** "A museum solo and
   critical press are required" is a wall. "This one is built out of art book
   fairs and consignment" is something to start on Tuesday.
3. **Money framed as what a door gives**, never as what anything has cost her,
   and measured against what an original already earns her: ¥31,900–115,500 with
   no client, brief or deadline. That benchmark is stated even where a route
   comes off worse for it.
4. **Second person, and no verdicts** (Scott, 2026-09-05/06). "You", addressed
   to a working professional — no imperatives, no encouragement, no promises,
   and no assessment of how she is doing. An intermediate draft swapped to the
   third person to kill the encouragement; it killed the address as well, and
   the address was worth keeping. Conditions, mechanics and figures; the
   conclusion is hers.

   The rule bans verdicts about HER, not facts about the institutions she has
   already reached. Saying what Galerie LE MONDE is in its field — who its
   director also represents, which clients that roster works for — lets her see
   the size of a door she is already through, and Scott's call (2026-09-07) is
   that she should: "she should see what a great thing she just did." Reducing
   the emotional load is a design objective in its own right (Bible05, Lesson
   12). "You did well" is the banned version; "here is what that place is" is
   not, and the difference is the subject of the sentence.
5. **Nothing is defined and nothing is described by negation.** She has six
   years of daily painting, eight zines and three solo shows: explaining what a
   gallery is, or what selling directly means, is the failure mode. And no "X is
   not Y, it is Z", no "rather than", no ", not the follower count" — Scott has
   asked four times and it keeps returning. Say what a thing is.

Her position across the five is deliberately uneven and that asymmetry is the
most useful content here: one is far along and one is at zero, and neither is
visible from where she stands. The `standing` line on each collapsed route is
where that asymmetry is legible in one pass.

**Shape.** Each route is a flat list of blocks — `prose`, `note`, `list`,
`defs`, `table`, `links`, `letter` — under a name and a tagline. `RealmBlocks`
in `SaffronPage.jsx` knows how to draw each kind and nothing else; the sequence,
the headings and the wording all live here, so a block can be added, reordered
or dropped without touching React. A `prose` block may hold several paragraphs
separated by a blank line; the renderer sets `white-space: pre-line`.

Every route opens on the same three blocks, from `_OPENERS` — what this is, what
it gives that the other four do not, what it costs to be on it — and then runs
into its own researched body. The opener earns its fixed shape where the old
five-part schema did not: three questions every route genuinely answers, before
any table.

Prose is written in paragraphs. A draft on 2026-09-07 carried the source
document's one-sentence-per-line markdown straight into the renderer, where it
became a column of terse commands — "a bunch of single sentence lines, which i
hate... it comes off as ordering her around" (Scott). Sentences that argue with
each other belong in the same paragraph.

Three earlier shapes are gone, and the reasons are worth keeping:

  - *Five prose blocks end to end* — life, money, requires, position, example —
    read as a wall (Scott, 2026-09-06: "this isn't very readable").
  - *Header · overview · advantages · strengths · dropdowns* replaced it and
    was better, but every route wore the same five-part costume whether or not
    it had five parts to say. A fixed schema makes a route with one real
    finding pad out to four.
  - *A per-route `scenario` dict* was the Selling Direct experiment that proved
    the block list; it was folded into the generic list once the other four
    followed.

The blocks carry what those fields carried, minus the padding. What they do
not carry is the computed `strengths`/`absent` ledger, which read her record
back to her — a professional with three solo shows does not need to be told
she has three solo shows, and the ledger's other half was a list of what she
lacks under a heading about what she has.
"""

from typing import Optional

from .book_economics_engine import DEFAULT_PRICE as _BOOK_PRICE, ROYALTY_BAND as _ROYALTY_BAND, reference_run
from .outreach_kit_engine import build as _build_outreach


def _t(en: str, zh: str) -> dict:
    # ja is deliberately absent for now rather than machine-guessed; the UI
    # falls back to en. Japanese was cut from the site (Scott, 2026-09-04).
    return {"en": en, "zh": zh}


# The print-run arithmetic has one home, in book_economics_engine. It was typed
# out by hand here once and drifted (107 against that engine's computed 109),
# which is exactly the two-sections-of-one-page-disagreeing failure the Data
# Patch Rule is about.
_BOOK = reference_run()

# The publisher row of the economics table, same rule: derived, not typed. A
# publisher royalty is a percentage of COVER price, so both figures fall out of
# book_economics_engine's own ROYALTY_BAND and DEFAULT_PRICE and cannot drift
# away from what that engine tells her two sections further down the page.
_ROY_LO = round(_BOOK_PRICE * _ROYALTY_BAND[0])
_ROY_HI = round(_BOOK_PRICE * _ROYALTY_BAND[1])
_ROY_PER_COPY = f"¥{_ROY_LO:,}–{_ROY_HI:,}"
_ROY_PER_COPY_ZH = f"{_ROY_LO:,}–{_ROY_HI:,} 日元"
_ROY_300 = f"¥{_ROY_LO * 300:,}–{_ROY_HI * 300:,}"
_ROY_300_ZH = f"{_ROY_LO * 300:,}–{_ROY_HI * 300:,} 日元"

# Her originals sell for ¥31,900–115,500 (artist_master_profile.json
# pricing.originals low_jpy/high_jpy). "How many paintings does this room cost"
# was being answered three different ways in the same section: Moon's "about one
# painting" only holds at her TOP price, KAZE's "four originals" only at her
# FLOOR, and LE MONDE's "about six" at neither (Fable audit, 2026-09-10). A room
# costs a RANGE of paintings because her paintings are a range of prices, so
# that is what it says now — the same convention RecurringDoors already uses.
_ORIGINAL_LO, _ORIGINAL_HI = 31_900, 115_500


def _paintings_for(cost_jpy: int, commission: float = 0.0) -> tuple:
    """(fewest, most) originals needed to cover a venue cost, at her price band.

    With a commission the gallery keeps a share of each sale, so she has to sell
    gross enough for her share to clear the fee.
    """
    gross = cost_jpy / (1 - commission)
    fewest = -(-int(gross) // _ORIGINAL_HI)   # ceil, at her top price
    most = -(-int(gross) // _ORIGINAL_LO)     # ceil, at her floor
    return fewest, most


def _paintings_phrase(cost_jpy: int, commission: float = 0.0, zh: bool = False) -> str:
    lo, hi = _paintings_for(cost_jpy, commission)
    if lo == hi:
        return f"{lo} 张画" if zh else (f"{lo} painting" if lo == 1 else f"{lo} paintings")
    return f"{lo}–{hi} 张画" if zh else f"{lo}–{hi} paintings"

# Same rule for the letter. `outreach_kit_engine` owns it, including the fix
# that matters: the line naming the show she attended is a placeholder, because
# a hardcoded gallery show once had her claim she had been somewhere she had
# not. Retyping it here would put a second copy one edit away from disagreeing.
_OUTREACH = _build_outreach()


# ── The five routes ──────────────────────────────────────────────────────────
#
# Rewritten 2026-09-06 to a structure an outside reviewer produced after reading
# the whole tab. Four things it does that six of my drafts did not:
#
#   1. It has a thesis. "The useful question now is where another route gives
#      you something the current one cannot," followed by four tests every route
#      is then answerable to. My versions had five sections and no argument
#      joining them.
#   2. Headings are decisions, not topics. "Fill the gap between ¥2,200 and
#      ¥31,900", not "How it works" — which I used as a heading three times.
#   3. It defines nothing. "You already know how to organise a solo show. You
#      have done it three times." She is a professional; the copy assumes it.
#   4. It ends in five experiments, one per route. That layer did not exist.
#
# Also: no "X is not Y, it is Z". Scott asked for that four times and it kept
# coming back. Say what a thing is.
#
# Figures unchanged - every one traces to the research reports of 2026-09-05/06.
#
# Two claims about her own history were removed for lack of any evidence, and
# both should stay out.
#
#   Colour Diary as a door-opener — "Colour Diary has already shown that a
#   finished book can function this way", under Selling Direct. It came in from
#   Scott's source document on 2026-09-06 after a verification pass had already
#   pulled a stronger form of the same claim the day before. Asked directly on
#   2026-09-07 he said: "i don't know how she did colour diary. she did it when
#   she was 20. i don't know anything else about it." Nobody on this side of the
#   app knows whether that book was ever put in front of a publisher, a gallery
#   or a buyer, so the sentence is gone. The Blurb-three-copies point stands on
#   its own without it.
#
#   The letter's reference to a show she had not attended. `outreach_kit_engine`
#   keeps that line a placeholder, and the letter is imported from there rather
#   than retyped, so there is one copy to keep honest.
#
# NB an unchecked date: the profile and `ibm_email_writer` both record Colour
# Diary as October 2021, which would make her about 22. Scott remembers 20.
# Nothing in the Strategy tab depends on the date, but `career_strategy_engine`
# writes copy around "Colour Diary (2021)" that would be wrong if the profile is.

# Two paragraphs, not four (Scott, 2026-09-08: "the first two lines can be one,
# and you can get rid of the last one"). The opening inventory and the question
# it sets up are one thought, and the old closing line — "the five routes below
# do different versions of that" — only announced the cards that follow it.
_FRAME = _t(
    "You already have a working practice — six years of paintings, an audience, direct sales, "
    "commissions and a record of exhibitions — so the useful question now is where another "
    "route gives you something this one cannot.\n\n"
    "An original already earns ¥31,900–115,500. That is the benchmark. Anything added to the "
    "practice should earn from work you have already made, reach buyers you cannot reach "
    "yourself, increase what the rest of the work is worth, or create revenue without requiring "
    "another original.",

    "你的创作和生意都已经运转起来了：六年的画、一批固定的观众、直接销售、委托，还有一份展览履历。"
    "所以现在值得问的是：换一条路，能得到什么现在这条路上得不到的东西。\n\n"
    "一张原作已经能卖到 31,900–115,500 日元，后面所有的账都拿这个数来比。往里面再加东西，"
    "至少要做到其中一件：让画完的作品再挣一次钱，卖给你自己够不着的买家，"
    "把其余作品的价钱一起带上去，或者不必再画一张原作也能有收入。")


_SELLING_DIRECT = [
    {"kind": "prose", "label": _t("The gap between ¥2,200 and ¥31,900",
                                  "2,200 到 31,900 日元之间的空档"),
     "text": _t(
        "You already sell successfully at both ends: postcards, zines and prints at ¥1,100–2,200, "
        "then originals beginning at ¥31,900. "
        "The missing part is the middle. "
        "Someone who has bought a zine and a print has no way to spend ¥5,000, ¥10,000 or ¥20,000 "
        "with you. The next purchase available is an original. "
        "The easiest test is to add that middle without buying inventory first.",

        "两头你都卖得动：明信片、zine、印刷品在 1,100–2,200 日元，原作从 31,900 日元起。"
        "断掉的是中间那一段。"
        "一个买过 zine、买过印刷品的人，在你这里花不掉 5,000、10,000 或者 20,000 日元——"
        "再往上就直接是原作了。"
        "最省事的办法，是先把中间那段补上，而且不用先囤货。")},

    {"kind": "table", "label": _t("Three products to start with", "可以先做的三样东西"),
     "headers": [_t("", ""), _t("Sells for", "售价"), _t("You keep", "你拿到"), _t("Margin", "毛利率")],
     "rows": [
        {"cells": [_t("A2 poster", "A2 海报"), _t("¥3,000", "3,000 日元"),
                   _t("¥1,465", "1,465 日元"), _t("44%", "44%")]},
        {"cells": [_t("A1 poster", "A1 海报"), _t("¥5,000", "5,000 日元"),
                   _t("¥2,268", "2,268 日元"), _t("43%", "43%")]},
        {"cells": [_t("Framed giclée, A4", "装裱微喷，A4"), _t("¥20,000", "20,000 日元"),
                   _t("¥7,507", "7,507 日元"), _t("38%", "38%")]},
     ]},

    {"kind": "prose", "text": _t(
        "List them through on-demand production first. Each copy is made only when somebody "
        "orders it, so the test requires no print run and no storage. "
        "The margin is lower than printing yourself. That is useful at this stage: the printer is "
        "carrying the inventory risk while you find out whether the product has a market.",

        "先用按需印刷上架。有人下单才做一件，所以这一轮试验没有起印量，也不占地方堆货。"
        "毛利率比自己印低，但现阶段这样更稳妥：库存的风险压在印厂那边，"
        "你只要弄清楚这件东西有没有人买。")},

    {"kind": "prose", "text": _t(
        "For products that already sell reliably, your existing model is better. A ten-pack of "
        "postcards costs about ¥170 when printed in a run of one hundred, against ¥1,835 on "
        "demand. Keep those in-house. "
        "If one of the new formats begins selling consistently, batch production becomes the "
        "second step.",

        "已经卖得稳的东西，还是你现在的做法划算。一套十张的明信片，印一百套时一套约 170 日元，"
        "按需印刷要 1,835 日元。这些继续自己印。"
        "哪种新产品开始稳定出货了，再转成批量生产，那是第二步。")},

    # Every figure in this paragraph and in the "Hardcover, China" row below is
    # read from book_economics_engine rather than typed. It was typed once and
    # drifted — 107 here against that engine's computed 109 — and the same page
    # then said two different things about the same run.
    {"kind": "prose", "label": _t("What decides whether it sells", "什么决定卖不卖得动"),
     "text": _t(
        "A follower count does not predict sales. Across the paired cases that could be checked, "
        "the share of an audience that actually bought ran from 0.26% to 15.8%, and the largest "
        "audience of the set converted worst. Price is the lever instead: a Tokyo illustrator "
        "with 27,000 followers — a fraction of your reach — published an art book at ¥11,000 and sold "
        "400 copies in four months, roughly ¥4 million. "
        "Two smaller levers decide most of the rest. Where your readers live changes the "
        "arithmetic more than how many they are, since air mail runs ¥2,720 a kilo to the US "
        "against ¥185 across Tokyo — and that split is one figure inside your own Instagram "
        "insights. And anything under three centimetres thick is worth ¥465 on every domestic "
        "parcel, decided at the design stage, before anything is printed.",

        "粉丝数预测不了销量。在能查到具体数字的几个案例里，真正掏钱的人占观众的比例从 0.26% 到 15.8%，"
        "而其中观众最多的那一位转化率最低。真正起作用的是价格：一位东京插画师，粉丝两万七千"
        "（只是你全部触达里的一小部分），自出版的画集定价 11,000 日元，四个月卖了 400 本，约四百万日元。"
        "剩下的大半，由另外两件小一点的事决定。你的读者住在哪里，比他们有多少人更能改变这笔账——"
        "航空小包寄一公斤到美国 2,720 日元，寄到东京市内 185 日元——"
        "而这个比例，你自己的 Instagram 后台里就有。"
        "另外，厚度控制在三厘米以内，每件国内包裹省 465 日元；这是在设计阶段、开印之前就定下的。")},

    {"kind": "prose", "label": _t("The book is a different decision", "做书，是另一个层面的决定"),
     "text": _t(
        f"A 128-page hardcover printed in China costs ¥{_BOOK['outlay_jpy']:,} for "
        f"{_BOOK['run']} copies. At ¥{_BOOK_PRICE:,} each, the production cost is recovered after "
        f"{_BOOK['breakeven_direct']} sales. "
        f"That leaves {_BOOK['run'] - _BOOK['breakeven_direct']} copies after break-even. "
        "The question is therefore demand and speed, rather than margin.",

        f"128 页的精装本，在中国印 {_BOOK['run']} 本要 {_BOOK['outlay_jpy']:,} 日元。"
        f"定价 {_BOOK_PRICE:,} 日元，卖出 {_BOOK['breakeven_direct']} 本收回制作成本。"
        f"回本之后还剩 {_BOOK['run'] - _BOOK['breakeven_direct']} 本。"
        "所以要判断的是需求和速度，利润率反倒是次要的。")},

    {"kind": "table",
     "headers": [_t("", ""), _t("Each", "每本"), _t("Up front", "先要付"),
                 _t("Sells for", "售价"), _t("Production cost recovered at", "回本所需册数")],
     "rows": [
        {"cells": [_t("Current B5 zine, 24pp", "现在的 B5 zine，24 页"), _t("¥498", "498 日元"),
                   _t("¥49,800 / 100", "49,800 / 100 本"), _t("¥1,980", "1,980 日元"), _t("34", "34")]},
        {"cells": [_t("210mm square softcover, 128pp", "210mm 方形平装，128 页"), _t("¥1,609", "1,609 日元"),
                   _t("¥482,700 / 300", "482,700 / 300 本"), _t("¥4,400", "4,400 日元"), _t("173", "173")]},
        {"cells": [_t("A4 softcover, 128pp", "A4 平装，128 页"), _t("¥1,306", "1,306 日元"),
                   _t("¥653,000 / 500", "653,000 / 500 本"), _t("¥4,400", "4,400 日元"), _t("212", "212")]},
        {"cells": [_t("Hardcover, 128pp, China", "精装，128 页，中国印"),
                   _t(f"¥{_BOOK['unit_jpy']:,}", f"{_BOOK['unit_jpy']:,} 日元"),
                   _t(f"¥{_BOOK['outlay_jpy']:,} / {_BOOK['run']}",
                      f"{_BOOK['outlay_jpy']:,} / {_BOOK['run']} 本"),
                   _t(f"¥{_BOOK_PRICE:,}", f"{_BOOK_PRICE:,} 日元"),
                   _t(str(_BOOK['breakeven_direct']), str(_BOOK['breakeven_direct']))]},
     ]},

    {"kind": "prose", "text": _t(
        "For a book intended as a product, the Chinese hardcover has the strongest economics of "
        "the formats checked. "
        "For a book intended to open another door, make three copies instead. Three Blurb copies "
        "cost about ¥31,000 and can go directly to a publisher, gallery or shop buyer.",

        "如果这本书是当商品卖，在查过的几种做法里，算下来还是在中国印精装本最划算。"
        "如果这本书是用来敲另一扇门的，那就只做三本。Blurb 三本约 31,000 日元，"
        "可以直接拿给出版社、画廊或者书店买手。")},

    # "What a book costs" was a standalone section until 2026-09-07 and then
    # briefly sat in Publishing. It belongs here: every figure in it is about
    # paying a printer, posting parcels and placing copies in shops, which is
    # this route. Publishing keeps the half that is about a publisher.
    {"kind": "component", "id": "book_economics",
     "label": _t("Whether a print run can pay for itself",
                 "印一批书，能不能把钱赚回来")},

    {"kind": "links", "label": _t("Where", "去哪里做"),
     "items": [
        {"name": _t("pixivFACTORY / BOOTH — first test for posters, canvas and framed prints",
                    "pixivFACTORY / BOOTH——海报、画布、装裱印刷的第一次试水"),
         "url": "https://factory.pixiv.net/"},
        {"name": _t("SUZURI — useful for smaller paper goods and low-risk experiments",
                    "SUZURI——小件纸制品，低风险的尝试"),
         "url": "https://suzuri.jp/"},
        # The old link went to the shop front, which reads as "just sign up" —
        # and INPRNT does not work that way. Artists join by invitation from an
        # existing seller, or by applying with three images that the artists
        # already there vote on. Saying so turns a wall back into a door with a
        # handle on it; the answer arrives in about two days either way.
        {"name": _t("INPRNT — the useful addition for buyers outside Japan. Artists there choose who joins, so it takes three images and a vote; the answer comes by email in about 48 hours.",
                    "INPRNT——面向日本以外的买家时，值得加上这一家。谁能进，是由站内已有的创作者投票决定的，所以要投三张图；结果大约 48 小时内邮件通知。"),
         "url": "https://www.inprnt.com/application/"},
     ]},
]


_GALLERIES = [
    {"kind": "prose", "label": _t("A gallery that carries the exhibition risk",
                                  "愿意承担办展风险的画廊"),
     "text": _t(
        "You already know how to organise a solo show. You have done it three times. "
        "The next useful gallery relationship is one that contributes something you currently "
        "supply yourself: the room, staffing, collectors, sales work and financial risk. "
        "The economics are unusually clear.",

        "办个展你已经会了，办过三次。"
        "下一段值得建立的画廊关系，要能接过你现在自己扛的那几样：场地、守场的人手、藏家、"
        "销售的活，还有资金上的风险。"
        "这笔账算得特别清楚。")},

    {"kind": "table",
     "headers": [_t("", ""), _t("You pay", "你付"), _t("They take", "他们抽"),
                 _t("Sales needed before you are even", "打平前要卖掉")],
     "rows": [
        {"cells": [_t("Representing gallery", "代理画廊"), _t("¥0", "0"), _t("about 50%", "约 50%"),
                   _t("¥0", "0")]},
        {"cells": [_t("Moon Gallery rental", "Moon Gallery 租赁"), _t("¥100,000 / 5 days", "10 万 / 5 天"),
                   _t("0%", "0%"),
                   _t(_paintings_phrase(100_000), _paintings_phrase(100_000, zh=True))]},
        # NOT "rental". The gallery states plainly that it is 「場所貸し」ではない
        # — the director picks who shows, from the work and from recommendations
        # by illustrators already showing there. Filing her show under "rental"
        # priced a selection as a room booking (Scott, 2026-09-07; confirmed at
        # galerielemonde.com/about and in the 2023 GENSEKI interview).
        {"cells": [_t("Galerie LE MONDE, 12-day solo", "Galerie LE MONDE，12 天个展"),
                   _t("¥374,000 / 12 days", "37.4 万 / 12 天"), _t("30%", "30%"),
                   _t(_paintings_phrase(374_000, 0.30),
                      _paintings_phrase(374_000, 0.30, zh=True))]},
     ]},

       # NOT a description of what LE MONDE is. "i do think you're leaning too hard
    # into what lemonde is and does. she knows, she already did it. it should be
    # talking about what that accomplished and what she can do with it now that
    # she's done it" (Scott, 2026-09-07). The show is an asset she is holding,
    # five weeks old; the question is what it is good for.
    #
    # The links below were deleted by accident in b22b800d — a reorder of the
    # paragraph above sliced from it to "The next move" and took the block in
    # between with it, after Scott had already said once not to cut this
    # material. Restored.
    # NOT a description of what LE MONDE is. "she knows, she already did it. it
    # should be talking about what that accomplished and what she can do with it
    # now that she's done it" (Scott, 2026-09-07).
    #
    # All three paragraphs opened on 它 in an earlier draft, which a cold reader
    # called monotonous and template-like, and the section never named the show
    # in its own body — the antecedent lived only in the heading. Each paragraph
    # now opens on a different thing: the show, the room, the step after it.
    {"kind": "prose", "label": _t("What the August show leaves you holding",
                                  "八月那场展给你留下了什么"),
     "text": _t(
        "The show at Galerie LE MONDE is the newest thing on your record, and the newest credit "
        "is what a first letter is built around — every gallery below reads it before it reads "
        "anything else.\n\n"
        "That room is not for hire, so what it carries is more than a date. The director selects, "
        "from the work and from recommendations by illustrators already showing there, so the "
        "credit reads as having been chosen — and it keeps saying that for as long as it is "
        "recent. Which is the argument for spending it now rather than next year.\n\n"
        "There is a documented next step attached to it, too: every illustrator on the agency's "
        "roster showed at the gallery first. They are closed to new artists at the moment, so "
        "staying in contact is the whole of the move — and the riso studio in the same building "
        "is a reason to go back, with the zines rather than the paintings.",

        "在 Galerie LE MONDE 的那场个展，是你履历上最新的一项；"
        "而最新的这一项，正是第一封信要围着写的内容——下面每一家画廊，都会先读它，再读别的。\n\n"
        "那个空间不对外出租，所以它带来的不只是一个日期。"
        "主理人是看作品本身、以及已经在那里办展的插画家的推荐来选人的，"
        "所以这一项读起来是“被选中过”，而且只要还新，它就一直在说这句话。"
        "这也正是趁现在用上它、而不是等到明年的理由。\n\n"
        "后面还接着一个明确的下一步：经纪公司名单上的每一位，都是先在画廊办过展的。"
        "他们目前不接新人，所以现在能做的就是保持联系——"
        "而同一栋楼里的孔版印刷工作室，本身就是一个再去一趟的由头，带 zine 去，不是带画。")},

    {"kind": "links", "label": _t("Same building", "同一栋楼里"),
     "items": [
        {"name": _t("Studio LE MONDE — risograph, Tuesday to Sunday 12:00–19:00, booked as a session with staff. contact@studiolemonde.com",
                    "Studio LE MONDE——孔版印刷，周二至周日 12:00–19:00，只在有工作人员在场的时段接受预约。contact@studiolemonde.com"),
         "url": "https://www.studiolemonde.com/"},
        {"name": _t("Agence LE MONDE — the roster it draws from, and who that roster works for: McDonald's, Asahi, Mizuho, ANNA SUI, GUCCI, Quarto, Pokémon. Not taking anyone on as of September 2026.",
                    "Agence LE MONDE——它就是从这里选人的；名单上的插画师在为这些客户做事：麦当劳、朝日啤酒、瑞穗银行、ANNA SUI、GUCCI、Quarto、宝可梦。截至 2026 年 9 月不接新人。"),
         "url": "https://www.agencelemonde.com/"},
     ]},

    {"kind": "prose", "text": _t(
        "Against that, the arithmetic of representation. A 50% commission can look large in "
        "isolation; against a ¥374,000 fee plus 30%, representation is cheaper until an "
        "exhibition reaches about ¥1.87 million in sales. The more important difference is "
        "who brings the buyers. So far, people buying your work have found you. Representation "
        "adds a collector base belonging to somebody else.",

        "另一边是代理的账。单看 50% 的抽成会觉得高；"
        "拿 374,000 日元的场地费再加 30% 抽成来比，只要那场展卖不到约 187 万日元，代理都更划算。"
        "更要紧的区别在于：买家是谁带来的。到现在为止，买你画的人是自己找到你的。"
        "代理带来的，是一份原本属于别人的藏家名单。")},

    {"kind": "prose", "label": _t("The next move", "下一步"),
     "text": _t(
        "Choose a small number of galleries where the work genuinely fits the programme. "
        "Visit first. Then send five paintings from one coherent series and ask whether they "
        "would be interested in seeing the work in person.",

        "挑几家展览方向确实合得上的画廊，数量不用多。"
        "先去看展。之后寄五张同一个系列的画，问他们有没有兴趣看看实物。")},

    # Checked one by one on 2026-09-07 and this list came back one for three.
    # GALLERY KOGURE is gone: the claim was "a close roster fit, including
    # detailed urban work on paper", and its roster of ~35 is lacquer, mixed
    # media, photography and sculpture with no architectural or watercolour
    # specialism visible at all. Tokyo Gallery + BTAP moved out of "immediate":
    # the six-Chinese-artists claim is exactly right, and the roster also holds
    # Xu Bing, which puts it in tier 4 — CLAUDE.md is explicit that tier 4 never
    # appears as something to act on now.
    # Researched and verified 2026-09-07 against each venue's own page. The
    # route had exactly one door before this, and its window was shut until
    # December. FACE is first because it is open today and closes on the 8th.
    {"kind": "prose", "label": _t("Open now, and closing on 8 October",
                                  "现在开放，10 月 8 日截止"),
     "text": _t(
        "FACE 2027 takes submissions from 7 September to 8 October, and shows the selected work "
        "at SOMPO Museum in Nishi-Shinjuku next March. Watercolour is named in the accepted "
        "media, alongside oil, acrylic, mineral pigment, printmaking, dyeing and photography. "
        "There is no nationality clause and no residency clause — the only practical requirement "
        "is getting the work there, by courier in late October or by hand on the 7th or 8th of "
        "November. Entry is ¥7,000. Works can be up to 200 × 170cm and there is no minimum size, "
        "so a small painting is eligible. Alongside the main prizes there is a U30 Frontier Award "
        "of ¥300,000 for anyone born on or after 1 April 1997.",

        "FACE 2027 的收件期是 9 月 7 日到 10 月 8 日，入选作品明年三月在西新宿的 SOMPO 美术馆展出。"
        "接受的媒介里明确写着水彩，和油画、丙烯、岩彩、版画、染色、摄影并列。"
        "没有国籍限制，也没有居住地限制——实际上要过的只有一关：把作品送到，"
        "10 月下旬用快递，或者在 11 月 7 日、8 日亲自送去。报名费 7,000 日元。"
        "尺寸上限 200 × 170 厘米，没有下限，所以小幅作品也可以投。"
        "除了主要奖项，还有一个 30 万日元的 U30 Frontier 奖，面向 1997 年 4 月 1 日之后出生的人。")},

    {"kind": "links",
     "items": [
        {"name": _t("FACE 2027 — the call, the delivery dates and the entry form",
                    "FACE 2027——征集要项、送件日期与报名表"),
         "url": "https://www.sompo-museum.org/news/2026/face2027/"},
     ]},

    {"kind": "prose", "label": _t("Three rooms in Tokyo that take the work as it is",
                                  "东京有三个空间，接受这样的作品"),
     "text": _t(
        "HAGI ART in Yanaka writes its remit as young artists' solo and group shows, art-book "
        "markets, and exhibitions about architecture, culture and daily life — and charges no "
        "venue fee at all, running the programme on the café below it. It selects on a written "
        "concept, so it takes a proposal by email rather than a booking.\n\n"
        "Gallery KAZE in Kichijoji is ¥110,000 for six days with no commission on sales, in 40m² "
        "with twenty metres of wall. It has a watercolour solo booked this October——青山一樹, "
        "「水彩でえがく情景」——and its 2027 calendar is still mostly open. At your prices "
        f"that room costs {_paintings_phrase(110_000)}.\n\n"
        "Moon Gallery you already know: ¥100,000 for five days, no commission, and nobody has to "
        "sit the room.",

        "谷中的 HAGI ART 把自己的方向写得很清楚：年轻创作者的个展与联展、艺术书市集，"
        "以及关于建筑、文化与日常生活的展览——而且完全不收场地费，"
        "整个项目靠楼下的咖啡店养着。它按方案选人，所以要发邮件提方案，不是订档期。\n\n"
        "吉祥寺的 Gallery KAZE，六天 11 万日元，销售不抽成，40 平方米、20 米挂画墙。"
        "今年十月那里有一场水彩个展——青山一树，《水彩でえがく情景》——2027 年的档期大半还空着。"
        f"按你的价格，租下这个空间等于要卖出 {_paintings_phrase(110_000, zh=True)}。\n\n"
        "Moon Gallery 你已经熟悉了：五天 10 万日元，不抽成，也不需要人守场。")},

    {"kind": "links",
     "items": [
        {"name": _t("HAGI ART, Yanaka — no venue fee; proposals go to info@hagiso.com as two A4 PDFs, a portfolio and a concept written for the space",
                    "HAGI ART，谷中——不收场地费；方案寄到 info@hagiso.com，两份 A4 PDF：作品集，以及一份专为这个空间写的展览构想"),
         "url": "https://hagiso.com/hagiart-concept/"},
        {"name": _t("Gallery KAZE, Kichijoji — ¥110,000 for six days, no sales commission, equipment included",
                    "Gallery KAZE，吉祥寺——六天 11 万日元，销售不抽成，设备可借"),
         "url": "https://gallery-kaze.jp/exhibition/"},
     ]},

    {"kind": "links", "label": _t("And the open call that comes round again",
                                  "以及每年都会再来一次的公开征集"),
     "items": [
        {"name": _t("biscuit gallery — its grid next open call has run every year since 2024. No application fee and no display fee, open to students and to artists under about forty who have not shown there before. The 2026 round took applications from late December to 30 April for an August show, so the next window opens around December.",
                    "biscuit gallery——它的 grid next 公开征集从 2024 年起每年都办。不收报名费，也不收展位费，面向学生以及大约四十岁以下、此前没有在那里展过的创作者。2026 那一轮的申请是12 月底到 4 月 30 日，展览在八月，所以下一个窗口大约在 12 月打开。"),
         "url": "https://biscuitgallery.com/gridnext-2026/"},
     ]},

    {"kind": "prose", "label": _t("Where this work sits higher up the same market",
                                  "同一个市场再往上，这类作品在哪里"),
     "text": _t(
        "Tokyo Gallery + BTAP has been running since 1950 and keeps six Chinese artists on its "
        "roster, several of them working in ink and watercolour on paper — the same materials, "
        "shown at the top of this market. Xu Bing is on that roster too, which places the gallery "
        "several stages further along than a first letter reaches. It is worth knowing as the "
        "shape of the ceiling.",

        "Tokyo Gallery + BTAP 从 1950 年开到现在，代理名单上有六位中国艺术家，"
        "其中几位用的就是纸上水墨与水彩——同样的材料，出现在这个市场的顶端。"
        "徐冰也在这份名单上——这家画廊不是一封陌生来信能够得着的。"
        "把它记住，是为了知道天花板长什么样。")},

    {"kind": "prose", "label": _t("A third arrangement, worth more than either",
                                  "还有第三种安排，比前面两种都划算"),
     "text": _t(
        "Between renting a room and being represented sits an open call that pays the artist to "
        "exhibit. TOKAS gives ¥150,000 toward the work and charges nothing for the venue, and its "
        "open calls run on a fixed yearly cycle, so they can be planned for rather than waited "
        "on.",

        "在租场地和被代理之间，还有一种安排：反过来付钱给艺术家办展的公开征集。"
        "TOKAS 提供 15 万日元制作经费，场地不收费；它的公开征集按固定的年度周期走，"
        "所以这是可以提前安排的事，不用干等。")},

    {"kind": "links",
     "items": [
        {"name": _t("TOKAS — open calls and application dates for all its programmes",
                    "TOKAS——各项目的公开征集与申请时间"),
         "url": "https://www.tokyoartsandspace.jp/en/application/index.html"},
     ]},

    {"kind": "note", "text": _t(
        "This is a narrower list than a directory of Tokyo galleries. That is useful. Gallery "
        "outreach works better as a relationship with ten plausible rooms than as mail sent to a "
        "hundred implausible ones.",

        "这份名单比一本东京画廊名录短得多，短正是它的用处。"
        "和十个真正对得上的空间建立关系，比给一百个不对路的空间发信管用。")},

    {"kind": "prose", "label": _t("The first letter", "第一封信"),
     "text": _t(
        "The first contact only has to make the work easy to look at. "
        "Use one link, five paintings from one series and one specific sentence showing why that "
        "gallery was chosen. "
        "For HAGI ART:",

        "第一次联系，只需要让人容易看到作品。"
        "一个链接，同一个系列的五张画，还有一句具体的话，说明为什么选了这一家。"
        "给 HAGI ART 的例子：")},

    # The letter is not retyped here. `outreach_kit_engine` owns it, including
    # the fix that matters: the show-attended line is a placeholder, because a
    # hardcoded "A Little Gem" sent her to claim she had been to a show she had
    # not been to. One copy of the letter, one place to fix it.
    {"kind": "letter", "text": _OUTREACH["letter_ja"]},

    # Six conventions became one. A painter with three solo shows has written
    # these emails; being told that attachments from strangers go unopened and
    # that prices go in only when asked is etiquette she already practises, and
    # a cold Chinese reader called the whole list "here is how to approach a
    # gallery, dear". The one item she flagged as genuinely new is the reframe
    # of silence, so that is what survives.
    {"kind": "note", "text": _OUTREACH["rules"][4]},
]


_LICENSING = [
    {"kind": "prose", "label": _t("The archive, earning a second time", "已经画完的作品，再挣一次钱"),
     "text": _t(
        "Licensing has one unusual advantage for you: the inventory already exists. "
        "Six years of daily painting is thousands of images that can potentially produce income "
        "while the originals remain yours. "
        "The value depends primarily on where and how an image is used:",

        "授权对你有一个别处没有的优势：你手上已经有的画就是现成的。"
        "六年每天画下来是好几千张图，原作还是你的，同时还能挣钱。"
        "值多少钱，主要看一张图被用在哪里、怎么用：")},

    {"kind": "table",
     "headers": [_t("Use", "用途"), _t("Published rate", "公开费率")],
     "rows": [
        {"cells": [_t("Small magazine illustration", "杂志内页小图"), _t("¥5,000", "5,000 日元")]},
        {"cells": [_t("Book cover", "书籍封面"), _t("¥70,000", "70,000 日元")]},
        {"cells": [_t("Magazine cover", "杂志封面"), _t("¥100,000", "100,000 日元")]},
        {"cells": [_t("Calendar", "挂历"), _t("¥800,000", "800,000 日元")]},
     ]},

    {"kind": "prose", "text": _t(
        "That makes the licence terms as important as the fee: format, territory, duration, "
        "exclusivity and reuse. "
        "Copyright transfer is priced at roughly two to three times a normal licence in the "
        "published Japanese rate card. Keep that distinction explicit whenever a buyer asks for "
        "permanent rights.",

        "所以授权条款和费用一样要紧：形式、地域、期限、是否独家、能不能再次使用。"
        "在日本公开的费率表上，著作权转让的定价大约是普通授权的两到三倍。"
        "只要对方要的是永久权利，就把这一条摆到明面上。")},

    {"kind": "prose", "label": _t("A small cover-ready series", "一小组能直接当封面用的画"),
     "text": _t(
        "Your subject matter already fits the book market: architecture, atmosphere, interiors, "
        "weather, light and quiet urban scenes. "
        "The compositional requirement is the part worth designing for. "
        "Covers need room for typography and cropping. Paint a small group vertically, with "
        "intentional quiet areas — sky, fog, water, wall, shadow or an open upper third. "
        "That gives art directors images they can actually build a cover around while keeping the "
        "work recognisably yours. "
        "Five to ten paintings would be enough to create the beginning of a licensing portfolio. "
        "Then place them where art directors already look:",

        "你的题材本来就贴合图书市场：建筑、氛围、室内、天气、光，还有安静的城市场景。"
        "值得专门去应对的，是构图上的要求。"
        "封面要放得下字，也要经得起裁切。画一小组竖构图，特意留出安静的区域——"
        "天空、雾、水面、墙、阴影，或者上三分之一整片留白。"
        "这样艺术总监手上就有了能用来设计封面的图，而作品看上去还是一眼就认得出是你的。"
        "五到十张，一个授权作品集的开头就有了。"
        "然后把它们放到艺术总监本来就会去看的地方：")},

    {"kind": "links",
     "items": [
        {"name": _t("イラストレーションファイルWeb — where Japanese art directors and book designers look for illustrators, and the form for being listed in it",
                    "イラストレーションファイルWeb——日本的艺术总监和装帧设计师找插画师的地方，以及申请收录的表格"),
         "url": "https://i.fileweb.jp/blog/file_oubo"},
        {"name": _t("amanaimages — Japanese stock licensing; published cover licences are ¥33,000–79,200",
                    "amanaimages——日本的图像授权；公开的封面授权价为 33,000–79,200 日元"),
         "url": "https://amanaimages.com/"},
        {"name": _t("Arcangel — specialised in book-cover imagery, accepts illustration and pays contributors 50% of net",
                    "Arcangel——专做书封图像，收插画，付给供稿人净额的 50%"),
         "url": "https://arcangel.com/become-a-contributor/"},
        # The link used to point at /en/studio, which is the marketing page and
        # carries no way in — checked 2026-09-07, no submission route on it at
        # all. This is the actual application: pre-register with 3-5 images, and
        # they review those alongside your existing online presence.
        {"name": _t("Bridgeman Studio — open to illustration; apply with three to five images and they review those alongside your online presence. Both exclusive and non-exclusive contracts exist, and non-exclusive leaves you free to license elsewhere.",
                    "Bridgeman Studio——接受插画；投三到五张图申请，他们会连同你现在网上的作品一起看。合同分独家与非独家两种，非独家可以同时在别处授权。"),
         "url": "https://partner-hub.bridgemanimages.com/en/apply-now"},
     ]},

    {"kind": "note", "text": _t(
        "This route can begin with work you already own and expand through paintings designed "
        "specifically for commercial use.",

        "这条路可以从你已经有的作品开始，再靠专门为商业用途画的作品往外扩。")},
]


_PUBLISHING = [
    {"kind": "prose", "label": _t("A book that still needs to be made",
                                  "一本还没做出来的书"),
     "text": _t(
        "The strongest publishing opportunity is a book concept with enough identity that a "
        "publisher can imagine selling it. "
        "Your existing paintings establish that you can execute it. The proposal establishes what "
        "the book is. "
        "That distinction matters because the publishers checked ask for projects and proposals. "
        "In the comparable Tokyo architecture title, forty of the fifty paintings were made after "
        "the deal was agreed. "
        "A strong proposal therefore needs:",

        "出版这条路上最有力的，是一个清楚到出版社一听就知道怎么卖的选题构想。"
        "你已有的画证明你做得出来；方案说明的是这本书到底是什么。"
        "这个区别之所以要紧，是因为查过的这几家出版社要的是方案和构想。"
        "拿来对照的那本东京建筑画集，五十张画里有四十张是在合同谈定之后才画的。"
        "所以一份有力的方案要有：")},

    {"kind": "list",
     "items": [
        _t("the idea of the book", "这本书的构想"),
        _t("why the paintings belong together", "这些画为什么属于同一本书"),
        _t("a sample sequence", "一组排好顺序的样张"),
        _t("several finished works showing the visual language", "几张完成的作品，用来呈现视觉语言"),
        _t("what remains to be painted", "还有哪些要画"),
        _t("the intended reader", "预设的读者"),
        _t("a rough scale and format", "大致的规模与开本"),
     ]},

    {"kind": "prose", "text": _t(
        "Your six-year archive gives you unusually strong material for that proposal even if the "
        "final book contains new work.",

        "即使最后成书用的是新画的作品，你这六年的积累也让这份方案有特别扎实的底子。")},

    {"kind": "prose", "label": _t("The economics", "这笔账"),
     "text": _t(
        "Publishing is weak as a per-copy revenue stream and strong as distribution.",
        "论每本能拿多少钱，出版社出版不占优势；论发行，它有优势。")},

    {"kind": "table",
     "headers": [_t("", ""), _t("You keep per copy", "每本你拿到"), _t("300 copies", "300 本")],
     "rows": [
        # Computed from book_economics_engine's ROYALTY_BAND × DEFAULT_PRICE
        # rather than typed. The typed figure was ¥115–240 — 3–6% of cover,
        # against the 8–10% that book_economics documents as the Japanese
        # convention and computes everything else from. Two sections of one tab
        # therefore quoted different royalties for the same book (Fable audit,
        # 2026-09-10). Line 122's comment already says the print-run arithmetic
        # has one home; this row simply had not been moved into it yet.
        {"cells": [_t("Publisher", "出版社出版"), _t(_ROY_PER_COPY, _ROY_PER_COPY_ZH),
                   _t(_ROY_300, _ROY_300_ZH)]},
        {"cells": [_t("Self-published hardcover", "自己出版的精装本"), _t("¥3,635", "3,635 日元"),
                   _t("¥1,090,500", "1,090,500 日元")]},
     ]},

    {"kind": "prose", "text": _t(
        "The publisher's contribution is everything surrounding those royalties: financing the "
        "print run, national bookshop distribution, ISBN, production, inventory and a publication "
        "record that remains attached to your name. "
        "Those benefits make the most sense when the book is expected to strengthen the rest of "
        "the practice as well as sell copies. The other side of the fork — paying a printer "
        "yourself, and what a run has to sell to come back — is worked out under Selling Direct.",

        "出版社真正给的是版税之外的那一整套：出印刷的钱、进全国书店、一个 ISBN、制作、库存，"
        "还有一条会一直挂在你名字上的出版记录。"
        "当这本书除了卖出去，还要带动你手上其他的事时，这些好处才最值。"
        "岔口的另一边——自己付钱给印厂，以及一批书要卖掉多少本才能回本——算在“直接卖”那一条里。")},

    # Who carries the outlay — the one real publisher-vs-self comparison in the
    # book material, and the only part of it that belongs on this side. The
    # print arithmetic went to Selling Direct, because printing a book, posting
    # it and putting it in shops IS selling direct (Scott, 2026-09-07); drawing
    # the same comparison in both routes buys nothing.
    {"kind": "component", "id": "publisher_fork",
     "label": _t("Who carries the ¥394,500", "394,500 日元由谁来出")},

    {"kind": "links", "label": _t("Three publishers with a published route in",
                                  "三家把入口写出来的出版社"),
     "items": [
        # All three used to point at a homepage, the one page that does not
        # tell you how to get in. Checked 2026-09-07: maar and seigensha both
        # run real submission routes, and MdN publishes exactly this kind of
        # book but states no route, so its line says what is true instead of
        # implying a door.
        {"name": _t("マール社——「いつでも、どなたでも」, and no publishing record required. If a proposal is taken they publish at their own expense, with nationwide bookshop distribution. A reply comes inside a month; nothing is returned.",
                    "マール社（Maar-sha）——投稿页写着「いつでも、どなたでも」（随时，任何人），也不要求你出过书。方案一旦被采用，由他们出钱出版，并进入全国书店。一个月内回复；寄去的东西不退。"),
         "url": "https://www.maar.com/plan"},
        {"name": _t("青幻舎——a form for proposals only: a portfolio showing the work, your history and profile, plus a plan and image files, attachments up to 10MB",
                    "青幻舎——只走方案投递专用表单：作品集（作品、活动经历、简介）、方案、图像数据，附件上限 10MB"),
         "url": "https://www.seigensha.com/proposal-contact/"},
        {"name": _t("MdN — publisher of the Tokyo Storefronts books, so this exact kind of book is already on their list. They publish no submission route, so an approach goes through their general enquiry form.",
                    "MdN——《东京店构え》系列就是他们出的，所以这一类书本来就在他们的书目里。他们没有公开投稿通道，要从一般咨询表单去问。"),
         "url": "https://books.mdn.co.jp/contact/"},
     ]},

    {"kind": "note", "text": _t(
        "The next useful piece of work here is therefore one book proposal, built well enough to "
        "send to all three with small changes.",

        "所以这条路上接下来真正有用的一件事，是把一份书的方案做扎实，"
        "扎实到只要小改一下就能同时递给这三家。")},
]


_COMMISSIONS = [
    {"kind": "prose", "label": _t("The painting and the usage, priced separately",
                                  "画和用途，分开计价"),
     "text": _t(
        # The "subject, schedule and finished image" sentence lives in the costs
        # block above; a cold reader found it printed twice, twenty lines apart.
        "Either the fee compensates for what a brief takes, or the commission creates value "
        "somewhere else. The national rate card gives a useful floor:",

        "一次委托拿走的东西，要么由费用补回来，要么得在别处产生价值。"
        "全国费率表给了一个有用的底线：")},

    {"kind": "table",
     "headers": [_t("Use", "用途"), _t("Published rate", "公开费率")],
     "rows": [
        {"cells": [_t("Book cover", "书籍封面"), _t("¥70,000", "70,000 日元")]},
        {"cells": [_t("Magazine cover", "杂志封面"), _t("¥100,000", "100,000 日元")]},
        {"cells": [_t("Small internal illustration", "内页小图"), _t("¥5,000", "5,000 日元")]},
        {"cells": [_t("Average coordinated job", "经手项目的平均费用"), _t("¥71,327", "71,327 日元")]},
     ]},

    {"kind": "prose", "text": _t(
        "Architecture and atmosphere are in specific demand for covers: literary fiction leans "
        "heavily on exactly this kind of image. "
        "Hand-painted watercolour sits in the second-highest of the five medium categories in "
        "that rate card. "
        "A ¥70,000 cover is therefore close to the price of one of your existing originals. The "
        "commercial job becomes more attractive when the licence expands, the image is reused, or "
        "the publication brings the work to the next client. "
        "Secondary use can pay 70%, 50%, 50% and 20% of the original fee as the same image is "
        "reused. "
        "That is the part worth protecting.",

        "建筑与氛围类的画在封面上有明确需求：文学小说的封面，大量依赖的正是这一类图像。"
        "那份费率表的五个媒介档次里，手绘水彩排在第二高。"
        "所以一张 70,000 日元的封面，价钱和你自己的一张原作差不多。"
        "当授权范围扩大、图像被再次使用，或者这次发表把作品带到下一个客户面前时，"
        "商业委托才变得更有吸引力。"
        "同一张图反复被用时，二次使用可以按原稿费再付一笔，公开的比例依次是 70%、50%、50%、20%。"
        "要护住的正是这一部分。")},

    {"kind": "prose", "label": _t("The terms, ready before the enquiry",
                                  "在询问到来之前就备好的条款"),
     "text": _t(
        "For every commercial commission, quote these separately:",
        "每一次商业委托，这四项分开报价：")},

    {"kind": "defs",
     "items": [
        {"term": _t("Painting fee", "绘制费"),
         "body": _t("The work required to make the image.", "做出这张图所需要的工作。")},
        {"term": _t("Licence", "授权"),
         "body": _t("Where it may appear, for how long, in which countries and for which use.",
                    "可以出现在哪里、用多久、在哪些国家、作什么用途。")},
        {"term": _t("Additional use", "追加使用"),
         "body": _t("A new fee when the same image is reused elsewhere.",
                    "同一张图被用到别处时，另计一笔费用。")},
        {"term": _t("Copyright transfer", "著作权转让"),
         "body": _t("A separate, substantially higher price when the client wants permanent ownership of the rights.",
                    "客户想永久拥有这些权利时，单独计价，而且高出许多。")},
     ]},

    # The Skeb / ココナラ / SKIMA copyright table was cut on 2026-09-07. It argued
    # against the page it sat on: Licensing says her subject reaches buyers
    # character work cannot, and then this sent her to three character-commission
    # platforms. It was also the least relevant thing in the route.
    {"kind": "prose", "text": _t(
        "That turns an ambiguous “How much for a painting?” into something you can price "
        "consistently.",

        "这样一来，“画一张多少钱”这种含糊的问题，就变成了一个你能给出稳定报价的问题。")},

    {"kind": "links", "label": _t("Two useful doors now", "现在就有两扇有用的门"),
     "items": [
        # Checked 2026-09-07. Two things the old line missed and both matter:
        # the fee is flat for up to five works, and the competition runs four
        # times a year, so a round that has closed is a wait of months rather
        # than a year.
        {"name": _t("ザ・チョイス — ¥1,500 flat, whether you enter one work or five. It runs four times a year with a different judge each round, and every selected work goes forward to the annual prize. Age, nationality and professional or amateur status are all explicitly unrestricted. Pay through Peatix before the postal deadline, which falls a day earlier than the deadline for the work itself.",
                    "ザ・チョイス——统一 1,500 日元，投一张和投五张一个价。一年办四次，每次换一位评审，入选作品都会进入年度奖。年龄、国籍、职业或业余，全都明确不设限。报名费通过 Peatix 预付，缴费截止在寄件截止的前一天。"),
         "url": "https://illustration-mag.jp/regular"},
        {"name": _t("HB FILE — ¥7,000, currently vol.37, and previously published work is accepted, so six years of finished paintings is already the portfolio. Every entrant's file stays available to designers and publishers in the gallery for a year; the top prizes are a week's solo show at HB Gallery in Omotesando.",
                    "HB FILE——7,000 日元，目前是第 37 届，接受已经发表过的作品，所以六年画完的东西本身就是作品集。每位投稿者的档案会在画廊向设计师和出版社开放一年；最高奖是在表参道 HB Gallery 办一周个展。"),
         "url": "https://hbgallery.com/compe.html"},
     ]},

    {"kind": "note", "text": _t(
        "Both are inexpensive ways to place the work in front of people who commission illustration.",
        "这两条都很便宜，都是把作品放到“会下委托的人”眼前的方式。")},
]


_FIRST_STEPS = {
    # "What to do first" / "先做什么" read as an order of business she owed
    # someone. It is five optional experiments, none of them due — the heading
    # now offers rather than instructs (Scott, 2026-09-08).
    "label": _t("Good places to start", "几个不错的起点"),
    # Three things the first cold reader was right about. FACE was buried at the
    # 40% mark and absent from this list, and it is the ONLY dated item in the
    # whole tab — so it goes first, with the date on it. The route names now
    # match the five section headings exactly, because she has to map the
    # summary back to the sections in about four seconds. And the five stopped
    # claiming to be small when two of them were projects: five cover-ready
    # paintings and a book proposal are not 一件很小的事, and saying so made the
    # close read as five more things to worry about.
    "intro": _t(
        "One of these has a date on it. The rest keep, and they are not the same size — two are "
        "an afternoon, three are a piece of work.",
        "其中一件有截止日期。其余的都不着急，而且它们大小不一样——两件是一个下午的事，三件是要动手做的活。"),
    "steps": [
        {"route": _t("Before 8 October", "10 月 8 日之前"),
         "step": _t("FACE 2027 — ¥7,000, watercolour named in the accepted media, no minimum size.",
                    "FACE 2027——7,000 日元，接受的媒介里写明水彩，尺寸没有下限。")},
        {"route": _t("Selling Direct", "直接卖"),
         "step": _t("An afternoon: list an A2 poster, an A1 poster and a framed A4 print on demand.",
                    "一个下午：用按需印刷上架一张 A2 海报、一张 A1 海报和一张装裱好的 A4 印刷品。")},
        {"route": _t("Galleries", "画廊"),
         "step": _t("An afternoon: pick one show to go and see, and get a five-image series link ready.",
                    "一个下午：挑一场展去看，准备好一个包含五张同系列作品的链接。")},
        {"route": _t("Licensing", "图像授权"),
         "step": _t("A piece of work: the first five vertical, cover-ready paintings.",
                    "要动手做的：头五张竖构图、可以直接当封面用的画。")},
        {"route": _t("Publishing", "出版"),
         "step": _t("A piece of work: one existing body of work written up as a one-page book idea.",
                    "要动手做的：把已有的一组作品，整理成一页纸的出书构想。")},
        {"route": _t("Commissions", "委托"),
         "step": _t("A piece of work: a reusable fee-and-licence template, written before the next enquiry.",
                    "要动手做的：一份可以反复用的“费用＋授权”模板，趁还没有人来问先写好。")},
    ],
    "close": _t(
        "Five experiments. What they turn up is worth more than choosing between the five "
        "from here.",
        "五个实验做下来，会比现在凭空挑选清楚得多。"),
}


# ── What opens each route ────────────────────────────────────────────────────
#
# Three blocks before the research: what the route is, what it gives that the
# other four do not, and what it costs to be on it.
#
# The first two are restored. They existed as `overview` and `advantages`, went
# unrendered when the routes moved to block lists, and were deleted on
# 2026-09-06 as dead fields — which they were, in the render. The writing was
# not dead: it is the researched comparative material, and without it the routes
# open straight into a price table and read as instructions (Scott, 2026-09-07:
# "there's no overview, why it's a good route for her... it comes off as
# ordering her around instead of presenting these things as great opportunities
# with obvious upsides and potential downsides"). Recovered from b3efe2be^.
#
# The third is new. A route with upsides and no costs reads as a pitch, and she
# is being asked to judge five of them against a practice that already works.
# The costs are stated about the ROUTE — half of each sale, somebody else's
# schedule, a room full of unsold copies — never about her capacity to bear
# them.
#
# Written as paragraphs. An intermediate draft carried Scott's source document's
# one-sentence-per-line markdown into the renderer, where it became a column of
# terse commands ("which i hate"). Sentences that argue with each other belong
# in the same paragraph.

_WHAT = _t("What this is", "这是什么样的一条路")
_GIVES = _t("What it gives you that the others don't", "这条路有、别的路没有的")
_COSTS = _t("What you'd be taking on", "你要承担的是什么")


def _opener(what, gives, costs):
    return [
        {"kind": "prose", "label": _WHAT, "text": what},
        {"kind": "prose", "label": _GIVES, "text": gives},
        {"kind": "prose", "label": _COSTS, "text": costs},
    ]


_OPENERS = {
    "no_gatekeepers": _opener(
        # Says what the route IS, and hands the price-gap finding to the body,
        # which is where the products table that answers it lives. All three of
        # the standing line, this block and "Fill the gap" used to state the
        # ¥2,200-to-¥31,900 break, so the first screen said one thing three
        # times.
        # Mechanics only. The comparison against the other four belongs in the
        # next block, which is what its heading promises.
        _t("Work goes out through your own shop — listings you write, prices you set, parcels you "
           "pack — and the money arrives per sale, as it sells. Postcards, zines, prints and "
           "originals all already run this way, alongside commissions taken directly.",

           "作品通过你自己的店铺卖出去——文案你写、价格你定、包裹你打——"
           "钱是一笔一笔进来的，卖一件收一件。"
           "明信片、zine、印刷品和原作现在都是这样在走，直接接的委托也是。"),

        # This block used to hold the four research findings — follower
        # conversion, the ¥11,000 comparable, shipping geography, the three-
        # centimetre threshold. All good, none of them an answer to "what does
        # this give me that the other four don't": they describe how the route
        # works, which is a briefing where a comparison was promised. They moved
        # into the body, next to the products table where they are operational.
        # The other four routes' upsides blocks are genuinely comparative; this
        # was the odd one out, and it is the first route she opens.
        _t("You keep the whole margin. A gallery takes about half of a sale, a publisher leaves "
           f"{_ROY_PER_COPY} of a ¥{_BOOK_PRICE:,} book, and a licence pays once for a use somebody else has "
           "defined — here everything above cost stays on your side. You set the price rather "
           "than arguing for it, and nothing waits on an application, a jury or somebody's "
           "programme, so a decision made on Monday can be earning by Friday. None of the other "
           "four can do that.\n\n"
           "It also starts from something the others have to build first. The audience is already "
           "there and already looking, so a new product reaches it the same afternoon, with no "
           "introduction to arrange and nobody's permission to wait for.",

           f"全部毛利都归你。每卖一张，画廊抽走大约一半；一本 {_BOOK_PRICE:,} 日元的书，出版社分给你 "
           f"{_ROY_PER_COPY_ZH}，授权那边，是别人按定好的用途一次性付你一笔钱——在这条路上，成本以外的钱全是你的。"
           "价格是你定的，不用再跟谁争取；也没有任何一件事要等申请、等评审、等别人的排期，"
           "所以周一做的决定，周五就可能在挣钱。其他四条路没有一条做得到。\n\n"
           "别的路要先把观众攒起来，这条路一开始就有。观众已经在了，而且已经在看，"
           "所以一件新东西当天下午就能到他们眼前，不用安排引荐，也不用等谁点头。"),

        _t("All of it stays yours: the listing, the photography, the packing, the postage, the "
           "customer emails, and the stock in the room. Volume comes from your own audience and "
           "from nowhere else, so a quiet month is quiet everywhere at once. A print run buys the "
           "better margin by taking on the risk — the copies that do not sell were paid for in "
           "advance.",

           "所有环节都还在你手上：上架、拍照、打包、寄件、回客户邮件，还有堆在房间里的货。"
           "销量只来自你自己的观众，没有第二个来源，所以一淡就是全线一起淡。"
           "批量印刷毛利更高，代价是风险你自己扛——卖不掉的那些，钱是先付掉的。")),

    "someone_else_sells": _opener(
        _t("A gallery funds the show, takes a commission and finds the buyers. Its own income "
           "depends on collectors who come back, so the people it introduces you to are people it "
           "expects to keep — which is why representation tends to raise what a single painting "
           "sells for rather than only how many sell.",

           "画廊出钱办展、抽佣金，并且负责找买家。它自己的收入取决于会回头再买的藏家，"
           "所以它介绍给你的人，是它打算长期留住的人——"
           "所以代理往往抬的是单张画的价，而不只是多卖几张。"),

        _t("The difference that matters is the direction the money runs: in a rental you pay for "
           "the room, and here the gallery pays for the show. Prices rise for a structural reason "
           "as well, since the person arguing for yours makes their own living from it.\n\n"
           "And standing on this route carries into the other four: an exhibition record is the "
           "one credential a publisher, an art director and a licensing buyer all read the same "
           "way, which is true of nothing else on this list.",

           "真正的区别在于钱的流向：租场地是你付场地费，这条路上是画廊出钱办展。"
           "价格会上去还有一层原因——帮你抬价的那个人，自己也靠这个吃饭。\n\n"
           "另外，你在这条路上站到的位置，会跟着你走到另外四条路上——"
           "出版社、艺术总监、授权买家读展览履历的方式是一样的，"
           "这份清单上没有第二样东西有这个作用。"),

        _t("Roughly half of each sale, and a say in what shows and when. Representation is also "
           "slow to start: the route in is attendance, then a letter, then months. And a "
           "gallery's attention follows its own programme, so a quiet year on their side is a "
           "quiet year on yours.",

           "每一笔销售的大约一半，以及展什么、什么时候展的部分决定权。"
           "代理这件事起步也慢：路径是先去看展，再写信，然后等上几个月。"
           "而且画廊的注意力跟着它自己的展览计划走，所以它清淡的一年，也是你清淡的一年。")),

    "work_goes_out": _opener(
        _t("Quiet money. An image is licensed for a defined use — stationery, homeware, "
           "packaging, book covers, brands — and the company licensing it handles manufacture, "
           "distribution and sale. The originals stay yours throughout; what changes hands is "
           "permission, for a stated place and a stated length of time.",

           "安静的钱。一张图按约定的用途授权出去——文具、家居、包装、书封、品牌——"
           "生产、铺货、销售都由拿到授权的公司负责。原作自始至终还是你的；"
           "交出去的是许可，限定在说好的场合和说好的期限之内。"),

        _t("It is the only one of the five that pays more than once for the same image; "
           "everywhere else a thing is made and then sold once. Nothing here asks for new "
           "painting, and public recognition is not part of the arrangement, so it suits a "
           "practice that wants to keep painting and manage as little else as possible.\n\n"
           "It is also the route least affected by where you live or what your visa says, since "
           "the buyer is a company anywhere and the goods are files — the only one of the five "
           "that would survive a move to another country unchanged.",

           "五条路里，只有这一条能为同一张图反复收钱；其他每一条都是做一件、卖一次。"
           "它不要求你另外画新东西，也不会带来公众知名度，"
           "所以你要是只想一直画下去、别的事尽量少管，这条路合适。\n\n"
           "住在哪里、签证是什么，对这条路的影响也最小——买家可以是任何地方的公司，交付的是文件；"
           "五条路里，只有这一条在你搬到另一个国家之后还能原样继续。"),

        _t("The money arrives on somebody else's schedule and in somebody else's volumes. The one "
           "illustrator publishing her actual income split has a twenty-year licensing practice "
           "with M&S, John Lewis and Unilever, and licensing is 3% of what she earns. The terms "
           "are where the value sits, and an unlimited buyout signed across a body of work "
           "removes the ability to license it again — the one mistake on this route that costs "
           "years rather than yen.",

           "钱按别人的时间表、别人的销量到账。"
           "查到的插画师里，只有一位公开过自己的收入构成：做了二十年授权，客户包括 M&S、John Lewis、联合利华——"
           "授权只占她收入的 3%。价值在条款里，"
           "而对一批作品签下无限期买断，就等于放弃了日后再次授权它的可能；"
           "这是这条路上唯一一种代价以年计、而不是以钱计的错误。")),

    "between_covers": _opener(
        _t("Books as the object — bought because they are books, sitting in shops and on shelves "
           "with an ISBN and a distributor behind them. With a publisher, they finance the print "
           "run and carry the inventory; you supply the work and the idea of the book.",

           "书本身就是一件商品——别人是冲着它是一本书才买的，摆在店里、架子上，"
           "背后有 ISBN 和发行商。有出版社参与时，印刷的钱和库存由他们承担；"
           "你出的是作品，和这本书的构想。"),

        _t("This is the only route whose price is knowable before anything starts; every other "
           "door on the list is an application and a wait. The object also works on all four of "
           "the others — a finished book is what a gallery, a publisher and an art director are "
           "each shown — and a book on a shelf finds strangers, reaching people who will never "
           "see a post. With a publisher there is no outlay and no inventory either, and "
           "distribution reaches bookshops nationally, which nothing else here offers at all.",

           "这是五条路里唯一一条在开始之前就知道价钱的；清单上其他每一扇门，都是先申请，然后等。"
           "做出来的东西在其他四条路上也都用得上——画廊、出版社、艺术总监，拿给他们看的是同一本成品书——"
           "而书摆在架子上，陌生人会拿起来翻——这些人永远刷不到你的帖子。"
           "有出版社参与时，同样不用出钱、家里不堆书，而且发行能进入全国书店；"
           "这一点这份清单上别处完全没有。"),

        # The per-copy figures live in the economics table two blocks down; this
        # block gave the same royalty figure against ¥3,635 and the two read as one
        # paragraph printed twice. The cost that is not in the table is the
        # waiting, so that is what this says.
        _t("With a publisher, the variable is their consent, and it moves on a timescale nobody "
           "controls — a proposal can sit for months and come back as nothing. Their share of "
           "each copy is the other half of that trade, and the economics below put a number on "
           "it. Self-publishing removes the waiting by asking for the money up front, and leaves "
           "a room full of copies until they move.",

           "有出版社参与时，不确定的只有一件事：对方点不点头，而这件事的时间表没有人能控制——"
           "一份方案可能压上几个月，最后石沉大海。"
           "他们从每本书里抽走的那部分，是这笔交易的另一半，下面的账里有具体数字。"
           "自己出版没有等待这回事，代价是钱要先掏，而且在书卖动之前家里一直堆着。")),

    "on_assignment": _opener(
        _t("Editorial illustration, book covers, commissioned work. A brief arrives, the work is "
           "delivered, payment follows a schedule, and the fee is set against how widely the "
           "image will be used rather than how long it took.",

           "杂志插画、书籍封面、委托创作。对方提需求，你交稿，按约定时间付款；"
           "费用是按这张图会被用到多广来定的，而不是按你画了多久。"),

        _t("It is the only one of the five with a predictable monthly number, and it is the least "
           "romantic of them — those two facts are the same fact. The work is paid for before it "
           "exists, where everywhere else the painting is made first and sold afterwards, if at "
           "all, and there is no inventory and no unsold stock waiting in a room. It is the only "
           "route here where the work is commissioned before it is made, so whether anybody "
           "wants it is answered before the first mark.",

           "五条路里只有这一条每月收入可以预期，也是最不浪漫的一条——这两件事其实是同一件事。"
           "这里是先付钱、后有作品；其他每一条都是先把画画出来，之后才谈卖不卖得掉。"
           "没有库存，也没有卖不掉的存货堆在房间里。"
           "这也是这里唯一一条“先被委托、后动笔”的路——有没有人要，在落第一笔之前就有答案了。"),

        _t("The subject, the schedule and the finished image stop being entirely yours. A ¥70,000 "
           "cover is close to what one of your own originals earns with no brief attached to it. "
           "And rates vary enormously between clients, which is the mechanism by which the "
           "portfolio you show decides which clients arrive.",

           "题材、进度和最终画面，不再完全由你决定。"
           "一张 70,000 日元的封面，和你自己一张原作挣到的差不多，而原作没有附带任何要求。"
           "另外，不同客户之间价差极大——所以才有那句话：你拿什么作品集，就接到什么活。")),
}


FUTURES = [
    {
        "id": "no_gatekeepers",
        # Names are dead plain by decision (Scott, 2026-09-06: "these titles are
        # terrible, what the hell does no gatekeepers even mean"). A title that
        # has to be decoded is a title that failed, and it fails twice as hard
        # translated. The texture moved down into the taglines, which is where a
        # reader has already agreed to spend a second.
        "name": _t("Selling Direct", "直接卖"),
        # The card explained her own practice back to her for six drafts — "the
        # work is made and distributed directly", "prints and postcards: low
        # margin, steady volume". She has run a shop for years (Scott: "she
        # already sells direct so you don't need to tell her what selling
        # direct is"). A card about a thing she does daily earns its place only
        # with something she does NOT already know. Hence the one finding it
        # leads on: the gap between ¥2,200 and ¥31,900, which is invisible from
        # inside her own shop because it is the part that isn't there.
        "blocks": _OPENERS["no_gatekeepers"] + _SELLING_DIRECT,
        "tagline": _t("Your own shop, your own prices, everything above cost.",
                      "自己的店，自己定价，扣掉成本，剩下的全归你。"),
    },
    {
        "id": "someone_else_sells",
        "blocks": _OPENERS["someone_else_sells"] + _GALLERIES,
        "name": _t("Galleries", "画廊"),
        "tagline": _t("A gallery sells your originals and finds the buyers.",
                      "画廊卖你的原作，并且负责找买家。"),
    },
    {
        "id": "work_goes_out",
        "blocks": _OPENERS["work_goes_out"] + _LICENSING,
        "name": _t("Licensing", "图像授权"),
        "tagline": _t("Someone pays to use a painting you have already made.",
                      "有人付钱，使用你已经画好的一张画。"),
    },
    {
        "id": "between_covers",
        "blocks": _OPENERS["between_covers"] + _PUBLISHING,
        "name": _t("Publishing", "出版"),
        "tagline": _t("A publisher makes a book of your work, and pays for it.",
                      "由出版社把你的作品做成一本书，钱也由他们出。"),
    },
    {
        "id": "on_assignment",
        "blocks": _OPENERS["on_assignment"] + _COMMISSIONS,
        "name": _t("Commissions", "委托"),
        "tagline": _t("Someone pays you to paint something new, to a brief.",
                      "有人付钱请你按要求画一张新的。"),
    },
]


def _standing(record: dict) -> dict:
    """One line per route, in the collapsed header under the tagline.

    The five routes sit closed by default, so what she actually sees is five
    names and five taglines carrying equal weight, with nothing saying which one
    she is already standing next to. This line is what makes the list navigable
    in the second before she picks one to open.

    It is a statement of what exists, never a grade. A reviewer proposed the
    graded form — "strongest fit", "promising, untested", "selective fit", with
    a note that one route has "not yet much evidence of commercial demand" — and
    that is three rules at once: Bible11 ("Saffron describes. She does not
    rank."), the no-verdicts rule this file was rewritten under, and the
    negation rule. The facts underneath the grades were sound, so the facts are
    here and the grades are not.

    The counts are read from her record for the reason the old ledger was: a
    hardcoded "two solo shows" goes stale the day there is a third, which is
    exactly how earlier career copy ended up calling a 2023 group show her
    latest news. Note that this is one line where the removed ledger was a
    four-bullet panel with a list of what she lacks attached — the difference is
    the point, not the arithmetic.
    """
    solos = record.get("solo_shows", 0)
    groups = record.get("confirmed_group_shows", 0)
    pubs = record.get("publications_confirmed", 0)
    zines = record.get("zines", 0)
    return {
        # Was "about 26,000" — the Instagram figure, and stale even for that. On
        # the route whose whole point is that nobody stands between her and a
        # buyer, the number that matters is everyone she can reach without a
        # gatekeeper: ~233,000 across five accounts (X 89.3k, Weibo 65k,
        # Xiaohongshu 44k, Instagram 27k, Bilibili 7.5k) — Weibo added
        # 2026-09-09. Quoting 26,000 here understated the one asset this
        # pathway runs on by nearly nine times.
        "no_gatekeepers": _t(
            "About 233,000 followers across five accounts and a shop already running, with a "
            "price ladder that stops at ¥2,200 and starts again at ¥31,900.",
            "五个账号合计约 23.3 万人在关注，店铺也已经开着；价位到 2,200 日元就断了，再往上直接跳到 31,900。"),
        # NOT "every room so far paid for from your side", which was here until
        # 2026-09-07. It graded her choices, and it graded them on a premise that
        # is probably wrong: Galerie LE MONDE is an illustration-world gallery
        # whose value is the people its owner introduces, so a fee paid there
        # bought introductions rather than twelve days of wall. Calling that
        # "paid for from your side" reads as a verdict on a decision she made
        # well. The venue is named instead of scored.
        "someone_else_sells": _t(
            f"{solos} solo shows and {groups} group shows, the most recent at Galerie LE MONDE in "
            "Harajuku.",
            f"{solos} 场个展、{groups} 场联展，最近的一场在原宿的 Galerie LE MONDE。"),
        # NOT "six years of images already made" — the route's own first block
        # opens on exactly that, and the two lines shared 42% of their content.
        # A different true fact instead: the subject sells into categories the
        # rest of the illustration market cannot reach.
        "work_goes_out": _t(
            "A subject that sells into interiors, hospitality, stationery and publishing — "
            "categories character work never reaches.",
            "一个能卖进室内、酒店餐饮、文具和出版的题材——角色类作品到不了的那些品类。"),
        "between_covers": _t(
            f"{zines} zines, {pubs} publications, and six years of daily work to build a book "
            "from.",
            f"{zines} 本 zine、{pubs} 本出版物，还有六年每天画下来的画，够从里面做出一本书。"),
        "on_assignment": _t(
            "Six years of delivering to a daily schedule, and a subject Japanese literary "
            "publishers buy covers in.",
            "六年来，你每天都按时把画交出来；你的题材也会被日本的文学类出版社买去做封面。"),
    }


def build(record: Optional[dict] = None) -> dict:
    """The five routes, the frame they answer to, and the five experiments.

    `record` supplies the counts in the standing lines and nothing else — see
    `_standing`. An earlier version took the same numbers and printed a
    per-route ledger of what she has and has not done; both halves are gone, and
    the argument is back only for the one line that replaced them.

    Her record still decides what the routes SAY — it is why Selling Direct
    opens on a price gap instead of an explanation of selling — but that is
    applied by whoever writes a block, never printed as a scoreboard.
    """
    standing = _standing(record or {})
    return {
        "futures": [{
            "id": f["id"],
            "name": f["name"],
            "tagline": f["tagline"],
            # Read in the collapsed row, so it is the one thing here written to
            # be useful without opening anything.
            "standing": standing.get(f["id"]),
            # A generic block list, so each route takes the shape its subject
            # wants instead of wearing a fixed five-part schema whether or not
            # it has five parts to say.
            "blocks": f["blocks"],
        } for f in FUTURES],
        # The frame the whole tab answers to, and the five experiments it ends
        # on. Without these the five routes are five essays with nothing joining
        # them - which is what six earlier drafts were.
        "frame": _FRAME,
        "first_steps": _FIRST_STEPS,
    }
