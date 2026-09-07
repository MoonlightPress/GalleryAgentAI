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

from .book_economics_engine import DEFAULT_PRICE as _BOOK_PRICE, reference_run
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
# ⚠ ONE CLAIM HERE IS UNVERIFIED, and is in the copy because Scott's source
# document has it (2026-09-06): "Colour Diary has already shown that a finished
# book can function this way", under Selling Direct. A verification pass on
# 2026-09-05 pulled the stronger form of the same claim — that Colour Diary had
# functioned as a pitch to a publisher — after finding no record of it, and the
# publishing research found no evidence either way that a finished book triggers
# acquisition. The weaker form as written may well be true (it was a real
# published book that went to shops); it has not been checked. Verify or cut it.
#
# The second claim that pass removed is still out: the letter's reference to a
# show she had not attended. `outreach_kit_engine` keeps that line a placeholder,
# and the letter is imported from there rather than retyped.

_FRAME = _t(
    "You already have a working practice: six years of paintings, an audience, direct sales, "
    "commissions and a record of exhibitions.\n\n"
    "The useful question now is where another route gives you something the current one cannot.\n\n"
    "An original already earns ¥31,900–115,500. That is the benchmark. Anything added to the "
    "practice should earn from work you have already made, reach buyers you cannot reach "
    "yourself, increase what the rest of the work is worth, or create revenue without requiring "
    "another original.\n\n"
    "The five routes below do different versions of that.",

    "你已经有一套运转起来的实践：六年的画、一群观众、直接销售、委托，还有一份展览履历。\n\n"
    "现在值得问的是：换一条路，能拿到什么是现在这条拿不到的。\n\n"
    "一张原作已经能卖到 31,900–115,500 日元，这是衡量的基准。往这套实践里再加东西，"
    "至少要做到其中一件：让画完的作品再挣一次钱，触到你自己够不着的买家，"
    "把其余作品的价值抬上去，或者不必再画一张原作也能有收入。\n\n"
    "下面五条路，各自是这件事的一个版本。")


