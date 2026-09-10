# Saffron Chinese audit — interface, overview, peers and press

Reviewed 2026-09-10 against the rendered Chinese page and current source. The engine and ladder reports preserve every original unit; this companion covers the remaining visible interface and supporting sections. Proposed replacements are editorial drafts. When a sentence changes a factual claim, the English and producing rule need the same correction.

## Shared editorial conventions

- Use **你** as ordinary direct address. State specific work she has made or shown; avoid grading her personality, worth, age or diligence.
- Use simplified Chinese for prose. Preserve official Japanese names and official artwork/exhibition titles; do not invent a Chinese title. Introduce a Chinese explanatory label only when useful.
- Use **视频、创作、作品、读者、关注者、印刷品、艺术微喷、联展、驻留、出版提案、销售佣金、使用范围** consistently. “版画” should mean an actual printmaking work, not every reproduction. “作品集” and “画集” should match the object.
- **关注数 ≠ 独立人数 ≠ 触达 ≠ 观看次数 ≠ 买家。** Platform does not establish audience language. A stocked or sold-out item does not establish a sale.
- Use **有记录 / 尚未确认 / 当届要求 / 测算 / 个案** where accurate. These are distinctions in evidence, not a disclaimer added to every sentence.
- Distinguish **作品授权** from **著作权转让**; an indefinite license is not automatically a copyright transfer. Do not offer universal legal conclusions in friendly copy.
- Chinese copy should use one main idea per paragraph. Practical body text should be upright, not italic. Use punctuation, not em-dash chains, to separate clauses.
- Avoid repeated **唯一、全部、肯定、只要……就、没有任何、最合适、最划算、任何人、每一家** unless evidence actually establishes the scope.
- Preserve warmth through concrete attention: naming a series, an exhibition and a practical use for its materials. Do not add invented feelings or reasons she has not replied, posted, sold or applied.
- Research paragraphs must not become instructions for her to redo the research. If a route is unknown, identify it as unresolved research; prepare the answer before making it a recommendation.

## Navigation, loading, section headings and empty states

Sources: `frontend/src/i18n/translations.js`; `SaffronV2.jsx` (`V2_COPY`, `PULSE_COPY`); `SaffronPage.jsx` (local label objects). Preserve established tab names **策略 / 日历 / 概况**. Keep **观察 / 山楂**, **中文 / English**, **收起**, **取消**, **保存**, **更新**, **已保存**, **资格要求**, **截止日期**, **展览经历**, **出版物**. These already read clearly.

| Current | Proposed | Reason / implementation |
|---|---|---|
| 路径 | 可以发展的方向 | More explicit optional heading. Keep 路径 if preserving familiar labels is preferred; the valuable change is the content preview. |
| Saffron 正在观察… | 山楂正在整理资料… | Localize companion consistently. |
| 山楂在为你俯瞰全局… | 山楂正在整理资料… | Existing line is understandable; proposed line describes loading plainly. |
| Error text that presents failure only as Saffron resting | 资料暂时没能加载。可以稍后重试。 | A network failure should not masquerade as a personality state. Add a working 重试 control if implemented. |
| 未来一年 | 未来一年 | Keep. |
| 有日期的条目 · 圆点表示当月开放的门 | 已收录的日期与预计征集时段 | Covers both confirmed dates and estimates without conflating them. |
| 有门开放 | 预计征集时段 | If actually confirmed open, use 正在征集 instead. State and date basis must decide label. |
| — 暂无日期 | 暂无已确认日期 | Empty database is not empty world. |
| {n} 条有日期 | {n} 项已标注日期 | Do not call all entries deadlines until event/interview/delivery dates are separated. |
| 暂无有日期的条目 | 暂无已确认日期 | Natural Chinese. Do not show this as a workaround for localization bug. |
| 本月有 {n} 扇门开放 | 本月有 {n} 项预计征集 | Only estimated items. Confirmed count uses 本月有 {n} 项正在征集. |
| 本月暂无有日期的条目。下面的门仍会轮到。 | 目前尚未收录本月的明确日期。下方列出了可提前了解的项目。 | Wording distinguishes missing data from no opportunities. |
| 显示其余 {n} 条 | 再看 {n} 项 | Short, conversational; retain original if consistency with rest of app matters. |
| 自 {d} 起没有新的。检索大约每月一次。 | 自 {d} 起，暂未收录新的项目。 | Cadence claim disagrees with changing maintenance/discovery schedules; do not promise monthly search. |
| 自 {d} 起，新增 {n} 条。 | 自 {d} 起，新收录 {n} 项。 | Specify newly catalogued, not freshly available/verified. Prefer names over large counts in the visible headline. |
| {served} 条中有 {ahead} 条带着可读的日期，其余的没有日期，或已经过去。 | 当前收录 {served} 项，其中 {ahead} 项标注了尚未过去的日期。 | Only after count contract is reconciled with calendar. Move to optional 数据说明; do not ask her to care about parser readability. |
| 会再次打开的门 | 可提前了解的征集项目 | Recurrence inference does not guarantee reopening. |
| 今天有 {o} 扇开着，最近的一扇 {s} 天后关。 | 当前有 {o} 项正在征集，最近一项将在 {s} 天后截止。 | Requires verified open state and real deadline. |
| 今天没有开着的。下面是接下来会开的，按时间排。 | 这些项目的下一轮时间尚需确认，可先了解准备要求。 | Must use a separate branch when rolling grants are open; current page contradicts 常年开着 below. |
| 现在开着 | 正在征集 | Standard term. |
| 常年开着 | 全年接受申请 | Verify actual program policy. |
| 时间为估计 | 预计时间，尚待公告 | Clear evidential status. |
| 现在着手正合适 | 可提前准备 | No implied deadline urgency. |
| 要准备好的 : | 准备材料： | Natural label and full-width colon. |
| ≈ {r} 张不必卖掉的画 | 资助金额及用途见下方 | Prefer actual currency/support type. Do not imply awards replace a known number of sales. |
| 制作预算，约等于 {r} 张画的开销 | 制作经费 | Her original list price is not production cost. |
| 画材，约等于 {r} 张画 | 画材支持 | An in-kind allowance is not cash. |
| 资助资源 | 资助项目 | Either acceptable; 项目 is slightly more concrete. |
| 很多艺术家只是因为不知道有哪些资助项目，便错过了申请机会。 | 申请条件、支持内容与准备材料，放在一起看。 | No unsupported diagnosis of artists' failures. |
| 从何入手 | 可以先了解 | Optional, concise. |

