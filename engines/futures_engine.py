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

The names are deliberately flat: "Selling Direct", "Gallery Representation",
"Licensing the Images", "Making Books", "Commissioned Work". An earlier set was
written for atmosphere ("No Gatekeepers", "The Work Goes Out Without You") and
was killed on sight — a title nobody can decode has failed, and it fails harder
in translation. The atmosphere lives in the tagline, one line down, where a
reader has already agreed to spend a second. The `id` keys still carry the old
phrasing; they are internal and stable, and renaming them would buy nothing.

Four rules, each learned the hard way:

1. **No prescribed destination.** She is self-taught, independent, and runs
   everything herself; a system that tells such a person what to want reads as
   presumptuous however good the research is. Show the range; the choice is hers.
2. **Types of things to pursue, not credentials to acquire.** "A museum solo and
   critical press are required" is a wall. "This one is built out of art book
   fairs and consignment" is something to start on Tuesday.
3. **Money framed as what a door gives**, never as what anything has cost her.
4. **Describe, do not address** (Scott, 2026-09-05). The first draft of this file
   was written in the second person and full of encouragement — "further along
   this one than any other", "the record is real", "one of them answers". She did
   not ask for reassurance or for advice; she reads this for possibilities. So
   every path is stated as a set of conditions and mechanics, in the third
   person, with no imperatives, no verdicts about her, and no promises. The
   `position` ledger is facts on both sides — what is in place and what is
   absent — and lets the reader draw the conclusion.

Her position across the five is deliberately uneven and that asymmetry is the
most useful content here: one is far along and one is at zero, and neither is
visible from where she stands.

