"""
recurring_calendar_engine.py

A year she can plan against, instead of a pile of scraped dates.

The seasonal calendar built from `deadline` fields shows whatever the pipeline
happened to catch this quarter: 231 items across four months, 78 in September
alone, and nothing at all past December — while every high-value door found in
the 2026-09-04 research opens in 2027 and is therefore invisible.

This module inverts that. The doors are AUTHORED here as recurring windows,
because recurrence is a durable fact about an institution ("TOKAS-Emerging
opens around June") that stays true after this year's date has passed, whereas
a scraped deadline rots the moment it expires. Everything time-dependent —
which door is next, how far away it is, whether she is inside its preparation
window right now — is COMPUTED per request, so nothing here goes stale.

Sources for every entry: reports/weekend_advice_research_2026-09-04.md, which
records the URL and a confidence tag per door. Entries whose recurrence was
inferred rather than read off an official page are marked `certain: False`.

The `prepare` field is the point of the whole thing. Four of the seven career
levers currently tell her to 留意 ("watch for") a call — which is dead waiting.
A lead time turns that into work she can do in a month when nothing is open.

VOICE: Saffron is SECOND person — it speaks to her ("you have", "your record").
Mochi is third. This module happens to be impersonal: it describes doors, not
her, so 0 of its 144 rendered strings use either person, and that is correct.

What the paragraph below originally said was "third person throughout", which
misread this module's impersonality as a house rule and stated it as one. On
2026-09-08 that sent the Saffron strategy ladders out written about her in the
third person, which reads as a case file to the person it is about. The five
strings it corrected were genuinely wrong — they ASSIGNED work — but the fix for
an imperative is to describe, not to switch person. Five strings addressed her directly ("A show you
were going to do anyway", "You qualify for the Mainland China track", "the
printed-matter world you already come from", 「为你这种情况设的」, and the
"paintings you don't have to sell" label in `SaffronPage.jsx`) and were rewritten
2026-09-06. The page describes; it does not talk to anyone.
"""

from calendar import monthrange
from datetime import date
from typing import Optional


def _t(en: str, zh: str, ja: str) -> dict:
    return {"en": en, "zh": zh, "ja": ja}


# ── The doors ────────────────────────────────────────────────────────────────
# opens_month: the month the call typically OPENS (not the deadline) — that is
# the date she needs to be ready for. prepare_lead: months before that when the
# preparation is worth starting.

