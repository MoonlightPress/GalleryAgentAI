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


FUTURES = [
    {
        "id": "no_gatekeepers",
        # Names are dead plain by decision (Scott, 2026-09-06: "these titles are
        # terrible, what the hell does no gatekeepers even mean"). A title that
        # has to be decoded is a title that failed, and it fails twice as hard
        # translated. The texture moved down into the taglines, which is where a
        # reader has already agreed to spend a second.
        "name": _t("Selling Direct", "直接卖"),
        "tagline": _t("The audience is the asset. Nothing stands between the work and the people who buy it.",
                      "观众本身就是资产。作品与买家之间没有任何中间人。"),
        "overview": _t(
            "The work is made and distributed directly. No gallery commission, no publisher "
            "deciding the next book, no client revisions.",
            "作品由本人制作，直接送到买家手里。没有画廊抽成，没有出版社决定下一本书，没有客户提修改意见。"),
        "advantages": [
            _t("The only one of the five where nobody is positioned to say no. The exposure here is not rejection, it is continuity — income tracks how regularly the work appears.",
               "五条路里唯一一条没有人站在能拒绝的位置上的。这条路的风险不是被拒绝，而是持续性——收入与作品出现的规律程度直接相关。"),
            _t("Nothing built here can be withdrawn by another party's decision. A gallery roster, a publisher's list and a client relationship can each end from the other side; an audience cannot be taken back.",
               "这里建起来的东西，不会因为另一方的一个决定而消失。画廊的代理名单、出版社的书目、客户关系，都可能由对方那一头结束；观众不会被收回去。"),
            _t("The fastest answer of the five. Sales data arrives within weeks of a launch, where an application takes most of a year to come back.",
               "五条路里回音最快的一条。发布后几周内就有销售数据，而一份申请要等上大半年才有回音。"),
            _t("The only one with a layer that stops scaling with hours. A recorded course is made once and sold indefinitely; everywhere else on this list, payment follows each thing made.",
               "唯一一条有「不随时间线性增长」那一层的路。录制课程做一次，可以长期卖下去；这份清单上的其他每一条，都是做一件、收一次钱。"),
        ],
        "money": _t(
            "Three layers, ascending in both what they pay and what they cost to set up. Prints "
            "and postcards: low margin, steady volume. Editions and originals: high margin, low "
            "volume. A recorded course: made once, sold indefinitely. The first two scale with "
            "hours worked. The third is the layer that converts an audience into an income, "
            "because it stops scaling with hours.",
            "三层，收入与前期投入同时递增。版画与明信片：利润低，但走量稳定。限量与原作：利润高，但数量少。"
            "录制课程：做一次，可以长期卖下去。前两层的收入与投入的时间成正比；"
            "第三层之所以是把观众转化为收入的那一层，正是因为它不再与时间成正比。"),
        "requires": [
            _t("A subject narrow enough to teach. For architectural painting that is usually perspective and the handling of light, rather than painting in general.",
               "一个窄到可以教的主题。就建筑绘画而言，通常是透视与光的处理，而不是「怎么画画」。"),
            _t("Three to five hours of recorded video. A course at this scale is a recording, not a curriculum.",
               "三到五小时的录制视频。这个规模的课程是一段录像，不是一套教学大纲。"),
            _t("An audience that already exists. The launch runs to the people following the work; no new audience is involved.",
               "一群已经存在的观众。发布面向的是已经在看作品的人，不涉及新观众。"),
            _t("About a month to a verdict. Sales data arrives within weeks of launch rather than after a year.",
               "大约一个月就能看到结论。销售数据在发布后几周内出现，而不是一年之后。"),
        ],
        "example": _t("Ohn Mar Win: over 80,000 students on Skillshare. By her own published figures, teaching is 77% of her income and licensing 3%. That position took eleven years.",
                      "Ohn Mar Win：Skillshare 上有八万多名学生。按她本人公开的数字，教学占其收入的 77%，授权占 3%。这个状态用了十一年。"),
    },
    {
        "id": "someone_else_sells",
        "name": _t("Gallery Representation", "画廊代理"),
        "tagline": _t("A gallery does the selling, the pricing, and the finding of buyers.",
                      "由画廊来销售、定价，并且负责找买家。"),
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
        "name": _t("Licensing the Images", "图像授权"),
        "tagline": _t("Images on things, manufactured and sold by other companies.",
                      "图像出现在各种东西上，由别的公司生产和销售。"),
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
        "name": _t("Making Books", "做书"),
        "tagline": _t("The book is the work, not a record of it.",
                      "书本身就是作品，而不是作品的记录。"),
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
        "name": _t("Commissioned Work", "接委托"),
        # The "only predictable monthly number" claim moved into advantages,
        # where it belongs as a comparison; a tagline repeating it read twice.
        "tagline": _t("Client work. Somebody asks for the picture, and pays for it.",
                      "客户工作。有人来要这张画，并且付钱。"),
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
            _t("A shop already operating, with its own buyers.",
               "一个已经在运转的店铺，有自己的买家。"),
            _t(f"{pubs} publications already sold straight to that audience.",
               f"{pubs} 本出版物，已经直接卖给了这群观众。"),
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
            "The layer that does not scale with hours: no course, no recorded product.",
            "不随时间线性增长的那一层：没有课程，没有可复制销售的产品。"),
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
