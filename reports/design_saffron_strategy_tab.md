# Design — Saffron's strategy tab

**Date:** 2026-09-04 · **Status:** design only, no code changed
**Scope:** the tab `SaffronPage` opens on (`useState('strategy')`) — `StrategicPathway` and `CareerDependencyMap`.
**Builds on:** `reports/weekend_site_solutions_2026-09-03.md` (structure), `reports/weekend_advice_research_2026-09-04.md` (named targets), `reports/weekend_prose_review_2026-09-04.md` (tone).
**Composes with:** the parallel design for the profile-tab trio (`CareerReadiness`, `CareerPosition`, `LongTermScenarios`) — boundary stated in §6.

---

## 1. Verdict on the Career Unlock Tree: **cut it**

I evaluated it independently and land on the same verdict as `weekend_site_solutions`, for two reasons that report did not use — and with a stricter rehoming requirement than "nothing on it needs a new home."

### 1a. It is the app's only *unverified* career surface

`CAREER_DEPENDENCY_MAP` is a hand-authored constant in `frontend/src/data/saffron_insights.js`. It is the one place in the career narrative that never passes through an engine, and it shows. Read against `weekend_advice_research_2026-09-04.md`, it currently tells her:

| The tree says | Reality |
|---|---|
| "Institutional open calls (Shoto Museum, **BankART1929**) on the strength of your record" | BankART Station / KAIKO ceased operating 31 March 2025 |
| "International residency (e.g. **Cité Internationale des Arts**)" | Partner-nomination only; no Tokyo partner found. Kansai residents only via Institut français |
| "**Japan Foundation** / TOKAS / ACC applications are well within reach now" | The Japan Foundation line is unverified; ACC is real but qualifies her *by Chinese citizenship*, which the tree never says |
| "Society membership (e.g. Japan Watercolor Society) — your exhibition record already supports applying" | The real route into Ueno Artist Project runs through 公募団体 membership; JWS itself unverified as an open application |
| "Royal / American Watercolour Society within reach as your record grows" | Tier 4. CLAUDE.md: Tier 4 must never be surfaced as actionable |

So it is not merely a third telling. It is a third telling that contradicts the researched levers rendered one tab over. Two surfaces in the same app now name different doors for the same goal, and the stale one is the prettier of the two.

### 1b. Its structure points backwards, and the one idea worth keeping is misplaced

Twenty of its items are "✓ thing you already did → what that unlocked." That is the *record*, and the record is `CareerPosition`'s job on the profile tab. The forward tiers (`near_term`, `mid_term`, `long_term`) are the levers, and the levers are the engine's job.

The single non-duplicate idea in the whole component is **causation** — that credentials are a graph, not a list; that X changes how Y reads. That idea is genuinely missing from the app and worth keeping. But it does not want to be a section. A separate "how the doors connect" map would re-create exactly the redundancy we're removing: a fourth rendering of the same door list, read at a moment when she isn't deciding anything.

