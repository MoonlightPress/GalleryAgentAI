# Design — Saffron's career trio: the record, the doors, the roads

**Date:** 2026-09-04 · **Status:** design only, no code changed
**Scope:** `CareerPosition`, `CareerReadiness`, `LongTermScenarios` — `frontend/src/components/SaffronPage.jsx`
**Builds on:** `reports/weekend_site_solutions_2026-09-03.md` (structure), `reports/weekend_advice_research_2026-09-04.md` (named targets, all confidence-tagged), `reports/weekend_prose_review_2026-09-04.md` (voice).
**Does not redo:** the redundancy census, the target research, or the line-level prose fixes. Where this doc quotes a target, the source and confidence tag live in the research report.

The mandate: *"Right now everything is very generic and hedging. We want to turbo charge this girl's art career. She's seen the broad version. Let's get specific."*

The test applied to every drafted line below: **could this sentence appear in an artist-career blog post?** If yes, it was cut and rewritten. The material that survives is material that requires knowing that she is a 26-year-old Chinese citizen, resident in Tokyo, enrolled as a student, with N2 Japanese, ~27k Instagram followers, five and a half years of daily watercolors, three self-funded solos, two Chinese museum group shows, and one book from 2021.

---

## 1. Lane assignment

### The recommendation

| Component | Tense | Owns | Never contains |
|---|---|---|---|
| **`CareerPosition`** → *Your record* | **Past** | Every confirmed fact, **and what those facts are already worth**: the CV as it should be written, which credits lead, what her three solos are and are not, and the eligibility/leverage combination her passport + visa + language + student status + audience produce. | Any sentence about what to do next. |
| **`CareerReadiness`** → *The next doors* | **Present** | The one lever, its named targets, the eligibility line per target, the near dates, and — new — **exactly what to send and how to send it**. | Any restatement of the record beyond a single evidence clause; any "over the next few years". |
| **`LongTermScenarios`** → *Three roads* | **Future** | The choice between gallery, book, and both — each road with its own next twelve months, its own hard part, and a way for her to say which one is hers. | Any hard date that also appears in *The next doors*; any "what's blocking now". |

And, on the other tab, one consequential yielding:

> **`StrategicPathway` stops narrating the next step and becomes the map.** It absorbs the only non-duplicate thing `CareerDependencyMap` had — how one door leads to another — and `CareerDependencyMap` is cut. Pathway keeps the ladder and the ShyTips; it loses `blocking_now` and `next_move`, which are `CareerReadiness`'s by lane.

### Where this agrees with Approach B, and the one place it doesn't

Approach B's skeleton is right and I adopt it: past / present / future, one owner each, nothing new built, Unlock Tree cut. Its instrumentation fix (fire on `SectionShell` open) has already landed as `trackId` — `career_position`, `career_readiness` and `long_term_scenarios` all track opens now.

**I reject one move: B folds the `blocking_gaps` into `CareerPosition` as ○ "not yet on record" rows and shrinks `CareerReadiness` to a small "Within reach" list of two columns.** Three reasons.

1. **It puts the best material in the app behind the wrong door.** The seven levers now carry 26 researched, named, dated, linked targets with per-target eligibility. That is the app's single most valuable payload. `CareerPosition`'s subtitle is literally "confirmed facts only" — a panel that promises facts cannot be the one that hands her `works@gallerykogure.com`.
2. **A record that argues stops being a record.** The ✓ / ○ list makes "no representation" a row in her own exhibition history. Her record is hers; a door she hasn't walked through is not a missing line in it. The warmth risk B itself flags ("must never read as a deficit list") is not a styling problem, it's structural.
3. **B leaves the present homeless in practice.** Under B the next step lives on `StrategicPathway`, one tab away, in a component that has no targets, no eligibility, no correction form and no deadline awareness. The engine data would have to be duplicated there — the exact failure mode both prior reports diagnosed.

**What I take from B instead:** the *deletion* half. `careerStatusLine`'s closing clause, `CAREER_SYNOPSIS`'s forward paragraph, and `_solo_bottleneck` inside Gallery Track all still cross lanes and all still go.

### Display order on the profile tab

Lanes are about **ownership**, not reading order. Reading order is decided separately, by CLAUDE.md's "actionability is the product":

1. **The next doors** — first, default open. A section whose collapsed summary can say *"Arts Council Tokyo has 20 days left"* must not be behind a click.
2. **Your record** — second, collapsed, with a summary line that earns the open ("the six lines worth leading with are picked out").
3. **Three roads** — third, collapsed. **Moved here from the strategy tab**, so the trio actually sits together and the strategy tab is left with one job (the map).
4. Benchmarks / Peers / Momentum — unchanged, below.

This is also the current order for 1 and 2, so the layout risk is confined to moving `LongTermScenarios` across tabs.

### Every currently visible field has a home

