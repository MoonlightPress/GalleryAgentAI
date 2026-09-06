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

**Shape.** Each route is a flat list of blocks — `prose`, `note`, `list`,
`table`, `links` — under a name and a tagline. `RealmBlocks` in
`SaffronPage.jsx` knows how to draw each kind and nothing else; the sequence,
the headings and the wording all live here, so a block can be added, reordered
or dropped without touching React.

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

from .book_economics_engine import DEFAULT_PRICE as _BOOK_PRICE, reference_run


def _t(en: str, zh: str) -> dict:
    # ja is deliberately absent for now rather than machine-guessed; the UI
    # falls back to en. Japanese was cut from the site (Scott, 2026-09-04).
    return {"en": en, "zh": zh}


# The print-run arithmetic has one home, in book_economics_engine. It was typed
# out by hand here once and drifted (107 against that engine's computed 109),
# which is exactly the two-sections-of-one-page-disagreeing failure the Data
# Patch Rule is about.
_BOOK = reference_run()


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
# Two claims that appeared in earlier drafts are NOT carried forward, because
# they were never supported: that Colour Diary has functioned as a pitch to a
# publisher (no record of it, and the publishing research found no evidence
# either way that a finished book triggers acquisition), and the letter's
# reference to a show she did not attend, fixed in outreach_kit_engine.

_FRAME = _t(
    "You already have a working practice: six years of paintings, an audience, direct sales, "
    "commissions and a record of exhibitions. The useful question now is where another route "
    "gives you something the current one cannot.\n\n"
    "An original already earns ¥31,900–115,500. That is the benchmark. Anything added to the "
    "practice should earn from work you have already made, reach buyers you cannot reach "
    "yourself, increase what the rest of the work is worth, or create revenue without requiring "
    "another original. The five routes below do different versions of that.",
    "你已经有一套在运转的实践：六年的画、一群观众、直接销售、委托，以及一份展览记录。"
    "现在有用的问题是：另一条路能给你什么，是现在这条给不了的。\n\n"
    "一张原作现在就能卖 31,900–115,500 日元。这是基准。"
    "任何要加进来的东西，都应该做到其中一件：让已经画完的作品再挣一次钱、"
    "触达你自己够不到的买家、抬高其余作品的价值，或者在不用再画一张原作的前提下带来收入。"
    "下面五条路，是这件事的五个不同版本。")