_SELLING_DIRECT = [
    {"kind": "prose", "label": _t("Fill the gap between ¥2,200 and ¥31,900",
                                  "把 2,200 到 31,900 日元之间的空档补上"),
     "text": _t(
        "You already sell successfully at both ends: postcards, zines and prints at ¥1,100–2,200, "
        "then originals beginning at ¥31,900. "
        "The missing part is the middle. "
        "Someone who has bought a zine and a print has no way to spend ¥5,000, ¥10,000 or ¥20,000 "
        "with you. The next purchase available is an original. "
        "The easiest test is to add that middle without buying inventory first.",

        "两头你都卖得动：明信片、zine、印刷品在 1,100–2,200 日元，原作从 31,900 日元起。"
        "空的是中间那一段。"
        "一个买过 zine、买过印刷品的人，在你这里花不掉 5,000、10,000 或者 20,000 日元——"
        "再往上就直接是原作了。"
        "最省事的试法，是先把中间补上，而且不先囤货。")},

    {"kind": "table", "label": _t("Start with three products", "先从三样东西开始"),
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

        "先用按需印刷上架。有人下单才做一件，所以这一轮试验不用起印量，也不用地方堆货。"
        "毛利率比自己印低。现阶段这反而有用：库存的风险压在印厂那边，"
        "你只要弄清楚这样东西有没有人买。")},

    {"kind": "prose", "text": _t(
        "For products that already sell reliably, your existing model is better. A ten-pack of "
        "postcards costs about ¥170 when printed in a run of one hundred, against ¥1,835 on "
        "demand. Keep those in-house. "
        "If one of the new formats begins selling consistently, batch production becomes the "
        "second step.",

        "已经卖得稳的东西，还是你现在的做法划算。一套十张的明信片，印一百套时一套约 170 日元，"
        "按需印刷要 1,835 日元。这些继续自己印。"
        "新形态里哪一样开始稳定出货，再转批量生产，那是第二步。")},

    # Every figure in this paragraph and in the "Hardcover, China" row below is
    # read from book_economics_engine rather than typed. It was typed once and
    # drifted — 107 here against that engine's computed 109 — and the same page
    # then said two different things about the same run.
    {"kind": "prose", "label": _t("What decides whether it sells", "什么决定卖不卖得动"),
     "text": _t(
        "A follower count does not predict sales. Across the paired cases that could be checked, "
        "the share of an audience that actually bought ran from 0.26% to 15.8%, and the largest "
        "audience of the set converted worst. Price is the lever instead: a Tokyo illustrator "
        "with 27,000 followers, about the same reach, published an art book at ¥11,000 and sold "
        "400 copies in four months, roughly ¥4 million. "
        "Two smaller levers decide most of the rest. Where those 26,000 live changes the "
        "arithmetic more than how many they are, since air mail runs ¥2,720 a kilo to the US "
        "against ¥185 across Tokyo — and that split is one figure inside your own Instagram "
        "insights. And anything under three centimetres thick is worth ¥465 on every domestic "
        "parcel, decided at the design stage, before anything is printed.",

        "粉丝数预测不了销量。在能够核对的成对案例里，真正掏钱的人占观众的比例从 0.26% 到 15.8%，"
        "而其中观众最多的那一位转化率最低。真正的杠杆是价格：一位东京插画师，两万七千粉丝，"
        "规模和你差不多，自出版的画集定价 11,000 日元，四个月卖了 400 本，约四百万日元。"
        "剩下的大半由两个小一些的杠杆决定。这两万六千人住在哪里，比他们有多少人更能改变这笔账——"
        "航空小包寄一公斤到美国 2,720 日元，寄到东京市内 185 日元——"
        "而这个比例就是你自己 Instagram 后台里的一个数字。"
        "另外，厚度控制在三厘米以内，每件国内包裹省 465 日元；这是在设计阶段、开印之前就定下的。")},

    {"kind": "prose", "label": _t("The book is a different decision", "书是另一个层面的决定"),
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
        "cost about ¥31,000 and can go directly to a publisher, gallery or shop buyer. Colour "
        "Diary has already shown that a finished book can function this way.",

        "如果这本书是当商品卖，在查过的几种做法里，中国印的精装本账最划算。"
        "如果这本书是用来敲另一扇门的，那就只做三本。Blurb 三本约 31,000 日元，"
        "可以直接拿给出版社、画廊或者书店买手。《Colour Diary》已经证明成品书能起到这个作用。")},

    {"kind": "links", "label": _t("Where", "去哪里做"),
     "items": [
        {"name": _t("pixivFACTORY / BOOTH — first test for posters, canvas and framed prints",
                    "pixivFACTORY / BOOTH——海报、画布、装裱印刷的第一次试水"),
         "url": "https://factory.pixiv.net/"},
        {"name": _t("SUZURI — useful for smaller paper goods and low-risk experiments",
                    "SUZURI——小件纸制品，低风险的尝试"),
         "url": "https://suzuri.jp/"},
        {"name": _t("INPRNT — the useful addition for buyers outside Japan",
                    "INPRNT——面向日本以外的买家时，值得加上的一个"),
         "url": "https://www.inprnt.com/"},
     ]},
]