**Shape** (Scott, 2026-09-06: "this isn't very readable... it should be section
header, overview, advantages of track, her strengths in it, then dropdowns for
details"). Each future previously dumped five prose blocks in a row — life,
money, requires, position, example — and read as a wall. The reading order is
now:

    header      name + tagline
    overview    two sentences, not a paragraph
    advantages  what this one gives that the other four do not
    strengths   what is already in place for it, computed from her record
    details     money · what it needs · someone living it, each behind a lid

Two of those are new framings rather than renamed blocks. **Advantages** is a
comparison the copy never actually made: the old `life` paragraphs each buried
one or two genuinely comparative claims ("the defining difference is not
prestige, it is the direction the money runs") inside descriptive prose, and
those are now pulled out and stated as comparisons. **Strengths** is the
positive half of the old `position` ledger, promoted above the fold; the
`absent` half moves down into the "what it needs" disclosure, where it belongs
anyway, because leading with what she lacks is the thing this file exists to
stop.

The shape lives here rather than in `SaffronPage.jsx` — the component walks
`details` and renders whatever the engine put in it, so a block can be added,
reordered or folded away without touching React.
"""

from typing import Optional

from .book_economics_engine import reference_run


def _t(en: str, zh: str) -> dict:
    # ja is deliberately absent for now rather than machine-guessed; the UI
    # falls back to en. Japanese was cut from the site (Scott, 2026-09-04).
    return {"en": en, "zh": zh}


# The print-run arithmetic has one home, in book_economics_engine. It was typed
# out by hand here once and drifted (107 against that engine's computed 109),
# which is exactly the two-sections-of-one-page-disagreeing failure the Data
# Patch Rule is about.
_BOOK = reference_run()


# ── Selling Direct, as a business scenario ───────────────────────────────────
#
# Scott, 2026-09-06: "these are business scenarios. 'i want to self publish my
# work' — 'ok, well, these are the advantages of doing that. these are the
# difficulties. these are the types of things you can sell direct to consumers:
# originals, prints, zines, postcards, keychains, commissions, calendars, etc.'
# here are the economics of each. here are your break even points. here is how
# you market them."
#
# And: "make that as effortless for her as possible."
#
# So this card is not a description of a kind of life. It is a scenario with an
# advantages column, a difficulties column, every product she could actually
# sell with the cost of each on BOTH fulfilment routes, and the moves that
# follow. The fulfilment axis — print-on-demand against buying a run — was
# missing entirely from every earlier draft, and it is the axis that decides
# how much of her week this costs. She has never used print-on-demand.
#
# Every figure below traces to one of three reports produced 2026-09-06:
#   reports/direct_sales_pod_2026-09-06.md            (POD platforms)
#   reports/direct_sales_goods_costs_2026-09-06.md    (printers, postage)
#   reports/direct_sales_international_2026-09-06.md  (overseas, commissions)
# plus reports/book_economics_2026-09-05.md for the art-book row. Nothing here
# is estimated; where a number was not found, the row says so.

_SELLING_DIRECT = {
    # The order Scott spelled out on 2026-09-06, and the argument it makes:
    #   here's what you have -> here's what you're missing (the middle) ->
    #   here's what filling it would cost and what you'd keep -> holding stock
    #   is the wrong way to do THESE particular things -> so, drop shipping,
    #   here is what that is -> here is the chart for the items that suit
    #   watercolour architecture specifically -> margins -> where to do it today.
    #
    # The filter matters as much as the numbers: "she wouldn't do T shirts
    # because her work does not work for something like that." Apparel, mugs and
    # phone cases are dropped from the chart even though the platforms offer
    # them. What is left is paper, pigment and wall.
    #
    # Second person. No definitions of things she already knows - an earlier
    # draft opened by explaining what selling direct means, to someone who has
    # done it for years.
    "have_label": _t("What you already have", "你已经有的"),
    "have": _t(
        "Two ends of a ladder. Postcards, zines and prints between ¥1,100 and ¥2,200, all "
        "returning 75–99% because printed paper costs almost nothing to make. Then originals from "
        "¥31,900 to ¥115,500, and commissions on top of that.",
        "一道阶梯的两头。明信片、zine、画作印刷在 1,100 到 2,200 日元之间，"
        "回报率 75–99%，因为印在纸上的东西几乎没有成本。另一头是 31,900 到 115,500 日元的原作，"
        "再往上是委托。"),
    "missing_label": _t("What you are missing", "你缺的那一段"),
    "missing": _t(
        "Everything between them. After ¥2,200 the next thing you sell costs fourteen times as "
        "much. Someone who has bought a zine and a print and liked both has nothing to buy next — "
        "the next step you offer them is a ¥31,900 painting. Most people who would happily spend "
        "¥8,000 on you never get the chance.",
        "中间全空着。2,200 日元之后，下一样东西贵了十四倍。"
        "一个买过 zine 和印刷、并且都喜欢的人，接下来没有可买的了——你给他的下一级是 31,900 日元的原作。"
        "大多数本来愿意在你这里花八千日元的人，根本没有机会花。"),
    "fill_label": _t("What fills it, and what it would cost", "填进去的东西，以及成本"),
    "fill_headers": [_t("", ""), _t("Sells for", "售价"), _t("Costs to make", "做出来要多少"),
                     _t("You keep", "你留下")],
    "fill": [
        {"what": _t("Poster, A2", "海报，A2"), "price": _t("¥3,000", "3,000 日元"),
         "cost": _t("¥1,400", "1,400 日元"), "keep": _t("¥1,465", "1,465 日元")},
        {"what": _t("Poster, A1", "海报，A1"), "price": _t("¥5,000", "5,000 日元"),
         "cost": _t("¥2,550", "2,550 日元"), "keep": _t("¥2,268", "2,268 日元")},
        {"what": _t("Canvas, F3", "画布，F3"), "price": _t("¥7,000", "7,000 日元"),
         "cost": _t("¥3,350", "3,350 日元"), "keep": _t("¥3,300", "3,300 日元")},
        {"what": _t("Framed giclée, A4", "装裱微喷，A4"), "price": _t("¥20,000", "20,000 日元"),
         "cost": _t("¥12,000", "12,000 日元"), "keep": _t("¥7,507", "7,507 日元")},
        {"what": _t("Art book, 128pp", "画集，128 页"), "price": _t("¥4,950", "4,950 日元"),
         "cost": _t("¥1,315 each, 300 at a time", "每本 1,315，一次 300 本"),
         "keep": _t("¥3,635", "3,635 日元")},
    ],
    "why_not_stock_label": _t("Why not just print a batch", "为什么不干脆自己印一批"),
    "why_not_stock": _t(
        "Because these are the wrong things to hold. A hundred postcards is a padded envelope in "
        "a cupboard; a hundred A1 posters is a tube rack, and every order is a trip to the post "
        "office with something that cannot be folded. Canvases and frames are worse — bulky, "
        "fragile, expensive to send and expensive to be wrong about. The one exception is the art "
        "book, which cannot be made any other way, and which is why it is the only thing on that "
        "list you would pay for up front.",
        "因为这些恰恰是最不适合囤的东西。一百张明信片是柜子里的一个信封袋；"
        "一百张 A1 海报是一整排纸筒，而且每一单都要抱着一件不能折的东西跑一趟邮局。"
        "画布和画框更糟——占地方、易损、寄起来贵，押错了也贵。"
        "唯一的例外是画集，它没有别的做法，这也是那份清单上唯一一样需要你先掏钱的东西。"),
    "ds_label": _t("So: drop shipping", "所以：按需代发"),
    "ds": _t(
        "You upload the file once. When someone buys, the printer makes that one copy and posts it "
        "to them under their own name — you never see the parcel, never buy stock, never go to the "
        "post office. You are paid the difference between what it cost to make and what you "
        "charged. Nothing is manufactured until it is sold, so listing something costs you nothing "
        "at all.",
        "你把文件传上去一次。有人下单时，印厂就做那一件，用他们自己的名义寄给买家——"
        "你不会碰到包裹，不用进货，也不用跑邮局。你拿到的是售价和制作成本之间的差额。"
        "在卖出去之前不会有任何东西被制作出来，所以挂一件商品上去，你一分钱都不用花。"),
    "ds_fit_label": _t("Why it suits your work in particular", "为什么它特别适合你的作品"),
    "ds_fit": [
        _t("What these platforms are good at is flat, printed, pigment-on-paper things — posters, "
           "postcards, framed prints, canvas, panels. That is your entire practice.",
           "这些平台真正擅长的，就是平面的、印刷的、颜料落在纸上的东西——海报、明信片、"
           "装裱印刷、画布、画板。而这正好就是你全部的创作。"),
        _t("It is worst at apparel, mugs and phone cases, which is where most artists lose money "
           "anyway and which your work would not sit well on regardless.",
           "它最不擅长的是服装、马克杯和手机壳，而那本来就是多数创作者赔钱的地方，"
           "你的作品放上去本来也不合适。"),
        _t("Every one of the middle rungs above is bulky, fragile or both. Those are exactly the "
           "items where not holding stock is worth the most.",
           "上面那几级中间价位的东西，不是占地方就是易损，或者两样都占。"
           "恰恰是这类东西，不囤货省下来的最多。"),
        _t("On BOOTH the parcel goes out from ピクシブ株式会社. Your name and address are not on it.",
           "在 BOOTH 上，包裹以「ピクシブ株式会社」的名义寄出，上面没有你的姓名和地址。"),
    ],
    "ds_chart_label": _t("What you could list this week, and what you would keep",
                         "这个星期就能上架的东西，以及你能留下多少"),
    "ds_chart_headers": [_t("", ""), _t("Sells for", "售价"), _t("You keep", "你留下"),
                         _t("Margin", "毛利率")],
    "ds_chart": [
        {"what": _t("Poster, B3", "海报，B3"), "price": _t("¥2,480", "2,480 日元"),
         "keep": _t("¥1,087", "1,087 日元"), "margin": _t("39%", "39%")},
        {"what": _t("Poster, A2", "海报，A2"), "price": _t("¥3,000", "3,000 日元"),
         "keep": _t("¥1,465", "1,465 日元"), "margin": _t("44%", "44%")},
        {"what": _t("Poster, A1", "海报，A1"), "price": _t("¥5,000", "5,000 日元"),
         "keep": _t("¥2,268", "2,268 日元"), "margin": _t("43%", "43%")},
        {"what": _t("Framed giclée, A4", "装裱微喷，A4"), "price": _t("¥20,000", "20,000 日元"),
         "keep": _t("¥7,507", "7,507 日元"), "margin": _t("38%", "38%")},
        # The wall and paper goods a Japanese buyer expects from an illustrator,
        # and the ones that sit in the missing band. The acrylic panel is the
        # useful find - the research calls it "the closest thing to a framed
        # print", and at ¥2,500 it lands in the gap for a fifth of the price of
        # the giclée. No magnets: none of these platforms offer them.
        {"what": _t("Acrylic panel — a wall piece, framed-print feel",
                    "亚克力画板——挂墙的，接近装裱印刷的效果"),
         "price": _t("¥2,500", "2,500 日元"),
         "keep": _t("¥1,026", "1,026 日元"), "margin": _t("41%", "41%")},
        {"what": _t("Acrylic block", "亚克力方块"), "price": _t("¥5,000", "5,000 日元"),
         "keep": _t("¥1,365", "1,365 日元"), "margin": _t("27%", "27%")},
        {"what": _t("Postcards, set of ten", "明信片，十张一套"), "price": _t("¥3,000", "3,000 日元"),
         "keep": _t("¥1,055", "1,055 日元"), "margin": _t("31%", "31%")},
        {"what": _t("Clear file", "文件夹"), "price": _t("¥1,600", "1,600 日元"),
         "keep": _t("¥616", "616 日元"), "margin": _t("31%", "31%")},
        {"what": _t("Masking tape", "和纸胶带"), "price": _t("¥1,600", "1,600 日元"),
         "keep": _t("¥504", "504 日元"), "margin": _t("32%", "32%")},
        {"what": _t("Stickers", "贴纸"), "price": _t("¥800", "800 日元"),
         "keep": _t("¥436", "436 日元"), "margin": _t("36%", "36%")},
    ],
    "ds_note": _t(
        "Lower percentages than printing your own — you are paying someone to hold the risk. On "
        "the things you already sell in quantity, keep printing your own: a ten-pack of postcards "
        "costs ¥170 in a run of a hundred against ¥1,835 on demand. Drop shipping is for the rungs "
        "you do not have yet.",
        "毛利率比自己印低——你付的是别人替你承担风险的钱。已经卖得动、量也起来的东西，继续自己印："
        "一套十张的明信片，印一百套时成本 170 日元，按需印刷要 1,835 日元。"
        "按需代发是用来补你还没有的那几级的。"),
    "books_label": _t("Books you could make yourself", "你自己就能做的书"),
    "books_note": _t(
        "One rung on this ladder is a book, and the format decides everything. The result is "
        "backwards from what you would expect: a hardcover printed in China pays for itself "
        "sooner than a softcover printed in Japan, because the unit cost is lower and the cover "
        "price is higher. Japanese offset hardcover cannot pay for itself at all — it would need "
        "more copies sold than were printed.",
        "这道阶梯上有一级是书，而做成什么形态，决定了一切。结论和直觉相反："
        "在中国印的精装本，比在日本印的平装本更快回本，因为单价更低、定价更高。"
        "在日本做胶印精装则永远回不了本——要卖掉的册数比印的还多。"),
    "books_headers": [_t("", ""), _t("Each", "每本"), _t("You would pay", "你要先付"),
                      _t("Sells for", "售价"), _t("Back at", "回本点")],
    "books": [
        {"what": _t("Zine, B5, 24pp, stapled — what you make now",
                    "Zine，B5，24 页，骑马钉——你现在做的"),
         "each": _t("¥498", "498 日元"), "outlay": _t("¥49,800 for 100", "印 100 本，49,800 日元"),
         "price": _t("¥1,980", "1,980 日元"), "be": _t("34 of 100", "100 本里的 34 本")},
        {"what": _t("Softcover, 210mm square, 128pp", "平装，210mm 方形，128 页"),
         "each": _t("¥1,609", "1,609 日元"), "outlay": _t("¥482,700 for 300", "印 300 本，482,700 日元"),
         "price": _t("¥4,400", "4,400 日元"), "be": _t("173 of 300", "300 本里的 173 本")},
        {"what": _t("Softcover, A4, 128pp", "平装，A4，128 页"),
         "each": _t("¥1,306", "1,306 日元"), "outlay": _t("¥653,000 for 500", "印 500 本，653,000 日元"),
         "price": _t("¥4,400", "4,400 日元"), "be": _t("212 of 500", "500 本里的 212 本")},
        {"what": _t("Hardcover, 128pp, printed in China", "精装，128 页，在中国印"),
         "each": _t("¥1,315", "1,315 日元"), "outlay": _t("¥394,500 for 300", "印 300 本，394,500 日元"),
         "price": _t("¥4,950", "4,950 日元"), "be": _t("109 of 300 — the best of these", "300 本里的 109 本——这几种里最好的")},
        {"what": _t("Hardcover, B5 offset, printed in Japan", "精装，B5 胶印，在日本印"),
         "each": _t("¥3,927", "3,927 日元"), "outlay": _t("¥1,963,500 for 500", "印 500 本，1,963,500 日元"),
         "price": _t("¥5,500", "5,500 日元"),
         "be": _t("1,249 — more than you printed", "1,249 本——比印的还多")},
    ],
    # Scott, 2026-09-06: "what about a small run as a way to entice publishers?"
    # This reframes the whole book question. A run judged as a PRODUCT has to
    # break even and small runs mostly cannot. A few copies judged as an OBJECT
    # TO SHOW does not have to break even at all - it has to exist and look
    # right. The research says so directly of Blurb: "never works as a resale
    # product... it is a proofing and personal-copy tool." That is the use.
    "proof_label": _t("Or a few copies, to put in front of someone",
                      "或者只做几本，拿去给人看"),
    "proof": _t(
        "A print run and a calling card are different objects, and only one of them has to break "
        "even. If the point is to hand a finished book to a publisher, a gallery or a shop buyer, "
        "you do not need three hundred of them — you need three. Print-on-demand is hopeless for "
        "reselling and ideal for exactly this, because there is no run to commit to at all. One "
        "Blurb copy is ¥10,275 and three are about ¥31,000, against ¥394,500 for a run you could "
        "actually sell. Colour Diary already did this job once.",
        "一批货和一张名片是两种东西，只有一种需要回本。如果目的是把一本成品书递到出版社、"
        "画廊或者书店买手手里，你不需要三百本——你需要三本。按需印刷拿来转卖是没戏的，"
        "但拿来做这件事正合适，因为根本不存在要押上的印量。Blurb 一本 10,275 日元，三本约 31,000，"
        "而能拿来卖的那种印量要 394,500。《Colour Diary》已经担任过一次这个角色。"),
    "today_label": _t("Where to do it, today", "今天就可以去这几个地方"),
    "today": [
        {"name": _t("pixivFACTORY — posters, canvas, framed prints, postcards. Sells through BOOTH, "
                    "which you can open in an afternoon.",
                    "pixivFACTORY——海报、画布、装裱印刷、明信片。通过 BOOTH 销售，一个下午就能开店。"),
         "url": "https://factory.pixiv.net/"},
        {"name": _t("SUZURI — stickers and smaller paper goods, no shop setup needed.",
                    "SUZURI——贴纸和小件纸制品，不需要另外开店。"),
         "url": "https://suzuri.jp/"},
        {"name": _t("INPRNT — prints for buyers outside Japan, who none of the above will post to. "
                    "Pays 50% of each sale.",
                    "INPRNT——面向日本以外的买家，上面几家都不寄国外。每笔销售支付 50%。"),
         "url": "https://www.inprnt.com/"},
    ],
}



# ── The other four realms ────────────────────────────────────────────────────
#
# Each is a generic block list so the shape can follow the realm rather than a
# fixed schema. Kinds: prose · note (inset) · list · table · links.
#
# Two rules Scott set on 2026-09-06, applied to all four:
#
#   1. Every realm is measured against what she ALREADY earns. One original is
#      ¥31,900-115,500, with no client, no brief and no deadline. That is the
#      yardstick, and it is stated even where a realm comes out worse - which
#      commissions does, on the fee alone.
#   2. Every realm states what it gives that ISN'T money. "Here is how this
#      system works and it is not to your benefit financially" is a legitimate
#      and useful thing for a section to say, but only if the non-monetary side
#      is stated too. Publishing pays ¥115-240 a copy and buys national
#      bookshop distribution; writing only the first half turns the section
#      into "don't bother", which is not a description, it is a verdict.
#
# Sources, all 2026-09-06 unless noted:
#   reports/galleries_2026-09-06.md
#   reports/licensing_2026-09-06.md
#   reports/publishing_2026-09-06.md
#   reports/commissions_2026-09-06.md
#   reports/book_economics_2026-09-05.md   (self-publishing comparison)

_BASELINE_EN = "One of your originals is ¥31,900–115,500, with no client, no brief and no deadline. That is the number every one of these has to beat."
_BASELINE_ZH = "你的一张原作是 31,900–115,500 日元，没有客户，没有要求，也没有交期。这几条路都要拿这个数字来比。"


_GALLERIES = [
    {"kind": "prose", "label": _t("How it works", "这件事是怎么运作的"),
     "text": _t(
        "Three arrangements share the word gallery and they are not the same business. A rental "
        "space sells you the room by the day. A consignment gallery hangs your work for nothing "
        "and takes a share of what sells. A gallery that represents you carries the cost of the "
        "show and takes a larger share, because its own income now depends on your prices going "
        "up.",
        "有三种安排共用「画廊」这个词，但它们是三门不同的生意。租赁空间是按天把场地卖给你。"
        "寄售画廊免费替你挂画，卖掉了抽成。代理你的画廊则自己承担办展的费用，抽成也更高——"
        "因为它自己的收入，从此取决于你的价格能不能往上走。")},
    {"kind": "table", "label": _t("What each one costs before you earn anything",
                                  "在你赚到第一块钱之前，每一种要花多少"),
     "headers": [_t("", ""), _t("You pay", "你要付"), _t("They take", "他们抽"),
                 _t("Paintings sold before you are even", "要卖掉几张画才打平")],
     "rows": [
        {"cells": [_t("A gallery that represents you", "代理你的画廊"), _t("Nothing", "不用付"),
                   _t("About 50%", "约 50%"), _t("None — the first sale is already profit",
                                                 "一张都不用——第一笔成交就已经是赚的")]},
        {"cells": [_t("Moon Gallery — rental", "Moon Gallery——租赁"),
                   _t("¥100,000 for 5 days", "5 天 10 万日元"), _t("Nothing", "不抽"),
                   _t("1", "1 张")]},
        {"cells": [_t("Galerie LE MONDE — rental", "Galerie LE MONDE——租赁"),
                   _t("¥374,000 for 12 days", "12 天 37.4 万日元"), _t("30%, and you pay for the DMs",
                                                                     "30%，宣传明信片还要你自己出"),
                   _t("6", "6 张")]},
     ]},
    {"kind": "note", "text": _t(
        "Which turns the usual complaint inside out. A gallery taking half sounds like the "
        "expensive option and is the cheapest room you can stand in: it costs nothing to enter "
        "and pays from the first sale. A rented room at ¥374,000 plus 30% only beats it once "
        "you have sold ¥1.87 million of work in twelve days.",
        "这就把平常那句抱怨整个翻了过来。「画廊要抽一半」听上去最贵，实际上是你能站进去的最便宜的一个房间："
        "进场不要钱，第一笔成交就开始分钱。而 37.4 万日元加 30% 的租赁空间，"
        "只有在十二天里卖出 187 万日元的作品之后，才会比它划算。")},
    {"kind": "list", "label": _t("What it gives you that is not money",
                                 "它给你的、不是钱的那部分"),
     "items": [
        _t("Buyers you would never have met. Everyone who has bought from you so far found you; a gallery's collectors are people who would not have.",
           "你自己遇不到的买家。到目前为止买过你作品的人，都是自己找上门的；画廊的藏家是那些不会自己找上门的人。"),
        _t("Someone whose own income depends on your prices rising. Nobody else in your working life has that incentive.",
           "有一个人，他的收入取决于你的价格能不能涨上去。你的工作里没有第二个人有这个动机。"),
        _t("A room, hung and lit and staffed, that you did not have to organise.",
           "一个布置好、打好灯、有人看场的空间，而且不用你自己张罗。"),
     ]},
    {"kind": "prose", "label": _t("The door is unmarked, not locked", "门没有锁，只是没挂牌"),
     "text": _t(
        "Eight Tokyo galleries were checked and none publishes a way in — but none publishes a "
        "refusal either. The advice that Tokyo galleries take no submissions comes from artists, "
        "never from a gallery, and nobody has ever quantified it. One gallery says the opposite "
        "out loud: biscuit gallery runs an open call, free to enter, students eligible, with a "
        "solo show as the prize.",
        "查了东京的八家画廊，没有一家公开写着怎么投稿——但也没有一家写着不收。"
        "「东京的画廊不接受投稿」这句话来自艺术家，从来不是来自画廊，而且没有人拿出过数据。"
        "有一家反而把话说反了：biscuit gallery 公开办征集，免费报名，接受学生，奖品是一次个展。")},
    {"kind": "links", "label": _t("Where to look", "可以从这几家看起"),
     "items": [
        {"name": _t("biscuit gallery — the one published open call, free, students eligible",
                    "biscuit gallery——唯一一个公开的征集，免费，接受学生"),
         "url": "https://biscuitgallery.com/"},
        {"name": _t("GALLERY KOGURE — Jimbocho. Roster includes photorealist urban scenes in ink on paper",
                    "GALLERY KOGURE——神保町。代理名单里有纸上水墨的写实城市景观"),
         "url": "https://gallerykogure.com/"},
        {"name": _t("Tokyo Gallery + BTAP — six Chinese artists on the roster, three working in ink on paper",
                    "Tokyo Gallery + BTAP——代理名单里有六位中国艺术家，其中三位做纸上水墨"),
         "url": "https://www.tokyo-gallery.com/"},
     ]},
    {"kind": "note", "text": _t(_BASELINE_EN, _BASELINE_ZH)},
]


_LICENSING = [
    {"kind": "prose", "label": _t("How it works", "这件事是怎么运作的"),
     "text": _t(
        "They are not buying the painting. They are buying permission to use it — for this book, "
        "in this country, for this long, in these formats. The painting stays yours and can be "
        "licensed again to someone else afterwards. The price has almost nothing to do with the "
        "picture and almost everything to do with the use.",
        "他们买的不是那张画，是使用它的许可——用在这本书上，在这个国家，用这么久，用这几种形式。"
        "画还是你的，之后还可以再授权给别人。价格几乎与画本身无关，几乎完全取决于用途。")},
    {"kind": "table", "label": _t("The same painting, priced by what it is used for",
                                  "同一张画，按用途定价"),
     "headers": [_t("Used as", "用作"), _t("Pays", "价格")],
     "rows": [
        {"cells": [_t("A small cut inside a magazine", "杂志内页的一小张插图"), _t("¥5,000", "5,000 日元")]},
        {"cells": [_t("A book cover", "书籍封面"), _t("¥70,000", "70,000 日元")]},
        {"cells": [_t("A magazine cover", "杂志封面"), _t("¥100,000", "100,000 日元")]},
        {"cells": [_t("A calendar", "挂历"), _t("¥800,000", "800,000 日元")]},
     ]},
    {"kind": "note", "text": _t(
        "One image, a hundred and sixty times the range. This is the whole subject: what is being "
        "sold is the use, so the first question about any offer is never how much, it is what for "
        "and for how long. Japan's published rate card prices copyright transfer — 著作権譲渡, "
        "handing it over permanently — at two to three times the licence fee. Anyone offering a "
        "flat fee and expecting to own the picture is asking for a discount of two thirds.",
        "同一张图，价格差一百六十倍。这就是这件事的全部：卖的是用途，"
        "所以面对任何一个报价，第一个问题从来不是「多少钱」，而是「用来做什么、用多久」。"
        "日本公开的费率表把「著作权转让」——也就是永久交出去——定在授权费的两到三倍。"
        "有人开一个总价、又想连版权一起拿走，等于是在要一个三分之二的折扣。")},
    {"kind": "prose", "label": _t("Why your existing paintings mostly cannot be covers",
                                  "为什么你已经画好的画大多做不了封面"),
     "text": _t(
        "A cover crops the image and puts type across it, so it needs empty space that was planned "
        "for. Both Japanese authorities that publish licensing tariffs exclude altered images, and "
        "one excludes covers by name for exactly this reason. The market for painterly, "
        "figureless, atmospheric covers is real and growing — it is documented as a deliberate "
        "move away from AI imagery — but it is reached by being commissioned to paint one, not by "
        "licensing one already painted.",
        "封面要裁切，还要在上面压字，所以它需要一块事先留出来的空白。"
        "日本两家公布授权费率的机构都把「经过改动的图像」排除在外，其中一家更是直接点名排除封面，原因正在于此。"
        "手绘的、没有人物的、讲氛围的封面，市场是真实的而且在扩大——有记录显示这是刻意在避开 AI 生成的图像——"
        "但进入这个市场的方式是被委托去画一张，而不是把已经画好的授权出去。")},
    {"kind": "prose", "label": _t("So paint some that can be", "那就画几张能当封面的"),
     "text": _t(
        "The thing stopping your existing work is compositional, not stylistic — the subject is "
        "already what this market wants. A cover is taller than it is wide, gets cropped, and "
        "needs a quiet area for the title, the author's name and a publisher's mark. Sky, fog, a "
        "blank wall, water, an empty upper third. None of that is a different kind of painting "
        "from the ones you already make; it is the same painting composed with a hole in it. And "
        "since you paint every day anyway, a handful made deliberately to those proportions costs "
        "you nothing you were not already spending.",
        "挡住你现有作品的是构图，不是风格——题材本身正是这个市场要的。"
        "封面比宽要高，会被裁切，还需要一块安静的地方放书名、作者名和出版社标志。"
        "天空、雾、一面空墙、水面，或者上三分之一整片留白。"
        "这些都不是另一种画法，还是你在画的那种画，只是构图时留了一个洞。"
        "而且你本来每天都在画，按这个比例特意画上几张，并不会多花你什么。")},
    {"kind": "note", "text": _t(
        "That also opens two doors your back catalogue cannot use. Arcangel — a business that "
        "exists only to sell book covers — keeps illustration as a top-level category beside "
        "photography and pays contributors 50% of net, with no minimum before it pays out. Its "
        "literary fiction collection is its smallest at 10,000 images, against 857,702 for "
        "contemporary fiction. The corner you would be aiming at is the emptiest shelf in the "
        "shop, which cuts both ways: less competition, and less traffic.",
        "这样还会打开两扇你的旧作用不上的门。Arcangel——一家只做书封生意的公司——"
        "把插画和摄影并列为一级分类，付给供稿人净额的 50%，而且没有起付门槛。"
        "它的文学小说图库是最小的一个，只有一万张，而当代小说有八十五万七千多张。"
        "你要瞄准的那个角落，是这家店里最空的一层货架——这一点是双向的：竞争少，来往的人也少。")},
    {"kind": "list", "label": _t("What it gives you that is not money",
                                 "它给你的、不是钱的那部分"),
     "items": [
        _t("The work goes places you will never go, and keeps earning after you have stopped thinking about it.",
           "作品会去到你永远不会去的地方，而且在你早就不再想着它之后，还在继续挣钱。"),
        _t("Nothing new has to be painted. This is the only realm here where the inventory is already six years deep.",
           "不需要新画一张。这是这里唯一一条「库存」已经积了六年的路。"),
        _t("It does not care where you live or what visa you hold. The buyer is a company somewhere and the goods are files.",
           "它不在意你住在哪里、拿的是什么签证。买家是某个地方的一家公司，交付的是文件。"),
     ]},
    {"kind": "links", "label": _t("Where to put the work", "把作品放到这些地方"),
     "items": [
        {"name": _t("イラストレーションファイルWeb — where Japanese art directors and book designers look",
                    "イラストレーションファイルWeb——日本的艺术总监和装帧设计师会去看的地方"),
         "url": "https://www.illustration-file.com/"},
        {"name": _t("amanaimages — Japanese stock licensing; ¥33,000–79,200 a cover licence",
                    "amanaimages——日本的图像授权；一次封面授权 33,000–79,200 日元"),
         "url": "https://amanaimages.com/"},
        {"name": _t("Arcangel — exists only to sell book covers, takes illustration, pays 50% of net",
                    "Arcangel——只做书封生意，收插画，付净额的 50%"),
         "url": "https://arcangel.com/become-a-contributor/"},
        {"name": _t("Bridgeman Studio — represents around a thousand artists for licensing, and says it is currently accepting submissions of illustration",
                    "Bridgeman Studio——为约一千位艺术家做授权代理，并且写明目前正在接受插画投稿"),
         "url": "https://www.bridgemanimages.com/en/studio"},
     ]},
    {"kind": "note", "text": _t(_BASELINE_EN, _BASELINE_ZH)},
]


_PUBLISHING = [
    {"kind": "prose", "label": _t("How it works", "这件事是怎么运作的"),
     "text": _t(
        "A publisher takes on a book of your paintings, pays for the printing, puts it into "
        "bookshops across the country and pays you a percentage of each copy. You put in no money "
        "and hold no stock. They decide the format, the print run and the timing, and they decide "
        "whether it happens at all.",
        "出版社把一本你的画集接下来，出印刷的钱，把书铺到全国的书店，再按每一本给你一个百分比。"
        "你不出钱，也不囤货。开本、印量、时间由他们定，做不做，也由他们定。")},
    {"kind": "table", "label": _t("What a copy is worth, either way", "一本书，两种做法各值多少"),
     "headers": [_t("", ""), _t("You keep per copy", "每本你留下"), _t("300 copies is worth", "300 本相当于")],
     "rows": [
        {"cells": [_t("Published by someone else", "由别人出版"),
                   _t("¥115–240 · 5–8% of the pre-tax price", "115–240 日元 · 税前定价的 5–8%"),
                   _t("¥34,500–72,000", "34,500–72,000 日元")]},
        {"cells": [_t("Published by you", "自己出版"), _t("¥3,635", "3,635 日元"),
                   _t("¥1,090,500", "1,090,500 日元")]},
     ]},
    {"kind": "note", "text": _t(
        "One copy you sell yourself is worth sixteen to thirty-two that a publisher sells for you. "
        "Selling three hundred yourself earns what a publisher earns you on five to sixteen "
        "thousand. There is also no advance: the guaranteed portion is paid at the end of the "
        "month of publication, not on signing. On the money alone this is the weakest thing on "
        "this page.",
        "你自己卖掉一本，抵得上出版社替你卖掉十六到三十二本。你自己卖三百本，"
        "相当于出版社替你卖五千到一万六千本。而且没有预付：保证的那部分在出版当月月底结算，不是签约时给。"
        "单看钱，这是这一页上最弱的一条。")},
    {"kind": "list", "label": _t("What it gives you that is not money",
                                 "它给你的、不是钱的那部分"),
     "items": [
        _t("Bookshops across the country, which self-publishing cannot reach at any price. The Tokyo architecture books that ran past a hundred thousand copies were published by MdN, not by their author.",
           "全国的书店——自出版无论花多少钱都进不去。那套卖过十万册的东京建筑画集，是由 MdN 出版的，不是作者自己出的。"),
        _t("A permanent object with an ISBN, in libraries and in second-hand shops for decades.",
           "一件有 ISBN 的、长久存在的东西，几十年里都会在图书馆和旧书店里。"),
        _t("A credential that keeps working after the print run sells out, in every conversation with a gallery, a publisher or an art director.",
           "一个在这一版卖完之后仍然有效的资历——面对画廊、出版社、艺术总监时，每一次谈话都用得上。"),
     ]},
    {"kind": "prose", "label": _t("What actually gets a book made", "真正促成一本书的是什么"),
     "text": _t(
        "A project, not a portfolio. Two international art publishers say outright that they do "
        "not look at portfolios; they want a book that has been thought through. Of the fifty "
        "paintings in the Tokyo architecture book, forty were made after the deal was signed — the "
        "book was proposed and then painted, not assembled from what already existed. There is no "
        "agent layer in Japan, so the proposal goes directly to the publisher.",
        "他们要的是一个企划，不是一本作品集。两家国际艺术书出版社明说不看作品集，"
        "他们想看的是一本已经想清楚的书。那本东京建筑画集里的五十张画，有四十张是在合同签下来之后才画的——"
        "书是先提出来、再画出来的，不是把现成的东西凑一本。日本没有经纪人这一层，企划直接递给出版社。")},
    {"kind": "links", "label": _t("The three doors that are actually published",
                                  "真正把门写出来的三家"),
     "items": [
        {"name": _t("マール社 — an open call for proposals, and it says plainly: not self-publishing, we bear the cost, sold in bookshops nationwide. A month of silence is a no.",
                    "マール社——公开征集企划，而且写得很清楚：这不是自费出版，费用由我社承担，在全国书店发售。一个月没有回音就是不通过。"),
         "url": "https://www.maar.com/"},
        {"name": _t("青幻舎 — a dedicated proposal form: portfolio, a written plan, images.",
                    "青幻舎——专门的企划投递表单：作品集、企划书、图像。"),
         "url": "https://www.seigensha.com/"},
        {"name": _t("MdN — the publisher of the Tokyo architecture books; accepts portfolios and proposals.",
                    "MdN——那套东京建筑画集的出版社；接受作品集与企划。"),
         "url": "https://books.mdn.co.jp/"},
     ]},
    {"kind": "note", "text": _t(_BASELINE_EN, _BASELINE_ZH)},
]


_COMMISSIONS = [
    {"kind": "prose", "label": _t("How it works", "这件事是怎么运作的"),
     "text": _t(
        "Two payments, not one. A fee for the work of painting it, and a licence for what they may "
        "do with it afterwards. A single number with no terms attached is a buyout: they own the "
        "picture, and you can never print it, sell it or license it again. Japan's published rate "
        "card puts that at two to three times a normal fee, so it is a thing to be paid for, not "
        "a thing to be assumed.",
        "是两笔钱，不是一笔。一笔是画这张画的劳务费，另一笔是他们此后可以拿它做什么的授权。"
        "只报一个总价、什么条件都不写，那就是买断：画归他们，你再也不能印它、卖它、把它授权出去。"
        "日本公开的费率表把买断定在正常费用的两到三倍，所以那是要收钱的，不是默认送出去的。")},
    {"kind": "table", "label": _t("What the national rate card says", "全国费率表上是怎么写的"),
     "headers": [_t("", ""), _t("Pays", "价格")],
     "rows": [
        {"cells": [_t("Book cover", "书籍封面"), _t("¥70,000", "70,000 日元")]},
        {"cells": [_t("Magazine cover", "杂志封面"), _t("¥100,000", "100,000 日元")]},
        {"cells": [_t("A small illustration inside", "内页小图"), _t("¥5,000", "5,000 日元")]},
        {"cells": [_t("Average across all jobs coordinated in a year", "一年里所有经手工作的平均值"),
                   _t("¥71,327", "71,327 日元")]},
     ]},
    {"kind": "note", "text": _t(
        "Hand-painted watercolour is named in that card by name, in the second-highest of five "
        "ranks. The rates above are the ones your medium is priced at, not a general figure.",
        "手绘水彩在那份费率表里是被点名写出来的，属于五级中的第二高级。"
        "上面这些价格，就是按你这个媒介定的，不是一个笼统的数字。")},
    {"kind": "prose", "label": _t("And ¥70,000 is not very much", "而 70,000 日元并不算多"),
     "text": _t(
        "It is roughly one of your originals, which you already sell with no client, no brief and "
        "no revisions. A hand-painted cover with sketch approval could take twenty to forty hours; "
        "nobody publishes an hour count for watercolour, so that is an estimate rather than a "
        "figure — but at the top of that range the fee is under ¥2,000 an hour. On the fee alone, "
        "this pays worse than painting what you want and selling it.",
        "这大约就是你的一张原作，而原作你现在就在卖，没有客户、没有要求、也不用改稿。"
        "一张手绘封面加上草图确认，可能要花二十到四十个小时；水彩的工时没有人公布过，"
        "所以这是估计而不是数据——但按上限算，时薪不到 2,000 日元。"
        "单看这笔费用，它比你画自己想画的、然后卖掉，要差。")},
    {"kind": "list", "label": _t("What makes it worth doing anyway",
                                 "那为什么它仍然值得做"),
     "items": [
        _t("¥70,000 is the bottom of the scale, not the top. The same painting is ¥800,000 as a calendar. What you are learning to price is the use, and the ceiling is eleven times a book cover.",
           "70,000 是这个尺度的底部，不是顶部。同一张画用作挂历是 800,000。你要学会定价的是用途，而天花板是一张书封的十一倍。"),
        _t("Secondary use pays again — 70%, 50%, 50% and 20% of the original fee as the same picture is reused. Painted once, paid four times.",
           "二次使用会再付一次——按原稿费的 70%、50%、50%、20%，同一张图被反复使用。画一次，收四次钱。"),
        _t("A credit is visible; a sold original is not. The private buyer takes the painting home and nobody sees it again. A published cover is how the next art director finds you.",
           "署名是看得见的，卖掉的原作不是。私人买家把画带回家，从此没有人再看到它。而一张出版过的封面，是下一位艺术总监找到你的方式。"),
     ]},
    {"kind": "note", "text": _t(
        "If those three do not happen, commissions are worse than what you do now. That is the "
        "honest test: not whether the first fee is good, but whether it leads to the second one.",
        "如果这三件事没有发生，那么接委托比你现在做的事更差。这就是老实的判断标准："
        "不是看第一笔钱好不好，而是看它有没有带来第二笔。")},
    {"kind": "table", "label": _t("Who keeps the copyright, by platform", "各平台的版权归谁"),
     "headers": [_t("", ""), _t("", "")],
     "rows": [
        {"cells": [_t("Skeb", "Skeb"), _t("Transfer is forbidden outright — the artist keeps it",
                                          "明确禁止转让——版权留在作者手里")]},
        {"cells": [_t("ココナラ", "ココナラ"), _t("You keep copyright, but grant a near-unlimited licence to use it",
                                                "版权归你，但授予对方一份近乎无限制的使用许可")]},
        {"cells": [_t("SKIMA (opt販売)", "SKIMA（opt 販売）"),
                   _t("Assigns copyright by default, including overseas — read before using",
                      "默认转让版权，包括海外——用之前先看清楚")]},
     ]},
    {"kind": "links", "label": _t("Two doors open to you now, both cheap",
                                  "现在就对你开着的两扇门，而且都不贵"),
     "items": [
        {"name": _t("ザ・チョイス — ¥1,500 to enter. Age, nationality and professional status are all explicitly irrelevant. Takes unframed originals.",
                    "ザ・チョイス——报名费 1,500 日元。年龄、国籍、专业与否，明确写着一概不问。收不装裱的原作。"),
         "url": "https://www.genkosha.co.jp/illustration/choice.html"},
        {"name": _t("HB FILE — ¥7,000, prints not originals. Win or lose, every entrant's file stays in the gallery for a year and is opened to designers and publishers.",
                    "HB FILE——7,000 日元，交印刷品而不是原作。无论得奖与否，每位参加者的作品档案都会在画廊保存一年，向设计师和出版社开放。"),
         "url": "https://hbgallery.com/compe.html"},
     ]},
    {"kind": "note", "text": _t(_BASELINE_EN, _BASELINE_ZH)},
]

FUTURES = [
    {
        "id": "no_gatekeepers",
        # Names are dead plain by decision (Scott, 2026-09-06: "these titles are
        # terrible, what the hell does no gatekeepers even mean"). A title that
        # has to be decoded is a title that failed, and it fails twice as hard
        # translated. The texture moved down into the taglines, which is where a
        # reader has already agreed to spend a second.
        "name": _t("Selling Direct", "直接卖"),
        # The business-scenario body. Only this card carries one so far; the
        # component falls back to the old shape for the other four, so they
        # keep working while they are converted one at a time.
        "scenario": _SELLING_DIRECT,
        # Rewritten 2026-09-06. Two things were wrong with this card and they
        # were the same thing.
        #
        # First, it explained her own practice back to her — "the work is made
        # and distributed directly", "prints and postcards: low margin, steady
        # volume". She has run a shop for years (Scott: "she already sells
        # direct so you don't need to tell her what selling direct is"). A card
        # about a thing she does daily has to earn its place with something she
        # does NOT already know, or it is condescension with a heading.
        #
        # Second, every one of its four `requires` bullets and its exemplar were
        # about recording an online course, under a heading about selling
        # paintings. Teaching is a different life; it is out of this card
        # entirely and parked rather than quietly folded somewhere else.
        #
        # What replaced both: the four findings in §5 of the book research that
        # a person already selling direct would not already have. All four are
        # measured, all four are actionable this week, and none of them is
        # visible from inside her own shop.
        "tagline": _t("The audience is already there. What moves the number is the price, not the follower count.",
                      "观众已经在了。真正让数字变动的是价格，不是粉丝数。"),
        "overview": _t(
            "Nothing on this path needs building — the shop runs, the work exists, about 26,000 "
            "people already follow it. What has never been tested is the middle of the price "
            "ladder: zines at ¥1,980, originals from ¥31,900, and nothing in between.",
            "这条路上没有什么要从头搭起来——店铺在运转，作品在，大约两万六千人已经在看。"
            "从来没有被试过的，是价格阶梯的中段：zine 卖 1,980 日元，原作从 31,900 日元起，中间是空的。"),
        "advantages": [
            # NB: the source report's own summary says the 906-follower artist
            # "produced fewer backers" than the 119K one — its table says 143
            # against 309, so the summary sentence is wrong and the table is
            # right. The finding is about RATE, not count: 15.8% against 0.26%.
            # Stated as rate here.
            _t("A follower count does not predict sales. Across the paired cases that could be checked, the share of an audience that actually bought ran from 0.26% to 15.8% — a sixtyfold spread — and the largest audience converted worst of all. Every named Japanese source asked the same question gave the same answer.",
               "粉丝数预测不了销量。在能够核对的成对案例里，真正掏钱的人占观众的比例从 0.26% 到 15.8% 不等——相差六十倍——而其中观众最多的那一位，转化率最低。所有被问到这个问题的日文来源，答案都一样。"),
            _t("The price is the lever. A Tokyo illustrator with 27,000 followers put a self-published art book out at ¥11,000 and sold 400 copies in four months — about ¥4 million. That price sits exactly in the empty middle of this shop's ladder.",
               "价格才是那根杠杆。一位东京插画师，两万七千粉丝，自出版的画集定价 11,000 日元，四个月卖了 400 本——约四百万日元。这个价格，正落在这家店铺阶梯上空着的中段。"),
            _t("Where the 26,000 live changes the arithmetic more than how many they are. Air mail to the US is ¥2,720 for a kilo — well over half the cover price of a ¥4,400 book, against ¥185 to post the same thing across Tokyo. That split is the largest unknown on this path, and it is one number inside her own Instagram insights.",
               "这两万六千人住在哪里，比他们有多少人更能改变这笔账。寄一公斤到美国，航空小包 2,720 日元——超过一本 4,400 日元的书定价的一半；而同样一件东西寄到东京市内是 185 日元。这个比例是这条路上最大的未知数，而它就是 Instagram 后台里的一个数字。"),
            _t("Under three centimetres thick is worth ¥465 on every parcel — ¥185 to post domestically instead of ¥650. It is decided at the design stage, before anything is printed, and the 428-page comparable was too thick for every cheap option.",
               "厚度控制在三厘米以内，每一件包裹就省下 465 日元——国内寄件 185 日元，而不是 650 日元。这是在设计阶段、开印之前就定下来的事；那本 428 页的参照书，因为太厚，所有便宜的寄件方式都用不了。"),
        ],
        "money": _t(
            "The costs on this path are small, fixed and mostly invisible until they have been "
            "paid. BASE takes 6.6% plus ¥40 a sale — about ¥330 on a ¥4,400 item; its cheaper "
            "plan only pays for itself past roughly 60 sales a month, so the standard one is the "
            "right one for now. Domestic postage is ¥185 under three centimetres and ¥650 over. "
            "Air mail abroad runs ¥1,250 to China, Korea or Taiwan, ¥2,130 to Europe and ¥2,720 "
            "to the US on a kilo; the illustrator who published his figures says higher shipping "
            "is what loses a sale between the cart and the checkout.",
            "这条路上的成本不大、固定，而且往往要等付掉了才看得见。BASE 每笔抽 6.6% 加 40 日元——"
            "一件 4,400 日元的商品大约 330 日元；它更便宜的方案要每月卖到六十件以上才划算，所以目前标准方案就是对的。"
            "国内邮费：厚度三厘米以内 185 日元，超过则 650 日元。寄到国外，一公斤的航空小包："
            "中国、韩国、台湾 1,250 日元，欧洲 2,130 日元，美国 2,720 日元；"
            "那位公开过自己数字的插画师说，运费一高，订单就在结账那一步流失掉。"),
        "requires": [
            _t("One number, from her own Instagram insights: what share of the 26,000 are in Japan. Everything else on this path prices differently depending on it, and looking it up takes a minute.",
               "一个数字，在自己的 Instagram 后台里：这两万六千人当中，有多大比例在日本。这条路上其余每一件事的定价都取决于它，而查一下只要一分钟。"),
            _t("One object priced in the empty middle of the ladder — somewhere between ¥1,980 and ¥31,900. That band is where the ¥11,000 comparable sits, and it is the only part of this shop that has never been tried.",
               "一件定价落在阶梯空档里的东西——在 1,980 和 31,900 日元之间。那本 11,000 日元的参照书正在这个区间，而这也是这家店铺唯一没试过的地方。"),
            _t("Three centimetres, decided at the design stage. It is worth ¥465 on every parcel and cannot be changed after printing.",
               "三厘米，在设计阶段就定下来。每件包裹省 465 日元，而且印完就改不了了。"),
            _t("A way to reach the people who have already bought, that is not the feed. Where a wide spread in sales could be explained at all, an existing list was the thing that explained it.",
               "一条能找到「已经买过的人」的通道，而不是靠信息流。凡是能解释销量为何差距如此之大的地方，能解释的那一项，都是一份已有的名单。"),
        ],
        "example": _t("タケウマ / studio_takeuma, in Tokyo: 27,000 followers — about the same audience — and a self-published 428-page art book at ¥11,000 that sold 400 copies in four months, roughly ¥4 million. He is an established commercial illustrator with a decade of bookshop relationships behind him, and it is one case, not a rate.",
                      "タケウマ / studio_takeuma，在东京：两万七千粉丝——观众规模差不多——自出版一本 428 页的画集，定价 11,000 日元，四个月卖出 400 本，约四百万日元。他是有十几年资历的商业插画师，背后有长期的书店关系；这是一个案例，不是一个比率。"),
    },
    {
        "id": "someone_else_sells",
        "blocks": _GALLERIES,
        "name": _t("Galleries", "画廊"),
        "tagline": _t("A gallery sells your originals and finds the buyers.",
                      "画廊卖你的原作，并且负责找买家。"),
        "overview": _t(
            "A gallery funds the show, takes a commission, and finds the buyers. Its own income "
            "depends on collectors who come back.",
            "画廊出钱办展、抽取佣金，并负责找买家。它自己的收入，取决于能不能找到会回头再买的藏家。"),
        "advantages": [
            _t("The defining difference is not prestige, it is the direction the money runs. In a rental arrangement the artist pays for the room; here the gallery pays for the show.",
               "这条路真正的分别不在名气，而在钱的流向。租赁场地时，是艺术家付场地费；在这条路上，是画廊出钱办展。"),
            _t("Per-painting prices rise for a structural reason: somebody whose own living depends on the price is the one arguing for it.",
               "每张画的价格会上去，原因是结构性的：替这个价格争取的人，自己也靠它吃饭。"),
            _t("A third arrangement sits between rental and representation and is worth more than either — an open call that pays the artist to exhibit. TOKAS gives ¥150,000 toward the work and charges nothing for the venue.",
               "在租场地和被代理之间还有第三种安排，比哪一种都划算：反过来付钱给艺术家办展的公开征集。TOKAS 提供 15 万日元制作经费，场地不收费。"),
            _t("Standing here carries into the other four. An exhibition record is the one credential a publisher, an art director and a licensing buyer all read the same way.",
               "在这条路上的位置会带到其他四条路上去。展览履历是出版社、艺术总监和授权买家都会以同样方式去读的那一项。"),
        ],
        "money": _t(
            "Commission replaces rent. A representing gallery takes 40–50%, more than a rental "
            "gallery's cut, against no payment up front, production and promotion covered, and "
            "buyers supplied. A third arrangement sits between the two and is worth more than "
            "either: an open call that pays the artist to exhibit. TOKAS gives ¥150,000 toward "
            "the work and charges nothing for the venue.",
            "佣金取代租金。代理画廊抽 40–50%，比租赁画廊抽得更多；代价的另一端是不需要预先付钱、"
            "制作与宣传由画廊承担、买家也由画廊带来。在两者之间还有第三种安排，比哪一种都划算："
            "反过来付钱给艺术家办展的公开征集。TOKAS 提供 15 万日元制作经费，场地不收费。"),
        "requires": [
            _t("Ten paintings that hang together as one body. Every funded door and every gallery conversation opens on the same ten.",
               "十张能作为一个整体挂在一起的画。每一个提供经费的项目、每一次与画廊的接触，面对的都是同样这十张。"),
            _t("Applications to the venues that pay rather than charge: TOKAS-Emerging around June, OPEN SITE around February, Kyoto Art Center around October.",
               "向那些付钱、而不是收钱的场地提交申请：TOKAS-Emerging 约在六月，OPEN SITE 约在二月，京都艺术中心约在十月。"),
            _t("Two visits, as a viewer, to each gallery whose roster resembles the work. Tokyo galleries run no submission box; the route in is attendance and then a letter.",
               "对每一家代理风格相近的画廊，以观众身份去两次。东京的画廊不设投稿箱，进入的方式是先到场，然后写信。"),
            _t("A first letter that requests nothing but a viewing. It contains no proposal, so there is nothing in it to decline, and any reply is a specification.",
               "一封只请求「看一下」的信。信里没有提案，所以没有什么可以被拒绝；而任何回复，本身就是一份要求说明。"),
        ],
        "example": _t("Where the road runs: Keita Morimoto paints night streets — a decade of them in Toronto before Tokyo — and is now with KOTARO NUKAGA in Japan and Almine Rech internationally, with work in the National Gallery of Canada and a 2025 solo at the 21st Century Museum in Kanazawa. That is far past a first gallery conversation, but it is the shape of the road.",
                      "这条路通向哪里：森本启太画夜晚的街道——来东京之前，他在多伦多画了十年——如今在日本由 KOTARO NUKAGA 代理，国际上则是 Almine Rech，作品被加拿大国立美术馆收藏，2025 年在金泽21世纪美术馆办个展。这已经远远超出「第一次与画廊接触」的阶段，但那条路的形状就是这样。"),
    },
    {
        "id": "work_goes_out",
        "blocks": _LICENSING,
        "name": _t("Licensing", "图像授权"),
        "tagline": _t("Someone pays to use a painting you have already made.",
                      "有人付钱，使用你已经画好的一张画。"),
        "overview": _t(
            "Quiet money. Images are licensed — stationery, homeware, packaging, book covers, "
            "brands — and other companies handle manufacture, distribution and sale.",
            "安静的钱。图像被授权出去——文具、家居、包装、书封、品牌——生产、铺货、销售都由别的公司负责。"),
        "advantages": [
            _t("The only one that pays more than once for the same image. Everywhere else on this list, a thing is made and then sold once.",
               "唯一一条同一张图可以反复收钱的路。这份清单上的其他每一条，都是做一件、卖一次。"),
            _t("Public recognition is not part of the arrangement, and nothing here asks for new painting. It fits a practice that wants to keep painting and manage as little as possible.",
               "这套安排里不包含公众知名度，也不要求为它另外画新作品。它适合一种想一直画下去、又尽量不去管别的事的工作方式。"),
            _t("The one least affected by residence or visa status. The buyer is a company anywhere and the goods are files.",
               "受居住地与签证状态影响最小的一条。买家可以是任何地方的公司，交付的是文件。"),
            _t("Architecture and cityscape reach buyers character work does not: interiors, hospitality, stationery, publishing, travel.",
               "建筑与城市题材能接触到角色类作品接触不到的买家：室内、酒店餐饮、文具、出版、旅行。"),
        ],
        "money": _t(
            "Two shapes. A flat fee is one payment for one defined use: simple, and capped. A "
            "royalty is a percentage of sales, ongoing and unbounded. One scale marker is worth "
            "having before the work goes in: the one illustrator found publishing her actual "
            "income split has a twenty-year licensing practice with M&S, John Lewis and "
            "Unilever, and licensing is 3% of her income against 77% from teaching. It pays "
            "well; it rarely pays most. Architecture and cityscape also licenses to a different "
            "set of buyers than character work — interiors, hospitality, stationery, publishing, "
            "travel.",
            "两种形式。一次性买断是一笔钱换一次约定用途：简单，但有上限。分成是按销售额抽成，持续发生，没有上限。"
            "投入之前有一个量级参考：目前找到的唯一一位公开自己收入构成的插画师，做了二十年授权，"
            "客户包括 M&S、John Lewis、联合利华——授权占她收入的 3%，教学占 77%。"
            "这条路可以赚钱，但很少成为收入的主要来源。另外，建筑与城市题材的授权对象和角色类作品完全不同："
            "室内、酒店餐饮、文具、出版、旅行。"),
        "requires": [
            _t("A set of images that hold up small and repeat. Licensing buys pattern and mood; single masterpieces are not the unit of sale.",
               "一组缩小之后依然成立、并且可以重复使用的图像。授权买的是图案与氛围；单张杰作不是这里的交易单位。"),
            _t("Contact with the categories already using this kind of imagery: stationery manufacturers, hotel and café interiors, publishers commissioning covers.",
               "与本来就在使用这类图像的领域建立接触：文具厂商、酒店与咖啡馆的室内、需要封面的出版社。"),
            _t("Contract literacy on one specific point. An unlimited buyout signed over a body of work removes the ability to license it again, and that is the one mistake here that costs years rather than money.",
               "在一个具体条款上的合同常识。对一批作品签下无限期买断，就等于放弃了日后再次授权它的可能；"
               "这是这条路上唯一一种代价以年计、而不是以钱计的错误。"),
        ],
        "example": _t("No verified example yet. This entry stays empty rather than carrying an invented one.",
                      "尚无经过核实的实例。此处留空，而不是填入一个杜撰的名字。"),
    },
    {
        "id": "between_covers",
        "blocks": _PUBLISHING,
        "name": _t("Publishing", "出版"),
        "tagline": _t("A publisher makes a book of your work, and pays for it.",
                      "由出版社把你的作品做成一本书，钱也由他们出。"),
        "overview": _t(
            "Books are the vehicle — not zines documenting a practice, but books bought because "
            "they are books.",
            "书是载体——不是记录创作过程的 zine，而是别人因为它是一本书才买下的书。"),
        "advantages": [
            _t("The only one of the five whose price is knowable before anything starts. Every other door on the list is an application and a wait.",
               "五条路里唯一一条在开始之前就能知道价钱的。清单上其他每一扇门，都是先申请，然后等。"),
            _t("The object works on the other four paths. A finished book is what a gallery, a publisher and an art director are each shown.",
               "做出来的东西在其他四条路上都用得上。画廊、出版社、艺术总监——拿给他们看的都是同一本成品书。"),
            _t("A book on a shelf finds strangers. It reaches people who will never see a post.",
               "书摆在架子上，会被陌生人拿起来。它能到达那些永远不会看到一条帖子的人。"),
            _t("The one fork inside this path changes more than any decision elsewhere on the list: whether a publisher is involved. With one there is no outlay and no inventory, and distribution reaches bookshops nationally, which self-publishing does not.",
               "这条路内部的那个岔口，比清单上任何其他决定都更能改变结果：有没有出版社参与。有出版社，就不需要出钱，家里也不堆书，发行能进入全国书店——这是自出版做不到的。"),
        ],
        "money": _t(
            f"Self-published, printed in China at {_BOOK['run']} copies: roughly "
            f"¥{_BOOK['outlay_jpy']:,} up front, recovered at {_BOOK['breakeven_direct']} copies sold "
            "directly. Printed in Japan at 100 copies it cannot break even at any sell-through; a "
            "small run is only viable at a high cover price. With a publisher there is no outlay "
            "and no inventory, the per-copy earning is roughly a tenth, and distribution reaches "
            "bookshops nationally. The publisher carries volume and risk. The variable it "
            "introduces is their consent. The whole arithmetic sits under “What a book "
            "costs” further down this page.",
            f"自己出版、在中国印 {_BOOK['run']} 本：前期约 {_BOOK['outlay_jpy']:,} 日元，"
            f"直接卖出 {_BOOK['breakeven_direct']} 本回本。"
            "在日本印 100 本，则无论卖得多好都无法回本；小批量只有在定价够高时才成立。"
            "有出版社时，不需要出钱，家里也不堆书，每本大约只拿十分之一，但发行能进入全国书店。"
            "出版社承担的是数量和风险。它引入的变量，是对方是否同意。"
            "完整的算法在本页下面的「一本书要花多少钱」里。"),
        "requires": [
            _t("Material, which already exists: six years of daily work is more than a book needs.",
               "材料——这一项已经具备：六年的日课，比做一本书所需要的还多。"),
            _t("Quotes from a Japanese and a Chinese printer against the same specification. The prices quoted to a Chinese speaker and to a foreigner are not the same prices.",
               "同一份规格，分别向日本和中国的印厂询价。报给中文使用者的价格，和报给外国人的价格，不是同一个价格。"),
            _t("A channel plan that does not depend on the audience: consignment in a few shops plus one fair booth. If those cover the run, direct sales become upside rather than a requirement.",
               "一套不依赖观众的销售计划：几家店的寄售，加一个书展摊位。如果这些能覆盖印量，"
               "直接销售就从「必须」变成了「额外」。"),
            _t("A finished object, if a publisher is the target. A self-published book is also the thing a publisher is shown; Colour Diary already performed that function once.",
               "如果目标是出版社，还需要一个成品。自己出的书同时也是拿给出版社看的东西；《Colour Diary》已经承担过一次这个功能。"),
        ],
        "example": _t("Mateusz Urbanowicz: his Tokyo architecture books (Tokyo Storefronts, Tokyo at Night) are published by MdN rather than self-published, and the series has passed 100,000 copies in Japan. He sells originals himself and has no gallery.",
                      "Mateusz Urbanowicz：他画东京建筑的书（《东京店构え》《东京夜行》）由 MdN 出版，不是自出版，这个系列在日本已经卖过十万册。原作由他自己销售，没有画廊代理。"),
    },
    {
        "id": "on_assignment",
        "blocks": _COMMISSIONS,
        "name": _t("Commissions", "委托"),
        # The "only predictable monthly number" claim moved into advantages,
        # where it belongs as a comparison; a tagline repeating it read twice.
        "tagline": _t("Someone pays you to paint something new, to a brief.",
                      "有人付钱请你按要求画一张新的。"),
        "overview": _t(
            "Editorial illustration, book covers, commissions. A brief arrives, the work is "
            "delivered, payment follows a schedule.",
            "杂志插画、书籍封面、委托创作。需求送来，稿件交付，按约定时间付款。"),
        "advantages": [
            _t("The only one of the five with a predictable monthly number. It is also the least romantic of them, and those two facts are the same fact.",
               "五条路里唯一一条每月收入可以预期的。它也是最不浪漫的一条——这两件事其实是同一件事。"),
            _t("The work is paid for before it exists. Everywhere else on this list the painting is made first and sold afterwards, if at all.",
               "这里是先付钱、后有作品。这份清单上的其他每一条，都是先把画画出来，之后才谈卖不卖得掉。"),
            _t("No inventory and no unsold stock. Nothing sits in a room waiting for a buyer.",
               "没有库存，也没有卖不掉的存货。不会有东西堆在房间里等买家。"),
            _t("Architecture and atmosphere are in specific demand for covers: literary fiction leans heavily on exactly this kind of image.",
               "建筑与氛围类的画在封面上有明确需求：文学小说的封面，大量依赖的正是这一类图像。"),
        ],
        "money": _t(
            "Per-commission fees, negotiated by scope of use. An agent takes 25–30% and supplies "
            "work that would not otherwise appear, though a large share of working illustrators "
            "operate without one and take commissions direct. Rates vary enormously by client, "
            "which is the mechanism by which the portfolio shown determines the work offered.",
            "按单收费，按使用范围议价。经纪人抽 25–30%，带来的是自己接触不到的工作；"
            "不过相当一部分一直在接活的插画家并没有经纪人，都是直接对接。"
            "不同客户之间价差极大——这正是「拿出什么作品集，就会被找去做什么活」的作用机制。"),
        "requires": [
            _t("A portfolio built around use rather than paintings. A cover mock-up reads to an art director in a way an exhibition photograph does not.",
               "一份围绕「用途」而不是「画作」构建的作品集。对艺术总监而言，一个封面样稿的可读性，和一张展览照片完全不同。"),
            _t("Entry to the industry's own competitions — The Choice, HB Gallery FILE. Those are where Japanese art directors look.",
               "参加这个行业自己的比赛——The Choice、HB Gallery FILE。日本的艺术总监会去看的就是这些。"),
            _t("Direct approach to publishers. Japanese literary publishers commission covers continuously.",
               "直接联系出版社。日本的文学出版社持续在找人画封面。"),
            _t("An agent, last. Representation follows a workload that needs managing; it does not precede it.",
               "经纪人放在最后。代理是在有活要管之后才出现的，不在那之前。"),
        ],
        "example": _t("Tatsuro Kiuchi: book jackets, editorial and advertising — Ikeido Jun's novels, the New York Times, Penguin, Uniqlo. He works without an agent; commissions come direct.",
                      "木内达朗：书籍封面、杂志插画与广告——池井户润的小说、《纽约时报》、企鹅出版、优衣库。他没有经纪人，工作直接找上门。"),
    },
]


_MONEY_LABEL = _t("How the money works", "钱是怎么来的")
_NEEDS_LABEL = _t("What this path needs", "这条路需要什么")
_LIVING_LABEL = _t("Someone living it", "有人正在这样生活")
_ABSENT_LABEL = _t("Of these, not in place yet", "这些里面，目前还没有的")


def build(evidence: Optional[dict] = None) -> dict:
    """Assemble each future in reading order: overview, advantages, strengths, details.

    Strengths and the absent line are computed rather than authored, for two
    reasons. The standings move as her record does, and a hardcoded "two solo
    shows" goes stale the moment there is a third — which is exactly how the old
    career copy ended up calling a 2023 group show her latest news. And prose
    here drifts into assessment: an early version opened one entry with "further
    along this one than any other", which is a compliment, not information.
    Statements of what exists carry the same finding and pass no verdict.

    The two halves used to sit side by side as a ledger under the heading
    "Current position". They are split now: what is in place reads above the
    fold as strengths, what is missing goes into the "what this path needs"
    disclosure, attached to the list of conditions it actually belongs to. The
    facts are identical; only what she meets first has changed.
    """
    ev = evidence or {}
    solos = ev.get("solo_shows", 0)
    groups = ev.get("confirmed_group_shows", 0)
    pubs = ev.get("publications_confirmed", 0)

    strengths = {
        "no_gatekeepers": [
            _t("Six years of daily work, published without a break.",
               "六年日课，中间没有断过。"),
            _t("An audience of about 26,000 that already exists — a launch here runs to people who are already looking.",
               "一群已经存在的、约 2.6 万人的观众——这里的发布面向的是本来就在看的人。"),
            # NOT "with its own buyers". Roughly three-quarters of the shop's
            # orders are Scott's own, so shop VOLUME cannot be used to claim the
            # audience converts — her prices are real data, her order counts are
            # not (project_scott_is_in_the_data).
            _t("A shop already running, with prices set and the listings live.",
               "一个已经在运转的店铺，价格定好，商品在架。"),
            _t(f"{pubs} publications already made and put out.",
               f"{pubs} 本出版物，已经做出来并发行过。"),
        ],
        "someone_else_sells": [
            _t(f"{groups} group shows and {solos} solo shows on the record.",
               f"履历上有 {groups} 场联展、{solos} 场个展。"),
            _t("Museum group exhibitions, and one showing outside Asia.",
               "美术馆群展，以及一次亚洲以外的展出。"),
            _t("A body of work already made at the scale a show needs.",
               "已经画出来的、达到办一场展所需规模的作品。"),
        ],
        "work_goes_out": [
            _t("Six years of images that repeat and hold up small — the raw material licensing buys.",
               "六年积累的、可重复且缩小后依然成立的图像——正是授权所购买的原料。"),
            _t("A subject that sells into categories character work never reaches.",
               "一个能进入角色类作品到不了的品类的题材。"),
            _t("A look that holds steady across six years — which is what a licensor buys, rather than any single image.",
               "六年里稳定不变的一种面貌——授权方买的是这个，而不是某一张画。"),
        ],
        "between_covers": [
            _t(f"{pubs} publications and eight zines already made and sold.",
               f"{pubs} 本出版物、八本 zine，都已经做出来并卖过。"),
            _t("Six years of daily work — more material than a book needs.",
               "六年的日课——比做一本书所需要的材料还多。"),
            _t("Colour Diary already did the job a publisher is shown.",
               "《Colour Diary》已经承担过「拿给出版社看」的那个作用。"),
            _t("Chinese-language negotiation with printers, which is the single largest lever on the cost.",
               "能用中文和印厂谈——这是成本上最大的一个杠杆。"),
        ],
        "on_assignment": [
            _t("Training in illustration and design, which is the training this field runs on.",
               "插画与设计的科班训练——这个领域运转所依赖的正是这套训练。"),
            _t("A subject Japanese literary publishers commission continuously.",
               "一个日本文学出版社持续在找人画的题材。"),
            _t("Six years of consistent delivery, which is what an art director is buying.",
               "六年不间断的产出——艺术总监买的正是这个。"),
        ],
    }

    absent = {
        "no_gatekeepers": _t(
            "Anything priced between ¥1,980 and ¥31,900, and a count of how many of the 26,000 "
            "are in Japan.",
            "1,980 到 31,900 日元之间的任何一件商品，以及一个数字：两万六千人里有多少在日本。"),
        "someone_else_sells": _t(
            "An exhibition funded by someone else. Every show on the record so far was paid for "
            "from this side.",
            "一场由别人出钱的展览。目前履历上的每一场，费用都出自这一侧。"),
        "work_goes_out": _t(
            "All of it. No licensing on record — the largest untouched category of the five.",
            "全部。履历上没有任何授权记录——这是五条路里最大的一片空白。"),
        "between_covers": _t(
            "A book made to be bought as a book, and quotes from a Chinese printer against a "
            "Japanese one.",
            "一本作为「书」被买走的书，以及一份中国印厂与日本印厂的对比报价。"),
        "on_assignment": _t(
            "Commercial work on record, and a portfolio that shows use rather than paintings.",
            "履历上的商业作品，以及一份展示「用途」而不是「画作」的作品集。"),
    }

    def _details(f: dict) -> list:
        # Ordered as the questions arrive: how does it pay, what does it take,
        # who is doing it. Each is one lid; four lids on a card is chrome.
        return [
            {"id": "money", "kind": "prose",
             "label": _MONEY_LABEL, "body": f["money"]},
            {"id": "needs", "kind": "list",
             "label": _NEEDS_LABEL, "items": f["requires"],
             "footnote_label": _ABSENT_LABEL, "footnote": absent.get(f["id"])},
            {"id": "example", "kind": "prose",
             "label": _LIVING_LABEL, "body": f["example"]},
        ]

    return {
        "futures": [{
            "id": f["id"],
            "name": f["name"],
            "tagline": f["tagline"],
            # A card with a `scenario` renders as a business scenario and
            # ignores everything below it. Without one it falls back to the
            # older shape, so the four cards still waiting to be converted keep
            # working rather than going blank.
            "scenario": f.get("scenario"),
            # The other four realms: a generic block list, so each can take the
            # shape its subject wants instead of a fixed schema.
            "blocks": f.get("blocks"),
            "overview": f["overview"],
            "advantages": f["advantages"],
            "strengths": strengths.get(f["id"], []),
            "details": _details(f),
        } for f in FUTURES],
        "note": _t(
            "Five kinds of success, not five strategies. They are not exclusive, and the record "
            "already sits on more than one of them.",
            "五种「成功」，而不是五种策略。它们并不互斥，而现有的履历已经落在其中不止一条上。"),
    }