The year strip cannot be fixed through wording. On the live page, the same September selection displayed **0 dated entries in Chinese and 53 in English**. `saffronTx()` translates arbitrary string values before `MONTH_EN.indexOf(m.month)` tries to match English names. Keep month identifiers/numbers and enum values untranslated; translate their display labels. See the improvement brief for reproduction and acceptance checks.

## Strategy-ladder interface

Source: `SaffronPage.jsx`, `LADDER_COPY`, around lines 787–809. All detailed state copy is in report 03.

| Current | Proposed | Reason |
|---|---|---|
| 推进策略 | 可以怎样推进 | Optional sequence, not grading. |
| 不同的目标，重叠的事项，不同的顺序 | 看看已有材料可以支持哪些方向，以及各自下一步需要什么。 | Explain practical value. |
| {b} 级里已经到了 {a} 级 | 已有 {a} 项记录 | Current count is the number of yes states, not a consecutive level reached. Show total only in evidence detail if useful. |
| 下一级： | 可以接着了解： | A missing milestone is not necessarily a prerequisite. |
| {n} 级没有查过 | 另有 {n} 项尚未确认 | Unknown is not an artist deficit. |
| 系统从来没有核实过这一项 | 目前没有足够记录确认这一项。 | Less accusatory and more accurate. |
| 同时也算进 | 也可用于 | Shared work is reusable, not a game score. |
| 阶梯是手写的，勾选是从你的记录里读出来的。 | 这些顺序供比较参考，可按你的目标和时间调整。 | Internal implementation story has no value to her. Must actually allow sequence to be optional. |

## Book chart and comparison labels

Source: `SaffronPage.jsx`, `BE_LABELS`, around line 1621. The underlying arithmetic must be fixed first; labels cannot make the current model valid.

| Current | Proposed |
|---|---|
| 一本书要花多少钱 | 印制成本与销售测算 |
| 先付 {v} | 预付支出 {v} |
| 要卖出 {n} 本 | 覆盖模型支出需售出 {n} 本 |
| 可以寄售 | 该情景下寄售结余为正 |
| 寄售会亏 | 该情景下寄售收入不足以覆盖所列费用 |
| {b} 种印法里，只有 {a} 种能把钱赚回来。 | 在当前售价和费用假设下，{a} 种方案可在整批售完前覆盖模型支出。 |
| 能回本 | 模型内可覆盖支出 |
| 回不了本 | 模型内仍有支出缺口 |
| 印 {n} 本 | 印量：{n} 本 |
| 卖 {n} 本回本 · 印量的 {p}% | 需售出 {n} 本，约占印量 {p}% |
| 要卖 {n} 本 · {x} 倍印量 | 所需销量为印量的 {x} 倍 |
| 每卖一本都在亏 | 当前售价低于每本所列成本 |
| 整条＝那一种印法印出来的数量；填色的部分＝要卖掉多少才回本。填色漫出右边，表示整批卖光之后成本仍有缺口。 | 整条表示印量，填色表示覆盖模型支出所需的销量。填色超出整条时，表示这批全部售出仍有缺口。 |