_SELLING_DIRECT = [
    {"kind": "prose", "label": _t("Fill the gap between ¥2,200 and ¥31,900",
                                  "把 2,200 到 31,900 日元之间的空档填上"),
     "text": _t(
        "You already sell successfully at both ends: postcards, zines and prints at ¥1,100–2,200, "
        "then originals beginning at ¥31,900. The missing part is the middle. Someone who has "
        "bought a zine and a print has no way to spend ¥5,000, ¥10,000 or ¥20,000 with you — the "
        "next purchase available is an original. The easiest test is to add that middle without "
        "buying inventory first.",
        "两头你都卖得很好：明信片、zine、画作印刷在 1,100–2,200 日元，原作从 31,900 日元起。"
        "缺的是中间。一个买过 zine 和印刷的人，在你这里没有办法花掉 5,000、10,000 或者 20,000 日元——"
        "他能买的下一样东西就是原作。最容易的试法，是先把中间那段补上，而不先囤货。")},
    {"kind": "table", "label": _t("Start with three products", "先从三样东西开始"),
     "headers": [_t("", ""), _t("Sells for", "售价"), _t("You keep", "你留下"), _t("Margin", "毛利率")],
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
        "orders it, so the test requires no print run and no storage. The margin is lower than "
        "printing yourself, and that is useful at this stage: the printer carries the inventory "
        "risk while you find out whether the product has a market.",
        "先用按需印刷上架。每一件都是有人下单之后才做，所以这次尝试不需要印量，也不需要地方放。"
        "毛利率比自己印低，而这在现阶段是有用的：由印厂承担库存风险，你只负责弄清楚这样东西有没有市场。")},
    {"kind": "prose", "text": _t(
        "For products that already sell reliably, your existing model is better. A ten-pack of "
        "postcards costs about ¥170 printed in a run of one hundred, against ¥1,835 on demand. "
        "Keep those in-house. If one of the new formats begins selling consistently, batch "
        "production becomes the second step.",
        "已经卖得稳的东西，你现在的做法更好。一套十张的明信片，印一百套时成本约 170 日元，"
        "按需印刷则要 1,835 日元。这些继续自己印。等新形态里有哪一样开始稳定卖动，再转成批量生产。")},
    # Every figure in this paragraph and in the "Hardcover, China" row below is
    # read from book_economics_engine rather than typed. It was typed once and
    # drifted — 107 here against that engine's computed 109 — and the same page
    # then said two different things about the same run.
    {"kind": "prose", "label": _t("The book is a different decision", "书是另一个层面的决定"),
     "text": _t(
        f"A 128-page hardcover printed in China costs ¥{_BOOK['outlay_jpy']:,} for "
        f"{_BOOK['run']} copies. At ¥{_BOOK_PRICE:,} each, the production cost is recovered "
        f"after {_BOOK['breakeven_direct']} sales, leaving "
        f"{_BOOK['run'] - _BOOK['breakeven_direct']} copies. The question is therefore demand "
        "and speed.",
        f"128 页的精装本在中国印 {_BOOK['run']} 本，需要 {_BOOK['outlay_jpy']:,} 日元。"
        f"定价 {_BOOK_PRICE:,} 日元，卖出 {_BOOK['breakeven_direct']} 本收回制作成本，"
        f"还剩 {_BOOK['run'] - _BOOK['breakeven_direct']} 本。所以要判断的是需求和速度。")},
    {"kind": "table",
     "headers": [_t("", ""), _t("Each", "每本"), _t("Up front", "先要付"),
                 _t("Sells for", "售价"), _t("Cost recovered at", "回本点")],
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
        "the formats checked. For a book intended to open another door, make three copies "
        "instead: three Blurb copies cost about ¥31,000 and can go directly to a gallery or a "
        "shop buyer. Publishers are a separate case — the three that accept submissions ask for a "
        "proposal rather than a finished book.",
        "如果这本书是要当商品卖，在查过的几种形态里，中国印的精装本经济上最划算。"
        "如果这本书是用来敲另一扇门的，那就只做三本：Blurb 三本约 31,000 日元，"
        "可以直接拿给画廊或书店买手。出版社是另一回事——接受投稿的那三家要的是企划书，不是成品书。")},
    {"kind": "links", "label": _t("Where", "去哪里做"),
     "items": [
        {"name": _t("pixivFACTORY / BOOTH — the first test for posters, canvas and framed prints",
                    "pixivFACTORY / BOOTH——海报、画布、装裱印刷的第一次试水"),
         "url": "https://factory.pixiv.net/"},
        {"name": _t("SUZURI — smaller paper goods and low-risk experiments",
                    "SUZURI——小件纸制品，低风险的尝试"),
         "url": "https://suzuri.jp/"},
        {"name": _t("INPRNT — the useful addition for buyers outside Japan",
                    "INPRNT——面向日本以外买家时，值得加上的一个"),
         "url": "https://www.inprnt.com/"},
     ]},
]


