"""
futures_engine.py

Five futures, replacing the three "long-term scenarios".

The old section offered a choice between Gallery, Publication, and Both — which
is not a choice: "both" is the obvious answer, and she has in fact been doing
both concurrently for years (Shanghai solo and two Chinese museum group shows in
2024-25, London, two Tokyo solos in 2026). A fork she is already on both sides
of is decoration.

These are not strategies, they are *kinds of success*, named for the thing that
actually defines each life. They have real tension — chasing licensing deals is
different daily work from chasing gallery shows — so choosing between them means
something, while "gallery or publishing" did not.

Three rules, each learned the hard way:

1. **No prescribed destination.** She is self-taught, independent, and runs
   everything herself; a system that tells such a person what to want reads as
   presumptuous however good the research is. Show the range, let her pick.
2. **Types of things to pursue, not credentials to acquire.** "You need a museum
   solo and critical press" is a wall. "This is built out of art book fairs and
   consignment" is something to start on Tuesday.
3. **Money framed as what a door gives**, never as what anything has cost her.

Her position across the five is deliberately uneven and that asymmetry is the
most useful content here: she is far along one of them and at zero on another,
and neither is visible from where she stands.
"""

from typing import Optional


def _t(en: str, zh: str) -> dict:
    # ja is deliberately absent for now rather than machine-guessed; the UI
    # falls back to en. Adding ja is tracked as follow-up work.
    return {"en": en, "zh": zh}