Keep currency, percentage and quantity formatting consistent. For narrow screens, display each scenario with its own clearly labelled figures rather than shrinking a wide table. A cash-recovery chart must state that expected units sold are not being predicted.

## Overview opening and exhibition record

Sources: `SaffronPage.jsx` (`CAREER_SYNOPSIS`, `CAREER_SUMMARY`, `SF_ZH_CV`, `CareerPosition`); `translations.js`; `api.py` → `career_position`.

**Current synopsis**

> 你一直在持续参展：在中国、日本及其他国家举办或参加过个展、联展和美术馆群展，也出版了首部个人作品集，并拥有稳定增长的受众。你的根基已经很扎实。接下来，比起继续堆叠履历，更重要的是加深画廊关系；如果你愿意，也可以开始了解代理合作，并继续发展由日常创作自然延伸出的出版方向。

**Replace with**

> 你的作品已经通过个展、联展和出版物，在不同地方与读者见面。最近的一场个展在原宿 Galerie LE MONDE，于 2026 年 9 月结束。这里整理了这些经历与作品资料，方便查看，也方便用于下一次介绍。

Do not characterize her record as a pile to stop adding to. No growth claim without a time series. The latest exhibition must be selected from current records, not hardcoded permanently into this proposed paragraph.

| Current | Proposed | Reason |
|---|---|---|
| 职业定位 | 创作与展览记录 | It is a record, not an assessment of rank. |
| 你现在实际所处的位置 — 仅限已确认的事实。 | 已记录的展览、出版与作品介绍。 | Avoid official-sounding claim that everything below has been independently verified. |
| 持续办展——个展、联展、美术馆与海外展，首部作品集，稳定的受众。 | 展览、出版与作品介绍，集中在这里。 | Do not imply every group show was self-organized. |
| 27k 粉丝 | Instagram 约 2.7 万关注者 | State platform and observation date; a lone number is ambiguous. |
| 13 联展 | 13 场展览记录 | The collection includes solo shows. Derive total and category counts from same records. |
| 2 出版物 | 2 项出版记录 | Keep categories explicit; zines may overlap, so do not sum blindly. |
| 五个平台上稳固且持续增长的受众 | 在五个平台上持续分享作品，并积累了关注。 | Still verify 持续 per platform; safer fallback: 五个平台上已有作品与关注记录. |
| 群体出版物，供稿者 | 合辑，参与供稿 | Idiomatic publishing term. |
| 机构（美术馆）联展 | 美术馆联展 | No need to repeat same fact in type and note. |
| 展览（来源未注明个展或联展） | 展览，类型待确认 | Short uncertainty label. |
| 联展（官方节庆海报艺术家） | 联展；参与官方海报创作 | Only if both are separately evidenced. A poster credit alone must not imply exhibition participation. |
| 首次在日本展出（展览资料中明确说明） | 首次在日本展出 | Put source in source detail. |
| 记录在册的首次画廊个展 | 首场已记录的画廊个展 | Records may be incomplete; do not claim life first unless established. |
| 记录在册的首次国际（英国）展出 | 首次已记录的英国展出 | Japan was already international relative to China. |
| 东京个展——记录在册的最新一场 | 东京个展 | April show is no longer latest. Latest badge must be computed, not translated from stale prose. |
| Third solo exhibition on record, and your first at a Harajuku gallery. Closed 6 September 2026. | 第三场已记录的个展，于 2026 年 9 月 6 日结束。 | Remove first-Harajuku inference unless substantiated. Her earlier Harajuku show was a group show. |
| August 25 – September 6, 2026 | 2026 年 8 月 25 日至 9 月 6 日 | Locale formatting from dates, not exact English sentence matching. |
| + 添加展览 | ＋ 添加展览记录 | Optional; keep secondary. |