_GALLERIES = [
    {"kind": "prose", "label": _t("Find a gallery that carries the exhibition risk",
                                  "找一家愿意承担办展风险的画廊"),
     "text": _t(
        "You already know how to organise a solo show. You have done it three times. The next "
        "useful gallery relationship is one that contributes what you currently supply yourself: "
        "the room, the staffing, the collectors, the sales work and the financial risk.",
        "你已经知道怎么办一场个展，办过三次了。下一段值得建立的画廊关系，"
        "是能把你现在自己扛的那些东西接过去的：场地、看场的人、藏家、销售的活，以及资金上的风险。")},
    {"kind": "table", "label": _t("The economics are unusually clear", "这笔账算得异常清楚"),
     "headers": [_t("", ""), _t("You pay", "你付"), _t("They take", "他们抽"),
                 _t("Sales before you are even", "打平前要卖掉")],
     "rows": [
        {"cells": [_t("Representing gallery", "代理画廊"), _t("¥0", "0"), _t("about 50%", "约 50%"),
                   _t("¥0", "0")]},
        {"cells": [_t("Moon Gallery rental", "Moon Gallery 租赁"), _t("¥100,000 / 5 days", "10 万 / 5 天"),
                   _t("0%", "0%"), _t("about one painting", "约一张画")]},
        {"cells": [_t("Galerie LE MONDE rental", "Galerie LE MONDE 租赁"),
                   _t("¥374,000 / 12 days", "37.4 万 / 12 天"), _t("30%", "30%"),
                   _t("about six paintings", "约六张画")]},
     ]},
    {"kind": "prose", "text": _t(
        "A 50% commission can look large in isolation. Against a ¥374,000 room fee plus 30%, "
        "representation is cheaper until the rental exhibition reaches about ¥1.87 million in "
        "sales. The more important difference is who brings the buyers. So far, people buying "
        "your work have largely found you. Representation adds a collector base belonging to "
        "somebody else.",
        "单看 50% 的抽成，会觉得很高。但对比 37.4 万日元的场租再加 30%，"
        "代理一直更划算，直到租场那次展览卖到约 187 万日元为止。"
        "更重要的分别在于谁把买家带来。到目前为止，买你作品的人基本上是自己找到你的。"
        "代理带来的，是一份属于别人的藏家名单。")},
    {"kind": "prose", "label": _t("The next move", "下一步"),
     "text": _t(
        "Choose a small number of galleries where the work genuinely fits the programme. Visit "
        "first. Then send five paintings from one coherent series and ask whether they would be "
        "interested in seeing the work in person. A relationship with ten plausible rooms does "
        "more than mail sent to a hundred implausible ones.",
        "挑几家作品确实贴合其展览方向的画廊，数量不用多。先去看展。"
        "然后寄五张同一个系列的画，问他们有没有兴趣看看实物。"
        "和十个说得通的空间建立关系，比给一百个说不通的空间发信有用。")},
    {"kind": "links", "label": _t("The immediate targets found in Tokyo",
                                  "在东京找到的几个可以马上去的对象"),
     "items": [
        {"name": _t("biscuit gallery — the clearest immediate route, because it publishes an open call. Free to enter, students eligible.",
                    "biscuit gallery——最明确的一条现成的路，因为它公开办征集。免费报名，接受学生。"),
         "url": "https://biscuitgallery.com/"},
        {"name": _t("GALLERY KOGURE — a close roster fit, including detailed urban work on paper",
                    "GALLERY KOGURE——代理名单贴合度很高，包括纸上的细密城市题材"),
         "url": "https://gallerykogure.com/"},
        {"name": _t("Tokyo Gallery + BTAP — a stronger China/Japan connection, six Chinese artists on the roster and several working in ink on paper",
                    "Tokyo Gallery + BTAP——中日之间的联系更强，代理名单上有六位中国艺术家，其中几位做纸上水墨"),
         "url": "https://www.tokyo-gallery.com/"},
     ]},
]


