# Saffron Chinese: naturalness only

11 September 2026 · current source snapshot `cf3881b0` · checked against the rendered Chinese Saffron.

## Overall judgment

The Chinese is noticeably smoother after the latest pass. Most of the longer paragraphs already sound like an articulate person talking to an artist. The remaining roughness is concentrated in short summaries, heavily compressed noun phrases, a few English-shaped metaphors, and the formal language of the venue tracker.

For the reader you described—a 26-year-old artist from Beijing—I would use contemporary mainland written Mandarin: direct, relaxed, intelligent, with room for the page's literary touches. There is no need to add Beijing slang or imitate how she personally speaks. An artist-facing reference can be more polished than a chat message and still sound natural.

This review preserves the existing message. It does not reassess prices, dates, eligibility, strategy, factual confidence, emotional framing or what she should do. Numbers and conditions remain as written. Confident claims stay confident; metaphors stay unless their Chinese syntax is the problem. No production files have been changed.

The suggestions below are **local replacements**. Replace only the quoted span and keep its surrounding text. A few rows quote a whole sentence or paragraph where the word order is the issue. “Optional” means the current Chinese is acceptable and the alternative is a preference, not a correction.

## What should stay

These work in Chinese and should not be flattened into generic professional prose:

- **安静的钱。** Short, evocative and easy to understand in context.
- **这样的门，只会从另一边打开。** The metaphor lands naturally.
- **五到十张，一个授权作品集的开头就有了。** Conversational and concrete.
- **趁还没有人来问先写好。** Natural spoken rhythm.
- **帮你抬价的那个人，自己也靠这个吃饭。** Direct, colloquial Chinese with a clear point.
- **一个下午的事 / 要动手做的活 / 自己扛 / 等谁点头。** These belong to the current voice; formality would not improve them.

Terms such as **受众、图像授权、艺术总监、作品集、开本、寄售** are normal in this context. They do not need to be replaced just because the reader is young. Likewise, **首屈一指** is natural Chinese; whether its claim is supported is outside this pass.

## Sentence-level suggestions


### 1. Directions and the opening