DOORS = [
    {
        "id": "tokas_emerging", "amount_jpy": 150000, "amount_kind": "production",
        "name": _t("TOKAS-Emerging", "TOKAS-Emerging（东京都现代美术空间）", "TOKAS-Emerging"),
        "opens": (6, 1), "closes": (7, 31), "prepare_lead": 2, "certain": True,
        "url": "https://www.tokyoartsandspace.jp/application/schedule.html",
        "gives": _t(
            "Free venue, ¥150,000 production grant, install and PR handled. Japan-resident, any nationality, under 35.",
            "免费场地、15 万日元制作经费，布展与宣传都由他们负责。在日本居住即可，不限国籍，35 岁以下。",
            "会場費なし、制作費15万円、設営と広報も先方持ち。日本在住であれば国籍不問、35歳以下。"),
        "prepare": _t(
            "A proposal and ten paintings that hang together as one body.",
            "一份展览提案，和十张能作为一个整体挂在一起的画。",
            "展示プランと、ひとつのまとまりとして掛けられる10点。"),
    },
    {
        # Deferred. TOKAS's own Japanese schedule page, 2026-09-06:
        # 「OPEN SITEは、TOKAS本郷メンテナンスのため、2027年度以降に公募を実施。」
        # The English page does not carry the notice, which is how this sat as
        # `certain: True` in February with ¥400,000 attached.
        "id": "tokas_open_site", "amount_jpy": 400000, "amount_kind": "production",
        "name": _t("TOKAS OPEN SITE", "TOKAS OPEN SITE", "TOKAS OPEN SITE"),
        "opens": (2, 1), "prepare_lead": 2, "certain": False,
        "url": "https://www.tokyoartsandspace.jp/application/schedule.html",
        "status_note": _t(
            "Paused. TOKAS Hongo is under maintenance and the next call is for fiscal 2027 onward, so there is no February round this time.",
            "暂停中。TOKAS 本乡馆正在施工，下一次征集要到 2027 年度以后，所以今年二月这一轮不会有。",
            "休止中。TOKAS本郷のメンテナンスのため、次の公募は2027年度以降。今回は2月の回がない。"),
        "gives": _t(
            "¥400,000 towards the exhibition, no age limit, solo proposals accepted.",
            "40 万日元展览经费，不限年龄，接受个展提案。",
            "展示に40万円、年齢制限なし、個展の企画も可。"),
        "prepare": _t(
            "The same body of work, plus a written plan for how it fills a room.",
            "同一批作品，外加一份「它如何撑起一个空间」的书面构想。",
            "同じ作品群と、それが空間をどう満たすかを書いた構想。"),
    },
    {
        # TOKAS's schedule page gives both the Domestic Young Creator residency
        # and the Inter-City Exchange (Dispatch) as September–November. As of
        # 2026-09-06 the open-call index still reads 「募集中の公募はありません」,
        # so the window has not started: `certain: False` keeps the green badge
        # off until the call is actually posted.
        "id": "tokas_residency",
        "name": _t("TOKAS residencies (local + exchange)", "TOKAS 驻地（国内・交流）", "TOKAS レジデンシー（国内・交流）"),
        "opens": (9, 15), "closes": (11, 30),
        "prepare_lead": 1, "certain": False,
        "url": "https://www.tokyoartsandspace.jp/application/index.html",
        "gives": _t(
            "60–90 days in Sumida with a production fee, or ~3 fully funded months in Taipei, Seoul or Helsinki. Nationality unrestricted.",
            "在墨田驻留 60–90 天并有制作费，或全额资助约 3 个月，前往台北、首尔或赫尔辛基。不限国籍。",
            "墨田で60〜90日・制作費付き、または台北・ソウル・ヘルシンキへ約3か月の全額助成。国籍不問。"),
        "prepare": _t(
            "A reason to be somewhere — what the place would change about the work.",
            "一个「为什么要去那里」的理由——那个地方会让作品发生什么变化。",
            "「なぜそこへ行くのか」——その土地が作品に何をもたらすか。"),
    },
    {
        # ¥500,000 is a GRAND PRIZE one entrant receives, not what the door
        # gives — so it gets no paintings line. The number that applies to
        # everyone who walks through is the booth fee, and it was missing.
        "id": "sicf", "amount_jpy": 500000, "amount_kind": "prize", "entry_fee_jpy": 48400,
        "name": _t("SICF (Spiral, Aoyama)", "SICF（青山 Spiral）", "SICF（青山スパイラル）"),
        "opens": (11, 1), "prepare_lead": 1, "certain": False,
        "url": "https://www.sicf.jp/",
        "gives": _t(
            "Juried, artist-direct, no age or nationality limit. A booth costs from ¥48,400. One entrant takes the Grand Prize — a solo show in Spiral's Atrium and ¥500,000.",
            "评审制，艺术家可直接报名，不限年龄与国籍。展位费从 48,400 日元起。其中一位拿到大奖——在 Spiral 中庭办个展，外加 50 万日元。",
            "審査制・作家直接応募、年齢国籍不問。ブースは48,400円から。うち一名がグランプリ——Spiralアトリウムでの個展と50万円。"),
        "prepare": _t(
            "Work that reads from across a room — the booth is seen at a distance first.",
            "要能从远处一眼看住的作品——展位首先是被远远看见的。",
            "遠くからでも成立する作品——ブースはまず遠目に見られる。"),
    },
    {
        # URL was the 2026 edition page, which now reads 「出展者募集を締め切りました」.
        # Edition-specific links rot every year; the programme root does not.
        "id": "independent_tokyo", "entry_fee_jpy": 45000,
        "name": _t("Independent Tokyo", "Independent Tokyo", "インディペンデント東京"),
        "opens": (10, 1), "prepare_lead": 1, "certain": False,
        "url": "https://www.tagboat.com/artevent/",
        "gives": _t(
            "Screened by the organiser, with 20–30 gallerists judging on the floor — one of the recognised routes galleries use to find new artists. A booth runs from about ¥45,000.",
            "由主办方筛选，现场有 20–30 位画廊主担任评审——这是画廊发掘新人的公认渠道之一。展位费约 45,000 日元起。",
            "主催者による選考、当日は20〜30名のギャラリストが審査——ギャラリーが新しい作家を見つける定番の場のひとつ。ブースは約45,000円から。"),
        "prepare": _t(
            "One coherent wall, and a short answer to the question every gallerist on the floor asks — what is being made at the moment.",
            "一面完整连贯的墙，和一句能回答「最近在做什么」的简短说明——现场每一位画廊主都会问这句。",
            "一面ぶんのまとまりと、会場のギャラリストが必ず訊く「いま何を作っているか」への短い答え。"),
    },
    {
        # This entry had the DEADLINE month recorded as the OPENING month, so a
        # competition that is open today and shuts in weeks rendered as a future
        # October door marked "worth starting now". vol.37 closes 2026-10-16
        # (postmark), verified 2026-09-06. Exactly the confusion the module
        # docstring says this file exists to avoid.
        "id": "hb_file",
        "name": _t("HB Gallery FILE competition", "HB Gallery FILE 大赛", "HBギャラリー FILEコンペ"),
        "opens": (7, 1), "closes": (10, 16),
        "prepare_lead": 1, "certain": True,
        "url": "https://hbgallery.com/compe.html",
        "gives": _t(
            "No eligibility restriction of any kind — nationality, age, residence or student status. Ten special-award winners, and grand-prize winners each get a one-week solo in Omotesando.",
            "没有任何资格限制——国籍、年龄、居住地、学生身份都不设门槛。十位特别奖得主，大奖得主各获得表参道的一周个展。",
            "応募資格の制限は一切なし——国籍、年齢、居住地、学生かどうかも問わない。特別賞10名、グランプリには表参道での1週間の個展。"),
        "prepare": _t(
            "15–20 works chosen as a set — this one is judged by art directors, not curators.",
            "15–20 张作为一组来选的作品——评审是艺术总监，不是策展人。",
            "ひと組として選んだ15〜20点——審査するのはキュレーターではなくアートディレクター。"),
    },
    {
        # The old `prepare` said "the only cost is choosing the work". The call
        # takes 新作・未発表 only — new work, not published anywhere. For an
        # artist whose practice IS a six-year daily Instagram diary that is the
        # largest ask on this page, and it was written as the smallest.
        "id": "grid_next",
        "name": _t("biscuit gallery — \"grid next\"", "biscuit gallery「grid next」", "biscuit gallery「grid next」"),
        "opens": (12, 25), "closes": (4, 30),
        "prepare_lead": 1, "certain": False,
        "url": "https://biscuitgallery.com/",
        "gives": _t(
            "Free to enter, free to exhibit, students welcome — and one entrant is given a solo show. Roughly 40 and under.",
            "免费报名、免费参展，接受学生——其中一位可获得个展。年龄大致在 40 岁以下。",
            "応募も展示も無料、学生も可——うち一名に個展。年齢はおおむね40歳以下。"),
        "prepare": _t(
            "One new painting kept off Instagram until the show — the call takes unpublished work only.",
            "一张新画，并且在展览之前不发到 Instagram——这个征集只收未发表的作品。",
            "Instagramに出していない新作を一点——応募できるのは未発表作のみ。"),
    },
    {
        "id": "kyoto_coprogram", "amount_jpy": 1000000, "amount_kind": "production",
        "name": _t("Kyoto Art Center Co-program", "京都艺术中心 Co-program", "京都芸術センター 共同事業"),
        "opens": (10, 1), "prepare_lead": 2, "certain": False,
        "url": "https://www.kac.or.jp/open_call/",
        "gives": _t(
            "The best-funded open call found anywhere in Japan — up to ¥1,000,000 for a solo, plus six weeks of studio.",
            "目前在日本找到的经费最充裕的公开征集——个展最高 100 万日元，外加六周工作室。",
            "日本で見つかった中で最も手厚い公募——個展に最大100万円、加えて6週間のスタジオ。"),
        "prepare": _t(
            "A project, not a portfolio — they fund something being made, not something finished.",
            "要的是一个项目，而不是作品集——他们资助的是正在发生的创作，不是已完成的东西。",
            "求められるのは作品集ではなく企画——完成品ではなく、これから作るものに出る助成。"),
    },
    {
        # Round 2 of 2026 runs 25 Aug 10:00 – 24 Sep 18:00, read off the
        # programme page 2026-09-06. TWO rounds a year, not three — the old
        # `rounds_per_year: 3` was wrong and pulled the next occurrence four
        # months forward instead of six.
        "id": "arts_council_tokyo_startup", "amount_jpy": 300000, "amount_kind": "production",
        "name": _t("Arts Council Tokyo Startup Grant", "东京艺术委员会 创业期扶持金", "アーツカウンシル東京 スタートアップ助成"),
        "opens": (8, 25), "closes": (9, 24),
        "prepare_lead": 1, "certain": True, "rounds_per_year": 2,
        "url": "https://www.artscouncil-tokyo.jp/grants/startup-grant-program/",
        "gives": _t(
            "Up to ¥300,000 towards a public activity in Tokyo — a budget for putting something on, rather than income. No nationality clause; it asks for residence in Tokyo. Two rounds a year, so a missed one comes round again.",
            "在东京举办公开活动最高 30 万日元——这是一笔办事的预算，不是收入。无国籍限制，但要求在东京居住。一年两轮，错过一轮还有下一轮。",
            "都内での公開活動に最大30万円——収入ではなく、実施のための予算。国籍条項はなく、都内在住が条件。年2回なので、逃しても次がある。"),
        "prepare": _t(
            "A show that was already going to happen — this funds the thing, not a new idea.",
            "一个本来就打算做的展览——它资助的是这件事本身，不是一个新点子。",
            "もともとやる予定だった展示でいい——新しい企画ではなく、その実施に出る助成。"),
    },
    {
        # "fits the criteria as written" was an interpretation stated as a
        # reading, and the zh went further ("正符合其评选标准" moves eligibility
        # into judging). The domestic grant scopes to activity carried out in
        # Japan; the overseas variant needs a host invitation.
        "id": "nomura", "amount_jpy": 1000000, "amount_kind": "production",
        "name": _t("Nomura Foundation", "野村财团 艺术文化助成", "野村財団 芸術文化助成"),
        "opens": (10, 1), "prepare_lead": 2, "certain": False,
        "url": "https://www.nomurafoundation.or.jp/culture/art_ov01.html",
        "gives": _t(
            "Up to ¥1,000,000 towards the activity itself. No nationality, residency or age clause. The domestic grant covers work carried out in Japan, so a China–Japan exchange fits on its Japanese leg.",
            "最高 100 万日元，用于活动本身。无国籍、居住地或年龄限制。国内这一项资助的是在日本进行的活动，所以中日交流展是以日本这一边的部分符合条件。",
            "活動そのものに最大100万円。国籍・居住・年齢の条項なし。国内枠は日本国内で行う活動が対象なので、中日をまたぐ企画は日本側の部分で合う。"),
        "prepare": _t(
            "A partner on the other side — this one is built around two places.",
            "另一边要有个合作方——这个项目的结构就是两个地方。",
            "向こう側の相手が要る——二つの場所を結ぶ形の企画。"),
    },
    {
        # The biggest sum on the page, and the card used to carry only the good
        # half. Verified on ACC's own page 2026-09-06: five years of practice
        # required, and fellows "should take a temporary leave of absence" from
        # university coursework. That second clause is not a detail for someone
        # on a 留学 status — a leave of absence is what cancels it. Deadline
        # 2026-11-10 09:59 ET.
        "id": "acc",
        "name": _t("Asian Cultural Council fellowship", "亚洲文化协会 个人奖助", "アジアン・カルチュラル・カウンシル フェローシップ"),
        "opens": (10, 1), "closes": (11, 10),
        "prepare_lead": 3, "certain": True,
        "url": "https://www.asianculturalcouncil.org/grant-opportunities",
        "gives": _t(
            "Up to US$35,000. Eligibility runs on citizenship, so a Chinese passport counts wherever its holder lives — a Japanese student visa does not, on its own. It asks for five years of practice, and fellows step away from university coursework for the duration.",
            "最高 3.5 万美元。资格看的是国籍，所以中国护照在哪里都算数——单靠日本的留学签证则不算。它要求五年的创作经历，并且奖助期间要从课业中暂时抽身。",
            "最大35,000米ドル。資格は国籍で決まるので、中国籍であれば居住地を問わない——日本の留学ビザ単体では対象にならない。5年の活動歴が条件で、フェロー期間中は大学の課程から一時的に離れることになる。"),
        "status_note": _t(
            "The leave-of-absence clause is the one to check first, since a 留学 residence status depends on being enrolled. The Immigration Information Centre answers this kind of question for free.",
            "先要弄清楚的是「休学」这一条，因为留学在留资格本身以在学为前提。外国人在留综合信息中心可以免费咨询这类问题。",
            "まず確かめるべきは休学の条項。留学の在留資格は在学が前提になっている。外国人在留総合インフォメーションセンターで無料で相談できる。"),
        "prepare": _t(
            "References, and a plan measured in months rather than weeks. Three months is the realistic run-up — this is the longest form on the list.",
            "推荐人，以及一份以「月」而不是「周」为单位的计划。三个月是实际需要的准备期——这是清单上最长的一份申请。",
            "推薦者と、週単位ではなく月単位の計画。準備には実際に3か月かかる——このリストで最も重い書類。"),
    },
    {
        "id": "holbein", "amount_jpy": 300000, "amount_kind": "in_kind",
        "name": _t("Holbein Scholarship", "好乐门（Holbein）奖学金", "ホルベイン・スカラシップ"),
        "opens": (4, 1), "closes": (7, 31), "prepare_lead": 1, "certain": False,
        "url": "https://www.holbein.co.jp/scholarship.html",
        "gives": _t(
            "¥300,000 of materials over a year, from a watercolor manufacturer. Residence in Japan, no nationality clause.",
            "一年内价值 30 万日元的画材，来自一家水彩颜料厂商。在日本居住即可，无国籍限制。",
            "水彩メーカーによる年間30万円分の画材支給。日本在住であればよく、国籍条項なし。"),
        "prepare": _t(
            "Almost nothing — the medium match is already the argument.",
            "几乎不需要准备——媒介本身就是最好的理由。",
            "ほぼ不要——画材が合っていること自体が理由になる。"),
    },
    {
        "id": "faam",
        "name": _t("Fukuoka Asian Art Museum residency", "福冈亚洲美术馆 驻地", "福岡アジア美術館 レジデンス"),
        "opens": (12, 1), "prepare_lead": 1, "certain": False,
        "url": "https://faam.city.fukuoka.lg.jp/residence/requirement/",
        "gives": _t(
            "A museum-hosted residency ending in an exhibition. Built for artists working across Asia — neither residence nor nationality restricted.",
            "由美术馆主办、以展览收尾的驻地项目。专为在亚洲各地创作的艺术家而设——不限居住地与国籍。",
            "美術館主催、展示で締めくくるレジデンス。アジアを横断して制作する作家のための枠——居住地も国籍も不問。"),
        "prepare": _t(
            "The two-city practice is the application — what the moving between them does to the work.",
            "往返两座城市的创作本身就是申请内容——在两地之间移动对作品做了什么。",
            "二都市をまたぐ制作そのものが申請内容——行き来が作品に何をしているか。"),
    },
    {
        # The one outbound link she has ever clicked, and it pointed at an About
        # page carrying no dates and no application status. The January 2027
        # edition filled in June 2026; the next way in is the edition after it.
        "id": "tabf", "entry_fee_jpy": 16500,
        "name": _t("Tokyo Art Book Fair", "东京艺术书展 TABF", "東京アートブックフェア"),
        "opens": (4, 1), "prepare_lead": 3, "certain": False,
        "url": "https://tokyoartbookfair.com/application-addition/",
        "gives": _t(
            "A booth among zines, artist books, and the people who buy them — the printed-matter circuit. The cheapest table is ¥16,500 and the fair takes no commission on sales.",
            "在 zine、艺术家书和买这些东西的人当中占一个展位——这是印刷品的圈子。最便宜的桌子 16,500 日元，销售不抽成。",
            "zine、アーティストブック、それを買う人たちの中に置くブース——印刷物の側の場。いちばん安い机で16,500円、売上に手数料はかからない。"),
        "status_note": _t(
            "The January 2027 edition is already full — applications closed in June 2026 — so the next way in is the edition after it. The call tends to open in spring.",
            "2027 年 1 月这一届已经满了——报名在 2026 年六月就截止了——能进的是再下一届。征集通常在春天开始。",
            "2027年1月の回はすでに満員——応募は2026年6月に締め切られた——入れるのはその次の回。募集はおおむね春に始まる。"),
        "prepare": _t(
            "Something printed and finished. Three months is production time; the paperwork is an afternoon.",
            "一件印好、做完的东西。三个月说的是制作时间；填表只要一个下午。",
            "刷り上がった一冊。3か月は制作にかかる時間で、書類は半日で済む。"),
    },
]