_LICENSING = [
    {"kind": "prose", "label": _t("Let the archive earn again", "让已经画完的东西再挣一次钱"),
     "text": _t(
        "Licensing has one unusual advantage for you: the inventory already exists. Six years of "
        "daily painting is thousands of images that can produce income while the originals remain "
        "yours. The value depends primarily on where and how an image is used.",
        "对你来说，授权有一个别处没有的优势：库存已经在了。"
        "六年的日课是好几千张图，它们可以在原作仍然属于你的情况下带来收入。"
        "价值主要取决于一张图被用在哪里、怎么用。")},
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
        "exclusivity and reuse. Copyright transfer is priced at roughly two to three times a "
        "normal licence in the published Japanese rate card. Keep that distinction explicit "
        "whenever a buyer asks for permanent rights.",
        "所以授权条款和费用同样重要：形式、地域、期限、独家与否、能不能再次使用。"
        "在日本公开的费率表上，著作权转让的定价大约是普通授权的两到三倍。"
        "只要对方要的是永久权利，就把这一条明确摆出来。")},
    {"kind": "prose", "label": _t("Make a small cover-ready series", "画一小组能直接当封面用的"),
     "text": _t(
        "Your subject matter already fits the book market: architecture, atmosphere, interiors, "
        "weather, light and quiet urban scenes. The compositional requirement is the part worth "
        "designing for. Covers need room for typography and cropping, so paint a small group "
        "vertically with intentional quiet areas — sky, fog, water, wall, shadow, an open upper "
        "third. That gives art directors images they can build a cover around while keeping the "
        "work recognisably yours. Five to ten paintings would be enough to begin.",
        "你的题材本来就贴合图书市场：建筑、氛围、室内、天气、光，以及安静的城市场景。"
        "值得专门去设计的，是构图上的要求。封面需要放字的地方，也需要能被裁切，"
        "所以画一小组竖构图，留出有意为之的安静区域——天空、雾、水面、墙、阴影，或者上三分之一整片留白。"
        "这样艺术总监就能围绕它做出一张封面，而作品看上去仍然一眼就是你的。五到十张就够开个头。")},
    {"kind": "links", "label": _t("Then place them where art directors already look",
                                  "然后把它们放到艺术总监本来就会去看的地方"),
     "items": [
        {"name": _t("イラストレーションファイルWeb — Japanese art directors and book designers",
                    "イラストレーションファイルWeb——日本的艺术总监与装帧设计师"),
         "url": "https://www.illustration-file.com/"},
        {"name": _t("amanaimages — Japanese stock licensing; published cover licences are ¥33,000–79,200",
                    "amanaimages——日本的图像授权；公开的封面授权价为 33,000–79,200 日元"),
         "url": "https://amanaimages.com/"},
        {"name": _t("Arcangel — specialised in book-cover imagery, accepts illustration, pays contributors 50% of net",
                    "Arcangel——专做书封图像，收插画，付给供稿人净额的 50%"),
         "url": "https://arcangel.com/become-a-contributor/"},
        {"name": _t("Bridgeman Studio — represents roughly a thousand artists and is currently accepting illustration submissions",
                    "Bridgeman Studio——代理约一千位艺术家，目前正在接受插画投稿"),
         "url": "https://www.bridgemanimages.com/en/studio"},
     ]},
]


_PUBLISHING = [
    {"kind": "prose", "label": _t("Pitch a book that still needs to be made",
                                  "提一本还没做出来的书"),
     "text": _t(
        "The strongest publishing opportunity is a book concept with enough identity that a "
        "publisher can imagine selling it. Your existing paintings establish that you can execute "
        "it; the proposal establishes what the book is. That distinction matters because the "
        "publishers checked ask for projects and proposals. In the comparable Tokyo architecture "
        "title, forty of the fifty paintings were made after the deal was agreed.",
        "出版这条路上最有力的机会，是一个面貌足够清楚、让出版社能想象出怎么卖的书的构想。"
        "你已有的画证明你做得出来；企划书说明的是这本书到底是什么。"
        "这个分别之所以重要，是因为查过的这几家出版社要的是企划和构想。"
        "在那本可比的东京建筑画集里，五十张画中有四十张是在合同谈定之后才画的。")},
    {"kind": "list", "label": _t("A strong proposal needs", "一份有力的企划书要有"),
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
        "Your six-year archive gives you unusually strong material for that proposal, even if the "
        "final book contains new work.",
        "即使最后成书用的是新画的作品，你这六年的积累也让这份企划书有异常扎实的底子。")},
    {"kind": "table", "label": _t("The economics", "这笔账"),
     "headers": [_t("", ""), _t("You keep per copy", "每本你留下"), _t("300 copies", "300 本")],
     "rows": [
        {"cells": [_t("Publisher", "出版社出版"), _t("¥115–240", "115–240 日元"),
                   _t("¥34,500–72,000", "34,500–72,000 日元")]},
        {"cells": [_t("Self-published hardcover", "自己出版的精装本"), _t("¥3,635", "3,635 日元"),
                   _t("¥1,090,500", "1,090,500 日元")]},
     ]},
    {"kind": "prose", "text": _t(
        "Publishing is weak as a per-copy revenue stream and strong as distribution. The "
        "publisher's contribution is everything surrounding those royalties: financing the print "
        "run, national bookshop distribution, an ISBN, production, inventory, and a publication "
        "record that stays attached to your name. Those benefits make the most sense when the "
        "book is expected to strengthen the rest of the practice as well as sell copies.",
        "论每本能拿多少，出版是弱的；论发行，它是强的。"
        "出版社真正提供的是围绕那点版税的一切：出印刷的钱、进入全国书店、一个 ISBN、"
        "制作、库存，以及一条会一直挂在你名字上的出版记录。"
        "当这本书除了卖出去，还被期待去带动其余的实践时，这些好处才最说得通。")},
    {"kind": "links", "label": _t("Three publishers with a published route in",
                                  "三家把入口写出来的出版社"),
     "items": [
        {"name": _t("マール社 — accepts proposals directly and finances accepted books itself",
                    "マール社——直接接受企划，通过后由他们出钱做书"),
         "url": "https://www.maar.com/"},
        {"name": _t("青幻舎 — a dedicated proposal route asking for a plan, portfolio and images",
                    "青幻舎——专门的企划投递通道，要企划书、作品集和图像"),
         "url": "https://www.seigensha.com/"},
        {"name": _t("MdN — accepts portfolios and proposals, and has already published successful Tokyo architecture books",
                    "MdN——接受作品集与企划，并且已经出过卖得很好的东京建筑画集"),
         "url": "https://books.mdn.co.jp/"},
     ]},
    {"kind": "note", "text": _t(
        "The next useful piece of work here is one book proposal, built well enough to send to "
        "all three with small changes.",
        "这条路上接下来真正有用的一件事，是把一份书的企划书做扎实，"
        "扎实到只要小改一下就能同时递给这三家。")},
]