**All 13 exhibition rows were read.** Preserve official titles and dates unless the specific changes above apply. Standardize location displays: 上海／广州／杭州／深圳／南京／天津／台州／东京／伦敦. Show a useful venue name with city; a complete romanized street address does not belong on the overview row. Preserve the full address in optional detail if needed. Use official `Galerie LE MONDE` consistently instead of alternately `Lemonde Tokyo`. Do not machine-translate book titles such as `defined Definition 02: A Documented Journey`; verify title typography separately.

## All ten peer cards

Sources: `api.py` → `peer_artists`; upstream seed/peer engine and translation cache; `SaffronPage.jsx` `SF_ZH_PEERS`. Several English originals were updated without updating exact-string translation keys. These are Chinese replacements for the prose displayed in this snapshot, not new biographical research. Memberships, client lists and sales totals should be retained only with dated primary sources. Research value comes from a concrete work or publishing example, not a generic fame summary.

Opening changes:

- **你身处优秀的同道之中** → **可参考的创作与出版案例**.
- **与你领域相近的优秀艺术家——是同道，而非高下的比较。** → **按作品题材、出版或合作方式，看看哪些经验可供参考。**
- **10位在相邻领域工作的艺术家 — 参照坐标，非直接比较** → **10 位创作者，各有可参考的作品或工作方式**.
- **这些是与你气味相投的同行，依据真实的重合挑选——每日水彩、日常生活、由线上走向出版的路径——而不是一份排名。有的在风格上与你相近，有的是事业路径上的参照；每条说明都会注明是哪一种。** → **下面分别说明可以参考的部分：有的是建筑与水彩的表现，有的是出版、委托或教学的工作方式。具体作品和案例比整体比较更有用。**
- **参照用途：** → **可以参考：**.

| Artist | Current description / problem | Replacement description | Replacement “可以参考” |
|---|---|---|---|
| Chien Chung-Wei（簡忠威） | 氛围感的城市与室内水彩，安静的场景，扎实的色调掌控。从台湾出发，通过 IWS 赛事建立了国际信誉。 / “首要事业路径参照” | 城市与室内题材的水彩作品，注重光线、色调与空间氛围。 | 城市水彩中的光线与空间处理，以及有明确来源的展览经历。 |
| 木内達朗 | Entire description remains English: “Atmospheric space for book jackets, editorial and advertising … Works without an agent; commissions come direct.” | 可研究他如何将空间与氛围用于书籍封面、编辑插画和广告项目。具体合作案例可从作品资料中查看。 | 不同委托项目的作品呈现和作品集组织。 |
| Thomas W. Schaller | 建筑水彩——楼宇、城市光线、氛围、安静的结构观察。富戏剧性情绪的大尺幅建筑习作。 | 以建筑、城市光线和空间为题材，画面常有鲜明的明暗与氛围变化。 | 建筑题材的构图、明暗与水彩表现。 |
| Cathy Read | 英国建筑水彩画家，以爱丁堡及英国城市场景著称。曾在伦敦及国际展出。 | 以城市建筑为题材，可以进一步查看其作品展示与销售方式。 | 建筑作品如何分类、介绍和直接销售。 |
| Mateusz Urbanowicz | Entire updated description remains English; includes 100k sales, “Sells originals himself, no gallery.” | 以东京店面、街景与建筑为题材创作水彩，并与 MdN 合作出版相关画集。 | 一个城市题材如何形成选题、样页和完整画集。 |
| Keiko Tanabe | 日本水彩画家，城市与旅行题材，轻盈而含蓄的氛围。曾参与 AWS 与 NWS 展览——扎根日本而具国际能见度的身份。 | 城市与旅行题材的水彩创作，可以结合其公开的展览和教学资料一起了解。 | 旅行题材的作品整理，以及展览与教学的安排。 |
| Lian Quan Zhen | 出生于中国的水彩画家，将中国水墨的感性与西方水彩技法融合。AWS 会员。 / “中国训练背景” | 可研究其水彩与水墨表现，以及围绕作品展开的出版和教学资料。 | 不同绘画方法如何用于作品、图书或课程介绍。 |
| Alvaro Castagnet | 城市水彩，风格松动而富氛围；从非西方根基建立了扎实的国际展览记录。AWS 签名会员。 | 城市题材的水彩作品，笔触自由，色彩与明暗对比鲜明。 | 城市水彩的画面处理，以及有来源的展览案例。 |
| Jean Haines | 英国知名水彩从业者与作者。风格松动而富表现力——与你安静的城市气质截然不同。仅作社群参照。 / “请勿用作风格参照或审美比较” | 以自由的水彩表现、图书与教学内容为人所知。这里主要关注其出版和教学的组织方式。 | 图书与课程如何围绕一种绘画方法展开。 |
| Ohn Mar Win | English income description: “Twenty-year practice … teaching 77%, licensing 3% … clearest evidence … what each route actually pays.” | 曾公开分享个人收入构成，可以作为教学与授权如何组合的个案。引用比例时需同时列出年份与统计范围。 | 一位创作者的收入组合；不能据此推算行业水平或你的收入。 |