FUTURES = [
    {
        "id": "no_gatekeepers",
        "name": _t("No Gatekeepers", "不需要谁点头"),
        "tagline": _t("The audience is the asset. Nobody's permission required.",
                      "观众本身就是资产。不需要任何人点头。"),
        "life": _t(
            "You make the work and put it out yourself. No gallery takes a cut, no publisher "
            "decides your next book, no client sends notes. The risk isn't rejection — there's "
            "nobody to reject you — it's that everything rests on you continuing to show up. "
            "The reward is that nothing can be taken away by someone else's decision.",
            "你做作品，然后自己把它送出去。没有画廊抽成，没有出版社替你决定下一本书，没有客户提修改意见。"
            "这条路的风险不是被拒绝——根本没有人能拒绝你——而是一切都取决于你能不能一直做下去。"
            "回报是：没有任何东西会因为别人的一个决定而消失。"),
        "money": _t(
            "Three layers, in ascending order of what they pay and how much work they are up "
            "front. Prints and postcards: low margin, steady. Editions and originals: high "
            "margin, low volume. And a course — made once, sold indefinitely. That third layer "
            "is the one that turns an audience into a living, and it's the one you don't have.",
            "三层，越往上收入越高、前期投入也越大。版画与明信片：利润低但稳定。限量与原作：利润高但量小。"
            "再往上是一门课——做一次，可以一直卖。第三层才是把观众变成生计的那一层，"
            "也正是你目前还没有的那一层。"),
        "steps": [
            _t("Pick the one thing people keep asking you about. For someone who paints buildings that is almost always how you handle perspective and light, not \"how to paint\".",
               "挑出那件别人反复来问你的事。对一个画建筑的人来说，几乎总是「透视和光你是怎么处理的」，而不是「怎么画画」。"),
            _t("Record it once. A course is three to five hours of video, not a curriculum.",
               "录一次就好。一门课是三到五小时的视频，不是一套教学大纲。"),
            _t("Launch it to the people already following the work. No new audience needed.",
               "面向已经在看你作品的人发布。不需要新的观众。"),
            _t("You find out in a month whether it sells, not in a year.",
               "一个月就知道卖不卖得动，而不是等一年。"),
        ],
        "example": _t("Ohn Mar Win — over 80,000 students on Skillshare. By her own published figures teaching is 77% of her income and licensing only 3%. It took her eleven years.",
                      "Ohn Mar Win——Skillshare 上有八万多名学生。按她自己公开的数字，教学占她收入的 77%，授权只占 3%。这条路她走了十一年。"),
    },
    {
        "id": "someone_else_sells",
        "name": _t("Someone Else Sells It", "有人替你卖"),
        "tagline": _t("A gallery does the selling, the pricing, and the finding of buyers.",
                      "由画廊来销售、定价，并且去找买家。"),
        "life": _t(
            "The defining difference isn't prestige, it's that the money flows the other way. "
            "Today you pay for the room. In this life the gallery pays for the show, takes a "
            "commission, and its job is to find collectors who come back. Prices per painting "
            "rise because someone whose living depends on it is arguing for them.",
            "这条路真正的分别不在于名气，而在于钱的流向反过来了。现在是你付场地费；"
            "在这条路上，是画廊出钱办展、抽取佣金，而它的工作就是找到会回头再买的藏家。"
            "每张画的价格会上去，因为有一个人靠这件事吃饭，在替你争取。"),
        "money": _t(
            "Commission replaces rent. A representing gallery takes 40–50% — more than a rental "
            "gallery's cut — but you pay nothing up front, they cover production and promotion, "
            "and they bring the buyers. Between the two sits a third option worth more than "
            "either: an open call that pays you to exhibit. TOKAS gives ¥150,000 toward the "
            "work and the venue is free.",
            "佣金取代了租金。代理画廊抽 40–50%，比租赁画廊抽得更多——但你不需要预先付一分钱，"
            "制作与宣传都由它承担，买家也由它带来。而在两者之间还有第三种，比哪一种都划算："
            "反过来付钱给你办展的公开征集。TOKAS 提供 15 万日元制作经费，场地免费。"),
        "steps": [
            _t("Ten paintings that hang together as one body. Every funded door and every gallery conversation starts here, and it's the same ten for all of them.",
               "十张能作为一个整体挂在一起的画。每一个提供经费的项目、每一次与画廊的接触，都从这里开始，而且是同样的这十张。"),
            _t("Apply to the venues that pay you rather than charge you — TOKAS-Emerging around June, OPEN SITE around February, Kyoto Art Center around October.",
               "去申请那些付钱给你、而不是收你钱的场地——TOKAS-Emerging 约在六月，OPEN SITE 约在二月，京都艺术中心约在十月。"),
            _t("Visit the galleries whose roster looks like your work. As a viewer. Twice.",
               "去看那些代理风格与你相近的画廊。以观众的身份，去两次。"),
            _t("Then write one email that introduces you and asks what they'd want to see. It doesn't ask for a show — so there's nothing to decline, and whatever comes back is something you can go and build.",
               "然后写一封邮件，做个自我介绍，并问他们希望看到什么。这封信不请求展览——所以没有什么可以被拒绝，"
               "而对方回复的任何内容，都是你接下来可以去做的东西。"),
            _t("Do that with ten galleries. One of them answers.",
               "对十家画廊都这样做。总有一家会回应。"),
        ],
        "example": _t("Where this road can end up: Keita Morimoto paints night streets — a decade of them in Toronto before Tokyo — and is now with KOTARO NUKAGA here and Almine Rech internationally, with work in the National Gallery of Canada and a 2025 solo at the 21st Century Museum in Kanazawa. Far past a first gallery conversation, but that is the shape of the road.",
                      "这条路可以通向哪里：森本启太画夜晚的街道——在来东京之前，他在多伦多画了十年——如今在东京由 KOTARO NUKAGA 代理，国际上则是 Almine Rech，作品被加拿大国立美术馆收藏，2025 年在金泽21世纪美术馆举办个展。这已经远远超过第一次与画廊接触的阶段，但那条路的形状就是这样。"),
    },
    {
        "id": "work_goes_out",
        "name": _t("The Work Goes Out Without You", "作品自己出门"),
        "tagline": _t("Your images on things, made and sold by other people.",
                      "你的图像出现在各种东西上，由别人生产、别人销售。"),
        "life": _t(
            "Quiet money. You license images — to stationery, homeware, packaging, book covers, "
            "brands — and other companies manufacture, distribute and sell them. You are not "
            "necessarily famous in this life. You are paid repeatedly for work you already made. "
            "It suits someone who wants to keep painting and not manage anything.",
            "安静的钱。你把图像授权出去——文具、家居、包装、书封、品牌——由别的公司去生产、铺货、销售。"
            "在这条路上你不一定出名。你只是为已经画好的作品，反复地拿到钱。"
            "它适合那种想一直画下去、又不想管别的事的人。"),
        "money": _t(
            "Two shapes. A flat fee is one payment for one use: simple, and capped. A royalty is "
            "a percentage of sales, ongoing and unbounded. Worth knowing before you chase it, "
            "though: the one illustrator we found who publishes her actual numbers has a "
            "twenty-year licensing practice with M&S, John Lewis and Unilever — and licensing "
            "is 3% of her income, against 77% from teaching. It can pay well; it rarely pays "
            "most. Architecture and cityscape work also licenses to different buyers than "
            "character work does: interiors, hospitality, stationery, publishing, travel.",
            "两种形式。一次性买断是一笔钱换一次使用：简单，但有上限。分成是按销售额抽成，持续发生、没有上限。"
            "但在投入之前值得知道：我们找到的唯一一位公开自己收入构成的插画师，"
            "做了二十年授权，客户包括 M&S、John Lewis、联合利华——而授权只占她收入的 3%，教学占 77%。"
            "这条路可以赚钱，但很少成为收入的主要来源。另外，建筑与城市题材的授权对象，"
            "和角色类作品完全不同：室内、酒店餐饮、文具、出版、旅行。"),
        "steps": [
            _t("Assemble a set of images that work small and repeat. Licensing buys pattern and mood, not single masterpieces.",
               "整理出一组缩小后依然成立、并且可以重复使用的图像。授权买的是图案与氛围，不是单张杰作。"),
            _t("Approach the categories that already use this kind of imagery: stationery makers, hotel and café interiors, publishers who need covers.",
               "去接触那些本来就在使用这类图像的领域：文具厂商、酒店与咖啡馆的室内、需要封面的出版社。"),
            _t("Never sign an unlimited buyout on a body of work you'd want to license again. This is the one place where a bad first contract costs years.",
               "永远不要为一批你日后还想再授权的作品签下无限期买断。这是唯一一处，第一份糟糕的合同会让你损失好几年。"),
        ],
        "example": _t("(No example named yet — this one needs research before a name goes here.)",
                      "（暂无实例——这一条需要先做研究，才能写上具体的人。）"),
    },
    {
        "id": "between_covers",
        "name": _t("Between Covers", "书里"),
        "tagline": _t("The book is the work, not a record of it.",
                      "书本身就是作品，而不是作品的记录。"),
        "life": _t(
            "Books are the vehicle. Not zines documenting the practice — books people buy "
            "because they are books. A publisher may be involved or not, and that single choice "
            "changes everything about how it feels and what it pays.",
            "书是载体。不是记录创作过程的 zine，而是别人因为它是一本书才买下的书。"
            "可能有出版社参与，也可能没有——而仅仅这一个选择，就会彻底改变它做起来的感觉和它带来的收入。"),
        "money": _t(
            "Self-published, printed in China at 300 copies: about ¥390,000 up front, and it "
            "pays for itself at 107 copies sold directly. Printed in Japan at 100 copies it "
            "cannot break even at any sell-through — a small run only works at a high cover "
            "price. With a publisher you pay nothing and carry no boxes, earn perhaps a tenth as "
            "much per copy, and reach bookshops nationally, which you cannot do alone. The "
            "publisher wins on volume and on risk. The only thing it depends on is them saying yes.",
            "自己出版、在中国印 300 本：前期约 39 万日元，直接卖出 107 本就能回本。"
            "在日本印 100 本，则无论卖得多好都无法回本——小批量只有在定价够高时才成立。"
            "如果有出版社，你不用出一分钱、家里也不用堆书，每本大约只拿十分之一的钱，"
            "但书能进入全国的书店，而这是你一个人做不到的。出版社在数量和风险上都更划算。"
            "唯一的变数，是他们愿不愿意点头。"),
        "steps": [
            _t("The material already exists — six years of daily work is more than a book needs.",
               "材料早就有了——六年的日课，比做一本书需要的还多。"),
            _t("Get quotes from both a Japanese and a Chinese printer for the same specification. You read Chinese; the prices quoted to a Chinese speaker are not the prices quoted to a foreigner.",
               "同样的规格，同时向日本和中国的印厂询价。你读中文——报给中文使用者的价格，和报给外国人的价格并不一样。"),
            _t("Cover the run through channels that don't depend on your audience: consignment at a few shops, one fair booth. If those cover it, every direct sale is upside rather than something the plan needs.",
               "让印刷成本通过不依赖你观众的渠道回收：几家店的寄售，加一个书展摊位。如果这些能覆盖成本，"
               "那么每一笔直接销售都是额外收获，而不是计划必须依赖的部分。"),
            _t("A self-published book is also the object you show a publisher. Colour Diary already did that job once.",
               "自己出的书，同时也是给出版社看的东西。《Colour Diary》已经做过一次这件事。"),
        ],
        "example": _t("Mateusz Urbanowicz — his Tokyo architecture books (Tokyo Storefronts, Tokyo at Night) are published by MdN, not self-published, and the series has passed 100,000 copies in Japan. He sells originals himself and has no gallery.",
                      "Mateusz Urbanowicz——他画东京建筑的书（《东京店构え》《东京夜行》）由 MdN 出版，并非自出版，这个系列在日本已经卖过十万册。原作由他自己销售，没有画廊代理。"),
    },
    {
        "id": "on_assignment",
        "name": _t("On Assignment", "接活"),
        "tagline": _t("Steady client work. The only one of these with a predictable monthly number.",
                      "稳定的客户工作。这几条路里，唯一一条每月收入可以预期的。"),
        "life": _t(
            "Editorial illustration, book covers, commissions. Someone briefs you, you deliver, "
            "you're paid on a schedule. Less romantic than the others and the only one that pays "
            "rent reliably. Architecture and atmosphere are in demand for covers specifically — "
            "literary fiction leans heavily on exactly this kind of image.",
            "杂志插画、书籍封面、委托创作。有人给你需求，你交稿，按约定时间拿钱。"
            "比其他几条路都不浪漫，但也是唯一一条能稳定付房租的。建筑与氛围类的画在封面上尤其抢手——"
            "文学小说的封面，大量依赖的正是这一类图像。"),
        "money": _t(
            "Per-commission fees, negotiated per use. An agent takes 25–30% and brings work you "
            "would not otherwise see — though plenty of working illustrators never have one and "
            "take commissions direct. Rates vary enormously by client, which is why the "
            "portfolio you show determines the work you're offered.",
            "按单收费，按使用范围议价。经纪人抽 25–30%，但会带来你自己接触不到的工作——"
            "不过也有不少一直在接活的插画家从来没有经纪人，都是直接对接。"
            "不同客户的价差极大——所以你拿出来的作品集，决定了别人会找你做什么样的活。"),
        "steps": [
            _t("Make a portfolio that shows the use, not the paintings. A cover mock-up reads to an art director in a way a gallery image does not.",
               "做一份展示「用途」而不是「画作」的作品集。对艺术总监来说，一个封面样稿的说服力，和一张展览图片完全不同。"),
            _t("Enter the industry's own competitions — The Choice, HB Gallery FILE. That is where Japanese art directors actually look.",
               "参加这个行业自己的比赛——The Choice、HB Gallery FILE。日本的艺术总监真正会去看的就是这些。"),
            _t("Approach publishers directly. Japanese literary publishers commission covers constantly.",
               "直接联系出版社。日本的文学出版社一直在找人画封面。"),
            _t("An agent comes after there's work to manage, not before.",
               "经纪人是在有活要管之后才出现的，不是在那之前。"),
        ],
        "example": _t("Tatsuro Kiuchi — book jackets, editorial and advertising: Ikeido Jun's novels, the New York Times, Penguin, Uniqlo. He works without an agent; the commissions come direct.",
                      "木内达朗——书籍封面、杂志插画与广告：池井户润的小说、《纽约时报》、企鹅出版、优衣库。他没有经纪人，工作都是直接找上门的。"),
    },
]