# Rolling doors have no window to wait for — they are always open, which makes
# them the answer to "what can I do in a month when nothing else is."
ALWAYS_OPEN = [
    {
        # The only door on this page with no barrier of any kind for her today,
        # and it was rendering as half a card: the component dropped `prepare`
        # for always-open entries, and no amount was carried, so a ~¥1.9M first
        # grant showed nothing while a ¥150,000 production budget showed a
        # paintings line. Reachability and prominence were inverted.
        "id": "greenshields", "amount_jpy": 1900000, "amount_kind": "cash",
        "name": _t("Elizabeth Greenshields Foundation", "Elizabeth Greenshields 基金会", "エリザベス・グリーンシールズ財団"),
        "url": "https://www.elizabethgreenshieldsfoundation.org/",
        "gives": _t(
            "A first grant of roughly CAD 18,000 for representational painting. Ages 18–41, students explicitly eligible, and no citizenship or residency requirement at all.",
            "具象绘画的首次资助约 1.8 万加元。18–41 岁，明确接受学生申请，且完全没有国籍或居住地要求。",
            "具象絵画への初回助成が約18,000カナダドル。18〜41歳、学生も明確に対象、国籍も居住地も問わない。"),
        "prepare": _t(
            "Rolling — there is no date to miss. Images of recent work and a short account of what is being painted.",
            "常年接受申请——没有会错过的截止日期。近期作品的图片，加一段简短的说明：现在在画什么。",
            "通年受付——逃す締切がない。近作の画像と、いま何を描いているかの短い説明。"),
    },
]