Repeated peer-trait replacements (apply to every occurrence):

| Current | Replacement |
|---|---|
| 风格松动／氛围松动的水彩 | 笔触自由／注重氛围的水彩 |
| 水彩从业者 | 水彩创作者 |
| 安静的观察 | 日常观察 |
| 立足亚洲的事业／从非西方根基发展的国际事业 | 展览与合作经历（only if sourced; otherwise omit） |
| 国际信誉 | 国际展览经历（when that is what was actually measured） |
| 以情绪为先的手法 | 注重氛围的表现 |
| 基于观察的实践 | 观察与写生 |
| 中国艺术训练背景 | Delete as shared trait unless both artists' training is relevant and verified |
| 与日本相连的身份 | 日本相关的创作与活动（only if precise and useful） |
| atmosphere and quiet observation | 空间氛围与日常观察 |
| illustration-side practice | 插画创作 |
| interior and exterior space | 室内与户外空间 |
| Tokyo as subject | 东京题材 |
| books from a daily practice | 由日常创作整理的出版物 |
| audience-funded income | 面向读者的销售与课程（specify actual mechanism） |
| self-published numbers | 创作者公开的数据 |
| JAPAN (TOKYO) | 日本（东京） |

Clear labels such as 建筑题材、城市与旅行水彩、出版与教学路径 can stay. All peer names should link through stable artist IDs; full-width parentheses in the localized 簡忠威 name currently prevent the verified Instagram lookup from matching, sending her to search instead.

## Press section

Source: `api.py` → `press_features`, `SaffronPage.jsx` → `PressFeatures` and localization maps.

| Current | Replacement | Reason |
|---|---|---|
| {n}个线上报道 | {n} 篇已记录的报道 | Correct classifier; evidence count must match ladders. |
| 曾报道过你作品的媒体与博客，以及下一步的投稿目标。 | 已有作品报道，以及可进一步研究的媒体。 | Potential editorial target is not confirmed submission route. |
| 已确认报道 | 已记录的报道 | Link is known; do not overstate independent validation. |
| 作品报道 | 作品介绍 | Accurately labels image-led feature. |
| 水彩作品的视觉报道——受众广泛，但无人物深度 | 以水彩作品展示为主的介绍文章。 | Do not diminish an achievement or invent reach. |
| 作品报道（第二部分） | 作品介绍（二） | Natural concise label. |
| 对同一批作品的后续报道 | 后续作品介绍。 | Same batch should not be asserted without inspection. |
| 投稿目标 | 可研究的媒体 | Separate verified open-submission outlets later. |
| 日本最重要的当代艺术刊物 | 日本当代艺术媒体。 | No subjective superlative. |
| 设计与艺术，对插画友好，东京读者群 | 关注设计、艺术与生活方式的媒体。 | Editorial friendliness and reader geography need evidence. |
| 全球首屈一指的英语插画师发掘平台 | 关注设计与插画的英语媒体。 | Remove ranking and discovery promise. |
| 家居室内与日常生活——与你的题材直接契合 | 关注居住空间与日常生活，可比较其具体选题。 | Topic match is a research lead, not guaranteed editorial fit. |
| 庞大的插画／摄影社群；有可投递的年度书籍奖项 | 艺术与视觉文化平台；具体征集需查看当届公告。 | Preserve painting fit; verify actual annual book mechanism before telling her to apply. |

Keep both Bored Panda articles and their existing links as separate records. Whether Design You Trust is also part of the confirmed record needs a single-source reconciliation, not a Chinese-only count patch.

## Coverage boundary

This is a full editorial pass on the currently mounted Saffron interface, authored research copy, all 24 ladder states and their expanded text, all recurring-program definitions, four rendered grant cards, all ten peer cards, all 13 exhibition records, press labels, and the 52 venue rows covered in report 06. The arbitrary opportunity catalogue feeding the date strip is not a fixed authored text set: 1,185 records were served in the observed session. Every such catalogue title/description across every month has **not** been independently translated or fact-checked in this review. The date-strip failures and visible malformed/irrelevant entries are recorded in the brief and need a dedicated data-quality rule. This review does not call unmounted collaboration/collector/revenue components live defects.