Causation belongs **at the point of decision** — one `leads_to` sentence attached to each move, inside the route. That is strictly better placement, and it costs no section. Plus one paragraph at the head of the route stating the convergence (the thing a map shows that per-item lines can't: that four different doors feed one conversation).

### 1c. Nothing vanishes silently — full disposition

| Currently visible in the tree | New home |
|---|---|
| `now` milestone, 7 × "✓ credential → unlocks" | `CareerPosition` (profile tab) already lists every one of these credentials as a ✓ row. The "unlocks" clauses become §4 S2 "What a gallerist checks" — the same claim, said as evaluation rather than as reward |
| `near_term`: gallery representation → collector network / fair access / someone handles sales | §4 S1 Move 5 `leads_to` + Move 4's closing line on Art Fair Tokyo |
| `near_term`: residency → "TOKAS appropriate to apply to" | §4 S1 Move 3, with the actual eligibility clause and the actual call window |
| `near_term`: grant → "funding for a named project" | §4 S1 Move 1 + §4 S3 item 6 (Nomura's 国際交流 line, named project) |
| `near_term`: society membership | Dropped as a *lever*; the JWS route is unverified. It survives as an engine flag (`jws_membership`) feeding readiness on the profile tab |
| `mid_term`: institutional open calls / international residency / book project | §4 S4 prep windows (Kyoto Art Center, FAAM, KAIR, TOKAS Exchange). The book project is `LongTermScenarios`' road — profile tab, not mine |
| `long_term`: RWS/AWS, licensing income, major press | Tier 4 and money. RWS/AWS: retire (CLAUDE.md forbids surfacing Tier 4 as actionable). Licensing: already a full section on the Money tab. Press: §4 S3 item 7 + the Relationships tab's `PressPitchMap` |
| `sf.depmap.*` i18n keys (zh/ja/en × 8) | Deleted |

**Recommendation:** delete `CareerDependencyMap`, `CAREER_DEPENDENCY_MAP`, and the eight `sf.depmap.*` keys in all three languages. Retire the words 解锁 / 解放 / unlock from the codebase's user-facing surface entirely.

---

## 2. What's wrong with the strategy tab as it stands

`StrategicPathway` is not broken — it is the *right shape for the wrong artist*. It renders an 8-step ladder with five ✓ and three ○. Five of its eight steps are her past. It is 60% a trophy case, and the three open steps are written at the altitude of "Build relationships with commercial galleries whose program fits your work."

Three specific failures:

1. **It answers "how far along am I" — a profile-tab question.** The strategy tab should answer "what happens next, in what order, and what do I do while waiting." The ladder can't: a ladder has no dates, no sequence logic (why step 7 after step 6?), and no notion of preparation.
2. **It has no clock.** Six real deadlines sit inside the next ten weeks (Arts Council Tokyo Sep 24, TOKAS mid-Sep, Asahi Oct 25, Nomura Oct 30, HB FILE mid-Oct, ACC Nov 10) and the tab mentions none. `sf.sub.pathway` says "Estimated timeline: 12–36 months from mid-2026", which is the opposite of a clock.
3. **It does not know she has a show on the wall right now.** `Light and Shadows and Cats`, Galerie LE MONDE, Harajuku, Aug 25 – approx. Sep 6 2026. Today is Sep 4. There are three things possible while a show is hanging and impossible after it comes down, and the app is silent on all three. This is the single most specific, most time-bound fact in her entire record, and no surface uses it.

---

## 3. The design in one line

**The strategy tab becomes the campaign: a live, dated route from her actual position to a representation conversation, plus the three things that make it winnable — what a gallerist checks and in what order, what she is eligible for that almost nobody else in Tokyo is, and what to have ready before each call opens.**

Four sections plus one time-bounded callout, using the disclosure primitives already in the file (`SectionShell` with `trackId`, `ShyTips`, `TargetsList`).

```
[callout]  These next few days          ← only while a show is up
S1  From here to a representation conversation   (open)
S2  What a gallerist checks, in order            (collapsed)
S3  What you hold that most painters here don't  (collapsed)
S4  The weeks before a door opens                (collapsed)
```

---

## 4. Section-by-section, with drafted copy

Every string below is drafted ZH-first (her default) with EN as fallback. **JA is not drafted here** — the brief scoped EN+ZH. Every new field needs a `_ja` sibling before ship; until then `locF()` falls back to EN, which is the existing behaviour and acceptable for one release. Tier vocabulary (Tier 1/2/3/4) appears nowhere. 解锁 / 升级 / 关卡 appear nowhere.

---

### Callout — 现在这几天 / "These next few days"

Renders **above** S1, not collapsible, only when an exhibition on record contains today's date. Disappears on its own when the show comes down.

> **zh:** 《Light and Shadows and Cats》还挂在原宿的 Galerie LE MONDE，到这个周日。
> 有三件事只有在展览还在的时候能做：拍一组展场照——一面墙、一个空间、一处细节，之后每一份申请要的都是这种照片；把作品清单上已经卖掉的标出来；请一位画廊主来看，只说一句"我的展在这里，到周日"，别的都不用说。
>
> **en:** *Light and Shadows and Cats* is up at Galerie LE MONDE in Harajuku until Sunday.
> Three things are possible while a show is hanging and impossible once it comes down: photograph the room — one wall, one space, one detail, the images every application will ask for; mark the sold works on your price list; and invite one gallerist to come, with nothing more than "my show is here until Sunday."

**Provenance:** new engine-computed block `current_show` in `career_strategy_report.json`, written by `engines/career_strategy_engine.py::_current_show()` — scans `artist_master_profile.career_history.exhibitions` + `memory/exhibition_log.json` for an entry whose date range contains `datetime.now()`, returns `{title, venue, city, ends_on, days_left, is_solo}`. The three actions are authored static copy keyed on `is_solo`. The venue/title/city/"until Sunday" are interpolated.
**Requires** ISO `start_date` / `end_date` fields on exhibition entries (source file — hand-editing legitimate under the Data Patch Rule) with a prose-date parser fallback for existing entries.

---

### S1 — 从这里到一次代理的洽谈 / "From here to a representation conversation"

Replaces `StrategicPathway`. Default open, `trackId="route"`.

**Title (zh):** 从这里到一次代理的洽谈 · **(en):** From here to a representation conversation
**Subtitle (zh):** 五步，按顺序排——不是按重要性，而是按哪一步能让下一步变容易。
**(en):** Five moves, ordered by which one makes the next one easier rather than by importance.
**Collapsed summary (zh):** 五步 · 第一步这个月就开着 · **(en):** Five moves · the first is open this month

**Opening paragraph — the convergence (this is where the Unlock Tree's one good idea lands):**

> **zh:** 画廊不是一扇要硬推的门，它是四条线汇到一起的地方：一次别人选中你的展、一笔别人出的钱、一次画廊主本来就在场的展出，和一群已经在看你作品的人。第四样你手上已经有了——每天两万七千人。另外三样在接下来的十二个月里都有具体的入口，而且第一个这个月就开着。
>
> **en:** A gallery isn't a door you push on. It's where four lines meet: a show someone else chose you for, money someone else put up, an appearance where gallerists are already in the room, and an audience that is already watching. You have the fourth — twenty-seven thousand people, daily. The other three have specific entrances inside the next twelve months, and the first one is open this month.

**Provenance:** authored static, with `27,000` interpolated from `social_presence.instagram.followers_approx`. The "you already have the fourth" clause is gated on `followers_approx >= 10000` — an engine rule, not a hand-patch.

---

Each move renders as: title · why it sits here · `TargetsList` (named doors, existing component) · **这周能做的一件事** (one verb, this week) · `leads_to` (one sentence of consequence, in the muted callout style).

#### Move 1 — 让履历上出现一次"别人选的" / "Put one selection on the record"

> **why here (zh):** 你的三场个展都是你自己做成的——上海 77ART、月画廊、LE MONDE。画廊主读一份简历时是分两栏读的：你自己办的展，和别人选中你的展。天津棉美术馆和台州横渡美术馆那两场是后者，只是它们在中国；日本这一栏现在正在写。这一栏最快能补上，而且这个月正好有门开着。
>
> **(en):** Your three solos are all shows you made happen — 77ART in Shanghai, Tsuki Gallery, LE MONDE. A gallerist reads a CV in two columns: shows you arranged, and shows someone chose you for. Mian Art Museum and Hengdu Art Museum are the second kind; they're in China. The Japan line in that column is the one being written now. It's the fastest line to add, and a door happens to be open this month.

> **这周能做的一件事 (zh):** 9月24日之前投东京艺术委员会的新人扶持金——最高30万日元，不看国籍，只看你住在东京，而"新進"的条件（第一次自主办展起三年内）你现在正好在里面。同一周把 HB Gallery FILE 大赛的要项读一遍：15到20张作为一组交上去，五位大奖得主各得一周个展，十月中截止。
>
> **(en):** Apply to the Arts Council Tokyo startup grant before September 24 — up to ¥300,000, nationality irrelevant, Tokyo residence is the test, and the "new" condition (within three years of your first self-organised Tokyo activity) is one you're inside right now. In the same week, read the HB Gallery FILE competition terms: 15–20 works submitted as a single set, five grand-prize winners each get a week-long solo, closing mid-October.

> **leads_to (zh):** 一次评审选中的展，会让之后每一封信的第一句话都不一样。
> **(en):** One juried selection changes the first sentence of every letter you write after it.

**Targets:** Arts Council Tokyo Startup Grant (open, → Sep 24) · HB Gallery FILE vol.37 (→ ~mid-Oct) · 絵の現在 選抜展 (fee deadline Sep 30 — already in her `build_toward`) · biscuit gallery "grid next" (free, opens ~late Dec).

#### Move 2 — 写信之前，先在场三次 / "Be in the room three times before you write"

> **why here (zh):** 东京的画廊不设投稿箱。这是这里的顺序：先当观众，在开幕上碰上画廊主，再被人引荐。三家离你的作品最近——神保町的 Gallery Kogure（纸上作品，以及从插画走进纯艺术的作者，形式和你最像）、新宿的 biscuit gallery（2021年开的，只做新人，也是东京唯一有免费公开征集的画廊）、中野的 Hidari Zingaro（他们八月那场展的十二位艺术家，全是在 Instagram 上找到的）。
>
> **(en):** Tokyo galleries don't run submission boxes. The local order is: be a viewer, meet the gallerist at an opening, get introduced. Three sit closest to your work — Gallery Kogure in Jimbocho (works on paper, and painters who came out of illustration, your format), biscuit gallery in Shinjuku (founded 2021, emerging artists only, the one Tokyo gallery running a free open call), and Hidari Zingaro in Nakano, whose August show found all twelve of its artists on Instagram.

> **这周能做的一件事 (zh):** 挑一场开幕去看。什么都不用带，也不用提自己的作品。回来写三行邮件说你去了、哪一件留住了你，签名里放上 Instagram 链接。剩下的常常是对方自己点开的。
>
> **(en):** Pick one opening and go. Bring nothing, and say nothing about your own work. Afterwards write three lines saying you came and which piece stayed with you, with your Instagram in the signature. The rest is usually them clicking it.

> **leads_to (zh):** 到第四次照面时，你的名字已经不需要解释了。
> **(en):** By the fourth time, your name no longer needs explaining.

`ShyTips` (the existing `SHY_TIPS_ZH`) attaches here — it is the etiquette expansion of exactly this move, and the prose review praised it. It moves from the bottom of the pathway to under Move 2.

#### Move 3 — 申请一个替你出钱办展的地方 / "Apply to the place that pays for the show"

> **why here (zh):** 东京都的 TOKAS 有一整套项目，资格线写的是"日本国内在住、国籍不問"。这条线把人还在中国的画家挡在外面，也把刚来日本、还没落户的人挡在外面——你两边都在里面。Emerging 给免费场地加15万日元制作费，35岁以下；OPEN SITE 的展览补助是40万日元；驻地那条线——隅田的国内驻地，以及派往赫尔辛基、台北、首尔的交流驻地——全额资助，征集大概就在这两周开放。2026年 Emerging 选出的六个人里有两位是中国艺术家。
>
> **(en):** TOKAS, run by the Tokyo Metropolitan government, has a whole family of programs whose eligibility line reads "resident in Japan, nationality unrestricted." That line keeps out painters still living in China and people who've arrived without registering; you're inside it from both directions. Emerging gives a free venue plus ¥150,000 production money, under 35. OPEN SITE carries a ¥400,000 exhibition grant. The residencies — one in Sumida, plus exchange places in Helsinki, Taipei and Seoul, fully funded — should open within the next two weeks. Two of the six artists chosen for Emerging in 2026 were Chinese.

> **这周能做的一件事 (zh):** 把驻地计划写成三句话。（一个现成的起点：两座城市的同一天——上海和东京，同一个下午的光。）之后每一份表格问的都是这三句，写一次就够。
>
> **(en):** Write the residency idea in three sentences. (A ready starting point: the same day in two cities — the light of one afternoon in Shanghai and in Tokyo.) Every form after this asks the same question; writing it once is enough.

> **leads_to (zh):** 一场机构出钱的展，和一场你自己租下来的展，在简历上读起来是两件事。
> **(en):** A show an institution paid for and a show you rented read as two different things on a CV.

**Targets:** TOKAS Local Emerging Creator Residency (call ~mid-Sep) · TOKAS Exchange Residency — Taipei / Seoul / Helsinki (call ~mid-Sep) · TOKAS-Emerging (call ~Jun 2027) · TOKAS OPEN SITE (call ~Feb 2027) · Art Center NEW, Yokohama (~Jun 2027).

#### Move 4 — 去画廊主必须在场的地方展出 / "Show where gallerists are required to be"

> **why here (zh):** Art Fair Tokyo 和 Tokyo Gendai 不接受艺术家自己报名——那是画廊替艺术家申请的。艺术家能自己报名的博览会是另一条路，而那正是画廊主来挑人的地方：Independent Tokyo 有四百来位艺术家，二三十位画廊主以评审身份在现场走，奖项里包含 tagboat 的代理；青山 Spiral 的 SICF，大奖是 Spiral 中庭的个展加50万日元制作费；别府的 Art Fair Beppu 由京都的 HAPS 策划，免报名费，路费和住宿有补贴。
>
> **(en):** Art Fair Tokyo and Tokyo Gendai don't take applications from artists — galleries apply on an artist's behalf. The artist-direct fairs are the other road, and they're where gallerists come to pick people: Independent Tokyo, ~400 artists with twenty to thirty gallerists walking the floor as judges and representation by tagboat among the prizes; SICF at Spiral in Aoyama, whose Grand Prix is a solo in Spiral's atrium plus ¥500,000 of production budget; and Art Fair Beppu, curated by HAPS in Kyoto, free to enter, with travel and accommodation subsidised.

> **这周能做的一件事 (zh):** 报名大约十月开放。现在能定的一件事：你要几面墙。报名费按板数算，而这个数字决定了你带哪十张画去。
>
> **(en):** The call opens around October. The one thing you can settle now: how many walls you want. The fee is priced by panel count, and that number decides which ten paintings go.

> **leads_to (zh):** 至于 Art Fair Tokyo 和 Tokyo Gendai——那是画廊替你申请的；有了代理，它们自己会来。
> **(en):** As for Art Fair Tokyo and Tokyo Gendai — a gallery applies to those for you. After representation they arrive on their own.

**Targets:** Independent Tokyo (call ~Oct) · SICF28 (call ~Nov, deadline ~Feb) · Art Fair Beppu Spring (call ~Jul 2027) · UNKNOWN ASIA, Osaka (call ~Jul 2027).

#### Move 5 — 那封信本身 / "The letter itself"

> **why here (zh):** 上面三件里有两件落在履历上之后，写给 Gallery Kogure（works@gallerykogure.com）的那封信就变了。它需要的东西不多：一句你是谁——在东京画水彩的中国画家，日记画到第六年；一句你看过他们的哪一场展、哪一件留住了你；三张图；一行写清作品现在在哪里展出，或者最近一次是被谁选中的；再加一句你住在东京、说日语、能自己布展也能到场。不附长篇简历，也不问他们要不要代理你——那个问题是他们后来自己提的。
>
> **(en):** Once two of the three above are on the record, the letter to Gallery Kogure (works@gallerykogure.com) becomes a different letter. It needs very little: one line of who you are — a Chinese painter in Tokyo, six years into a daily watercolor diary; one line about which of their shows you saw and which piece stayed with you; three images; one line naming where the work is showing now, or what selected it last; and one line saying you live in Tokyo, speak Japanese, and can install the work and be there. No attached CV essay, and no asking whether they'd represent you — that question is one they raise themselves, later.

> **leads_to (zh):** 代理几乎从来不是从一封信开始的。但那封信决定了下次见面时你是谁。
> **(en):** Representation almost never starts with a letter. The letter decides who you are the next time you meet.

**Section closing hint** (replaces `NEXT_STEP_HINT`, which currently contradicts the dated actions above it):

> **zh:** 不急。有确定日期的地方山楂都写下来了；其余的，想做的时候再做。
> **(en):** No rush. Where there's a real date, Saffron has written it down; everything else is whenever you feel like it.

**Provenance for S1:**

| Piece | Source |
|---|---|
| Move list, order, gating | **New engine field** `campaign` in `career_strategy_report.json`, from `engines/career_strategy_engine.py::_campaign_sequence(evidence, levers)`. Each move: `{id, title, title_zh, why_here, why_here_zh, this_week, this_week_zh, leads_to, leads_to_zh, targets[], source_lever_ids[], shown_when}` |
| "your three solos are all shows you made happen" | **New engine flag** `has_curated_solo` from `_has_curated_solo(profile, ex_log)` — true when any solo has `venue_model` other than `rental`/`self_funded`. Move 1 disappears when it flips true. Needs a `venue_model` field on exhibition entries (source file) |
| Museum names, gallery names, grant names, amounts, windows | `_next_tier_levers()` `targets[]` — already exists, already researched, already localized |
| `leads_to` | **New authored field per lever**, `leads_to` / `leads_to_zh` / `leads_to_ja`, added inside `_next_tier_levers()`. Extend `test_career_graduated_ladder.py::test_every_graduated_lever_is_localized` to cover it |
| "closing Sep 24 / N days from today" | Existing `_act_grant_urgency()`; generalize to `_window_urgency(date)` so every dated target gets the same near/far phrasing |
| ShyTips body | Existing `SHY_TIPS_ZH` / `_EN` / `_JA` in `api.py` — moved, not rewritten |
| Move 5's letter contents | Authored static. The Instagram / N2 / "lives in Tokyo" clauses gate on `social_presence`, `japanese_proficiency`, `current_city` |

---

### S2 — 画廊主看一位没有代理的画家时，按什么顺序看 / "What a gallerist checks, in order"

Collapsed, `trackId="gallerist_lens"`.

**Title (zh):** 画廊主看一位没有代理的画家时，按什么顺序看
**(en):** What a gallerist checks, and in what order
**Subtitle (zh):** 这是从东京的画廊怎么挑人里读出来的顺序。六件事里，你已经有四件很结实。
**(en):** The order read out of how Tokyo galleries actually pick people. Of the six, four of yours are already solid.
**Collapsed summary (zh):** 六件事 · 其中四件你已经很强 · **(en):** Six things · you're already strong on four

Each check renders as a row: **他在看什么** / **你现在能拿出的** / **拿这个去说**.

**1. 能不能一个人撑起一个空间 / Can she carry a room alone**
> **你现在能拿出的 (zh):** 三场个展，最近一场正挂在原宿。 **(en):** Three solos, the most recent hanging in Harajuku right now.
> **拿这个去说 (zh):** 《永遠の昨日》和现在这场的展场照——一面墙一张，而不是单幅作品的图。画廊主要看的是一个被撑住的空间。
> **(en):** Installation shots from *The Eternal Yesterday* and this current show — one image per wall, rather than images of single works. What he's looking at is a room being held.

**2. 是一批作品，还是一种画法 / A body of work, or a manner**
> **(zh):** 2020年起每天一张，到今年是第六年。这是一批作品，而且它自己会讲时间——大多数同龄画家拿不出这个。
> **(en):** One painting a day since 2020, six years in. That's a body of work, and it tells time on its own — most painters your age can't put that on a table.
> **拿这个去说 (zh):** 同一个季节的十二张，按顺序排。不是六年里最好的四十张。
> **(en):** Twelve from one season, in sequence. Not forty bests from six years.

**3. 有没有人替你选过 / Has anyone selected you**
> **(zh):** 天津棉美术馆和台州横渡美术馆那两场美术馆群展是别人选的——这一条比它听起来重。日本这一栏现在正在写，上面第一步写的就是它。
> **(en):** The museum group shows at Mian Art Museum and Hengdu Art Museum were somebody else's choice — that counts for more than it sounds like. The Japan line in that column is the one being written now; Move 1 above is that line.

**4. 卖得动吗，什么价位 / Does it sell, and at what price**
> **(zh):** 你有自己的店（gegyjiji.base.shop），三场个展也都有销售。画廊要看的是一个能重复的价位，不是一个总数——他要知道把你的画挂到墙上，标多少钱是合理的。
> **(en):** You have your own shop (gegyjiji.base.shop) and sales from three solos. What a gallery wants is a repeatable price point rather than a total — he needs to know what it's reasonable to put on the wall next to your work.
> **拿这个去说 (zh):** 一张作品清单：标题、年份、材质（水彩・紙）、尺寸、含税价格、已售的标出来。
> **(en):** A price list: title, year, medium (watercolour on paper), size, price including tax, sold works marked.

**5. 有没有人已经在看 / Is anyone already watching**
> **(zh):** 两万七千人，每天。东京同龄的画家大多在两千到五千之间。这是你身上最不寻常的一项——中野的 Hidari Zingaro 八月那场展，十二位艺术家全是从 Instagram 挑的。
> **(en):** Twenty-seven thousand people, daily. Most painters your age in Tokyo sit between two and five thousand. This is the most unusual thing you carry — the twelve artists in Hidari Zingaro's August show in Nakano were all picked off Instagram.

**6. 好不好一起做事 / Is she easy to work with**
> **(zh):** 你住在东京，日语到 N2，能自己布展、能到场、自己做过宣传。把这一句放在第一封邮件的最后一行，比任何形容词都管用——画廊主脑子里正在算的，是这场展要花他多少力气。
> **(en):** You live in Tokyo, your Japanese is N2, you can install, attend, and have done your own PR. One line at the end of a first email does more than any adjective — what he's quietly calculating is how much of the show he'd have to carry.

**Provenance:** the six checks and their order are **authored static** (`GALLERIST_LENS` in the engine, not the frontend — it must localize through the same `_zh` path as the levers). `你现在能拿出的` for each check is **engine-templated** from `career_evidence` + profile: solo count and newest solo title/venue from `_current_show()`/`exhibitions`; museum names from entries with `significance` containing "museum"/"Institutional"; follower count from `social_presence`; `japanese_proficiency`, `current_city`, `is_student` from `visual_profile`. New engine function `engines/career_strategy_engine.py::_gallerist_lens(profile, evidence)` → `gallerist_lens[]` in the report. Check 3's "the Japan line is being written now" text is gated on `has_juried_selection == False` and swaps to the credit itself once true.

---

### S3 — 你手上有、东京大多数画家没有的 / "What you hold that most painters here don't"

Collapsed, `trackId="leverage"`.

**Title (zh):** 你手上有、东京大多数画家没有的
**(en):** What you hold that most painters here don't
**Subtitle (zh):** 资格是一种资产。你这几样叠在一起的组合很少见，而它决定了哪些门本来就为你开着。
**(en):** Eligibility is an asset. Your particular stack is rare, and it decides which doors are already open to you.
**Collapsed summary (zh):** 七样 · 其中三样有期限 · **(en):** Seven things · three of them on a clock

Each item: **你有的** → **它打开的** (with `TargetsList`) → optional **期限**.

**1. 中国国籍 / Chinese citizenship**
> **(zh):** 亚洲文化协会（ACC）的中国大陆通道看的是国籍，不是住址——住在东京不影响你走这条线，最高三万五千美元，10月1日到11月10日。成都 A4 的国际驻地全额资助，含一万元人民币制作费，2026年12月31日截止。野村财团那条"国际交流"的线，本来就是拿来资助中日之间的项目的。
> **(en):** The Asian Cultural Council's Mainland China track keys on citizenship, not address — living in Tokyo doesn't affect it. Up to US$35,000, October 1 to November 10. A4 in Chengdu runs a fully funded international residency with a ¥10,000 RMB production budget, closing December 31 2026. And Nomura's "international exchange" line exists to fund exactly a China–Japan project.

**2. 日本在住 ＋ 住民登録 / Japan residence with registration**
> **(zh):** TOKAS 一整家项目写的都是"日本国内在住・国籍不問"：Emerging（免费场地＋15万日元制作费）、OPEN SITE（40万日元展览补助）、隅田的国内驻地、以及派往赫尔辛基／台北／首尔的全额交流驻地。人还在中国的画家申请不了；刚到日本还没登记的也申请不了。这一格加上第一格，是这一页里最少见的组合。
> **(en):** The whole TOKAS family reads "resident in Japan, nationality unrestricted": Emerging (free venue plus ¥150,000 production), OPEN SITE (a ¥400,000 exhibition grant), the domestic residency in Sumida, and the fully funded exchange places in Helsinki, Taipei and Seoul. A painter still in China can't apply. Someone newly arrived without registration can't either. This one stacked on the first is the rarest combination on the page.

**3. 26岁 / Twenty-six**
> **(zh):** TOKAS Emerging 是35岁以下，横滨 Art Center NEW 的公开征集也是35岁以下，加拿大 Elizabeth Greenshields 是18到41岁。 **期限：** 三十五岁。
> **(en):** TOKAS Emerging is under 35, Art Center NEW in Yokohama is under 35, Elizabeth Greenshields in Canada is 18 to 41. **Clock:** thirty-five.

**4. 还在读书 / Still enrolled**
> **(zh):** Elizabeth Greenshields 基金会明确接受学生，专门资助具象绘画，随时可投，首笔大约一万七千加元。反过来，Pollock-Krasner 要等你毕业之后——那扇门是留着以后开的。
> **(en):** The Elizabeth Greenshields Foundation explicitly accepts students, funds representational painting specifically, takes applications any time, and its first grant is around CAD 17,000. The other way round, Pollock-Krasner opens after you graduate — that one is kept for later.
> **期限：** 毕业那天，第一扇门关，第二扇门开。 **Clock:** the day you graduate, the first closes and the second opens.

**5. 日语 N2 / N2 Japanese**
> **(zh):** 横滨 Art Center NEW 要求能用日语沟通，TOKAS 的申请表也是日语的。在东京的外国画家，大多停在这一格。
> **(en):** Art Center NEW requires Japanese communication and TOKAS's forms are in Japanese. Most foreign painters in Tokyo stop at this one.

**6. 上海和东京两张展览网络 / Two exhibition networks, Shanghai and Tokyo**
> **(zh):** 一个横跨两地的展览不只是一场展，它是一个可以被资助的"项目"——野村财团（10月1日至30日，最高100万日元）看的正是这个。外滩的 Swatch 驻地常年可投，是回到上海那张网上的现成落脚点。
> **(en):** A show across both cities isn't just a show, it's a fundable *project* — which is exactly what Nomura (October 1–30, up to ¥1,000,000) is looking at. The Swatch residency on the Bund takes applications year-round and is a ready base from which to re-enter the Shanghai network.

**7. 每天更新的两万七千人 / Twenty-seven thousand people, daily**
> **(zh):** Kaikai Kiki 八月那场展的十二位艺术家全是从 Instagram 找到的。Colossal 的水彩栏目常年在写你这一类作品，投稿地址是 submissions@thisiscolossal.com——他们要的是一批作品，不是一场展览的信息。
> **(en):** All twelve artists in Kaikai Kiki's August show were found on Instagram. Colossal's watercolour desk runs work like yours continuously, and takes pitches at submissions@thisiscolossal.com — what they want is a body of work rather than an exhibition announcement.

**Closing line:**
> **(zh):** 三样带着期限：三十五岁、学生身份，还有东京艺术委员会算的"新進"（第一次自主办展起三年内）。有日期的，山楂都写在下面一节里了。
> **(en):** Three of these carry a clock: thirty-five, being enrolled, and the Arts Council Tokyo "new" window (within three years of your first self-organised show). Everything with a date is written down in the section below.

**Provenance:** **new engine** `engines/eligibility_leverage_engine.py::build_leverage_inventory(profile)` → `memory/eligibility_leverage.json`, merged into `career_strategy_report.json` as `leverage[]`. It matches profile facts (`visual_profile.nationality`, `.age`, `.japanese_proficiency`, `.current_city`, `is_student`, exhibition cities, `social_presence.instagram.followers_approx`) against a static `ELIGIBILITY_RULES` table authored from `weekend_advice_research_2026-09-04.md` §2–§5. Each rule: `{id, requires:{...}, asset, asset_zh, opens:[targets], expires, expires_note}`. Items whose `requires` no longer match are dropped automatically — when she turns 36 or stops being a student, the page changes with no hand edit. This is what makes the section Data-Patch-Rule clean: the *rules* are authored; the *inventory* is computed.

---

### S4 — 门开之前的那几周 / "The weeks before a door opens"

Collapsed, `trackId="prep"`. This is the section that answers "what do I do in the six weeks before a window opens" instead of 留意.

**Title (zh):** 门开之前的那几周 · **(en):** The weeks before a door opens
**Subtitle (zh):** 征集开放那天就能投出去，靠的是之前几周准备好的六样东西。准备好之后，每一份申请都变成拼装，而不是重写。
**(en):** Applying the day a call opens comes from six things prepared in the weeks before. Once they exist, every application is assembly rather than invention.
**Collapsed summary (zh):** 一套六件的底稿 · 十二扇门的开放时间 · **(en):** A six-piece kit · when twelve doors open

**底稿六件 / The kit — six pieces**

1. **十张，不是四十张 / Ten, not forty**
   > **(zh):** 一组，一个季节，按顺序排；300dpi 和网页尺寸各存一份。评审看的是这十张之间的关系。
   > **(en):** One set, one season, in sequence; saved at 300dpi and at web size. What a jury reads is the relationship between the ten.
2. **日文履历 / A Japanese CV**
   > **(zh):** 学歴／個展／グループ展／受賞・掲載，倒序，每一行写清场地、城市、年月。日本的评审在找这个格式；找不到的时候，他们得自己替你拼。
   > **(en):** 学歴 / 個展 / グループ展 / 受賞・掲載, reverse chronological, each line naming venue, city, month. Japanese juries look for this shape; when it isn't there they have to assemble it themselves.
3. **作品清单（作品リスト）/ A work list**
   > **(zh):** 标题／年份／材质（水彩・紙）／尺寸（毫米）／含税价格／已售标记。画廊和博览会要的都是这一张。
   > **(en):** Title / year / medium (watercolour on paper) / size in mm / price including tax / sold marked. Galleries and fairs both ask for this one sheet.
4. **三句话的计划 / A three-sentence plan**
   > **(zh):** 你想做什么、为什么在这里做、为什么是现在。驻地和奖助的表格问的都是这三句。
   > **(en):** What you want to make, why here, why now. Every residency and grant form is asking these three.
5. **展场照 / Installation shots**
   > **(zh):** 一面墙、一个空间、一处细节。LE MONDE 这场撤展之前拍下来——展览撤了就补不回来了。
   > **(en):** One wall, one space, one detail. Photograph the LE MONDE show before it comes down — once a show is struck, these can't be made again.
6. **两百字的自述，日文和中文各一份 / A 200-character statement in Japanese and Chinese**
   > **(zh):** 从你在胡椒粒那边写下的那段拿。
   > **(en):** Taken from what you wrote with Peppercorn.

**门什么时候开 / When the doors open** — rendered as rows, each: door · 开放 · 什么时候开始准备 · 这扇门额外要的.

| 门 | 开放 | 开始准备 | 这扇门另外要的 |
|---|---|---|---|
| 东京艺术委员会 新人扶持金 | 现在，9月24日截止 | 现在 | 一份预算，和一场具体的公开活动 |
| TOKAS 驻地（国内・交流） | 约九月中开放，约六周 | 现在 | 三句话计划＋日文表格 |
| HB Gallery FILE vol.37 | 约十月中截止 | 现在开始挑 | 15–20张作为一组，报名费 7,000 日元 |
| 朝日新闻文化财团 | 10月25日 | 十月初 | 非营利性质的展览——自主策划或艺术家自营空间更合适 |
| 野村财团 | 10月1日–30日 | 十月初 | 一个有名字、有预算的项目 |
| 亚洲文化协会（ACC） | 10月1日–11月10日 | 现在联系推荐人 | 两位推荐人，11月16日前送达 |
| Independent Tokyo | 约十月开放 | 十月 | 决定板数——它同时决定报名费和带哪十张 |
| 京都艺术中心 Co-program | 约十月至十一月 | 十月 | 最高100万日元制作费；场地在京都 |
| SICF28 | 约十一月开放，二月截止 | 十一月 | 一个展位方案 |
| biscuit gallery grid next | 约十二月底开放 | 十二月 | 免费，40岁以下，学生可投 |
| 福冈亚洲美术馆 驻地 | 约十二月底至一月 | 十二月 | 美术馆主办，以一场展览收尾 |
| 神山 KAIR（徳岛） | 约一月至二月 | 一月 | 明确写着绘画；乡村，适合另起一组作品 |

EN header row: Door · Opens · Start preparing · What this one wants beyond the kit.

**Closing line:**
> **(zh):** 写着"约"的日期是照往年推的，不是官方公布的——山楂会在真的公布之后把它改成确定的。
> **(en):** Dates marked "around" are read off previous years rather than announced — Saffron will make them firm once they are.

**Provenance:** **new engine** `engines/application_prep_engine.py::build_prep_windows(today)` → `prep_windows[]` in `career_strategy_report.json`. Static authored source table `PREP_DOORS` (door id, name, url, `opens`, `opens_confidence: direct|inferred`, `lead_weeks`, `extra_needs`, `extra_needs_zh`) sourced line-by-line from `weekend_advice_research_2026-09-04.md`. The engine computes `start_preparing` = `opens − lead_weeks`, sorts by it, renders "现在 / 十月 / 约十二月" from that date, and drops rows more than 14 months out. `opens_confidence: inferred` is what renders the 约 / "around" prefix and the closing line — never present a pattern-derived window as an announced date. `APPLICATION_KIT` (the six pieces) is authored static; item 5's "before it comes down" clause is gated on `current_show` being non-empty.

---

## 5. What is deliberately *not* on this tab

- **Counts, readiness percentages, tier labels, progress bars.** Those are the profile tab's material and CLAUDE.md forbids showing tiers at all.
- **The record.** `CareerPosition` owns it. S1 and S2 cite specific credits as evidence inside a forward sentence; neither lists her CV.
- **The choice between roads.** `LongTermScenarios` owns "gallery vs. book vs. both." This tab assumes nothing about which she wants — S1's title says "a representation conversation", not "your goal", and Move 5 explicitly leaves the representation question to the gallery to raise.
- **The whole deadline feed.** The Calendar tab renders every dated opportunity in `opportunities.json`, month by month. S4 renders twelve *named campaign doors* with preparation lead times. The distinction to enforce in code: Calendar answers "what closes in November"; S4 answers "what do I do in October so that November is easy." If they ever converge, S4 wins and the calendar drops the duplicated rows.

---

## 6. How this composes with the profile-tab redesign

The parallel agent owns `CareerReadiness`, `CareerPosition`, `LongTermScenarios`. One sentence each, and one contested asset.

| Narrative | Owner | Rule |
|---|---|---|
| The record — what has happened | `CareerPosition` (profile) | This tab never lists exhibitions. It cites at most two, always inside a forward clause |
| How ready / how she compares | `CareerReadiness`, benchmarks, peers, momentum (profile) | This tab never states readiness, progress, or a comparison to peers |
| The three possible lives — gallery / book / both | `LongTermScenarios` (profile) | This tab plans *one* of those roads in detail and never argues she should choose it. If Scenarios stays on the strategy tab instead, it renders **below S4** and this tab's opening paragraph gains one clause acknowledging the book road |
| The route, the doors, the dates, the preparation | **This tab** | The profile tab states no deadline and names no gallery, grant or residency |
| Corrections to the record ("I already did this") | `GapCorrectionForm`, `ReadinessCorrection` (profile) | Corrections are about the record, so they live with the record. This tab has no forms |

**The one contested asset: `blocking_gaps` / the seven researched levers.** They are currently rendered by `CareerReadiness` on the profile tab, and they are the most specific material in the app. They are *route* content — doors, windows, named targets — so **their rendering moves here**, distributed across S1's five moves (via `source_lever_ids`), S3's leverage items, and S4's prep rows. `career_strategy_report.json` keeps `blocking_gaps` unchanged as the engine's output; only the rendering moves. What `CareerReadiness` keeps on the profile tab is the readiness columns ("getting closer" / "keep an eye on") and the correction forms.

**If both designs claim the levers, this is the tie-break to apply:** a door with a date belongs to strategy; a fact about her record belongs to profile.

**One duplicate to delete on sight:** `careerStatusLine`'s closing clause ("接下来的方向是画廊关系与代理") and `CAREER_SYNOPSIS`'s closing sentence are both forward statements on the profile tab. With this design live, S1's opening paragraph is the single copy of that thought. Both closing clauses go.

---

## 7. What this requires in code

**Delete**
- `CareerDependencyMap` (`SaffronPage.jsx` ~L1734) and its `MILESTONE_DOT_COLORS`
- `CAREER_DEPENDENCY_MAP` (`frontend/src/data/saffron_insights.js` ~L488) and its import
- `sf.depmap.*` — 8 keys × zh/ja/en in `frontend/src/i18n/translations.js`
- `.sf-depmap*` CSS rules
- The `else` branch pathway in `api.py` (~L2360) — it names 3331 Arts Chiyoda (closed 2023) and targets a first solo she has had three times. Replace the whole `_foundation_complete` conditional with the campaign block

**New engine work** (all in `engines/`, all pipeline-run, no hand-patched JSON)
1. `career_strategy_engine.py::_current_show()` → `current_show` block. Needs ISO `start_date`/`end_date` on exhibition entries (source file) with a prose-date parser fallback
2. `career_strategy_engine.py::_has_curated_solo()`, `_has_juried_selection()`, `_has_fair_showing()` → three new `career_evidence` flags. Needs an optional `venue_model: rental|curated|institution` field on exhibition entries. Also **fixes the bug** `weekend_advice_research` §0.1 found: `solo_venue_quality` is gated `if solo_shows < 3` and so never fires — re-gate it on `has_curated_solo`
3. `career_strategy_engine.py::_campaign_sequence()` → `campaign.moves[]`, each with `shown_when` evidence gating and `source_lever_ids` into the existing levers
4. `career_strategy_engine.py::_gallerist_lens()` → `gallerist_lens[]`
5. `career_strategy_engine.py`: add `leads_to` / `leads_to_zh` / `leads_to_ja` to every lever in `_next_tier_levers()`
6. `career_strategy_engine.py`: generalize `_act_grant_urgency()` → `_window_urgency(date, lang)` so every dated target gets consistent near/far phrasing
7. **New** `engines/eligibility_leverage_engine.py` → `memory/eligibility_leverage.json` + `leverage[]` in the report. Static `ELIGIBILITY_RULES` table; computed inventory
8. **New** `engines/application_prep_engine.py` → `prep_windows[]` + `application_kit[]`. Static `PREP_DOORS` table with `opens_confidence`; computed `start_preparing`
9. Register 7 and 8 in `run_full_mochi_pipeline.py`'s `PIPELINE`, before the career-strategy step

**API**
- `api.py` `/api/career_strategy`: pass through `campaign`, `current_show`, `gallerist_lens`, `leverage`, `prep_windows`, `application_kit`
- `api.py` `/api/saffron`: `pathway` is no longer rendered — keep the field one release for cache compatibility, then remove

**Frontend** (`frontend/src/components/SaffronPage.jsx`)
- New: `CurrentShowCallout`, `RouteToRepresentation` (replaces `StrategicPathway`), `GalleristLens`, `LeverageInventory`, `PrepWindows`
- Reuse unchanged: `SectionShell`, `ShyTips`, `TargetsList`, `locF`, `SectionErrorBoundary`, `TrackedSection`
- Strategy tab order: callout → `RouteToRepresentation` (open) → `SectionOpenContext.Provider value={false}` → `GalleristLens`, `LeverageInventory`, `PrepWindows`
- Give every section a `trackId` (`route`, `gallerist_lens`, `leverage`, `prep`) and wrap each in `TrackedSection` — including the default-open first one, which is currently the least-measured block on the page
- One new CSS block for the prep table; it must scroll inside its own container on a phone

**i18n**
- New keys: `sf.sec.route`, `sf.sub.route`, `sf.sum.route`, `sf.sec.gallerist`, `sf.sub.gallerist`, `sf.sum.gallerist`, `sf.sec.leverage`, `sf.sub.leverage`, `sf.sum.leverage`, `sf.sec.prep`, `sf.sub.prep`, `sf.sum.prep`, `sf.label.thisWeek`, `sf.label.leadsTo`, `sf.label.opens`, `sf.label.startPrep`, `sf.label.alsoWants`, `sf.label.youCanShow`, `sf.label.leadWith`, `sf.label.clock` — zh/ja/en
- JA copy for every new field is unwritten; `locF()` falls back to EN. Ship one release on that fallback, then commission JA
- Add `route`, `gallerist_lens`, `leverage`, `prep` to `SECTION_LABELS` in `engines/visit_tracking.py`

**Tests**
- Extend `test_career_graduated_ladder.py::test_every_graduated_lever_is_localized` to cover `leads_to_zh`
- New: every `campaign.moves[]`, `gallerist_lens[]`, `leverage[]`, `prep_windows[]` entry has a `_zh` sibling for every prose field
- New: no user-facing string in the report or `SaffronPage.jsx` contains `Tier `, `解锁`, `解放`, or `unlock`
- New: `prep_windows` rows with `opens_confidence: inferred` render with the 约 / "around" prefix