_COMMISSIONS = [
    {"kind": "prose", "label": _t("Price the painting and the usage separately",
                                  "画和用途，分开定价"),
     "text": _t(
        "A commission asks you to give up something your originals preserve: complete control "
        "over the subject, the schedule and the finished image. So the fee has to compensate for "
        "that, or the commission has to create value somewhere else.",
        "接委托意味着交出一些你画自己作品时保有的东西：对题材、进度和最终画面的完全掌控。"
        "所以要么费用能补偿这一点，要么这次委托得在别的地方产生价值。")},
    {"kind": "table", "label": _t("The national rate card gives a useful floor",
                                  "全国费率表给了一个有用的底线"),
     "headers": [_t("Use", "用途"), _t("Published rate", "公开费率")],
     "rows": [
        {"cells": [_t("Book cover", "书籍封面"), _t("¥70,000", "70,000 日元")]},
        {"cells": [_t("Magazine cover", "杂志封面"), _t("¥100,000", "100,000 日元")]},
        {"cells": [_t("Small internal illustration", "内页小图"), _t("¥5,000", "5,000 日元")]},
        {"cells": [_t("Average coordinated job", "经手工作的平均值"), _t("¥71,327", "71,327 日元")]},
     ]},
    {"kind": "prose", "text": _t(
        "Hand-painted watercolour sits in the second-highest of the five medium categories in "
        "that rate card. A ¥70,000 cover is therefore close to the price of one of your existing "
        "originals. The commercial job becomes more attractive when the licence expands, the "
        "image is reused, or the publication brings the work to the next client. Secondary use "
        "can pay 70%, 50%, 50% and 20% of the original fee as the same image is reused. That is "
        "the part worth protecting.",
        "在那份费率表的五个媒介档次里，手绘水彩排在第二高。"
        "所以 70,000 日元一张封面，差不多就是你一张现有原作的价格。"
        "当授权范围扩大、图像被再次使用，或者这次发表把作品带到下一个客户面前时，"
        "商业委托才变得更有吸引力。同一张图被反复使用时，二次使用可以按原稿费的 "
        "70%、50%、50%、20% 再付。值得护住的正是这一部分。")},
    {"kind": "list", "label": _t("Build the terms before the enquiry arrives",
                                 "在询问找上门之前，先把条款准备好"),
     "items": [
        _t("Painting fee — the work required to make the image.",
           "绘制费——做出这张图所需要的工作。"),
        _t("Licence — where it may appear, for how long, in which countries, for which use.",
           "授权——可以出现在哪里、用多久、在哪些国家、作什么用途。"),
        _t("Additional use — a new fee when the same image is reused elsewhere.",
           "追加使用——同一张图被用到别处时，另计一笔费用。"),
        _t("Copyright transfer — a separate, substantially higher price when the client wants permanent ownership of the rights.",
           "著作权转让——当客户想永久拥有这些权利时，单独计价，而且高出许多。"),
     ]},
    {"kind": "prose", "text": _t(
        "That turns an ambiguous “how much for a painting?” into something you can price "
        "consistently.",
        "这样一来，「画一张多少钱」这种含糊的问题，就变成了你可以稳定报价的东西。")},
    {"kind": "table", "label": _t("Platform terms matter as well", "平台条款同样要紧"),
     "headers": [_t("Platform", "平台"), _t("Copyright", "版权")],
     "rows": [
        {"cells": [_t("Skeb", "Skeb"), _t("Transfer prohibited; the artist retains it",
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
        {"name": _t("ザ・チョイス — ¥1,500 entry; age, nationality and professional status explicitly unrestricted. Accepts unframed originals.",
                    "ザ・チョイス——报名费 1,500 日元；年龄、国籍、是否职业都明确不设限。收不装裱的原作。"),
         "url": "https://www.genkosha.co.jp/illustration/choice.html"},
        {"name": _t("HB FILE — ¥7,000 entry; every entrant's file stays available to designers and publishers in the gallery for a year.",
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
        "Each of these can be tested with one small piece of work, alongside everything already "
        "running.",
        "每一条都可以用一件很小的事去试，和现在在做的一切并行。"),
    "steps": [
        {"route": _t("Direct", "直接销售"),
         "step": _t("List an A2 poster, an A1 poster and a framed A4 print on demand.",
                    "用按需印刷上架一张 A2 海报、一张 A1 海报和一张装裱的 A4 印刷。")},
        {"route": _t("Gallery", "画廊"),
         "step": _t("Choose one gallery exhibition to attend, and prepare a five-image series link.",
                    "选一场画廊的展去看，并准备好一个五张同系列作品的链接。")},
        {"route": _t("Licensing", "授权"),
         "step": _t("Make the first five vertical, cover-ready paintings.",
                    "画出头五张竖构图、可以直接当封面用的画。")},
        {"route": _t("Publishing", "出版"),
         "step": _t("Turn one existing body of work into a one-page book concept.",
                    "把已有的一组作品，写成一页纸的书的构想。")},
        {"route": _t("Commissions", "委托"),
         "step": _t("Write a reusable fee-and-licence template before the next enquiry arrives.",
                    "在下一个询问到来之前，写好一份可以反复用的「费用＋授权」模板。")},
    ],
    "close": _t(
        "That gives you five experiments. Their results will tell you much more than choosing one "
        "of the five in advance.",
        "这样你就有了五个实验。它们的结果能告诉你的，远比事先在五条路里挑一条要多。"),
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
        "blocks": _SELLING_DIRECT,
        "tagline": _t("Your own shop, your own prices, everything above cost.",
                      "自己的店，自己定价，成本之上全归你。"),
    },
    {
        "id": "someone_else_sells",
        "blocks": _GALLERIES,
        "name": _t("Galleries", "画廊"),
        "tagline": _t("A gallery sells your originals and finds the buyers.",
                      "画廊卖你的原作，并且负责找买家。"),
    },
    {
        "id": "work_goes_out",
        "blocks": _LICENSING,
        "name": _t("Licensing", "图像授权"),
        "tagline": _t("Someone pays to use a painting you have already made.",
                      "有人付钱，使用你已经画好的一张画。"),
    },
    {
        "id": "between_covers",
        "blocks": _PUBLISHING,
        "name": _t("Publishing", "出版"),
        "tagline": _t("A publisher makes a book of your work, and pays for it.",
                      "由出版社把你的作品做成一本书，钱也由他们出。"),
    },
    {
        "id": "on_assignment",
        "blocks": _COMMISSIONS,
        "name": _t("Commissions", "委托"),
        "tagline": _t("Someone pays you to paint something new, to a brief.",
                      "有人付钱请你按要求画一张新的。"),
    },
]


def build() -> dict:
    """The five routes, the frame they answer to, and the five experiments.

    No arguments. An earlier version took her computed career evidence and used
    it to print a per-route ledger of what she has and has not done. Both halves
    are gone: the "has" half read her own record back to a person who lived it,
    and the "has not" half was a list of what she lacks, which is the thing this
    file exists to stop. Her record still decides what the routes SAY — it is
    why Selling Direct opens on a price gap rather than an explanation of
    selling — but it is applied by whoever writes a block, not printed as a
    scoreboard.
    """
    return {
        "futures": [{
            "id": f["id"],
            "name": f["name"],
            "tagline": f["tagline"],
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
