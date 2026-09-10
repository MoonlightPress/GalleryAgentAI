"""
book_economics_engine.py

What a book actually costs, in her numbers.

She has said she wants another book, and she has six years of daily
architectural watercolor plus eight zines already. So the useful thing is not
advice about whether to publish — it is the arithmetic of the thing she is going
to do anyway, which nobody has ever put in front of her.

This is the one item on her whole list with a **fixed, knowable cost**.
Everything else — a grant, a residency, a gallery, a commission — is an
application and a wait. That is why it is worth costing precisely.

Every figure traces to reports/book_economics_2026-09-05.md, which carries the
source URL and a confidence tag per number. Printing quotes are for a ~128pp
full-colour hardcover.

**What this section is for** (Scott, 2026-09-05: "the books section is
incoherent, i don't even know what it's trying to say"). The first version
showed a chart, three route rows, a pricing note and a caveat — four points and
no claim. The questions actually being asked were *"so an art book is a loss
leader?"* and *"this is why you have a publisher, so they eat the upfront
costs"*, and those two have one answer between them:

> **The cost of a book is knowable and small. Whether the copies sell is
> neither. That asymmetry is the entire decision — and absorbing it is exactly
> what a publisher is.**

So the section now leads with that claim, answers the loss-leader question
outright (it is not a loss; it is slow), puts the publisher-versus-self fork
next as the thing the arithmetic is actually about, gives the sell-through
numbers that set the pace, and folds the route-by-route arithmetic into a
disclosure underneath. §6.5 finding 9 of the research report is the warrant:
*"Sell-through is the binding constraint, not unit cost... the cost side of this
model is far better evidenced than the revenue side."*

Three findings shape the model:

1. **Printing in China is 4-6x cheaper**, and she is Chinese, reads the
   language, and has the network. The quoted prices are what an English-speaking
   foreigner is given; a Chinese-speaking negotiator should do better. The
   system had been treating her cross-border position as biography; here it is
   money.

2. **Consignment only works below roughly ¥1,500 a unit.** At the standard 70/30
   split every route except China-at-300-or-more loses money on every copy a
   shop sells. Run size and sales channel are therefore a single decision, not
   two — which is the thing a prose paragraph cannot convey and a chart can.

3. **The break-even is reached early in the run, not late.** 300 copies from
   China is back at ~109 and the remaining ~191 are profit. "Loss leader" is the
   wrong word; "slow" is the right one, and a fair moving 20-25 copies at the
   median is what makes it slow.

Third person throughout, no second person and no imperatives — the same rule
`futures_engine` documents. An earlier route note read "you would be negotiating
in Chinese"; it now states the fact without addressing anyone.
"""

from typing import Optional


def _t(en: str, zh: str) -> dict:
    return {"en": en, "zh": zh}


# ── Printing routes ──────────────────────────────────────────────────────────
# unit = landed cost per copy in JPY (China includes freight; LCL bills a 1 CBM
# minimum, so freight does not scale below 500 and the curve flattens after it).

ROUTES = [
    {
        "id": "china",
        "name": _t("Printed in China", "在中国印"),
        "note": _t("Landed in Tokyo, freight included. These are the prices quoted to an English speaker; the same specification asked for in Chinese is a different price.",
                   "运抵东京、含运费。这些是报给英语使用者的价格；同一份规格用中文去问，是另一个价格。"),
        "runs": {100: 3685, 300: 1315, 500: 890},
    },
    {
        "id": "japan_digital",
        "name": _t("Printed in Japan, digital", "在日本印，数码印刷"),
        "note": _t("Two-week turnaround, no customs — but capped at B5 and about 96 pages.",
                   "两周交货，不用过海关——但尺寸上限是 B5，页数约 96 页。"),
        "runs": {100: 3204},
    },
    {
        "id": "japan_offset",
        "name": _t("Printed in Japan, offset A4", "在日本印，A4 胶印"),
        "note": _t("The full-size hardcover route domestically. Included because it is what most people assume they have to do.",
                   "在日本做全尺寸精装的做法。列在这里，是因为多数人以为只能这样做。"),
        "runs": {100: 24283, 300: 8514, 500: 5386},
    },
]

# Her zines sell at ¥1,980. A hardcover sits higher; the researched band for
# comparable self-published art books in Japan is ¥4,400–5,500 tax-inclusive.
# ¥3,300 is a trap — it reads as the top of the doujin market rather than the
# bottom of the art-book market, and sits under unit cost at small runs.
DEFAULT_PRICE = 4950
CONSIGNMENT_SHARE = 0.70          # 委託 70/30 is the standard anchor
FAIR_BOOTH_JPY = 16500            # cheapest Tokyo Art Book Fair entry, no commission
FAIR_SELL_THROUGH = (20, 25)      # median from 26 real Japanese exhibitor reports


