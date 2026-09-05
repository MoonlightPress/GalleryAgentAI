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
"""

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
        "id": "tokas_emerging", "amount_jpy": 150000,
        "name": _t("TOKAS-Emerging", "TOKAS-Emerging（东京都现代美术空间）", "TOKAS-Emerging"),
        "opens_month": 6, "prepare_lead": 2, "certain": True,
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
        "id": "tokas_open_site", "amount_jpy": 400000,
        "name": _t("TOKAS OPEN SITE", "TOKAS OPEN SITE", "TOKAS OPEN SITE"),
        "opens_month": 2, "prepare_lead": 2, "certain": True,
        "url": "https://www.tokyoartsandspace.jp/application/schedule.html",
        "gives": _t(
            "¥400,000 exhibition grant, no age limit, solo proposals accepted.",
            "40 万日元展览经费，不限年龄，接受个展提案。",
            "展示助成40万円、年齢制限なし、個展の企画も可。"),
        "prepare": _t(
            "The same body of work, plus a written plan for how it fills a room.",
            "同一批作品，外加一份「它如何撑起一个空间」的书面构想。",
            "同じ作品群と、それが空間をどう満たすかを書いた構想。"),
    },
    {
        "id": "tokas_residency",
        "name": _t("TOKAS residencies (local + exchange)", "TOKAS 驻地（国内・交流）", "TOKAS レジデンシー（国内・交流）"),
        "opens_month": 9, "prepare_lead": 1, "certain": False,
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
        "id": "sicf", "amount_jpy": 500000,
        "name": _t("SICF (Spiral, Aoyama)", "SICF（青山 Spiral）", "SICF（青山スパイラル）"),
        "opens_month": 11, "prepare_lead": 1, "certain": True,
        "url": "https://www.spiral.co.jp/artcat/sicf",
        "gives": _t(
            "Juried, artist-direct, no age or nationality limit. Grand Prize is a solo show in Spiral's Atrium plus ¥500,000.",
            "评审制，艺术家可直接报名，不限年龄与国籍。大奖是在 Spiral 中庭举办个展，外加 50 万日元。",
            "審査制・作家直接応募、年齢国籍不問。グランプリは Spiral アトリウムでの個展と50万円。"),
        "prepare": _t(
            "Work that reads from across a room — the booth is seen at a distance first.",
            "要能从远处一眼看住的作品——展位首先是被远远看见的。",
            "遠くからでも成立する作品——ブースはまず遠目に見られる。"),
    },
    {
        "id": "independent_tokyo",
        "name": _t("Independent Tokyo", "Independent Tokyo", "インディペンデント東京"),
        "opens_month": 10, "prepare_lead": 1, "certain": True,
        "url": "https://www.tagboat.com/artevent/independenttokyo2026/index.php",
        "gives": _t(
            "Screened by the organiser, with 20–30 gallerists judging on the floor. The recognised way galleries find new artists.",
            "由主办方筛选，现场有 20–30 位画廊主担任评审。是画廊发掘新艺术家的公认渠道。",
            "主催者による選考、当日は20〜30名のギャラリストが審査。ギャラリーが新しい作家を見つける定番の場。"),
        "prepare": _t(
            "One coherent wall, and a short answer to \"what are you working on now.\"",
            "一面完整连贯的墙，和一句「你最近在做什么」的简短回答。",
            "一面ぶんのまとまりと、「いま何を作っているか」への短い答え。"),
    },
    {
        "id": "hb_file",
        "name": _t("HB Gallery FILE competition", "HB Gallery FILE 大赛", "HBギャラリー FILEコンペ"),
        "opens_month": 10, "prepare_lead": 1, "certain": False,
        "url": "https://hbgallery.com/compe.html",
        "gives": _t(
            "No eligibility restriction. Five grand-prize winners each get a one-week solo in Omotesando.",
            "无资格限制。五位大奖得主各获得表参道的一周个展。",
            "応募資格の制限なし。グランプリ5名にそれぞれ表参道での1週間の個展。"),
        "prepare": _t(
            "15–20 works chosen as a set — this one is judged by art directors, not curators.",
            "15–20 张作为一组来选的作品——评审是艺术总监，不是策展人。",
            "ひと組として選んだ15〜20点——審査するのはキュレーターではなくアートディレクター。"),
    },
    {
        "id": "grid_next",
        "name": _t("biscuit gallery — \"grid next\"", "biscuit gallery「grid next」", "biscuit gallery「grid next」"),
        "opens_month": 12, "prepare_lead": 1, "certain": False,
        "url": "https://biscuitgallery.com/gridnext-2026/",
        "gives": _t(
            "Free to enter, free to exhibit, students welcome — and one entrant is given a solo show.",
            "免费报名、免费参展，接受学生——其中一位可获得个展。",
            "応募も展示も無料、学生も可——うち一名に個展。"),
        "prepare": _t(
            "Nothing to buy and nothing to lose — the only cost is choosing the work.",
            "不用花钱，也没什么可失去的——唯一的成本是把作品选出来。",
            "費用も持ち出しもなし——かかるのは作品を選ぶ手間だけ。"),
    },
    {
        "id": "kyoto_coprogram", "amount_jpy": 1000000,
        "name": _t("Kyoto Art Center Co-program", "京都艺术中心 Co-program", "京都芸術センター 共同事業"),
        "opens_month": 10, "prepare_lead": 2, "certain": False,
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
        "id": "arts_council_tokyo_startup", "amount_jpy": 300000,
        "name": _t("Arts Council Tokyo Startup Grant", "东京艺术委员会 创业期扶持金", "アーツカウンシル東京 スタートアップ助成"),
        "opens_month": 8, "prepare_lead": 1, "certain": True, "rounds_per_year": 3, "window_months": 2,
        "url": "https://www.artscouncil-tokyo.jp/grants/startup-grant-program/",
        "gives": _t(
            "Up to ¥300,000 for a public activity in Tokyo. No nationality clause. Three rounds a year, so a missed one comes round again.",
            "在东京的公开活动最高 30 万日元。无国籍限制。一年三轮，错过一轮还有下一轮。",
            "都内での公開活動に最大30万円。国籍条項なし。年3回あるので、逃しても次がある。"),
        "prepare": _t(
            "A show you were going to do anyway — this funds the thing, not a new idea.",
            "一个你本来就打算做的展览——它资助的是这件事本身，不是一个新点子。",
            "もともとやる予定だった展示でいい——新しい企画ではなく、その実施に出る助成。"),
    },
    {
        "id": "nomura", "amount_jpy": 1000000,
        "name": _t("Nomura Foundation", "野村财团 艺术文化助成", "野村財団 芸術文化助成"),
        "opens_month": 10, "prepare_lead": 2, "certain": True,
        "url": "https://www.nomurafoundation.or.jp/culture/art_ov01.html",
        "gives": _t(
            "Up to ¥1,000,000. No nationality, residency or age clause. International exchange counts — a China–Japan show fits the criteria as written.",
            "最高 100 万日元。无国籍、居住地或年龄限制。国际交流也在范围内——一场中日交流展正符合其评选标准。",
            "最大100万円。国籍・居住・年齢の条項なし。国際交流も対象——中日をまたぐ展示は要件にそのまま合う。"),
        "prepare": _t(
            "A partner on the other side — this one wants two places, not one.",
            "另一边要有个合作方——这个项目要的是两个地方，而不是一个。",
            "向こう側の相手が要る——ひとつの場所ではなく、二つを結ぶ企画。"),
    },
    {
        "id": "acc",
        "name": _t("Asian Cultural Council fellowship", "亚洲文化协会 个人奖助", "アジアン・カルチュラル・カウンシル フェローシップ"),
        "opens_month": 10, "prepare_lead": 3, "certain": True,
        "url": "https://www.asianculturalcouncil.org/grant-opportunities",
        "gives": _t(
            "Up to US$35,000. You qualify for the Mainland China track by citizenship — where you live doesn't matter.",
            "最高 3.5 万美元。凭中国国籍即可申请中国大陆项目——住在哪里并不影响资格。",
            "最大35,000米ドル。中国籍で中国本土枠の対象——居住地は問われない。"),
        "prepare": _t(
            "References, and a plan for months rather than weeks. Start early; this is the longest form on the list.",
            "推荐人，以及一份以「月」而不是「周」为单位的计划。早点开始——这是清单上最长的一份申请。",
            "推薦者と、週単位ではなく月単位の計画。早めに——このリストで最も重い書類。"),
    },
    {
        "id": "holbein", "amount_jpy": 300000, "amount_in_kind": True,
        "name": _t("Holbein Scholarship", "好乐门（Holbein）奖学金", "ホルベイン・スカラシップ"),
        "opens_month": 4, "prepare_lead": 1, "certain": False,
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
        "opens_month": 12, "prepare_lead": 1, "certain": False,
        "url": "https://faam.city.fukuoka.lg.jp/residence/requirement/",
        "gives": _t(
            "A museum-hosted residency ending in an exhibition. Built for artists working across Asia — neither residence nor nationality restricted.",
            "由美术馆主办、以展览收尾的驻地项目。专为在亚洲各地创作的艺术家而设——不限居住地与国籍。",
            "美術館主催、展示で締めくくるレジデンス。アジアを横断して制作する作家のための枠——居住地も国籍も不問。"),
        "prepare": _t(
            "The two-city practice is the application — say what moving between them does to the work.",
            "往返两座城市的创作本身就是申请内容——说清楚在两地之间移动对作品做了什么。",
            "二都市をまたぐ制作そのものが申請内容——行き来が作品に何をしているかを書く。"),
    },
    {
        "id": "tabf",
        "name": _t("Tokyo Art Book Fair", "东京艺术书展 TABF", "東京アートブックフェア"),
        "opens_month": 4, "prepare_lead": 3, "certain": False,
        "url": "https://tokyoartbookfair.com/en/about/",
        "gives": _t(
            "A booth in the printed-matter world you already come from — zines, artist books, and the people who buy them.",
            "在你本来就来自的那个印刷品世界里有一个展位——zine、艺术家书，以及会买它们的人。",
            "もともとあなたがいる印刷物の世界でのブース——zine、アーティストブック、そしてそれを買う人たち。"),
        "prepare": _t(
            "Something printed and finished. Three months is the production time, not the paperwork.",
            "一件印好、做完的东西。三个月说的是制作时间，不是填表时间。",
            "刷り上がった一冊。3か月は制作にかかる時間で、書類の時間ではない。"),
    },
]

# Rolling doors have no window to wait for — they are always open, which makes
# them the answer to "what can I do in a month when nothing else is."
ALWAYS_OPEN = [
    {
        "id": "greenshields",
        "name": _t("Elizabeth Greenshields Foundation", "Elizabeth Greenshields 基金会", "エリザベス・グリーンシールズ財団"),
        "url": "https://www.elizabethgreenshieldsfoundation.org/",
        "gives": _t(
            "Built for exactly this: representational painting, ages 18–41, students explicitly eligible, and no citizenship or residency requirement at all.",
            "几乎是为你这种情况设的：具象绘画，18–41 岁，明确接受学生申请，且完全没有国籍或居住地要求。",
            "まさにこの条件のための助成：具象絵画、18〜41歳、学生も明確に対象、国籍も居住地も問わない。"),
        "prepare": _t("Rolling — there is no date to miss.", "常年接受申请——没有会错过的截止日期。", "通年受付——逃す締切がない。"),
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


def build(today: Optional[date] = None) -> dict:
    """The next twelve months of doors, ordered by how soon each opens.

    `months_away` and `preparing_now` are derived here rather than stored, so
    the calendar re-sorts itself as the year turns and never needs regenerating.
    """
    today = today or date.today()

    def next_occurrence(opens_month: int, rounds_per_year: Optional[int]) -> date:
        # A door with several rounds a year does not wait twelve months. Arts
        # Council Tokyo runs three rounds, so its real gap is four months — an
        # annual model put it eleven months out while a round was closing in
        # twenty days, which is exactly the kind of miss this file exists to
        # prevent.
        step = max(1, 12 // rounds_per_year) if rounds_per_year else 12
        m = opens_month
        while m < today.month:
            m += step
        if m > 12:
            return date(today.year + 1, ((m - 1) % 12) + 1, 1)
        return date(today.year, m, 1)

    def open_right_now(opens_month: int, rounds_per_year: Optional[int], window: int) -> bool:
        # A call that opened last month and runs for a few weeks is OPEN, not
        # "eleven months away" — and an open door outranks every future one.
        step = max(1, 12 // rounds_per_year) if rounds_per_year else 12
        m = opens_month
        while m + step <= today.month:
            m += step
        return m <= today.month < m + window

    upcoming = []
    for d in DOORS:
        when = next_occurrence(d["opens_month"], d.get("rounds_per_year"))
        months_away = (when.year - today.year) * 12 + (when.month - today.month)
        is_open = open_right_now(d["opens_month"], d.get("rounds_per_year"), d.get("window_months", 1))
        if is_open:
            months_away = 0
        upcoming.append({
            "open_now": is_open,
            "id": d["id"],
            "name": d["name"],
            "url": d["url"],
            "gives": d["gives"],
            "prepare": d["prepare"],
            "opens_month": d["opens_month"],
            "opens_year": when.year,
            "months_away": months_away,
            # Inside the run-up: close enough that the preparation is the work.
            "preparing_now": months_away <= d["prepare_lead"],
            "prepare_lead": d["prepare_lead"],
            "certain": d.get("certain", False),
            "rounds_per_year": d.get("rounds_per_year"),
            "amount_jpy": d.get("amount_jpy"),
            "amount_in_kind": d.get("amount_in_kind", False),
            "in_paintings": _in_paintings(d.get("amount_jpy")),
        })

    upcoming.sort(key=lambda x: (not x["open_now"], x["months_away"], x["name"]["en"]))
    return {
        "generated_for": today.isoformat(),
        "doors": upcoming,
        "always_open": ALWAYS_OPEN,
        "preparing_now_count": sum(1 for x in upcoming if x["preparing_now"]),
        "open_now_count": sum(1 for x in upcoming if x["open_now"]),
    }