| Currently rendered | Home |
|---|---|
| `CAREER_SYNOPSIS` (static) | **Deleted.** Its factual half becomes `record_summary_line` (engine); its forward half is Pathway's and Readiness's. |
| `careerStatusLine` full sentence | Stays in **Your record** as one evidence line; the closing "what's next" clause is dropped (Readiness owns it). |
| `MilestoneMarker` ×3 (IG / shows / pubs) | **Your record**, unchanged. |
| exhibitions ✓ rows, publications ✓ rows, audience row | **Your record**, unchanged, plus the new CV/solo/eligibility disclosures beneath. |
| `AddShowInline` | **Your record**, unchanged. |
| `next_unlock` card (gap / detail / action / targets / hint) | **The next doors**, unchanged shape, plus the outreach kit disclosure. |
| `GapCorrectionForm`, `ReadinessCorrection` | **The next doors**, unchanged. |
| "N more directions" collapse + other gaps | **The next doors**, unchanged. |
| `CadenceTip` | **The next doors**, unchanged (it is a present-tense rhythm, not a record fact). |
| `immediate_priorities` — the "Now" column | **Cut from Saffron.** It is Mochi's page, already. Stays in `career_strategy_report.json` for engines. |
| `build_toward` / `watch_list` — "Getting closer" / "Keep an eye on" | **The next doors**, moved behind one disclosure so the outreach kit gets the vertical space. |
| Scenario cards ×3, `saffron_view` | **Three roads**, moved to the profile tab. |
| `CareerDependencyMap` | **Cut** (as B recommends). Its "unlocks" logic moves into Pathway's step details. |
| Pathway `blocking_now` / `next_move` | **Cut from Pathway.** One copy, in The next doors. |

---

## 2. Section design — *The next doors* (present)

Component: `CareerReadiness`. Title change per the prose review: `sf.cr.title` 职业准备度 → **接下来的门 / The next doors**; `sf.cr.subtitle` → 你走到了哪里，下一步通向哪里 / *Where you are, and where the next step leads.*

### 2.1 Visible by default

**a. The collapsed summary becomes the nearest real date.** Today the summary is `careerStatusLine` — the same sentence as the body's first line, and a sentence about the past. Replace with `soonest_door_line`, computed every regeneration from the nearest future `window_date` across all levers' targets.

> **zh** 东京艺术委员会的申请还剩 20 天 · TOKAS 的驻地征集这两周开放
> **en** Arts Council Tokyo has 20 days left · TOKAS's residency call opens within two weeks

Fallback when nothing is inside 45 days (the line must never invent urgency):

> **zh** 最近的一扇门在 12 月：biscuit gallery 的 grid next，免费，学生也能投。
> **en** The nearest door is in December: biscuit gallery's grid next — free to enter, students welcome.

**b. One evidence line, then straight to the door.** `careerStatusLine` keeps its record clause and loses its forward clause:

> **zh** 8 场联展、3 场个展、海外的展出——这早就不是起点了。
> **en** Eight group shows, three solos, a showing abroad — this stopped being a beginning a while ago.

**c. The next-step card**, unchanged in shape (`gap` / `detail` / `action` / `TargetsList` / hint / `GapCorrectionForm`). The engine's current copy for `gallery_representation` already passed the prose review; leave it.

**d. New — the eligibility line inside each target row.** `TargetsList` gains one line under `why`, rendered in a smaller, warmer weight. This is the highest specificity-per-character material in the design: it is impossible to write without knowing her passport, her visa, her enrolment and her age.

| Target | `eligibility_zh` | `eligibility_en` |
|---|---|---|
| Arts Council Tokyo Startup Grant | 只看是否住在东京，不问国籍——你符合；申请的正是你今年已经做过的事。 | Tokyo residence, no nationality clause — you qualify, and it funds exactly what you already did this year. |
| Elizabeth Greenshields | 18–41 岁、画具象、学生明确可以——三条你全中，而且没有截止日期。 | 18–41, representational painting, students explicitly eligible — all three are you, and there's no deadline at all. |
| TOKAS-Emerging | 住在日本即可，不限国籍，35 岁以下——你 26 岁，条件全满足；2026 年入选的六人里有两位中国艺术家。 | Japan-resident, nationality unrestricted, under 35 — you're 26 and clear on all of it; two of the six chosen in 2026 were Chinese artists. |
| TOKAS Local Emerging Creator Residency | 「日本国内在住（国籍不問）」——这一行几乎是照着你的情况写的。 | "Resident in Japan, nationality unrestricted" — that clause reads as if it were written for you. |
| Asian Cultural Council | 凭中国国籍走中国大陆通道，住在东京不影响。唯一要看的是"五年专业经历"——你从 2021 年算起，刚好在边上。 | Your Chinese citizenship opens the Mainland China track; the Tokyo address doesn't matter. The one thing to check is the five-years-professional rule — counting from 2021, you're right on the line. |
| Art Center NEW (New New Artists) | 35 岁以下，免费投，但全程用日语——你的 N2 够用。 | Under 35, free to enter, conducted in Japanese — your N2 covers it. |
| biscuit gallery — grid next | 免费、40 岁以下、学生可投。 | Free, under 40, students accepted. |
| HB Gallery FILE competition | 没有任何资格限制——年龄、国籍、学历都不问。 | No eligibility restriction at all — not age, not nationality, not enrolment. |
| Holbein Scholarship | 住在日本即可，不问国籍；办这个奖的就是做水彩颜料的公司。 | Residence in Japan, no nationality clause — and the company behind it makes watercolor paint. |

**e. New — the outreach kit.** A `ShyTips`-pattern disclosure directly under the action line, toggle label **具体怎么写这封信 ▾ / What to actually send ▾**. This answers the brief's "what a Tokyo gallery actually wants to see in a first email."

Opening line (visible when opened):