def build(evidence: Optional[dict] = None) -> dict:
    """Where she already stands on each future, computed from her real record.

    Deliberately not authored prose: the standings move as her record does, and a
    hardcoded "you have two solo shows" goes stale the moment she has a third —
    which is exactly how the old career copy ended up describing a 2023 group
    show as her latest news.
    """
    ev = evidence or {}
    solos = ev.get("solo_shows", 0)
    groups = ev.get("confirmed_group_shows", 0)
    pubs = ev.get("publications_confirmed", 0)

    standing = {
        "no_gatekeepers": _t(
            f"Further along this one than any other. Six years of daily work, an audience that "
            f"already watches it, a shop that already works, and {pubs} publications. The only "
            f"missing layer is the one that scales.",
            f"这条路你走得比其他任何一条都远。六年的日课、一群已经在看的观众、一个已经在运转的店铺，"
            f"以及 {pubs} 本出版物。唯一缺的，是那一层可以规模化的。"),
        "someone_else_sells": _t(
            f"{groups} group shows, {solos} solo shows, museum group exhibitions, an "
            f"international showing. The record is real. What's missing is a show someone else "
            f"paid for — and that single credential changes the conversation.",
            f"{groups} 场联展、{solos} 场个展、美术馆群展、一次海外展出。履历是实打实的。"
            f"缺的是一场由别人出钱办的展览——而正是这一项，会改变对话的性质。"),
        "work_goes_out": _t(
            "Effectively at zero, and it's the largest untouched category here. It's also the "
            "one least affected by where you live or what visa you hold.",
            "基本还是零，而这是这里最大的一片未被触及的领域。它也是受居住地与签证影响最小的一条。"),
        "between_covers": _t(
            f"{pubs} publications already, and of everything this app has ever put in front of "
            f"you, an art book fair is the one thing you followed.",
            f"已经有 {pubs} 本出版物。而在这个应用曾经推到你面前的所有东西里，"
            f"你真正点进去看的，是一个艺术书展。"),
        "on_assignment": _t(
            "Your training is in illustration and design, which is precisely this world — but "
            "there's no commercial work on record. The distance is short and mostly about how "
            "the work is presented.",
            "你学的是插画与设计，而这正是这个领域——但履历上没有商业作品。"
            "距离其实不远，主要是作品如何呈现的问题。"),
    }

    return {
        "futures": [{**f, "standing": standing.get(f["id"])} for f in FUTURES],
        "note": _t(
            "Five different kinds of success, not five strategies. You are already on more than "
            "one of them.",
            "五种不同的「成功」，而不是五种策略。其中不止一条，你其实已经在走了。"),
    }
