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
    {"kind": "prose", "label": _t("The book is a different decision", "书是另一个层面的决定"),
     "text": _t(
        "A 128-page hardcover printed in China costs ¥394,500 for 300 copies. At ¥4,950 each, the "
        "production cost is recovered after 109 sales, leaving 191 copies. The question is "
        "therefore demand and speed, rather than margin.",
        "128 页的精装本在中国印 300 本，需要 394,500 日元。定价 4,950 日元，卖出 109 本收回制作成本，"
        "还剩 191 本。所以要判断的是需求和速度，而不是利润率。")},
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
        {"cells": [_t("Hardcover, 128pp, China", "精装，128 页，中国印"), _t("¥1,315", "1,315 日元"),
                   _t("¥394,500 / 300", "394,500 / 300 本"), _t("¥4,950", "4,950 日元"), _t("109", "109")]},
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
        "These routes do not require a career change. Each can be tested with one small piece of "
        "work.",
        "这几条路都不需要你改变职业方向。每一条都可以用一件很小的事去试。"),
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
        # The business-scenario body. Only this card carries one so far; the
        # component falls back to the old shape for the other four, so they
        # keep working while they are converted one at a time.
        "blocks": _SELLING_DIRECT,
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
        "tagline": _t("Your own shop, your own prices, everything above cost.",
                      "自己的店，自己定价，成本之上全归你。"),
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
        # The frame the whole tab answers to, and the five experiments it ends
        # on. Without these the five routes are five essays with nothing joining
        # them - which is what six earlier drafts were.
        "frame": _FRAME,
        "first_steps": _FIRST_STEPS,
    }