FAIR_MEDIAN_LOW, FAIR_MEDIAN_HIGH = FAIR_SELL_THROUGH
CONSIGNMENT_UNIT_CEILING = 1500   # landed cost above which 70/30 stops clearing

# A publisher pays a royalty on cover price rather than a margin per copy. 8-10%
# is the Japanese convention and nobody has quoted her anything, so the band is
# carried as a band and labelled as convention — never as an offer.
ROYALTY_BAND = (0.08, 0.10)


def _options(price_jpy: int) -> list:
    options = []
    for r in ROUTES:
        for run, unit in sorted(r["runs"].items()):
            outlay = run * unit
            direct = price_jpy - unit
            consign = round(price_jpy * CONSIGNMENT_SHARE) - unit
            be_direct = (outlay / direct) if direct > 0 else None
            be_consign = (outlay / consign) if consign > 0 else None
            options.append({
                "route": r["id"],
                "route_name": r["name"],
                "route_note": r["note"],
                "run": run,
                "unit_jpy": unit,
                "outlay_jpy": outlay,
                "margin_direct_jpy": direct,
                "margin_consignment_jpy": consign,
                "breakeven_direct": round(be_direct) if be_direct else None,
                "breakeven_consignment": round(be_consign) if be_consign else None,
                # Cannot pay for itself at any sell-through: the bar overshoots
                # the run in the chart, which is the whole point of drawing it.
                "impossible": not be_direct or be_direct > run,
                # A shop that takes 30% turns a thin margin negative outright.
                "consignment_viable": bool(be_consign and be_consign <= run),
            })

    return options


def reference_run(price_jpy: int = DEFAULT_PRICE) -> dict:
    """The 300-from-China case — the one every other section quotes.

    Exposed rather than restated, because it was restated once and drifted:
    `futures_engine` carried a hand-typed "recovered at 107 copies" against this
    engine's computed 109. Two sections of the same page disagreeing about the
    same number is precisely the failure the Data Patch Rule exists to prevent,
    so the number now has one home and the other engine imports it.
    """
    for o in _options(price_jpy):
        if o["route"] == "china" and o["run"] == 300:
            return o
    raise LookupError("the china/300 reference case is missing from ROUTES")


def _fen(n: int) -> str:
    return "¥" + f"{n:,}"