# Her own published prices, read from gegyjiji.base.shop on 2026-09-04 and
# stored on the profile under `market_presence`. Money means nothing to a
# painter as a number; it means something as paintings. A ¥400,000 grant is
# "five paintings you don't have to sell," and that is a sentence about what
# she gets rather than a comment on what anything cost her.
_ORIGINAL_LOW_JPY = 31900
_ORIGINAL_HIGH_JPY = 115500


def _in_paintings(amount_jpy: int) -> Optional[dict]:
    """Translate an award into a range of her own originals.

    A range, not a point estimate: her originals span ¥31,900 to ¥115,500, and
    collapsing that to one number would invent a precision she never quoted.
    """
    if not amount_jpy:
        return None
    fewest = max(1, round(amount_jpy / _ORIGINAL_HIGH_JPY))
    most = max(1, round(amount_jpy / _ORIGINAL_LOW_JPY))
    return {"fewest": fewest, "most": most, "same": fewest == most}


def _on(year: int, month: int, day: int) -> date:
    """A real date, clamped to the last day of that month rather than to the 28th.

    Clamping everything to 28 silently moved published deadlines up to three
    days earlier — 31 July became 28 July. On a page whose whole job is telling
    her when something shuts, that is not a rounding error.
    """
    return date(year, month, min(day, monthrange(year, month)[1]))