_GALLERIES = [
    {"kind": "prose", "label": _t("Find a gallery that carries the exhibition risk",
                                  "找一家愿意承担办展风险的画廊"),
     "text": _t(
        "You already know how to organise a solo show. You have done it three times. "
        "The next useful gallery relationship is one that contributes something you currently "
        "supply yourself: the room, staffing, collectors, sales work and financial risk. "
        "The economics are unusually clear.",

        "办个展你已经会了，办过三次。"
        "下一段值得建立的画廊关系，要能接过你现在自己扛的那几样：场地、看场的人、藏家、"
        "销售的活，还有资金上的风险。"
        "这笔账算得异常清楚。")},

    {"kind": "table",
     "headers": [_t("", ""), _t("You pay", "你付"), _t("They take", "他们抽"),
                 _t("Sales needed before you are even", "打平前要卖掉")],
     "rows": [
        {"cells": [_t("Representing gallery", "代理画廊"), _t("¥0", "0"), _t("about 50%", "约 50%"),
                   _t("¥0", "0")]},
        {"cells": [_t("Moon Gallery rental", "Moon Gallery 租赁"), _t("¥100,000 / 5 days", "10 万 / 5 天"),
                   _t("0%", "0%"), _t("about one painting", "约一张画")]},
        # NOT "rental". The gallery states plainly that it is 「場所貸し」ではない
        # — the director picks who shows, from the work and from recommendations
        # by illustrators already showing there. Filing her show under "rental"
        # priced a selection as a room booking (Scott, 2026-09-07; confirmed at
        # galerielemonde.com/about and in the 2023 GENSEKI interview).
        {"cells": [_t("Galerie LE MONDE, 12-day solo", "Galerie LE MONDE，12 天个展"),
                   _t("¥374,000 / 12 days", "37.4 万 / 12 天"), _t("30%", "30%"),
                   _t("about six paintings", "约六张画")]},
     ]},

    {"kind": "prose", "text": _t(
        "A 50% gallery commission can look large in isolation. Against a ¥374,000 fee plus 30%, "
        "representation is cheaper until that exhibition reaches about ¥1.87 million in sales. "
        "That comparison covers the money and misses what the fee bought at LE MONDE. The gallery "
        "chooses who shows: the director picks illustrators from the work itself and from "
        "recommendations by illustrators already showing there, and says he is looking at whether "
        "somebody connects to a particular kind of commercial job. The dates came with being "
        "chosen. "
        "The more important difference is who brings the buyers. "
        "So far, people buying your work have largely found you. Representation adds a collector "
        "base belonging to somebody else.",

        "单看 50% 的抽成会觉得高。对着 374,000 日元的费用再加 30% 来算，代理一直更便宜，"
        "直到那场展卖到约 187 万日元为止。"
        "这个比法算清了钱，却漏掉了在 LE MONDE 那笔费用换到的东西。那家画廊挑人："
        "主理人从作品本身、以及已经在那里办展的插画家的推荐里选人，"
        "并且说他看的是这个人能接上哪一类商业工作。档期是跟着「被选中」一起来的。"
        "更要紧的分别在于：买家是谁带来的。"
        "到现在为止，买你画的人基本上是自己找上门的。代理带来的，"
        "是一份原本属于别人的藏家名单。")},

    # The find of 2026-09-07. Same director, same address, two more businesses,
    # and she has already been through the gallery door. The agency line says
    # "not recruiting" because the site says so — a route stated as open when it
    # is closed is the failure this file keeps catching.
    #
    # This block was cut once, same day, on the reasoning that she showed there
    # in August and knows all of it. Scott put it back: "bragging about how
    # important that gallery is will make her feel great. she should see what a
    # great thing she just did." Do not cut it again.
    #
    # The line that separates this from the padding rule two rules up: these are
    # facts about LE MONDE, not assessments of her. Naming the roster and the
    # clients says what the institution is and lets her weigh what showing there
    # was worth. "You did well to show there" would be the version that breaks
    # the rule, and it is not what is written here.
    {"kind": "links", "label": _t("The same address, three businesses",
                                  "同一个地址，三门生意"),
     "items": [
        {"name": _t("Agence LE MONDE — the illustration agency the gallery's director also runs. Roster of about ten; clients include McDonald's, Asahi, Mizuho, ANNA SUI, GUCCI, Quarto and Pokémon. Every illustrator on it showed at the gallery first. The site says it is not recruiting at the moment.",
                    "Agence LE MONDE——画廊主理人同时经营的插画经纪公司。代理约十位；客户包括麦当劳、朝日啤酒、瑞穗银行、ANNA SUI、GUCCI、Quarto、宝可梦。名单上的每一位都是先在画廊办过展。网站写明目前不招募。"),
         "url": "https://www.agencelemonde.com/"},
        {"name": _t("Studio LE MONDE — risograph studio in the same building, open since September 2023. Tuesday to Sunday, 12:00–19:00, printing booked as a session with staff. contact@studiolemonde.com",
                    "Studio LE MONDE——同一栋楼里的孔版印刷工作室，2023 年 9 月起。周二至周日 12:00–19:00，印刷按有工作人员在场的时段预约。contact@studiolemonde.com"),
         "url": "https://www.studiolemonde.com/"},
        {"name": _t("Galerie LE MONDE — exhibition enquiries go by email, then a usage form. Six days ¥198,000, twelve days ¥374,000. hello@galerielemonde.com",
                    "Galerie LE MONDE——办展先发邮件谈，再填使用申请表。六天 198,000 日元，十二天 374,000 日元。hello@galerielemonde.com"),
         "url": "https://www.galerielemonde.com/about"},
     ]},

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
    {"kind": "links", "label": _t("The immediate target found in Tokyo",
                                  "在东京找到的、可以马上去的一家"),
     "items": [
        {"name": _t("biscuit gallery — its grid next open call has run every year since 2024. No application fee and no display fee, open to students and to artists under about forty who have not shown there before. The 2026 round took applications from late December to 30 April for an August show, so the next window opens around December.",
                    "biscuit gallery——它的 grid next 公开征集从 2024 年起每年都办。不收报名费，也不收展位费，面向学生以及大约四十岁以下、此前没有在那里展过的作者。2026 那一轮的申请是十二月底到四月三十日，展览在八月，所以下一个窗口大约在十二月打开。"),
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
        "徐冰也在这份名单上，这说明它比一封初次去信能够到的位置要靠前好几段。"
        "把它记住，是为了知道天花板长什么样。")},

    {"kind": "prose", "label": _t("A third arrangement, worth more than either",
                                  "还有第三种安排，比哪一种都划算"),
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
        "和十个说得通的空间建立关系，比给一百个说不通的空间发信管用。")},

    {"kind": "prose", "label": _t("The first letter", "第一封信"),
     "text": _t(
        "The first contact only has to make the work easy to look at. "
        "Use one link, five paintings from one series and one specific sentence showing why that "
        "gallery was chosen. "
        "For Gallery Kogure:",

        "第一次联系，只需要让人容易看到作品。"
        "一个链接，同一个系列的五张画，还有一句具体的话，说明为什么选了这一家。"
        "给 GALLERY KOGURE 的例子：")},

    # The letter is not retyped here. `outreach_kit_engine` owns it, including
    # the fix that matters: the show-attended line is a placeholder, because a
    # hardcoded "A Little Gem" sent her to claim she had been to a show she had
    # not been to. One copy of the letter, one place to fix it.
    {"kind": "letter", "text": _OUTREACH["letter_ja"]},

    {"kind": "list", "label": _OUTREACH["rules_label"], "items": _OUTREACH["rules"]},
]