| # / location | Current span | Smoother wording | Why |
|---|---|---|---|
| 1<br>[futures_engine.py:220](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:220) | 你已经有一套运转起来的创作和生意——六年的画、一批固定的观众、直接销售、委托，还有一份展览履历——所以现在值得问的是：换一条路，能拿到什么现在这条路上拿不到的东西。 | 你的创作和生意都已经运转起来了：六年的画、一批固定的观众、直接销售、委托，还有一份展览履历。所以现在值得问的是：换一条路，能得到什么现在这条路上得不到的东西。 | Removes the awkward 一套…创作和生意 and the long sentence interrupted twice. Keeps every item, the business framing and the question. |
| 2 · Optional<br>[futures_engine.py:220](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:220) | 往里面再加东西，至少要做到其中一件： | 在现有的基础上再加一项，至少要做到其中一件： | Gives 里面 a clear referent; the four requirements following the colon stay exactly as they are. |
| 3<br>[futures_engine.py:274](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:274) | 新形态里哪一样开始稳定出货，再转批量生产，那是第二步。 | 哪种新产品开始稳定出货了，再转成批量生产，那是第二步。 | 新形态 sounds abstract here; the same products and sequence remain. |
| 4<br>[futures_engine.py:310](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:310) | 书是另一个层面的决定 | 做书，是另一个层面的决定 | A book is an object; making one is the decision. Small grammatical completion. |
| 5<br>[futures_engine.py:341](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:341) | 如果这本书是当商品卖，在查过的几种做法里，中国印的精装本账最划算。 | 如果这本书是当商品卖，在查过的几种做法里，算下来还是在中国印精装本最划算。 | 账最划算 is a strained collocation. Keeps the same strongest-value claim and comparison scope. |
| 6<br>[futures_engine.py:356](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:356) | 一批印量能不能把钱赚回来 | 印一批书，能不能把钱赚回来 | 印量 is a quantity, not a batch of objects. |
| 7<br>[futures_engine.py:500](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:500) | 或者11 月 7、8 日本人送去 | 或者在 11 月 7 日、8 日亲自送去 | Prevents 日本人 from being read as “Japanese person.” Dates and personal delivery are unchanged. |
| 8 · Optional<br>[futures_engine.py:665](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:665) | 值得专门去应对的，是构图上的要求。 | 值得专门考虑的，是构图上的要求。 | 应对要求 is stiff in this sentence; 考虑要求 carries the same practical point. |
| 9<br>[futures_engine.py:665](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:665) | 能围着它做封面的图 | 能用来设计封面的图 | Replaces an English-shaped “design around it” construction. |
| 10<br>[futures_engine.py:735](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:735) | 一段排好顺序的样张 | 一组排好顺序的样张 | 一组 matches pages/samples; 一段 normally counts a passage or stretch. |
| 11<br>[futures_engine.py:749](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:749) | 论每本能拿多少，出版是弱的；论发行，它是强的。 | 论每本能拿多少钱，出版社出版不占优势；论发行，它有优势。 | Natural Chinese comparison while retaining both the weak and strong sides. |
| 12 · Optional<br>[futures_engine.py:769](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:769) | 这些好处才最值 | 这些好处才最有价值 | Completes the adjective without changing the preceding condition. |
| 13<br>[futures_engine.py:769](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:769) | 一批印量要卖掉多少才回得来 | 一批书要卖掉多少本才能回本 | Makes the counted object and 回来 referent explicit. |
| 14<br>[futures_engine.py:836](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:836) | 经手工作的平均值 | 经手项目的平均费用 | The table is about fees: supplies the missing object of 平均值. |
| 15<br>[futures_engine.py:884](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:884) | 一个你能稳定报价的问题 | 一个你能给出稳定报价的问题 | 报价 is not naturally modified by 稳定 in that verb construction. |
| 16 · Optional<br>[futures_engine.py:923](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:923) | 而且它们大小不一样 | 而且事情的大小也不一样 | Refers naturally to task size; the two-afternoon/three-making distinction is retained. |
| 17<br>[futures_engine.py:932](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:932) | 一张装裱的 A4 印刷 | 一张装裱好的 A4 印刷品 | 印刷 names a process; the sentence needs 印刷品, the object. |
| 18<br>[futures_engine.py:935](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:935) | 把一个五张同系列作品的链接准备好 | 准备好一个包含五张同系列作品的链接 | Removes the stacked classifiers 一个五张; no extra material is requested. |
| 19<br>[futures_engine.py:941](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:941) | 把已有的一组作品，写成一页纸的书的构想 | 把已有的一组作品，整理成一页纸的出书构想 | Reduces stacked 的 and fixes the artwork-to-written-concept construction. |
| 20<br>[futures_engine.py:1001](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1001) | 作品通过你自己的店铺出去 | 作品通过你自己的店铺卖出去 | Supplies the missing sales verb; same channel and activity. |
| 21<br>[futures_engine.py:1017](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1017) | 整个毛利都归你。 | 全部毛利都归你。 | 全部 is the normal collocation with an amount such as 毛利. |
| 22<br>[futures_engine.py:1017](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1017) | 价格是你定的，不需要替它争取 | 价格是你定的，不用再跟谁争取 | 替它争取 sounds translated; retains the claim that she need not negotiate for her chosen price. |
| 23<br>[futures_engine.py:1170](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1170) | 题材、进度和最终画面不再完全是你的。 | 题材、进度和最终画面，不再完全由你决定。 | Completes the intended point about creative control in this paragraph. |
| 24<br>[futures_engine.py:1199](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1199) | 自己的店，自己定价，成本之上全归你。 | 自己的店，自己定价，扣掉成本，剩下的全归你。 | 成本之上 is an English-shaped phrase; all financial claims are preserved. |
| 25 · Optional<br>[futures_engine.py:1291](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1291) | 还有六年每天画下来的画，够从里面做出一本书。 | 还有六年来每天画下来的作品，足够从中做出一本书。 | Avoids 画下来…画 and supplies the natural time marker 六年来. |
| 26<br>[futures_engine.py:1295](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1295) | 六年每天按时把画交出来，以及一个题材——会被日本的文学类出版社买去做封面。 | 六年来，你每天都按时把画交出来；你的题材也会被日本的文学类出版社买去做封面。 | Turns two disconnected noun/verb fragments into two sentences with subjects. Keeps the daily delivery and publishing claims. |