def _shift(anchor: date, months: int) -> date:
    """Same day-of-month, `months` later, clamped to the end of the month."""
    m = anchor.month - 1 + months
    return _on(anchor.year + m // 12, m % 12 + 1, anchor.day)


def build(today: Optional[date] = None) -> dict:
    """The next twelve months of doors, ordered by what closes soonest.

    Rewritten 2026-09-06 after a review checked every entry against the
    institutions' own pages and found the timing model was the problem, not the
    data. Three faults, all of which made the section state guesses as facts:

    1. **`window_months` defaulted to 1.** A call that runs September to
       November flipped to "eleven months away" on 1 October while it still had
       two months left. That is the exact miss the docstring above claims this
       file prevents; it prevented it for one door and reproduced it elsewhere.
    2. **Nothing recorded a CLOSING date.** The top card was badged "Open now"
       with no date at all while its round closed in eighteen days. When a door
       is open, the only number that matters is when it shuts.
    3. **`open_now` ignored `certain`.** An inferred window rendered a green
       "Open now" badge, and the UI suppressed its own "timing approximate"
       caveat in exactly that branch — so the least certain claim was the one
       stated most confidently. TOKAS residencies was badged open on a day
       TOKAS's own page read 「募集中の公募はありません」.

    So a door now carries real dates: `opens` and `closes` as (month, day), and
    only a door whose dates are read off an official page is allowed the open
    badge. Anything inferred says so.
    """
    today = today or date.today()

    def step_of(d: dict) -> int:
        return max(1, 12 // d["rounds_per_year"]) if d.get("rounds_per_year") else 12

    def opened_by(d: dict, ref: date) -> date:
        """The most recent opening at or before `ref`."""
        month, day = d["opens"]
        when = _on(ref.year - 1, month, day)
        while _shift(when, step_of(d)) <= ref:
            when = _shift(when, step_of(d))
        return when

    def closes_of(d: dict, opened: date) -> Optional[date]:
        """The closing that belongs to the round which began on `opened`.

        A window is a DURATION, not a fixed calendar date, because a door with
        more than one round a year closes once per round. Arts Council opens
        25 Aug and closes 24 Sep — thirty days — so its February round closes in
        March, not the following September. Reading the stored (month, day)
        literally gave the February round a 207-day window.

        Pairing to the opening also has to survive a round that crosses the new
        year: grid next runs 25 December to 30 April.
        """
        if not d.get("closes"):
            return None
        om, od = d["opens"]
        cm, cd = d["closes"]
        base_open = _on(2000, om, od)
        base_close = _on(2000, cm, cd)
        if base_close < base_open:
            base_close = _on(2001, cm, cd)
        return opened + (base_close - base_open)

    upcoming = []
    for d in DOORS:
        last_open = opened_by(d, today)
        closes = closes_of(d, last_open)
        # Open means: this round has started, has a published closing date, and
        # that date has not passed. `certain` gates the badge — an inferred
        # window is a guess, and a guess rendered green is worse than a guess
        # rendered as a month. A door with no known closing date never gets it.
        is_open = bool(d.get("certain") and closes and last_open <= today <= closes)

        next_open = last_open if last_open > today else _shift(last_open, step_of(d))
        months_away = 0 if is_open else (
            (next_open.year - today.year) * 12 + (next_open.month - today.month))
        days_left = (closes - today).days if is_open else None
        if not is_open:
            closes = closes_of(d, next_open)

        upcoming.append({
            "open_now": is_open,
            "id": d["id"],
            "name": d["name"],
            "url": d["url"],
            "gives": d["gives"],
            "prepare": d["prepare"],
            # A note that qualifies the door itself — a suspension, a shut
            # application window — rather than anything about her.
            "status_note": d.get("status_note"),
            # The month of the NEXT round, not the door's base month. With two
            # rounds a year those differ: Arts Council's base month is August,
            # but from October the next one is February, and the card said
            # "August, 4 months away".
            "opens_month": next_open.month,
            "opens_year": next_open.year,
            "closes_month": closes.month if closes else None,
            "closes_day": closes.day if closes else None,
            "days_left": days_left,
            "months_away": months_away,
            # Inside the run-up: close enough that the preparation is the work.
            "preparing_now": (not is_open) and months_away <= d["prepare_lead"],
            "prepare_lead": d["prepare_lead"],
            "certain": d.get("certain", False),
            "rounds_per_year": d.get("rounds_per_year"),
            "amount_jpy": d.get("amount_jpy"),
            # What KIND of money, because the paintings line reads as income and
            # three of these are restricted production budgets, one is a prize
            # exactly one entrant receives, and one is materials.
            "amount_kind": d.get("amount_kind", "cash"),
            "amount_in_kind": d.get("amount_kind") == "in_kind",
            "entry_fee_jpy": d.get("entry_fee_jpy"),
            "in_paintings": _in_paintings(d.get("amount_jpy"))
            if d.get("amount_kind", "cash") != "prize" else None,
        })

    # Open doors first, then by what closes soonest, then by how near. The old
    # tie-break was the ENGLISH name, which put six October doors in an order
    # invisible to a Chinese reader.
    upcoming.sort(key=lambda x: (not x["open_now"],
                                 x["days_left"] if x["days_left"] is not None else 999,
                                 x["months_away"],
                                 not x["certain"]))
    return {
        "generated_for": today.isoformat(),
        "doors": upcoming,
        "always_open": ALWAYS_OPEN,
        "preparing_now_count": sum(1 for x in upcoming if x["preparing_now"]),
        "open_now_count": sum(1 for x in upcoming if x["open_now"]),
    }