> **zh** 东京的画廊不设投稿箱，但这不代表不能写信。写得对的第一封信很短——看过他们的展、三句话说清你是谁、一个链接、五张画。下面这封可以直接改名字用。
> **en** Tokyo galleries don't run submission boxes, but that doesn't mean you can't write. A first email that works is short — you saw their show, three sentences on who you are, one link, five paintings. The draft below only needs the name changed.

Then the drafted Japanese email (she works in Japanese; the ZH beneath is a gloss, not a second version):

```
件名：作品を見ていただけますでしょうか — 水彩・GEGYjiji

ギャラリー小暮 ご担当者様

はじめまして。東京で水彩を描いております GEGYjiji と申します。
先日「A Little Gem」を拝見し、紙の小さな作品を大切に扱われる場だと感じ、
ご連絡いたしました。

2020年から毎日一枚の水彩を描き続けており、東京の室内や街角、
光と猫を主題にしています。今年8月には原宿の Galerie LE MONDE で
個展を開催、これまでに上海と東京で個展を3回、天津・台州の美術館での
グループ展にも参加しました。Instagram（@gegyjiji）では
約2.7万人の方にご覧いただいています。

作品5点を下記にまとめております。
もしご興味をお持ちいただけましたら、実物をお持ちして
ご覧いただければ幸いです。

［リンク］

GEGYjiji
@gegyjiji
```

The rules beneath it, as bullets — each one is a real Tokyo-gallery convention, not general email advice:

> **zh**
> • 附件不要超过一封信能装的量——放一个链接（Instagram 或一个网页相册），别塞五个 JPG。
> • 五张，一个系列，不要选集锦。他们要判断的是你能不能撑起一面墙，不是你会画多少种东西。
> • 一定要提到你看过他们的哪一场展。这一句是整封信里唯一无法伪造的部分，也是他们唯一会读两遍的地方。
> • 不要问"能不能给我一次个展"。第一封信只问一句：能不能看一下。
> • 十天没有回音就当作没看到，不是拒绝。三个月后他们下一场展开幕时再写一次，那时你已经是"来过两次的人"。
> • 尺寸和价格先不写。等他们回信问了再说——先问价格会把信变成一份报价单。
>
> **en**
> • Don't attach more than an email should carry — one link (Instagram, or one web album), not five JPGs.
> • Five images, one series, never a greatest-hits mix. What they're judging is whether you can hold a wall, not how many things you can paint.
> • Always name which of their shows you went to. It's the one sentence in the email that can't be faked, and the one they'll read twice.
> • Don't ask for a solo show. A first email asks one thing: will you look.
> • No reply in ten days means unseen, not refused. Write again three months later when their next show opens — by then you're someone who has been twice.
> • Leave out sizes and prices. Wait until they ask, or the email turns into a quote sheet.

**Why this belongs to Readiness and not Peppercorn:** it is not a question to her and not a record of her — it is the content of the present step, and the present step is this lane's whole job.

### 2.2 Behind a disclosure

- **其他方向 / More directions** — the remaining six levers (`otherGaps`). Unchanged mechanism, unchanged copy.
- **正在靠近 / 留意 — Getting closer / Keep an eye on** — the two remaining opportunity columns, now folded into one collapsible so the outreach kit sits above the fold. Toggle: **还有 {n} 个在路上 ▾ / {n} more on the way ▾**.
- **The "Now" column is gone.** It is Mochi's, and CLAUDE.md is explicit that Saffron describes rather than advises the day.

### 2.3 One engine correction this section depends on

`_next_tier_levers()` gates `solo_venue_quality` behind `if solo_shows < 3:`. She has three, so **the lever most relevant to her right now never fires.** The gate is also measuring the wrong thing — the count isn't the issue, the venue model is. Replace with `if not has_curated_solo:` (see §5, `_solo_venue_kind`). Until that lands, the whole solo-venue design in §3.3 has no data path.

---

## 3. Section design — *Your record* (past)

Component: `CareerPosition`. Title `sf.sec.careerPosition` 职业定位 → **你的履历 / Your record**. Subtitle → **已经在册的一切，以及它现在能替你换来什么 / Everything already on record — and what it can get you now.**

That subtitle is the whole upgrade in one line. The section stops being a list she already knows and becomes the place she goes when she has to *use* her record: filling a form, writing a CV, deciding whether she's eligible.

### 3.1 Visible by default

**a. Collapsed summary** (`record_summary_line`, engine-computed):

> **zh** 8 场联展、3 场个展、2 场美术馆群展、1 本作品集——写履历时该领头的六行，山楂挑好了。
> **en** Eight group shows, three solos, two museum group shows, one book — the six lines worth leading with are picked out.

**b. The synopsis replaced.** `CAREER_SYNOPSIS` is hardcoded, still, and its second half is forward-looking (other lane). Replace with a live, past-tense paragraph — `record_synopsis`, built from `career_evidence` + `diary_scale`:

> **zh** 从 2020 年到现在，每天一张水彩，五年多没有断过。这些画长成了《Colour Diary》，长成了上海和东京的三场个展，长成了天津和台州两家美术馆的群展。你的履历不是一份计划，是已经发生过的事。
> **en** Since 2020, one watercolor a day, five and a half years without a break. Those paintings became *Colour Diary*, became three solo shows in Shanghai and Tokyo, became group exhibitions at two museums in Tianjin and Taizhou. Your record isn't a plan — it's a list of things that already happened.