### 2. Book economics

| # / location | Current span | Smoother wording | Why |
|---|---|---|---|
| 27 · Optional<br>[book_economics_engine.py:78](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:78) | 这些是报给英语使用者的价格；同一份规格用中文去问，是另一个价格。 | 这些是给英语使用者的报价；同样的规格，用中文去问，价格就不一样。 | Smoother collocations. Does not add a promise of a lower price or change the existing price-difference claim. |
| 28<br>[book_economics_engine.py:269](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:269) | 做一本书要花多少钱，可以在开始之前精确到日元算出来；能卖多快，则完全算不出来。一头是固定的价钱，另一头是没有底的销售速度——要决定的全部就是这个落差，而把这个落差接过去，正是出版社的作用。 | 做一本书要花多少钱，在开始之前就能算出来，精确到日元；能卖多快，则完全算不出来。一边是确定的费用，另一边是没法确定的销售速度——做决定时要考虑的，就是这个落差。而承担这份不确定性，正是出版社的作用。 | Fixes the order of 精确到日元 and the awkward 没有底的销售速度 / 要决定的全部 / 把落差接过去. Preserves the paragraph’s certainty and its account of the publisher’s role. |
| 29<br>[book_economics_engine.py:284](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:284) | 这批印量就付清了 | 这批书的印制成本就收回来了 | Natural wording for the same recovery point; does not change the count or the 净赚 claim that follows. |
| 30 · Optional<br>[book_economics_engine.py:329](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:329) | 没有要收回的钱 | 没有需要收回的前期投入 | Expresses the same zero-upfront-investment point more naturally in this table. |
| 31<br>[book_economics_engine.py:364](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:364) | 这几条路里能满足的是 | 这几条路里，能满足这一条件的有 | Supplies the object of 满足 and introduces the following list cleanly. |

### 3. Strategy ladders