def build(price_jpy: int = DEFAULT_PRICE) -> dict:
    """The claim first, the fork second, the pace third, the arithmetic under a lid.

    `impossible` is the finding a table hides and the chart exists for: at some
    combinations the copies needed to break even exceed the copies printed, so
    no sell-through whatsoever recovers the outlay. Printing 100 in Japan at a
    normal cover price is that case — the intuitive choice, and arithmetically
    hopeless. It lives in the disclosure now, because it is evidence for the
    claim rather than the claim itself.
    """
    options = _options(price_jpy)
    ref = reference_run(price_jpy)
    left = ref["run"] - ref["breakeven_direct"]
    roy_lo, roy_hi = (round(price_jpy * r / 10) * 10 for r in ROYALTY_BAND)
    booth_copies = -(-FAIR_BOOTH_JPY // ref["margin_direct_jpy"])          # ceil
    fairs_lo = -(-ref["breakeven_direct"] // FAIR_MEDIAN_HIGH)
    fairs_hi = -(-ref["breakeven_direct"] // FAIR_MEDIAN_LOW)

    # A small run is not rescued by selling harder — it is rescued by pricing
    # higher. The clearest comparable is a Tokyo illustrator with 27k followers
    # (she has ~27k on Instagram alone, ~233k across five platforms — this is a
    # comparable for PRICING, not for reach) who priced a self-published art book
    # at ¥11,000 and sold
    # 400 copies in four months. At that price a 100-copy run pays for itself at
    # 41 copies; at ¥4,950 it cannot pay for itself at all. Worth showing,
    # because "print a small run" is the intuitive move and the arithmetic
    # only works with the price attached.
    high = 11000
    small = next((o for o in options if o["route"] == "japan_digital" and o["run"] == 100), None)
    high_price_case = None
    if small:
        margin = high - small["unit_jpy"]
        high_price_case = {
            "price_jpy": high,
            "run": small["run"],
            "breakeven": round(small["outlay_jpy"] / margin) if margin > 0 else None,
            "note": _t(
                "The same 100-copy run priced at ¥11,000 pays for itself at 41 copies. A small run is not rescued by selling harder; it is rescued by the price on the cover.",
                "同样是印 100 本，如果定价 11,000 日元，卖 41 本就能回本。小批量不是靠多卖救回来的，是靠封底那个价格。"),
        }

    viable = [o for o in options if not o["impossible"]]
    best = min(viable, key=lambda o: o["breakeven_direct"] / o["run"]) if viable else None

    # ── the claim ────────────────────────────────────────────────────────────
    # Two sentences, because the section had none. Everything below is evidence
    # for these.
    claim = _t(
        "What a book costs can be worked out to the yen before anything starts. "
        "How fast the copies sell cannot be worked out at all. That gap — a fixed "
        "price against an open-ended sell-through — is the whole of the decision, "
        "and carrying it is what a publisher is.",
        "做一本书要花多少钱，可以在开始之前精确到日元算出来；能卖多快，则完全算不出来。"
        "一头是固定的价钱，另一头是没有底的销售速度——要决定的全部就是这个落差，"
        "而把这个落差接过去，正是出版社的作用。")

    # The loss-leader question, answered outright rather than left to inference.
    # Opened "It is not a loss" / 「它不是亏本生意」 until 2026-09-07 — the
    # negation pattern the copy rules keep catching, and it plants the word
    # "loss" in the reader's head to argue with it. The money is the same; it
    # now says what the outlay buys and calls the thing by its real name, which
    # is slow.
    not_a_loss = _t(
        f"The money comes back, on a long timescale. {_fen(ref['outlay_jpy'])} buys {ref['run']} "
        f"copies; the run is paid off at {ref['breakeven_direct']} sold and the other {left} are "
        f"profit. Slow is the accurate word for it, and the pace below is what makes it slow.",
        f"钱是能回来的，只是周期长。{_fen(ref['outlay_jpy'])} 换来 {ref['run']} 本；"
        f"卖到第 {ref['breakeven_direct']} 本这批印量就付清了，剩下的 {left} 本是净赚。"
        f"准确的说法是「慢」——下面的数字说明的正是它为什么慢。")

    # ── the fork: who carries the outlay ─────────────────────────────────────
    # Same six rows on both sides so the comparison reads across, not down.
    fork = {
        "label": _t(f"Who carries the {_fen(ref['outlay_jpy'])}",
                    f"这 {_fen(ref['outlay_jpy'])} 由谁来出"),
        "row_labels": [
            _t("Up front", "先要付的钱"),
            _t("Back at", "回本点"),
            _t("Per copy", "每卖一本"),
            _t("Reach", "能到达的地方"),
            _t("Where the copies sit", "书放在哪里"),
            _t("The variable", "不确定的那一项"),
        ],
        "columns": [
            {
                "id": "self",
                "name": _t("Self-published", "自己出版"),
                "values": [
                    _t(f"{_fen(ref['outlay_jpy'])} — {ref['run']} copies, printed in China, landed in Tokyo",
                       f"{_fen(ref['outlay_jpy'])}——{ref['run']} 本，在中国印，运抵东京"),
                    _t(f"{ref['breakeven_direct']} copies of {ref['run']}; the other {left} are profit",
                       f"{ref['run']} 本里的第 {ref['breakeven_direct']} 本；剩下 {left} 本是净赚"),
                    _t(f"{_fen(ref['margin_direct_jpy'])} on a direct sale",
                       f"直接卖出，{_fen(ref['margin_direct_jpy'])}"),
                    _t("Own shop, a few consignment shops, one fair booth at a time",
                       "自己的店铺、几家寄售的书店、一次一个展位"),
                    _t(f"{ref['run']} hardcovers in a room until they move",
                       f"{ref['run']} 本精装书堆在房间里，直到卖完"),
                    _t(f"How long {ref['breakeven_direct']} copies takes",
                       f"卖到第 {ref['breakeven_direct']} 本要多久"),
                ],
            },
            {
                "id": "publisher",
                "name": _t("With a publisher", "有出版社"),
                "values": [
                    _t("Nothing", "不用付"),
                    _t("Nothing to get back", "没有要收回的钱"),
                    _t(f"A royalty. {int(ROYALTY_BAND[0] * 100)}–{int(ROYALTY_BAND[1] * 100)}% of cover is the "
                       f"Japanese convention — around {_fen(roy_lo)}–{_fen(roy_hi)} here, against "
                       f"{_fen(ref['margin_direct_jpy'])} direct. Convention, not an offer: nobody has quoted a rate.",
                       f"版税。日本的惯例是定价的 {int(ROYALTY_BAND[0] * 100)}–{int(ROYALTY_BAND[1] * 100)}%，"
                       f"在这里大约 {_fen(roy_lo)}–{_fen(roy_hi)}，对比自己直接卖的 {_fen(ref['margin_direct_jpy'])}。"
                       f"这是行业惯例，不是谁开出的条件——目前没有任何出版社报过价。"),
                    _t("Bookshops nationally", "全国的书店"),
                    _t("The publisher's warehouse", "出版社的仓库"),
                    _t("Their consent", "对方同不同意"),
                ],
            },
        ],
        "note": _t(
            "Mateusz Urbanowicz's Tokyo books — Tokyo Storefronts, Tokyo at Night — are published by "
            "MdN rather than self-published, and the series has passed 100,000 copies in Japan. "
            "Self-publishing has no route to that number; equally, no self-published run waits for "
            "anyone's permission. That is the whole of the trade.",
            "Mateusz Urbanowicz 画东京的那两本书——《东京店构え》《东京夜行》——由 MdN 出版，不是自出版，"
            "这个系列在日本卖过十万册。自出版没有任何途径能到那个数字；反过来，自出版也不需要等谁点头。"
            "这就是这笔交易的全部内容。"),
    }

    # ── the pace: what actually sets the timeline ────────────────────────────
    pace = {
        "label": _t("How fast copies actually move", "书实际上卖得有多快"),
        "facts": [
            _t(f"The median at a Japanese art book fair is {FAIR_MEDIAN_LOW}–{FAIR_MEDIAN_HIGH} copies. "
               f"On fairs alone, {ref['breakeven_direct']} copies is {fairs_lo}–{fairs_hi} of them.",
               f"日本艺术书展的中位数是 {FAIR_MEDIAN_LOW}–{FAIR_MEDIAN_HIGH} 本。只靠书展的话，"
               f"{ref['breakeven_direct']} 本要摆 {fairs_lo}–{fairs_hi} 次摊。"),
            _t(f"The cheapest Tokyo Art Book Fair booth is {_fen(FAIR_BOOTH_JPY)}, with no commission on "
               f"sales. At these costs it pays for itself in {booth_copies} copies — inside the first hour.",
               f"东京艺术书展最便宜的展位是 {_fen(FAIR_BOOTH_JPY)}，销售不抽成。按这里的成本，"
               f"卖 {booth_copies} 本就回本了——第一个小时之内。"),
            _t(f"Consignment at the standard 70/30 only clears when the landed cost is under roughly "
               f"{_fen(CONSIGNMENT_UNIT_CEILING)} a copy, which among these routes means China at {ref['run']} or more. Run size and "
               f"sales channel are therefore one decision, not two.",
               f"按 70/30 的标准寄售分成，落地成本要低于大约 {_fen(CONSIGNMENT_UNIT_CEILING)} 才有得赚，"
               f"在这几条路里就是中国印 {ref['run']} 本以上。所以印多少和在哪里卖是同一个决定，不是两个。"),
        ],
    }

    return {
        "price_jpy": price_jpy,
        "options": options,
        "best_id": f'{best["route"]}_{best["run"]}' if best else None,
        "high_price_case": high_price_case,
        "fair_booth_jpy": FAIR_BOOTH_JPY,
        "fair_sell_through": list(FAIR_SELL_THROUGH),
        "reference": ref,
        "claim": claim,
        "not_a_loss": not_a_loss,
        "fork": fork,
        "pace": pace,
        # The route-by-route arithmetic is now evidence behind a lid rather than
        # the opening move. It answers "which route", which is the second
        # question; the section leads with the first.
        "detail_label": _t("The arithmetic, route by route", "每一条路的算法"),
        "note": _t(
            "A print run is the only item on this list with a price that can be known in advance. Everything else is an application and a wait.",
            "在这份清单上，印一本书是唯一一件事先就能知道价钱的事。其余每一样，都是先申请，然后等。"),
        "caveat": _t(
            "Break-even is knowable; how many copies sell is not. Every figure here is sourced; the sell-through numbers are medians from other people's fairs, not a forecast.",
            "回本的数字可以算出来，能卖多少本却算不出来。这里每一个数字都有出处；而销售数字是别人书展的中位数，不是预测。"),
    }