_LICENSING = [
    {"kind": "prose", "label": _t("Let the archive earn again", "让已经画完的东西再挣一次钱"),
     "text": _t(
        "Licensing has one unusual advantage for you: the inventory already exists. "
        "Six years of daily painting is thousands of images that can potentially produce income "
        "while the originals remain yours. "
        "The value depends primarily on where and how an image is used:",

        "授权对你有一个别处没有的优势：库存已经在了。"
        "六年的日课是好几千张图，它们可以在原作仍然归你的情况下带来收入。"
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

    {"kind": "prose", "label": _t("Make a small cover-ready series", "画一小组能直接当封面用的"),
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
        "值得专门去设计的，是构图上的要求。"
        "封面要放得下字，也要经得起裁切。画一小组竖构图，留出有意为之的安静区域——"
        "天空、雾、水面、墙、阴影，或者上三分之一整片留白。"
        "这样艺术总监手上就有了能围着它做封面的图，而作品看上去还是一眼就认得出是你的。"
        "五到十张，就够开出一个授权作品集的头。"
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
        {"name": _t("Bridgeman Studio — represents roughly a thousand artists for licensing and is currently accepting illustration submissions",
                    "Bridgeman Studio——代理约一千位艺术家做授权，目前正在接受插画投稿"),
         "url": "https://www.bridgemanimages.com/en/studio"},
     ]},

    {"kind": "note", "text": _t(
        "This route can begin with work you already own and expand through paintings designed "
        "specifically for commercial use.",

        "这条路可以从你已经有的作品开始，再靠专门为商业用途画的作品往外扩。")},
]


_PUBLISHING = [
    {"kind": "prose", "label": _t("Pitch a book that still needs to be made",
                                  "提一本还没做出来的书"),
     "text": _t(
        "The strongest publishing opportunity is a book concept with enough identity that a "
        "publisher can imagine selling it. "
        "Your existing paintings establish that you can execute it. The proposal establishes what "
        "the book is. "
        "That distinction matters because the publishers checked ask for projects and proposals. "
        "In the comparable Tokyo architecture title, forty of the fifty paintings were made after "
        "the deal was agreed. "
        "A strong proposal therefore needs:",

        "出版这条路上最有力的机会，是一个面貌足够清楚、让出版社能想象出怎么卖的书的构想。"
        "你已有的画证明你做得出来；企划书说明的是这本书到底是什么。"
        "这个分别之所以要紧，是因为查过的这几家出版社要的是企划和构想。"
        "那本可比的东京建筑画集，五十张画里有四十张是在合同谈定之后才画的。"
        "所以一份有力的企划书要有：")},

    {"kind": "list",
     "items": [
        _t("the idea of the book", "这本书的构想"),
        _t("why the paintings belong together", "这些画为什么属于同一本书"),
        _t("a sample sequence", "一段样张的排序"),
        _t("several finished works showing the visual language", "几张完成作品，用来呈现视觉语言"),
        _t("what remains to be painted", "还有哪些要画"),
        _t("the intended reader", "预设的读者"),
        _t("a rough scale and format", "大致的规模与开本"),
     ]},

    {"kind": "prose", "text": _t(
        "Your six-year archive gives you unusually strong material for that proposal even if the "
        "final book contains new work.",

        "即使最后成书用的是新画的作品，你这六年的积累也让这份企划书有异常扎实的底子。")},

    {"kind": "prose", "label": _t("The economics", "这笔账"),
     "text": _t(
        "Publishing is weak as a per-copy revenue stream and strong as distribution.",
        "论每本能拿多少，出版是弱的；论发行，它是强的。")},

    {"kind": "table",
     "headers": [_t("", ""), _t("You keep per copy", "每本你拿到"), _t("300 copies", "300 本")],
     "rows": [
        {"cells": [_t("Publisher", "出版社出版"), _t("¥115–240", "115–240 日元"),
                   _t("¥34,500–72,000", "34,500–72,000 日元")]},
        {"cells": [_t("Self-published hardcover", "自己出版的精装本"), _t("¥3,635", "3,635 日元"),
                   _t("¥1,090,500", "1,090,500 日元")]},
     ]},

    {"kind": "prose", "text": _t(
        "The publisher's contribution is everything surrounding those royalties: financing the "
        "print run, national bookshop distribution, ISBN, production, inventory and a publication "
        "record that remains attached to your name. "
        "Those benefits make the most sense when the book is expected to strengthen the rest of "
        "the practice as well as sell copies.",

        "出版社真正给的是围着那点版税的一切：出印刷的钱、进全国书店、一个 ISBN、制作、库存，"
        "还有一条会一直挂在你名字上的出版记录。"
        "当这本书除了卖出去，还被指望去带动其余的实践时，这些好处才最说得通。")},

    # "What a book costs" was a standalone section until 2026-09-07, sitting
    # apart from the two routes that already discuss books. Its own claim says
    # what it is for — the cost is knowable to the yen, the sell-through is not,
    # and carrying that gap is what a publisher is — which makes it evidence for
    # the fork directly above, not a section. Behind a lid, because it answers a
    # question only some readers are asking at this point.
    {"kind": "component", "id": "book_economics",
     "label": _t("What the book itself costs to make",
                 "做出这本书本身要花多少钱")},

    {"kind": "links", "label": _t("Three publishers with a published route in",
                                  "三家把入口写出来的出版社"),
     "items": [
        {"name": _t("マール社 — accepts proposals directly and finances accepted books itself",
                    "マール社——直接接受企划，通过之后由他们出钱做书"),
         "url": "https://www.maar.com/"},
        {"name": _t("青幻舎 — has a dedicated proposal route asking for a plan, portfolio and images",
                    "青幻舎——有专门的企划投递通道，要企划书、作品集和图像"),
         "url": "https://www.seigensha.com/"},
        {"name": _t("MdN — accepts portfolios and proposals and has already published successful Tokyo architecture books",
                    "MdN——接受作品集与企划，而且已经出过卖得很好的东京建筑画集"),
         "url": "https://books.mdn.co.jp/"},
     ]},

    {"kind": "note", "text": _t(
        "The next useful piece of work here is therefore one book proposal, built well enough to "
        "send to all three with small changes.",

        "所以这条路上接下来真正有用的一件事，是把一份书的企划书做扎实，"
        "扎实到只要小改一下就能同时递给这三家。")},
]


_COMMISSIONS = [
    {"kind": "prose", "label": _t("Price the painting and the usage separately",
                                  "画和用途，分开定价"),
     "text": _t(
        "A commission asks you to give up something your originals preserve: complete control "
        "over the subject, schedule and finished image. "
        "So the fee has to compensate for that, or the commission has to create value somewhere "
        "else. "
        "The national rate card gives a useful floor:",

        "接委托意味着交出一些你画自己作品时保有的东西：题材、进度和最终画面的完全掌控。"
        "所以要么费用能补回这一点，要么这次委托得在别处产生价值。"
        "全国费率表给了一个有用的底线：")},

    {"kind": "table",
     "headers": [_t("Use", "用途"), _t("Published rate", "公开费率")],
     "rows": [
        {"cells": [_t("Book cover", "书籍封面"), _t("¥70,000", "70,000 日元")]},
        {"cells": [_t("Magazine cover", "杂志封面"), _t("¥100,000", "100,000 日元")]},
        {"cells": [_t("Small internal illustration", "内页小图"), _t("¥5,000", "5,000 日元")]},
        {"cells": [_t("Average coordinated job", "经手工作的平均值"), _t("¥71,327", "71,327 日元")]},
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
        "所以 70,000 日元一张封面，差不多就是你一张现有原作的价钱。"
        "当授权范围扩大、图像被再次使用，或者这次发表把作品带到下一个客户面前时，"
        "商业委托才变得更有吸引力。"
        "同一张图反复被用时，二次使用可以按原稿费的 70%、50%、50%、20% 再付。"
        "要护住的正是这一部分。")},

    {"kind": "prose", "label": _t("Build the terms before the enquiry arrives",
                                  "在询问找上门之前，先把条款准备好"),
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

    {"kind": "prose", "text": _t(
        "That turns an ambiguous “How much for a painting?” into something you can price "
        "consistently. "
        "Platform terms matter as well:",

        "这样一来，「画一张多少钱」这种含糊的问题，就变成了你可以稳定报价的东西。"
        "平台条款同样要紧：")},

    {"kind": "table",
     "headers": [_t("Platform", "平台"), _t("Copyright", "版权")],
     "rows": [
        {"cells": [_t("Skeb", "Skeb"), _t("Transfer prohibited; artist retains it",
                                          "禁止转让；版权留在作者手里")]},
        {"cells": [_t("ココナラ", "ココナラ"),
                   _t("Artist retains copyright while granting broad usage rights",
                      "版权归作者，但授予对方很宽的使用权")]},
        {"cells": [_t("SKIMA opt販売", "SKIMA opt 販売"),
                   _t("Copyright assigned by default, including overseas rights",
                      "默认转让版权，包括海外权利")]},
     ]},

    {"kind": "links", "label": _t("Two useful doors now", "现在就有两扇有用的门"),
     "items": [
        {"name": _t("ザ・チョイス — ¥1,500 entry; age, nationality and professional status are explicitly unrestricted. Accepts unframed originals.",
                    "ザ・チョイス——报名费 1,500 日元；年龄、国籍、是否职业都明确不设限。收不装裱的原作。"),
         "url": "https://illustration-mag.jp/choice"},
        {"name": _t("HB FILE — ¥7,000 entry; every entrant's file remains available to designers and publishers in the gallery for a year.",
                    "HB FILE——报名费 7,000 日元；每位参加者的作品档案会在画廊向设计师和出版社开放一年。"),
         "url": "https://hbgallery.com/compe.html"},
     ]},

    {"kind": "note", "text": _t(
        "Both are inexpensive ways to place the work in front of people who commission illustration.",
        "这两条都很便宜，都是把作品放到「会下委托的人」眼前的方式。")},
]


_FIRST_STEPS = {
    "label": _t("What to do first", "先做什么"),
    "intro": _t(
        "These routes do not require a career change. Each can be tested with one small piece of "
        "work.",
        "这几条路都不要求你改变职业方向。每一条都可以用一件很小的事去试。"),
    "steps": [
        {"route": _t("Direct", "直接销售"),
         "step": _t("list an A2 poster, A1 poster and framed A4 print on demand.",
                    "用按需印刷上架一张 A2 海报、一张 A1 海报和一张装裱的 A4 印刷。")},
        {"route": _t("Gallery", "画廊"),
         "step": _t("choose one gallery exhibition to attend and prepare a five-image series link.",
                    "选一场画廊的展去看，并准备好一个五张同系列作品的链接。")},
        {"route": _t("Licensing", "授权"),
         "step": _t("make the first five vertical, cover-ready paintings.",
                    "画出头五张竖构图、可以直接当封面用的画。")},
        {"route": _t("Publishing", "出版"),
         "step": _t("turn one existing body of work into a one-page book concept.",
                    "把已有的一组作品，写成一页纸的书的构想。")},
        {"route": _t("Commissions", "委托"),
         "step": _t("write a reusable fee-and-licence template before the next enquiry arrives.",
                    "在下一个询问到来之前，写好一份可以反复用的「费用＋授权」模板。")},
    ],
    "close": _t(
        "That gives you five experiments. Their results will tell you much more than choosing one "
        "of the five in advance.",
        "这样你就有了五个实验。它们的结果能告诉你的，远比事先在五条路里挑一条要多。"),
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

           "作品通过你自己的店铺出去——文案你写、价格你定、包裹你打——"
           "钱按每一笔销售走，卖掉一件到一件。"
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
           "¥115–240 of a ¥4,400 book, and a licence pays once for a use somebody else has "
           "defined — here everything above cost stays on your side. You set the price rather "
           "than arguing for it, and nothing waits on an application, a jury or somebody's "
           "programme, so a decision made on Monday can be earning by Friday. None of the other "
           "four can do that.\n\n"
           "It also starts from something the others have to build first. The audience is already "
           "there and already looking, so a new product reaches it the same afternoon, with no "
           "introduction to arrange and nobody's permission to wait for.",

           "整个毛利都归你。画廊抽走一笔销售的大约一半，出版社在一本 4,400 日元的书里给你留下 "
           "115–240 日元，授权是按别人定好的用途一次性付钱——在这条路上，成本之上的全部留在你这边。"
           "价格是你定的，不需要替它争取；也没有任何一件事要等申请、等评审、等别人的排期，"
           "所以周一做的决定，周五就可能在挣钱。其他四条路没有一条做得到。\n\n"
           "它的起点也是别的路要先搭出来的东西。观众已经在了，而且已经在看，"
           "所以一件新东西当天下午就能到他们眼前，不用安排引荐，也不用等谁点头。"),

        _t("All of it stays yours: the listing, the photography, the packing, the postage, the "
           "customer emails, and the stock in the room. Volume comes from your own audience and "
           "from nowhere else, so a quiet month is quiet everywhere at once. A print run buys the "
           "better margin by taking on the risk — the copies that do not sell were paid for in "
           "advance.",

           "所有环节都还在你手上：上架、拍照、打包、寄件、回客户邮件，还有堆在房间里的货。"
           "销量只来自你自己的观众，没有别的来源，所以淡的月份是同时到处都淡。"
           "批量印刷用承担风险换来更好的毛利——卖不掉的那些，钱是先付掉的。")),

    "someone_else_sells": _opener(
        _t("A gallery funds the show, takes a commission and finds the buyers. Its own income "
           "depends on collectors who come back, so the people it introduces you to are people it "
           "expects to keep — which is why representation tends to raise what a single painting "
           "sells for rather than only how many sell.",

           "画廊出钱办展、抽佣金，并且负责找买家。它自己的收入取决于会回头再买的藏家，"
           "所以它介绍给你的人，是它打算长期留住的人——"
           "这也是为什么代理往往抬高的是单张画卖多少，而不只是卖掉几张。"),

        _t("The difference that matters is the direction the money runs: in a rental you pay for "
           "the room, and here the gallery pays for the show. Prices rise for a structural reason "
           "as well, since the person arguing for yours makes their own living from it.\n\n"
           "And standing on this route carries into the other four: an exhibition record is the "
           "one credential a publisher, an art director and a licensing buyer all read the same "
           "way, which is true of nothing else on this list.",

           "真正的分别在于钱的流向：租场地是你付房租，这条路上是画廊出钱办展。"
           "价格会上去还有一个结构性的原因——替你的价格争取的那个人，自己也靠它吃饭。\n\n"
           "另外，在这条路上的位置会带到其他四条路上去——"
           "展览履历是出版社、艺术总监和授权买家都会以同样方式去读的那一项，"
           "这份清单上没有第二样东西有这个作用。"),

        _t("Roughly half of each sale, and a say in what shows and when. Representation is also "
           "slow to start: the route in is attendance, then a letter, then months. And a "
           "gallery's attention follows its own programme, so a quiet year on their side is a "
           "quiet year on yours.",

           "每一笔销售的大约一半，以及展什么、什么时候展的部分决定权。"
           "代理这件事起步也慢：进入的方式是先到场，然后写信，然后等上几个月。"
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
           "它不要求你另外画新东西，也不包含公众知名度，"
           "所以它适合一种想一直画下去、其余的事尽量少管的工作方式。\n\n"
           "它也是受你住在哪里、签证是什么影响最小的一条——买家可以是任何地方的公司，交付的是文件；"
           "五条路里，只有这一条在你搬到另一个国家之后还能原样继续。"),

        _t("The money arrives on somebody else's schedule and in somebody else's volumes. The one "
           "illustrator publishing her actual income split has a twenty-year licensing practice "
           "with M&S, John Lewis and Unilever, and licensing is 3% of what she earns. The terms "
           "are where the value sits, and an unlimited buyout signed across a body of work "
           "removes the ability to license it again — the one mistake on this route that costs "
           "years rather than yen.",

           "钱按别人的时间表、别人的销量到账。"
           "目前找到的唯一一位公开自己收入构成的插画师，做了二十年授权，客户包括 M&S、John Lewis、联合利华——"
           "授权只占她收入的 3%。价值在条款里，"
           "而对一批作品签下无限期买断，就等于放弃了日后再次授权它的可能；"
           "这是这条路上唯一一种代价以年计、而不是以钱计的错误。")),

    "between_covers": _opener(
        _t("Books as the object — bought because they are books, sitting in shops and on shelves "
           "with an ISBN and a distributor behind them. With a publisher, they finance the print "
           "run and carry the inventory; you supply the work and the idea of the book.",

           "书作为一件东西——别人因为它是一本书才买下它，摆在店里、架子上，"
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
           "而书摆在架子上会被陌生人拿起来，到达那些永远不会看到一条帖子的人。"
           "有出版社参与时，同样不用出钱、家里不堆书，而且发行能进入全国书店；"
           "这一点这份清单上别处完全没有。"),

        # The per-copy figures live in the economics table two blocks down; this
        # block gave the same ¥115-240 against ¥3,635 and the two read as one
        # paragraph printed twice. The cost that is not in the table is the
        # waiting, so that is what this says.
        _t("With a publisher, the variable is their consent, and it moves on a timescale nobody "
           "controls — a proposal can sit for months and come back as nothing. Their share of "
           "each copy is the other half of that trade, and the economics below put a number on "
           "it. Self-publishing removes the waiting by asking for the money up front, and leaves "
           "a room full of copies until they move.",

           "有出版社参与时，变量是对方同不同意，而这件事的时间表没有人能控制——"
           "一份企划可能压上几个月，最后回来的是没有下文。"
           "他们从每本里拿走的那一份是这笔交易的另一半，下面的账里有具体数字。"
           "自己出版把等待这一项去掉了，代价是钱要先掏，而且在书卖动之前家里一直堆着。")),

    "on_assignment": _opener(
        _t("Editorial illustration, book covers, commissioned work. A brief arrives, the work is "
           "delivered, payment follows a schedule, and the fee is set against how widely the "
           "image will be used rather than how long it took.",

           "杂志插画、书籍封面、委托创作。需求送来，稿件交付，按约定时间付款；"
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
           "这也是这里唯一一条「先被委托、后动笔」的路——有没有人要，在落第一笔之前就有答案了。"),

        _t("The subject, the schedule and the finished image stop being entirely yours. A ¥70,000 "
           "cover is close to what one of your own originals earns with no brief attached to it. "
           "And rates vary enormously between clients, which is the mechanism by which the "
           "portfolio you show decides which clients arrive.",

           "题材、进度和最终画面不再完全是你的。"
           "一张 70,000 日元的封面，和你自己一张原作挣到的差不多，而原作没有附带任何要求。"
           "另外，不同客户之间价差极大——这正是「拿出什么作品集，就会被找去做什么活」的作用机制。")),
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
                      "自己的店，自己定价，成本之上全归你。"),
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
        "no_gatekeepers": _t(
            "About 26,000 followers and a shop already running, with a price ladder that stops at "
            "¥2,200 and starts again at ¥31,900.",
            "大约两万六千人在看，店铺已经在运转；价格阶梯停在 2,200 日元，再往上直接跳到 31,900。"),
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
            f"{zines} 本 zine、{pubs} 本出版物，还有六年的日课可以从中做出一本书。"),
        "on_assignment": _t(
            "Illustration and design training, and a subject Japanese literary publishers buy "
            "covers in.",
            "科班的插画与设计训练，以及一个日本文学出版社会买来做封面的题材。"),
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