**c. Markers, exhibition rows, publication rows, audience row, `AddShowInline`** — all unchanged.

### 3.2 Disclosure — *能直接用的履历 / Your CV, ready to use*

Toggle: **能直接复制的履历 ▾ / Copy-ready CV ▾**

This answers "which of her existing group shows are the CV lines worth leading with and which to drop." Japanese convention (year / title / venue, city), because that is the form every target in §2 asks for.

Intro line:

> **zh** 十二条履历，一次全放上去反而没人读。这六行是有分量的——美术馆、个展、被点名策划的群展。其余的合成一行，一样是真的，只是不必抢位置。
> **en** Twelve credits, and putting all twelve on the page is how none of them get read. These six carry weight — museums, solos, a named curated group show. The rest go in one line at the bottom; just as true, just not competing for the top.

**领头的六行 / The six that lead:**

```
2026  個展「Light and Shadows and Cats」Galerie LE MONDE（東京・原宿）
2026  個展「永遠の昨日」月画廊（東京）
2025  個展「和光和影和猫」77ART（上海）
2024–25  「生活在別処」棉美術館（天津）
2024–25  「PiPa 生長的聲音」横渡美術館（台州）
2023  「Tide from China Part1」ACG_Labo（東京・原宿）
2021  『Colour Diary』刊行（初の個人作品集）
```

**合成一行 / The sweep line:**

```
ほか、広州・深圳・杭州・南京・ロンドンでのグループ展（2021–2025）
```

The per-line reasoning, as small notes beside each (this is the part no blog post could write):

> **zh**
> • 两家美术馆放在个展下面，是因为在日本的申请表上，"美術館" 这两个字比场地大小更管用——它证明有机构替你做过判断。
> • 「Tide from China Part1」留着，不是因为 2023 年多重要，而是因为那是有人策划、点名邀请的群展，还有五位同场艺术家的名字可以查。租来的场地做不到这一点。
> • 伦敦那场（Scribbles Winter Wonderland，2025）留在最后那一行里。它不适合领头，但奖助表格上问"是否有海外展出经历"的时候，它就是那个"是"。别删。
> • 广州「你好春天」、深圳「魔女的盛宴3」、南京「本该如此」都是好事，但它们和 2026 年的东京个展放在同一页上，会把整份履历往回拉五年。
>
> **en**
> • The two museums sit under the solos because on a Japanese application form the word 美術館 does more work than venue size — it's proof an institution made a judgement about you.
> • "Tide from China Part1" stays, not because 2023 matters, but because it was curated, invited, and has five named co-exhibitors anyone can look up. A rented room can't say that.
> • London (Scribbles Winter Wonderland, 2025) stays in the sweep line. It shouldn't lead — but when a grant form asks whether you've exhibited internationally, that show is the yes. Don't delete it.
> • Guangzhou, Shenzhen and Nanjing were all good. On the same page as a 2026 Tokyo solo, they pull the whole record back five years.

**One ambiguity the engine should surface rather than guess:** 「視線」(软果银, Hangzhou, Mar–May 2021) is recorded with type "group/solo not specified". If it was a solo, it's a fourth solo and belongs above the sweep line. This becomes a Peppercorn question, not a Saffron assertion:

> **zh (胡椒粒)** 2021 年杭州软果银那场「視線」，是个展还是联展？山楂想把它放对位置。
> **en (Peppercorn)** The 2021 show at 软果银 in Hangzhou — "Line of Sight" — was that a solo or a group show? Saffron wants to file it in the right place.

### 3.3 Disclosure — *三场个展，和第四场会不一样在哪 / Your three solos, and how a fourth could differ*

Toggle: **关于这三场个展 ▾ / About the three solos ▾**

This answers "what separates her three pay-to-exhibit solos from a curated one and precisely what closes that gap." The prose review's rule holds: **honour the three first, the rental point second.**

> **zh** 三场个展，每一场都是你自己谈下来、自己付钱、自己布起来的。这件事本身很难，很多人一场都没做成。接下来会不一样的，是让场地反过来为展览付钱——这不是"更好的展"，是另一种性质的展：有人替你选、替你宣传、替你留下画册。
> **en** Three solos, each one you arranged, paid for and installed yourself. That is hard, and plenty of people never manage one. What would be different next is a venue that pays for the show instead of the other way round — not a better show, a different kind of show: someone else chooses you, publicises it, and leaves a catalogue behind.

Then the comparison, as two short columns:

| | **你走过的路 / What you've done** | **第四场可以是 / What a fourth could be** |
|---|---|---|
| 谁付钱 · Who pays | 你付场租（月画廊约 ¥100,000／5天；Galerie LE MONDE 12 天的个展约 ¥374,000） | 场地付制作费（TOKAS-Emerging ¥150,000；OPEN SITE ¥400,000；京都艺术中心最高 ¥1,000,000） |
| 谁选的 · Who chose | 你申请，他们接受 | 评审从几百份里选出几个（2026 年 TOKAS-Emerging：186 投 6 中） |
| 展完留下什么 · What's left after | 你自己的照片 | 画册、新闻稿、机构官网上的一页存档 |
| 履历上怎么读 · How it reads on a CV | 「個展」 | 「個展（東京都〇〇公募選出）」 |

And precisely what closes it — the three doors, with what each asks for **first**:

> **zh**
> • **TOKAS-Emerging**（住在日本即可、不限国籍、35 岁以下）——下一轮 2027 年 6–7 月。第一步问的是一份个展提案：你想做的那个展，如果有制作经费的话。
> • **SICF（青山 Spiral）**——大奖是在 Spiral 中庭办个展，加 ¥500,000 制作费。征集大约 11 月开。第一步问的是十张能挂成一个展位的画。
> • **Shibuya Hikarie 8/CUBE**——付费，但要过委员会评审，在车站上方，107 平米。2026 年秋天会开下一轮。这是"付费"和"被选中"之间的那一级台阶。
>
> 三个入口问的第一样东西，其实是同一样：一份提案，和十张挂在一起说得通的画。先做那个，三扇门就同时准备好了。
>
> **en**
> • **TOKAS-Emerging** (Japan resident, any nationality, under 35) — next call June–July 2027. What it asks for first is a solo proposal: the show you'd make if the production money existed.
> • **SICF (Spiral, Aoyama)** — the Grand Prize is a solo in Spiral's Atrium plus ¥500,000. Call opens around November. What it asks for first is ten paintings that would hang together as one booth.
> • **Shibuya Hikarie 8/CUBE** — paid, but committee-screened, above the station, 107 m². Next call autumn 2026. It's the step between paying and being chosen.
>
> All three ask for the same thing first: a proposal, and ten paintings that make sense side by side. Make that once and three doors are ready at the same time.

### 3.4 Disclosure — *只有你手上有的这套条件 / The combination only you have*

Toggle: **你符合的条件比你想的多 ▾ / You qualify for more than you'd think ▾**

This answers the brief's "how her Chinese citizenship + Tokyo residence + N2 + ~26k Instagram combine into eligibility and leverage most artists don't have." It is the single strongest turbo-charge in this design, because it is *pure* specificity: every line is unwritable without her file.

> **zh** 中国国籍、住在东京、还在念书、日语 N2、两万七千人在看你画画——这五件事分开看都平常，凑在一起就打开了一批别人进不去的门。山楂把它们对着申请条款一条条查过了。
> **en** A Chinese passport, a Tokyo address, still enrolled, N2 Japanese, and twenty-seven thousand people watching you paint. Ordinary one at a time; together they open a set of doors most people can't reach. Saffron checked each of them against the actual eligibility clauses.

**中国国籍 / Chinese citizenship**
> **zh** 亚洲文化协会（ACC）的中国大陆通道认的是国籍，不是住址——住在东京完全不影响，最高 35,000 美元，10 月 1 日开放。中文媒体那边你也是"旅日华人青年艺术家"这个身份，《艺术新闻／中文版》和《Hi 艺术》都写这类人。
> **en** The Asian Cultural Council's Mainland China track goes by citizenship, not address — living in Tokyo changes nothing. Up to US$35,000, opens October 1. It also gives you a name Chinese-language press already publishes: a young Chinese artist based in Japan. TANC and Hi艺术 both run that story.

**住在东京 / A Tokyo address**
> **zh** 这一条比国籍还管用。TOKAS 的两个驻地写的是「日本国内在住（国籍不問）」——住在日本就行，护照不问。东京艺术委员会的扶持金也只看住在不在东京，最高 30 万日元，9 月 24 日截止。ホルベイン 的画材奖学金同样只要求住在日本。
> **en** This one does more work than the passport. Both TOKAS residencies say 日本国内在住（国籍不問） — resident in Japan, passport not asked. Arts Council Tokyo's grant also only checks whether you live in Tokyo: up to ¥300,000, closing September 24. Holbein's materials scholarship, same clause.

**日语 N2 / N2 Japanese**
> **zh** 横滨 Art Center NEW 的公募全程用日语，35 岁以下、免费投，大奖是展览加 20 万日元报酬——N2 足够填表和面谈。这一条也是画廊开幕式上真正起作用的东西：东京的画廊不看投稿箱，看的是见过面的人。
> **en** Art Center NEW in Yokohama runs entirely in Japanese — under 35, free to enter, Grand Prix is an exhibition plus a ¥200,000 fee. N2 covers the form and the conversation. It's also what actually works at an opening: Tokyo galleries don't read submission boxes, they remember people they've met.

**还在念书 / Still a student**
> **zh** 学生身份在这里是加分不是减分。加拿大的 Elizabeth Greenshields 基金会明确写着学生可以申请，画具象、18–41 岁，没有截止日期——你三条全中。biscuit gallery 的 grid next 也收学生。要留意的只有一条：Pollock-Krasner 不收在读学生，那个等毕业再说。
> **en** Being enrolled counts for you here, not against you. Canada's Elizabeth Greenshields Foundation says students are eligible in so many words — representational painting, 18–41, no deadline. All three are you. biscuit gallery's grid next takes students too. Only one to note: Pollock-Krasner excludes enrolled students, so that one waits until you've graduated.

**26 岁 / Twenty-six**
> **zh** 35 岁以下、40 岁以下这类门槛，现在全部对你开着——TOKAS-Emerging（35以下）、Art Center NEW（35以下）、grid next（40以下）、Greenshields（18–41）。这不是永远的。
> **en** Every under-35 and under-40 gate is open to you right now — TOKAS-Emerging, Art Center NEW, grid next, Greenshields. That isn't permanent.