| # / location | Current span | Smoother wording | Why |
|---|---|---|---|
| 32 · Optional<br>[strategy_ladders.js:STATES.g_publication.detail](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 从每日日记的实践里长出来 | 从每天画日记这件事里长出来 | Keeps 长出来 and the same daily activity; removes the literal academic translation of practice. |
| 33<br>[strategy_ladders.js:STATES.g_solo.label](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 个展，包括在东京 | 个展，也包括在东京办的 | Completes the location phrase without changing the record. |
| 34<br>[strategy_ladders.js:STATES.a_look.label](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 缩略图大小也认得出的面貌 | 缩成缩略图也认得出的画风 | 画风 is natural for the recognizable look of paintings. |
| 35<br>[strategy_ladders.js:STATES.a_look.detail](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 那种面貌必须自己立得住 | 那种画风必须自己立得住 | Keeps the figurative 立得住 and changes only the noun to match the heading. |
| 36<br>[strategy_ladders.js:STATES.a_found.detail](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 也是这条阶梯往上乘算的基数 | 也是后面各级计算增长时的基数 | 乘算 attached directly to 阶梯往上 is hard to parse. Keeps the numerical-base argument. |
| 37<br>[strategy_ladders.js:STATES.a_motion.treatment.blocks.1.text](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 这一级只是你每天都要坐的那张桌子的副产品 | 这一级只是你每天坐在那张桌前画画时，顺带留下的东西 | The by-product comes from painting at the desk, not from the desk itself. |
| 38<br>[strategy_ladders.js:STATES.a_motion.treatment.blocks.4.text](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 看到这种面貌是手工做出来的 | 看到这种画风是手工画出来的 | Uses painting vocabulary for the same handmade-style claim. |
| 39<br>[strategy_ladders.js:STATES.a_weekly.label](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 让作画视频抵达那些从没看过的人 | 让从没看过的人也能看到你的作画视频 | Videos reach people naturally in English; the reordered Chinese is smoother. |
| 40<br>[strategy_ladders.js:STATES.a_weekly.treatment.blocks.0.label](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 短视频是长视频的 8.5 倍 | 短视频的播放量是长视频的 8.5 倍 | Names the quantity being compared; preserves 8.5 and the qualification after the dash. |
| 41<br>[strategy_ladders.js:STATES.a_weekly.treatment.blocks.0.text](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 播放中位数 | 播放量的中位数 | Completes the noun; no statistics change. |
| 42<br>[strategy_ladders.js:STATES.a_weekly.treatment.blocks.2.text](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 受众会涨 | 受众会增加 | 涨 works with 粉丝数; 增加 collocates better with 受众. |
| 43<br>[strategy_ladders.js:STATES.a_borrowed.label](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 出现在别人的受众里 | 出现在别人的受众面前 | People are the audience, not a container. |
| 44<br>[strategy_ladders.js:STATES.a_second.treatment.blocks.2.label](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 视频放在这里的位置 | 视频在这里起什么作用 | Natural Chinese heading for the role described below. |
| 45<br>[strategy_ladders.js:STATES.a_second.treatment.blocks.4.text](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 五个账号之间有多少是同一批人，没有量过 | 五个账号之间有多少人是重复关注的，还没有统计过 | Natural wording for the same unmeasured overlap; all following totals and interpretations are retained. |
| 46<br>[strategy_ladders.js:STATES.l_reproduces.detail](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 授权真正会买的品类 | 授权客户真正会买的品类 | Supplies the buyer as the grammatical subject. |
| 47<br>[strategy_ladders.js:STATES.l_inbound.detail](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 有常设的“艺术家系列”（アーティストコレクション）手账封面系列 | 有常设的“艺术家系列”（アーティストコレクション）手账封面 | Removes the doubled 系列 while preserving the official title. |
| 48<br>[strategy_ladders.js:GOALS.2.why.a_look](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js) | 一种能铺开成一整条产品线的面貌 | 一种能延展成一整条产品线的画风 | Natural wording for the same style/product-line connection; preserves the rest of the argument. |

### 4. Recurring calls

| # / location | Current span | Smoother wording | Why |
|---|---|---|---|
| 49<br>[recurring_calendar_engine.py:132](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:132) | 要能从远处一眼看到的作品 | 作品要让人从远处一眼就能看到 | Reorders the sentence instead of adding an attention-grabbing requirement. |
| 50<br>[recurring_calendar_engine.py:148](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:148) | 一面完整连贯的墙 | 一面作品完整、连贯的展示墙 | Makes clear that 完整连贯 describes the displayed work, not the physical wall. |
| 51<br>[recurring_calendar_engine.py:197](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:197) | 外加六周工作室 | 外加六周的工作室使用时间 | Completes the duration phrase; keeps six weeks. |
| 52<br>[recurring_calendar_engine.py:234](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:234) | 所以中日交流展是以日本这一边的部分符合条件 | 所以中日交流展中，在日本开展的那部分符合条件 | Removes the malformed 是以…的部分 structure; preserves the same geographic condition. |
| 53<br>[recurring_calendar_engine.py:238](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:238) | 这个项目的结构就是两个地方 | 这个项目本身就涉及两地 | Natural wording for the same two-location structure. |
| 54<br>[recurring_calendar_engine.py:291](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:291) | 在两地之间移动对作品做了什么 | 往返两地给作品带来了什么变化 | Keeps the question; removes the literal 对作品做了什么. |

### 5. Grant cards

| # / location | Current span | Smoother wording | Why |
|---|---|---|---|
| 55<br>[saffron_insights.js:GRANT_LANDSCAPE.items.0.why_apply_zh](C:/ScottStuff/GalleryAgentAI/frontend/src/data/saffron_insights.js) | 在一个公立机构做一个个展 | 在一家公立机构办一场个展 | Natural classifiers and exhibition verb; the rest of the sentence stays. |
| 56 · Optional<br>[saffron_insights.js:GRANT_LANDSCAPE.items.1.eligibility_zh](C:/ScottStuff/GalleryAgentAI/frontend/src/data/saffron_insights.js) | 有一件事没有任何地方写明 | 有一件事，哪里都没有写明 | Smooths the double noun phrase without weakening 没有任何地方. |
| 57<br>[saffron_insights.js:GRANT_LANDSCAPE.items.1.tip_zh](C:/ScottStuff/GalleryAgentAI/frontend/src/data/saffron_insights.js) | 项目里算得上合规支出的那部分 | 项目中符合规定的那部分支出 | Same eligible-expense condition, smoother syntax. |
| 58<br>[saffron_insights.js:GRANT_LANDSCAPE.items.2.eligibility_zh](C:/ScottStuff/GalleryAgentAI/frontend/src/data/saffron_insights.js) | 需要属于官方列出的 26 个国家或地区（包括美国）之一的国籍或永久居留权 | 需要拥有官方列出的 26 个国家或地区（包括美国）之一的国籍或永久居留权 | 拥有 takes 国籍/居留权 as its object; 属于 does not. |
| 59<br>[saffron_insights.js:GRANT_LANDSCAPE.items.2.eligibility_zh](C:/ScottStuff/GalleryAgentAI/frontend/src/data/saffron_insights.js) | 在受资助的奖学金期间 | 在奖学金资助期间 | Removes the redundant and tangled modifier. |
| 60<br>[saffron_insights.js:GRANT_LANDSCAPE.items.3.why_apply_zh](C:/ScottStuff/GalleryAgentAI/frontend/src/data/saffron_insights.js) | 这是这页上唯一一条核实过、确实存在的中国国籍途径。 | 这是这页上唯一一条核实过、确实存在、面向中国公民的申请途径。 | 中国国籍途径 is not a natural noun phrase. Keeps 唯一, 核实过 and 确实存在. |

### 6. Interface and overview

| # / location | Current span | Smoother wording | Why |
|---|---|---|---|
| 61<br>[SaffronV2.jsx:52](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronV2.jsx:52) | 自 ${d} 起没有新的。检索大约每月一次。 | 自 ${d} 起暂无新增。检索大约每月一次。 | Supplies a natural noun-like 新增; preserves the monthly-search statement. |
| 62<br>[SaffronV2.jsx:55](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronV2.jsx:55) | ${served} 条中有 ${ahead} 条带着可读的日期，其余的没有日期，或已经过去。 | ${served} 条中有 ${ahead} 条带有可识别的日期，其余的没有日期，或日期已经过去。 | Dates are 带有, not 带着; clarifies the subject of 已经过去. No count/category changes. |
| 63<br>[SaffronV2.jsx:78](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronV2.jsx:78) | 暂无有日期的条目 | 暂无带日期的条目 | Avoids the awkward adjacent 无有. Apply the same wording inside 本月暂无有日期的条目。 |
| 64<br>[SaffronV2.jsx:81](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronV2.jsx:81) | 下面的门仍会轮到。 | 下面这些门还会依次打开。 | Keeps the doors metaphor and promised recurrence; fixes the incomplete 轮到. |
| 65 · Optional<br>[SaffronPage.jsx:798](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:798) | 重叠的事项 | 有重合的事项 | More natural collocation; leaves the shared-task structure intact. |
| 66<br>[SaffronPage.jsx:1090](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:1090) | 要准备好的 | 需要准备什么 | Natural section label for the unchanged requirements below. |
| 67<br>[SaffronPage.jsx:1091](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:1091) | 时间为估计 | 预计时间 | Idiomatic compact label for the same estimated timing. |
| 68<br>[SaffronPage.jsx:1646](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:1646) | 整条＝那一种印法印出来的数量；填色的部分＝要卖掉多少才回本。填色漫出右边，表示整批卖光之后成本仍有缺口。 | 整条表示按这种印法印出的总数；填色部分表示要卖掉多少本才能回本。填色超出右边，表示整批卖光后仍有成本没收回来。 | Natural chart explanation; preserves the bar, filled area, overflow and unrecovered-cost meanings. |
| 69<br>[SaffronPage.jsx:148](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:148) | 群体出版物，供稿者 | 合作出版物，参与供稿 | Natural credit wording without adding an authorship claim. |
| 70<br>[translations.js:491](C:/ScottStuff/GalleryAgentAI/frontend/src/i18n/translations.js:491) | {n}个线上报道 | {n}篇线上报道 | 篇 is the normal classifier for an article. |
| 71<br>[translations.js:445](C:/ScottStuff/GalleryAgentAI/frontend/src/i18n/translations.js:445) | 依据真实的重合挑选 | 按你们确实相通的地方挑选 | Keeps the claim of actual overlap, with a natural Chinese noun phrase. |

### 7. Peer and press descriptions

| # / location | Current span | Smoother wording | Why |
|---|---|---|---|
| 72<br>[SaffronPage.jsx:118](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:118) | 氛围感的城市与室内水彩 | 富有氛围感的城市与室内水彩 | Adds the missing modifier 富有. |
| 73<br>[SaffronPage.jsx:122](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:122) | 富戏剧性情绪的大尺幅建筑习作 | 大尺幅的建筑习作，画面情绪富有戏剧性 | Natural word order; retains the emotional quality, dramatic character and scale. |
| 74<br>[SaffronPage.jsx:120](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:120) | 扎根日本而具国际能见度的身份 | 扎根日本、同时在国际上受到关注 | Removes the unnatural identity-as-visibility construction; retains both parts. |
| 75<br>[SaffronPage.jsx:121](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:121) | 以日本为出身 | 从日本出发 | Natural phrasing for the same origin/career-path context. |
| 76<br>[SaffronPage.jsx:130](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:130) | 风格松动而富氛围 | 风格松弛，富有氛围感 | 松动 suggests loosening or coming unstuck; 松弛 describes the same loose visual style naturally. |
| 77<br>[SaffronPage.jsx:140](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:140) | 氛围松动的水彩 | 松弛、有氛围感的水彩 | Separates the style and atmosphere modifiers. |
| 78<br>[SaffronPage.jsx:132](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:132) | 风格松动而富表现力 | 风格松弛，富有表现力 | Same stylistic claim, natural collocation. |
| 79<br>[SaffronPage.jsx:266](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:266) | 水彩作品的视觉报道——受众广泛，但无人物深度 | 以水彩作品展示为主的报道——受众广泛，但没有深入介绍创作者本人 | Clarifies the same image-led feature and lack of biographical depth; retains both judgments. |
| 80<br>[SaffronPage.jsx:110](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:110) | 有可投递的年度书籍奖项 | 有可报名的年度书籍奖项 | One applies for an award rather than delivering it. |

### 8. Repeated venue wording

| # / location | Current span | Smoother wording | Why |
|---|---|---|---|
| 81<br>[translation_cache.json:B&B / TABF / UTRECHT research template](C:/ScottStuff/GalleryAgentAI/memory/translation_cache.json) | 具名联系人 | 有明确姓名的联系人 | 具名 is legal/administrative diction here. Keeps the requirement for a named contact. |
| 82<br>[translation_cache.json:flotsam / Book and Sons / COW BOOKS / Books Ruhe / tata](C:/ScottStuff/GalleryAgentAI/memory/translation_cache.json) | 浏览其线上库存 | 看看网店里的在售商品 | 库存 sounds like an inventory system; preserves browsing stock without narrowing it to books. |
| 83<br>[translation_cache.json:Bookshop visit template](C:/ScottStuff/GalleryAgentAI/memory/translation_cache.json) | 确认风格契合度 | 确认风格是否合适 | Natural phrasing for the same fit check. |
| 84<br>[translation_cache.json:Cafe/gallery visit template](C:/ScottStuff/GalleryAgentAI/memory/translation_cache.json) | 实地察看展示空间，并与负责人洽谈近期展览档期 | 实地看看展示空间，再和负责人谈谈近期的展览档期 | Preserves the visit, responsible person and scheduling discussion; removes official-report diction. |
| 85<br>[translation_cache.json:MOUNT ZINE / Tacoche](C:/ScottStuff/GalleryAgentAI/memory/translation_cache.json) | 请将作品实体样本邮寄或亲自送至 | 请把作品的实物样本寄过去，或亲自送到 | Natural mainland phrasing; preserves the two physical-delivery options. |
| 86<br>[translation_cache.json:Design Festa / ERA / reload](C:/ScottStuff/GalleryAgentAI/memory/translation_cache.json) | 在正式接洽之前 | 正式联系前 | Same timing and action, lighter register. |
| 87<br>[translation_cache.json:Design Festa / reload](C:/ScottStuff/GalleryAgentAI/memory/translation_cache.json) | 观察其策展风格与受众群体 | 看看他们的策展风格，以及受众是什么样的人 | Smoother sentence about the same curatorial style and audience. |
| 88<br>[translation_cache.json:Gallery 456](C:/ScottStuff/GalleryAgentAI/memory/translation_cache.json) | 这是未来目标，暂不紧迫 | 这是以后的目标，现在不急 | Keeps the existing lack of urgency without adding new advice. |
| 89<br>[translation_cache.json:Komiyama](C:/ScottStuff/GalleryAgentAI/memory/translation_cache.json) | 一份附有样页的针对性提案 | 一份有针对性的提案，附上样页 | Unstacks the modifiers; preserves both targeting and sample pages. |

## Two small presentation details

- The calendar currently displays **9月 2026**. **2026 年 9 月** is the natural Chinese order; the date itself is unchanged.
- Render the preparation label as **需要准备什么：**, with no extra spaces around the full-width colon. The current spacing produces **要准备好的 ：**.

## Scope and use

Read: the five directions and their expanded text; book economics and publisher comparison; all 24 ladder states and their expanded treatments; all recurring-call definitions; the four visible grant cards; the current interface; the overview and exhibition copy; the ten live peer cards; press; and all 52 visible venue rows. The Japanese draft letter was left alone. Unmounted legacy sections were excluded. English text that is still displayed in Chinese mode has not been newly translated here; that would be a separate translation-completion pass.

The 436-unit source inventory includes neutral labels/numbers and 11 unmounted fields. Reading an item does not mean it needs rewriting. Only selected awkward spans are listed above, and repeated venue sentences are handled as shared wording patterns. These suggestions do not alter the actions, urgency, fit judgments or conditions in those rows.

For any later implementation, preserve the unquoted text and interpolation fields. Apply recurring wording at its authored source or translation rule rather than hand-editing regenerated cache data. The source links are locators for review, not a request to modify every linked file.

This replaces the earlier review as the **language-only** recommendation. The earlier content/strategy rewrite proposals are not incorporated here.