**两万七千人 / Twenty-seven thousand**
> **zh** Kaikai Kiki 现在这场展，十二位艺术家是从 Instagram 上找到的，画廊自己写明了这一点。你每天一张、画了五年多的账号，本身就是一扇门——不是"推广渠道"，是被看见的方式。Colossal 的水彩栏目要的正好是这种故事。
> **en** Kaikai Kiki's current show is twelve artists they found on Instagram — the gallery says so itself. An account that has posted one painting a day for five and a half years is a door in its own right, not a marketing channel. Colossal's watercolor desk wants exactly that story.

**不用看的三个 / Three you can stop looking at**
> **zh** 三个日本的老牌海外研修奖助——ポーラ、吉野石膏、文化庁——都要求日本国籍或永住。它们经常被推荐给在日本的艺术家，但对你是关着的。知道这一点，比反复研究要省时间。
> **en** Three well-known Japanese overseas-study grants — Pola, Yoshino Gypsum, and the Agency for Cultural Affairs — all require Japanese nationality or permanent residency. They get recommended to artists in Japan constantly; for you they're shut. Knowing that is worth more than researching them twice.

---

## 4. Section design — *Three roads* (future)

Component: `LongTermScenarios`. Title `sf.sec.longTerm` 长期路径 → **三条路 / Three roads**. Subtitle → **接下来几年可以往哪走——选哪条由你 / Where the next few years can go — the choice is yours.**

Names, per the prose review: **画廊这条路 / The gallery road**, **书这条路 / The book road**, **两条一起走 / Both at once**. Labels: `sf.label.bottleneck` 瓶颈 → **难处在于 / The hard part**; `sf.label.rightIf` 适合条件 → **适合你，如果 / Yours if**.

Collapsed summary (replacing `3 paths · The next few years`, which says nothing):

> **zh** 画廊、书、或者两条一起走 — 选哪条由你
> **en** Gallery, book, or both at once — yours to choose

### 4.1 Visible by default, per card

Name · tagline · fit label · description · `requires_now` — all as now, with these copy changes:

**画廊这条路 / The gallery road** — `bottleneck` stops being `_solo_bottleneck` (that sentence is Readiness's, three times over) and becomes road-specific:

> **zh 难处在于：** 东京的画廊不看投稿，看人。这条路是最慢的，因为它要花的不是时间也不是钱，是反复出现——去开幕、被记住、第二次去的时候他们已经认得你。
> **en The hard part:** Tokyo galleries don't read submissions, they read people. This is the slow road, and what it costs isn't time or money — it's showing up repeatedly, until the second visit is to someone who already knows your face.

**书这条路 / The book road** — the current bottleneck says the diary "just needs packaging", which the prose review flagged as reductive:

> **zh 难处在于：** 画不缺——五年多的日记全在那里。缺的是一个顺序：哪一张排在哪一张后面，一本书才有走完的感觉。这件事只能你自己做，别人替不了。
> **en The hard part:** The paintings aren't the problem — five and a half years of diary are already there. What's missing is a sequence: which page follows which, so the book has somewhere to arrive. Nobody can do that part for you.

**两条一起走 / Both at once** — `best_fit_signal` keeps its line ("the daily diary is simultaneously publication material and gallery-worthy work"), which the prose review called the one that sees her.

`saffron_view`, rewritten off the "it's not A, it's B" construction:

> **zh** 这是三个方向，选哪个由你。想两条都要，那就让它们互相喂养——一场在书店画廊的展，一步就同时推进两边。
> **en** Three directions, and the choice is yours. If you want both, let them feed each other — a bookshop-gallery show moves both at once.

### 4.2 Disclosure — *这条路的下一年 / What the next twelve months look like on this road*

Toggle per card: **这一年具体是什么样 ▾ / The next twelve months ▾**

This is where the future stops being abstract. Each road gets three to four named, dated moves — drawn from the same target pool as Readiness but **filtered by road and stated without repeating Readiness's near dates as urgency**. Readiness says "20 days left"; here the same door is a milestone on a route.

**画廊这条路 / The gallery road**
> **zh**
> 9月 · 东京艺术委员会的扶持金——申请里要写的那份展览计划，之后三个投稿都能用。
> 10月 · Independent Tokyo 开征集。二十到三十位画廊主会到现场看，这是他们公开承认在找人的地方。
> 11月 · SICF 开征集。大奖是 Spiral 中庭的个展。
> 12月 · biscuit gallery 的 grid next——免费，去年的获奖者后来进了 Kaikai Kiki 的展。
> 一整年只需要准备一样东西：十张挂在一起说得通的画，和一段说明。四个入口问的都是它。
>
> **en**
> September · Arts Council Tokyo's grant — the exhibition plan you write for it will serve three later applications.
> October · Independent Tokyo opens. Twenty to thirty gallerists judge on the floor; it's the one place they publicly admit to scouting.
> November · SICF opens. The Grand Prize is a solo in Spiral's Atrium.
> December · biscuit gallery's grid next — free, and last year's winner ended up in a Kaikai Kiki show.
> The whole year needs one thing prepared: ten paintings that hang together, and a paragraph about them. All four doors ask for that.

**书这条路 / The book road**
> **zh**
> 秋天 · MOUNT ZINE 的秋季招募——不收费，不评审，放上去就在架上。
> 随时 · 给 Colossal 写信（submissions@thisiscolossal.com）：把日记说成一件事——从哪一年开始、为什么每天、一共多少张。附六张图。
> 冬天 · 把 2021 年之后的画按季节排一遍。这是第二本书唯一真正的工作量。
> 春天 · Tokyo Art Book Fair 的申请通常这时候开。
>
> **en**
> Autumn · MOUNT ZINE's autumn intake — no fee, no screening; put it in and it's on the shelf.
> Any time · Write to Colossal (submissions@thisiscolossal.com). Describe the diary as one thing — when it started, why every day, how many by now. Six images.
> Winter · Sequence everything painted since 2021 by season. That's the only real labour in a second book.
> Spring · Tokyo Art Book Fair applications usually open.

**两条一起走 / Both at once**
> **zh**
> 这两周 · TOKAS 的驻地征集会开。这一个同时算在两条路上：墨田的工作室是画画的时间，也是把一本书排完的时间。
> 全年 · 一场在书店画廊的展——UTRECHT 或 Book and Sons——一次同时推进两边。
> 代价是真实的：两条路都走，意味着每一条都比别人慢一点。要不要付这个价，只有你知道。
>
> **en**
> Next two weeks · TOKAS's residency call opens. This one counts on both roads: studio months in Sumida are painting time and book-sequencing time at once.
> All year · One show at a bookshop gallery — UTRECHT or Book and Sons — advances both in a single move.
> The cost is real: walking both means each goes a little slower than it would alone. Whether that's worth paying is yours to know.

### 4.3 The one new feature this design asks for: let her answer

The three roads are a question, and questions belong to Peppercorn. Right now the app asks it and then forgets, so every regeneration re-hedges across all three. One small button per card — **这条路像我 / This one sounds like me** — writing `scenario_lean` into `memory/peppercorn_profile.json`, is what lets the app stop presenting three of everything.

Confirmation copy:

> **zh** 记下了。山楂会往这个方向多看一点——想换随时改。
> **en** Noted. Saffron will look a little harder in that direction — change it whenever you like.

And the downstream effect, stated honestly on the card so it never feels like a trap:

> **zh** 选了之后，麻薯每天挑的三件事会偏向这一边。另外两条路不会消失。
> **en** Once you pick, the three things Mochi lines up each day lean this way. The other two roads don't disappear.

This is the follow-on the prior report called Approach C, and it is the only thing here that adds a feature rather than moving one. It is worth it: it's the mechanism that converts hedging into specificity everywhere else in the app, which is the mandate.

---

## 5. Where every piece of data comes from

Per CLAUDE.md's Data Patch Rule, everything derived is named as an engine rule. Nothing below is a hand-patch to a generated JSON file.

### New engine-computed fields

| Field | Computed by | Input | Notes |
|---|---|---|---|
| `window_date` (on each `targets[]` entry) | authored alongside the existing `window` string in `engines/career_strategy_engine.py::_next_tier_levers()` | — | ISO date or `null`. The prose `window` stays; this is the machine-readable sibling everything else sorts on. |
| `soonest_door_line` / `_zh` / `_ja` | **new** `_soonest_door()` in `career_strategy_engine.py` | all levers' `targets[].window_date` | Nearest ≤45 days → the urgency line; else the "nearest door is in {month}" fallback. Recomputed every regeneration, so it can never stale into false urgency (same pattern as the existing `_act_grant_urgency()`). |
| `record_summary_line` / `_zh` / `_ja` | **new** `_record_summary()` in `career_strategy_engine.py` | `career_evidence` + `cv_lead_lines` length | Counts only; no forward clause. |
| `record_synopsis` / `_zh` / `_ja` | **new** `_record_synopsis()` in `career_strategy_engine.py` | `career_evidence`, `diary_scale`, publication titles, museum venue names | Replaces the hardcoded `CAREER_SYNOPSIS` constant, which is **deleted** from `SaffronPage.jsx`. |
| `diary_scale` `{years, started}` | **new** `_diary_scale()` in `career_strategy_engine.py` | `career_history.daily_practice.started` | Emits years elapsed, never a fabricated painting count. |
| `cv_lead_lines` `{lead[], sweep[], ambiguous[]}` | **new** `engines/cv_line_engine.py::build_cv_lines()` | `career_history.exhibitions` + `exhibition_log.json` | Ranks by `venue_weight` (institutional > solo > named-curated group > community group) × recency × city weight; `lead` = top 6, `sweep` = remainder rolled into one localized line, `ambiguous` = entries whose `type` contains "not specified". Runs in the pipeline; writes into `career_strategy_report.json`. |
| `solo_venue_kind` (per solo) + `has_curated_solo` | **new** `_solo_venue_kind()` in `career_strategy_engine.py` | a `VENUE_MODEL` lookup table (`rental` / `vetted_paid` / `curated` / `institutional`), keyed by venue name | Defaults to `unknown` for unlisted venues — **never guesses "paid"**, because calling a real show a rental when it wasn't is the one failure this section cannot survive. Replaces the broken `if solo_shows < 3:` gate. |
| `eligibility` / `_zh` / `_ja` (on each `targets[]` entry) | **new** `engines/eligibility_engine.py::annotate_targets()` | `visual_profile.nationality`, `current_city`, `japanese_proficiency`, `is_student`, `age`, `social_presence.instagram.followers_approx` matched against a static `ELIGIBILITY_RULES` table (one entry per named program, transcribed from the research report with its confidence tag) | A rule fires only when every clause it names is satisfiable from the profile; an unmatched clause suppresses the line rather than hedging it. |
| `eligibility_profile` `{opens[], closes[], leverage[]}` | same engine, `build_eligibility_profile()` | same inputs | Drives §3.4. `closes[]` is what makes the "three you can stop looking at" block honest. |
| `road` (on each `targets[]` entry) | authored in `_next_tier_levers()` | — | `"gallery"` / `"book"` / `"both"`. |
| `road_next_12_months` (per scenario) | **new** `_road_calendar()` in `api.py`'s scenario block | levers' targets filtered by `road`, sorted by `window_date` | Assembled, not authored — so a closed call drops out of the road calendar automatically. |
| `scenario_lean` | **Peppercorn**, written to `memory/peppercorn_profile.json` by the existing profile POST path | her click | Source/app-state file — hand-editable, no rule needed. Anything derived from it (scoring lean) is an engine rule. |

### Authored static copy (lives in code, not in data)

| Copy | Home |
|---|---|
| The outreach kit — intro, the JA email draft, the six rules | **new** `engines/outreach_kits.py`, keyed by `gap_id`, attached to each lever by `_next_tier_levers()`. Per-gap, so `residency` and `critical_press` can each get their own kit later without touching the component. |
| CV disclosure intro + the four per-line notes | `engines/cv_line_engine.py` (they explain the ranking, so they belong beside it) |
| The paid-vs-curated comparison table and the three-doors paragraph | `engines/career_strategy_engine.py`, inside the `solo_venue_quality` lever |
| §3.4's six eligibility paragraphs + the "three to stop looking at" | `engines/eligibility_engine.py` |
| Road bottlenecks, `saffron_view`, the lean confirmation | `api.py` scenario block (where they already live) |
| Section titles, subtitles, toggle labels, column labels | `frontend/src/i18n/translations.js` — zh / ja / en |

### Existing fields, unchanged

`career_evidence`, `blocking_gaps[]` with `gap`/`detail`/`action`/`targets`, `level.next_unlock`, `build_toward`, `watch_list`, `career_position.exhibitions|publications|social`, `instagram_strategy.strategy` (the cadence tip), and every `_zh`/`_ja` sibling `locF()` already reads.

### Language

ZH is the real copy — the app forces zh on load. Every string above is drafted zh-first with EN as the fallback `locF()` uses when `_zh` is absent. **JA is not drafted here and must not be left to fall through**: `locF()` returns the raw English field when `_ja` is missing, which is exactly the leak the June i18n sweep closed. Every new field needs a `_ja` sibling before it ships, and `test_career_graduated_ladder.py::test_every_graduated_lever_is_localized` should be extended to cover `eligibility`, `outreach_kit` and the new top-level lines, not just `gap`/`detail`/`action`.

---

## 6. What this requires in code

Ordered so each step is shippable on its own.

1. **Fix the dead gate.** `_next_tier_levers()` line ~506: `if solo_shows < 3:` → `if not has_curated_solo:`, with `_solo_venue_kind()` + `VENUE_MODEL` added. Without this the solo-venue lever never fires and §3.3 has no data. *(One function, one table.)*
2. **Add `window_date` + `road` to every existing target** in `_next_tier_levers()`, and write `_soonest_door()`. Unlocks the Readiness summary line and the road calendars.
3. **Delete `CAREER_SYNOPSIS`** from `SaffronPage.jsx` and render `record_synopsis` / `record_summary_line` from the report. Delete the forward clause from `careerStatusLine`.
4. **New `engines/cv_line_engine.py`**, wired into the pipeline; `CareerPosition` gains the CV disclosure (reuse the `ShyTips` shape). Route `cv_lead_lines.ambiguous` into Peppercorn's question list.
5. **New `engines/eligibility_engine.py`** + `ELIGIBILITY_RULES`; `TargetsList` gains a third line (`eligibility`); `CareerPosition` gains the §3.4 disclosure.
6. **New `engines/outreach_kits.py`**; `CareerReadiness`'s next-step card gains the kit disclosure under the action line.
7. **Cut the "Now" column**; fold "Getting closer" / "Keep an eye on" behind one toggle.
8. **Move `LongTermScenarios` to the profile tab**, third position, inside the existing `SectionOpenContext.Provider value={false}`. Rename the three roads, replace the Gallery/Publication bottlenecks, add `road_next_12_months` + its disclosure.
9. **Cut `CareerDependencyMap`** and its `saffron_insights.js` constant; move its "unlocks" phrasing into `pathway.steps[].detail`. Strip `blocking_now` / `next_move` from `StrategicPathway`.
10. **Add the `scenario_lean` button** + the `peppercorn_profile.json` field + the scoring hook that reads it. The only new feature; do it last, and only after 1–9 are stable.
11. **i18n**: new keys for every title, subtitle and toggle above, in zh / ja / en. Extend the localization test to the new lever fields.
12. **Add `career_position` and `long_term_scenarios` to `SECTION_LABELS`** in `engines/visit_tracking.py` so the trio's `trackId` opens are readable next month.

### Two things to verify before shipping copy

- **The Le Monde show's end date** is `reported secondhand, not yet independently verified` in the profile. The CV line above prints it as a 2026 solo; confirm the venue spelling and dates before that string goes to a gallery.
- **ACC's five-years-professional rule** is `inferred` on the citizenship-vs-residence handling. The §2.1 eligibility line says "you're right on the line", which is honest; do not upgrade it to "you qualify" without confirming with ACC.
