# Saffron Chinese audit — engine-owned copy

2026-09-10. Exact source wording is preserved below. Line numbers refer to this review snapshot. This is an editorial proposal, not a production patch.

Every `_t(en, zh)` unit in the three active content engines was read. Neutral names, quantities, currencies and already-clear labels are retained unless flagged. A retained numeric literal is **not** factual approval: numeric tables remain subject to the model/source blockers in the improvement brief. “Hold” entries provide safe draft wording but must not be shipped with the old model. English must be corrected alongside Chinese wherever the underlying claim changes.

For f-strings, `{...}` preserves the source expression; implementers must retain real interpolation rather than paste expressions into the UI.


## engines/futures_engine.py


### futures_engine.py · 001 · Rewrite

[engines/futures_engine.py:220](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:220)

**Current**

> 你已经有一套跑起来的创作和生意——六年的画、一批固定的观众、直接销售、委托，还有一份展览履历——所以现在值得问的是：换一条路，能拿到什么现在这条路上拿不到的东西。
> 
> 一张原作已经能卖到 31,900–115,500 日元，后面所有的账都拿这个数来比。往里面再加东西，至少要做到其中一件：让画完的作品再挣一次钱，卖给你自己够不着的买家，把其余作品的价钱一起带上去，或者不必再画一张原作也能有收入。


**Replace with**

你从 2020 年开始持续画水彩日记，也已经有了出版物、个展和自己的店铺。这些积累，可以继续用于出版、画廊合作和图像授权。

下面整理了几种合作方式的收入来源、准备工作与实际入口，方便你比较：哪一种能用上现有作品，又符合接下来的创作安排。


**Reason:** Recognize concrete work; remove awkward business metaphor, false either/or route choice, and the requirement that every creative choice monetize.


### futures_engine.py · 002 · Rewrite

[engines/futures_engine.py:237](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:237)

**Current**

> 2,200 到 31,900 日元之间的空档


**Replace with**

印刷品与原作之间，可以尝试什么价位


**Reason:** Turn a supposed deficiency into a research question.


### futures_engine.py · 003 · Rewrite

[engines/futures_engine.py:239](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:239)

**Current**

> 两头你都卖得动：明信片、zine、印刷品在 1,100–2,200 日元，原作从 31,900 日元起。断掉的是中间那一段。一个买过 zine、买过印刷品的人，在你这里花不掉 5,000、10,000 或者 20,000 日元——再往上就直接是原作了。最省事的办法，是先把中间那段补上，而且不用先囤货。


**Replace with**

目前记录中的明信片、zine 和印刷品标价为 1,100–2,200 日元，原作从 31,900 日元起。中间价位可以作为一个产品试验方向，例如尺寸更大的艺术微喷或装裱印刷品。是否值得做，还需要比较样品质量、制作成本和实际订单。


**Reason:** Listed prices do not prove both ends sell. A price gap does not establish demand; multiple-item orders are also possible.


### futures_engine.py · 004 · Rewrite

[engines/futures_engine.py:253](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:253)

**Current**

> 可以先做的三样东西


**Replace with**

三种可比较的产品方案


**Reason:** Avoid commissioning three products as an implied instruction.


### futures_engine.py · 005 · Retain wording

[engines/futures_engine.py:254](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:254)

**Current**

> 


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 006 · Retain wording

[engines/futures_engine.py:254](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:254)

**Current**

> 售价


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 007 · Rewrite

[engines/futures_engine.py:254](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:254)

**Current**

> 你拿到


**Replace with**

每件预计结余


**Reason:** You take home is not net profit; define included deductions next to table.


### futures_engine.py · 008 · Hold for model correction

[engines/futures_engine.py:254](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:254)

**Current**

> 毛利率


**Replace with**

结余占售价比例


**Reason:** Only use once numerator and denominator reconcile; see pricing blocker in brief.


### futures_engine.py · 009 · Retain wording

[engines/futures_engine.py:256](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:256)

**Current**

> A2 海报


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 010 · Retain wording

[engines/futures_engine.py:256](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:256)

**Current**

> 3,000 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 011 · Retain wording

[engines/futures_engine.py:257](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:257)

**Current**

> 1,465 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 012 · Retain wording

[engines/futures_engine.py:257](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:257)

**Current**

> 44%


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 013 · Retain wording

[engines/futures_engine.py:258](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:258)

**Current**

> A1 海报


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 014 · Retain wording

[engines/futures_engine.py:258](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:258)

**Current**

> 5,000 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 015 · Retain wording

[engines/futures_engine.py:259](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:259)

**Current**

> 2,268 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 016 · Retain wording

[engines/futures_engine.py:259](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:259)

**Current**

> 43%


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 017 · Retain wording

[engines/futures_engine.py:260](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:260)

**Current**

> 装裱微喷，A4


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 018 · Retain wording

[engines/futures_engine.py:260](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:260)

**Current**

> 20,000 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 019 · Retain wording

[engines/futures_engine.py:261](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:261)

**Current**

> 7,507 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 020 · Retain wording

[engines/futures_engine.py:261](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:261)

**Current**

> 38%


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 021 · Rewrite

[engines/futures_engine.py:264](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:264)

**Current**

> 先用按需印刷上架。有人下单才做一件，所以这一轮试验没有起印量，也不占地方堆货。毛利率比自己印低，但现阶段这样更稳妥：库存的风险压在印厂那边，你只要弄清楚这件东西有没有人买。


**Replace with**

按需印刷通常在收到订单后生产，可以减少预先备货。这里可以先比较一种产品的样品、色彩还原、费用和配送方式，再决定是否上架。前期仍可能有打样费，也需要准备图像和商品说明。


**Reason:** POD reduces inventory but is not zero effort or zero risk; remove claim that the factory absorbs all risk.


### futures_engine.py · 022 · Rewrite

[engines/futures_engine.py:274](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:274)

**Current**

> 已经卖得稳的东西，还是你现在的做法划算。一套十张的明信片，印一百套时一套约 170 日元，按需印刷要 1,835 日元。这些继续自己印。新形态里哪一样开始稳定出货，再转批量生产，那是第二步。


**Replace with**

如果某种明信片已经有稳定订单，批量印刷可能更划算。比较时需要使用相同纸张、尺寸、印量和交付条件。新产品可以先小范围试卖，有了订单记录，再判断是否增加印量。


**Reason:** Avoid claiming knowledge of her sales or incomparable costs. Hold the 170/1,835 comparison pending like-for-like specifications.


### futures_engine.py · 023 · Rewrite

[engines/futures_engine.py:289](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:289)

**Current**

> 什么决定卖不卖得动


**Replace with**

销量还取决于哪些条件


**Reason:** Natural heading without pretending to isolate a causal driver.


### futures_engine.py · 024 · Rewrite

[engines/futures_engine.py:290](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:290)

**Current**

> 粉丝数预测不了销量。在能查到具体数字的几个案例里，真正掏钱的人占观众的比例从 0.26% 到 15.8%，而其中观众最多的那一位转化率最低。真正起作用的是价格：一位东京插画师，两万七千粉丝，只是你影响力的一小部分，自出版的画集定价 11,000 日元，四个月卖了 400 本，约四百万日元。剩下的大半，由另外两件小一点的事决定。你的读者住在哪里，比他们有多少人更能改变这笔账——航空小包寄一公斤到美国 2,720 日元，寄到东京市内 185 日元——而这个比例，你自己的 Instagram 后台里就有。另外，厚度控制在三厘米以内，每件国内包裹省 465 日元；这是在设计阶段、开印之前就定下的。


**Replace with**

已有案例可以帮助比较定价和产品形式，但不能直接推算你的销量。即使关注数量接近，读者所在地、购买习惯、书的规格和销售方式也可能不同。

对印刷品来说，值得一起核算的是到手价格：售价、包装、运费及平台手续费。书的尺寸和厚度会影响可用的配送服务，因此最好在打样前一并比较。


**Reason:** Remove unmatched follower comparison, causal claims from tiny observational sample, and shipping quotes with different service conditions. Keep sourced cases in evidence detail, dated and named.


### futures_engine.py · 025 · Rewrite

[engines/futures_engine.py:310](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:310)

**Current**

> 书是另一个层面的决定


**Replace with**

做成一本书，需要先确定哪些事


**Reason:** Replace vague other-level decision.


### futures_engine.py · 026 · Hold for model correction

[engines/futures_engine.py:311](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:311)

**Current**

> 128 页的精装本，在中国印 {_BOOK['run']} 本要 {_BOOK['outlay_jpy']:,} 日元。定价 {_BOOK_PRICE:,} 日元，卖出 {_BOOK['breakeven_direct']} 本收回制作成本。回本之后还剩 {_BOOK['run'] - _BOOK['breakeven_direct']} 本。所以要判断的是需求和速度，利润率反倒是次要的。


**Replace with**

这份方案比较的是 128 页精装书的印制成本。印量、售价和销售渠道会共同影响需要预付的金额，以及收回这笔支出所需的销量。具体数字应在确认规格、运费和各项销售费用后计算。


**Reason:** Current 109-copy cash-recovery number double-counts production cost; do not polish it into a stronger claim.


### futures_engine.py · 027 · Retain wording

[engines/futures_engine.py:324](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:324)

**Current**

> 


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 028 · Rewrite

[engines/futures_engine.py:324](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:324)

**Current**

> 每本


**Replace with**

每本印制成本


**Reason:** Define unit cost.


### futures_engine.py · 029 · Rewrite

[engines/futures_engine.py:324](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:324)

**Current**

> 先要付


**Replace with**

整批预付金额／印量


**Reason:** The cells include both cash outlay and quantity.


### futures_engine.py · 030 · Retain wording

[engines/futures_engine.py:325](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:325)

**Current**

> 售价


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 031 · Hold for model correction

[engines/futures_engine.py:325](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:325)

**Current**

> 回本所需册数


**Replace with**

收回预付支出所需销量


**Reason:** Distinguish cash recovery from accounting margin.


### futures_engine.py · 032 · Rewrite

[engines/futures_engine.py:327](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:327)

**Current**

> 现在的 B5 zine，24 页


**Replace with**

B5 zine 方案，24 页


**Reason:** Do not call a model specification her current product unless verified.


### futures_engine.py · 033 · Retain wording

[engines/futures_engine.py:327](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:327)

**Current**

> 498 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 034 · Retain wording

[engines/futures_engine.py:328](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:328)

**Current**

> 49,800 / 100 本


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 035 · Retain wording

[engines/futures_engine.py:328](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:328)

**Current**

> 1,980 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 036 · Hold for model correction

[engines/futures_engine.py:328](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:328)

**Current**

> 34


**Replace with**

{cash_recovery_copies}


**Reason:** Replace the hand-written 34 with a shared calculation. Pure prepaid printing divided by price, excluding all selling costs, gives ceil(49800/1980)=26; that diagnostic is not the final sales target.


### futures_engine.py · 037 · Retain wording

[engines/futures_engine.py:329](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:329)

**Current**

> 210mm 方形平装，128 页


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 038 · Retain wording

[engines/futures_engine.py:329](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:329)

**Current**

> 1,609 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 039 · Retain wording

[engines/futures_engine.py:330](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:330)

**Current**

> 482,700 / 300 本


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 040 · Retain wording

[engines/futures_engine.py:330](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:330)

**Current**

> 4,400 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 041 · Hold for model correction

[engines/futures_engine.py:330](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:330)

**Current**

> 173


**Replace with**

{cash_recovery_copies}


**Reason:** Replace the hand-written 173 with a shared calculation. The same simplified diagnostic gives ceil(482700/4400)=110, before all selling costs.


### futures_engine.py · 042 · Retain wording

[engines/futures_engine.py:331](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:331)

**Current**

> A4 平装，128 页


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 043 · Retain wording

[engines/futures_engine.py:331](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:331)

**Current**

> 1,306 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 044 · Retain wording

[engines/futures_engine.py:332](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:332)

**Current**

> 653,000 / 500 本


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 045 · Retain wording

[engines/futures_engine.py:332](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:332)

**Current**

> 4,400 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 046 · Hold for model correction

[engines/futures_engine.py:332](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:332)

**Current**

> 212


**Replace with**

{cash_recovery_copies}


**Reason:** Replace the hand-written 212 with a shared calculation. The same simplified diagnostic gives ceil(653000/4400)=149, before all selling costs.


### futures_engine.py · 047 · Retain wording

[engines/futures_engine.py:333](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:333)

**Current**

> 精装，128 页，中国印


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 048 · Retain wording

[engines/futures_engine.py:334](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:334)

**Current**

> {_BOOK['unit_jpy']:,} 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 049 · Retain wording

[engines/futures_engine.py:335](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:335)

**Current**

> {_BOOK['outlay_jpy']:,} / {_BOOK['run']} 本


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 050 · Retain wording

[engines/futures_engine.py:337](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:337)

**Current**

> {_BOOK_PRICE:,} 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 051 · Hold for model correction

[engines/futures_engine.py:338](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:338)

**Current**

> str(_BOOK['breakeven_direct'])


**Replace with**

{cash_recovery_copies}


**Reason:** Use the corrected shared cash model, with explicit included costs and upward whole-copy rounding. Introduce the named field in the producing engine; do not paste this placeholder literally.


### futures_engine.py · 052 · Rewrite

[engines/futures_engine.py:341](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:341)

**Current**

> 如果这本书是当商品卖，在查过的几种做法里，中国印的精装本账最划算。如果这本书是用来敲另一扇门的，那就只做三本。Blurb 三本约 31,000 日元，可以直接拿给出版社、画廊或者书店买手。


**Replace with**

用于销售的版本，需要比较印制成本、质量、运输和库存。用于提案的版本，可以先做少量样书，帮助出版社或画廊了解内容和编排。这两种用途适合分别询价。


**Reason:** Remove categorical cheapest conclusion and arbitrary three-copy command. Blurb quote belongs in dated specifications.


### futures_engine.py · 053 · Rewrite

[engines/futures_engine.py:356](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:356)

**Current**

> 一批印量能不能把钱赚回来


**Replace with**

印制方案与收支测算


**Reason:** Current title mistakes run size for profit assurance.


### futures_engine.py · 054 · Retain wording

[engines/futures_engine.py:359](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:359)

**Current**

> 去哪里做


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 055 · Rewrite

[engines/futures_engine.py:361](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:361)

**Current**

> pixivFACTORY / BOOTH——海报、画布、装裱印刷的第一次试水


**Replace with**

pixivFACTORY／BOOTH：查看海报、画布和装裱印刷品的制作选项


**Reason:** Keep destination clear; avoid unsupported beginner/low-risk framing.


### futures_engine.py · 056 · Rewrite

[engines/futures_engine.py:364](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:364)

**Current**

> SUZURI——小件纸制品，低风险的尝试


**Replace with**

SUZURI：查看可制作的产品与费用


**Reason:** Do not imply every paper format is supported or costless.


### futures_engine.py · 057 · Rewrite

[engines/futures_engine.py:372](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:372)

**Current**

> INPRNT——面向日本以外的买家时，值得加上这一家。谁能进，是由站内已有的创作者投票决定的，所以要投三张图；结果大约 48 小时内邮件通知。


**Replace with**

INPRNT：查看艺术微喷的申请方式、分成和配送范围


**Reason:** Three-image/48-hour details need current platform verification before remaining in actionable copy.


### futures_engine.py · 058 · Rewrite

[engines/futures_engine.py:380](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:380)

**Current**

> 愿意承担办展风险的画廊


**Replace with**

比较画廊的投入与合作方式


**Reason:** Representation is not a promise that the gallery bears every risk.


### futures_engine.py · 059 · Rewrite

[engines/futures_engine.py:382](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:382)

**Current**

> 办个展你已经会了，办过三次。下一段值得建立的画廊关系，要能接过你现在自己扛的那几样：场地、守场的人手、藏家、销售的活，还有资金上的风险。这笔账算得特别清楚。


**Replace with**

你已有三场个展记录。接下来比较画廊时，可以进一步看它能提供哪些支持：展览空间、现场人员、作品介绍、销售，以及与藏家的联系。不同合作方式的费用和责任，可以放在一起比较。


**Reason:** Specific recognition without patronizing you already know how or prescribing a single next step.


### futures_engine.py · 060 · Retain wording

[engines/futures_engine.py:394](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:394)

**Current**

> 


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 061 · Rewrite

[engines/futures_engine.py:394](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:394)

**Current**

> 你付


**Replace with**

艺术家承担的场地费


**Reason:** Zero venue fee is not zero total cost.


### futures_engine.py · 062 · Rewrite

[engines/futures_engine.py:394](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:394)

**Current**

> 他们抽


**Replace with**

销售佣金


**Reason:** Neutral professional label.


### futures_engine.py · 063 · Rewrite

[engines/futures_engine.py:395](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:395)

**Current**

> 打平前要卖掉


**Replace with**

覆盖场地费所需销量


**Reason:** Do not label this total break-even; packing, transport, labor and production are excluded.


### futures_engine.py · 064 · Retain wording

[engines/futures_engine.py:397](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:397)

**Current**

> 代理画廊


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 065 · Retain wording

[engines/futures_engine.py:397](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:397)

**Current**

> 0


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 066 · Retain wording

[engines/futures_engine.py:397](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:397)

**Current**

> 约 50%


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 067 · Retain wording

[engines/futures_engine.py:398](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:398)

**Current**

> 0


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 068 · Retain wording

[engines/futures_engine.py:399](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:399)

**Current**

> Moon Gallery 租赁


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 069 · Retain wording

[engines/futures_engine.py:399](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:399)

**Current**

> 10 万 / 5 天


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 070 · Retain wording

[engines/futures_engine.py:400](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:400)

**Current**

> 0%


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 071 · Delete

[engines/futures_engine.py:401](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:401)

**Current**

> _paintings_phrase(100000, zh=True)


**Replace with**

删除按原作标价折算销量的数值；费用比较保留日元金额。


**Reason:** Asking-price ranges do not establish net cash retained from her actual sales. This deletion is an implementation direction, not replacement UI text.


### futures_engine.py · 072 · Retain wording

[engines/futures_engine.py:407](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:407)

**Current**

> Galerie LE MONDE，12 天个展


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 073 · Retain wording

[engines/futures_engine.py:408](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:408)

**Current**

> 37.4 万 / 12 天


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 074 · Retain wording

[engines/futures_engine.py:408](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:408)

**Current**

> 30%


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 075 · Delete

[engines/futures_engine.py:409](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:409)

**Current**

> _paintings_phrase(374000, 0.3, zh=True)


**Replace with**

删除按原作标价折算销量的数值；费用比较保留日元金额。


**Reason:** Do not convert public gallery terms into an implied personal break-even in paintings. This deletion is an implementation direction, not replacement UI text.


### futures_engine.py · 076 · Rewrite

[engines/futures_engine.py:431](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:431)

**Current**

> 八月那场展给你留下了什么


**Replace with**

Galerie LE MONDE 个展，可以怎样用于下一次介绍


**Reason:** Name the achievement and utility instead of vague what it left you.


### futures_engine.py · 077 · Rewrite

[engines/futures_engine.py:433](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:433)

**Current**

> 在 Galerie LE MONDE 的那场个展，是你履历上最新的一项；而最新的这一项，正是第一封信要围着写的内容——下面每一家画廊，都会先读它，再读别的。
> 
> 那个空间不对外出租，所以它带来的不只是一个日期。主理人是看作品本身、以及已经在那里办展的插画家的推荐来选人的，所以这一项读起来是“被选中过”，而且只要还新，它就一直在说这句话。这也正是趁现在用上它、而不是等到明年的理由。
> 
> 后面还接着一个明确的下一步：经纪公司名单上的每一位，都是先在画廊办过展的。他们目前不接新人，所以现在能做的就是保持联系——而同一栋楼里的孔版印刷工作室，本身就是一个再去一趟的由头，带 zine 去，不是带画。


**Replace with**

你最近在原宿 Galerie LE MONDE 举办了个展。这段经历可以放进最新的作品资料：展览介绍、现场照片，以及同一组作品的链接，让下一位读者看到作品在空间中的呈现。


**Reason:** Keep appreciation grounded. Put verified gallery/agency context in separate sourced detail without implying representation or inherited client relationships. Remove mind-reading, urgency tied to diminishing freshness, and an unprompted caveat that diminishes the achievement. Historical fees are not her personal invoice.


### futures_engine.py · 078 · Rewrite

[engines/futures_engine.py:456](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:456)

**Current**

> 同一栋楼里


**Replace with**

可以进一步了解的相关机构


**Reason:** Same-building detail must be verified; utility is the service, not a pretext to revisit.


### futures_engine.py · 079 · Rewrite

[engines/futures_engine.py:458](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:458)

**Current**

> Studio LE MONDE——孔版印刷，周二至周日 12:00–19:00，只在有工作人员在场的时段接受预约。contact@studiolemonde.com


**Replace with**

Studio LE MONDE：孔版印刷工作室。可查看制作项目、预约方式和当前营业时间。


**Reason:** Exact schedule and contact should come from maintained official link, not long-lived prose.


### futures_engine.py · 080 · Rewrite

[engines/futures_engine.py:461](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:461)

**Current**

> Agence LE MONDE——它就是从这里选人的；名单上的插画师在为这些客户做事：麦当劳、朝日啤酒、瑞穗银行、ANNA SUI、GUCCI、Quarto、宝可梦。截至 2026 年 9 月不接新人。


**Replace with**

Agence LE MONDE：可查看其代理插画师及合作案例。是否接受申请，以当前官方说明为准。


**Reason:** Do not imply exhibition guarantees consideration or quietly inherit another artist’s client list.


### futures_engine.py · 081 · Rewrite

[engines/futures_engine.py:466](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:466)

**Current**

> 另一边是代理的账。单看 50% 的抽成会觉得高；拿 374,000 日元的场地费再加 30% 抽成来比，只要那场展卖不到约 187 万日元，代理都更划算。更要紧的区别在于：买家是谁带来的。到现在为止，买你画的人是自己找到你的。代理带来的，是一份原本属于别人的藏家名单。


**Replace with**

按“场地费 374,000 日元＋销售佣金 30%”与“无场地费＋销售佣金 50%”这两种假设比较，在其他条件相同的情况下，销售总额约 187 万日元时，两者的场地费和佣金合计相同。

实际选择还需要看画廊提供的服务、合作范围和买家来源。这里比较的是费用结构，不是对某次展览价值的评价。


**Reason:** Make comparison explicitly hypothetical and like-for-like; do not infer how her buyers found her.


### futures_engine.py · 082 · Rewrite

[engines/futures_engine.py:478](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:478)

**Current**

> 下一步


**Replace with**

联系前可以准备的资料


**Reason:** An available starting point rather than an order.


### futures_engine.py · 083 · Rewrite

[engines/futures_engine.py:479](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:479)

**Current**

> 挑几家展览方向确实合得上的画廊，数量不用多。先去看展。之后寄五张同一个系列的画，问他们有没有兴趣看看实物。


**Replace with**

一组方向一致的作品链接，加上近期个展的介绍和现场照片，可以作为联系材料。是否先到访、提交 PDF 或填写表单，按每家画廊公开的要求准备。


**Reason:** Respect actual submission routes rather than universal visit-then-email etiquette.


### futures_engine.py · 084 · Rewrite

[engines/futures_engine.py:498](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:498)

**Current**

> 现在开放，10 月 8 日截止


**Replace with**

FACE 2027：本轮报名截至 2026 年 10 月 8 日


**Reason:** Explicit year; status must expire automatically.


### futures_engine.py · 085 · Rewrite with verified source

[engines/futures_engine.py:500](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:500)

**Current**

> FACE 2027 的收件期是 9 月 7 日到 10 月 8 日，入选作品明年三月在西新宿的 SOMPO 美术馆展出。接受的媒介里明确写着水彩，和油画、丙烯、岩彩、版画、染色、摄影并列。没有国籍限制，也没有居住地限制——实际上要过的只有一关：把作品送到，10 月下旬用快递，或者11 月 7、8 日本人送去。报名费 7,000 日元。尺寸上限 200 × 170 厘米，没有下限，所以小幅作品也可以投。除了主要奖项，还有一个 30 万日元的 U30 Frontier 奖，面向 1997 年 4 月 1 日之后出生的人。


**Replace with**

FACE 2027 的报名期为 2026 年 9 月 7 日至 10 月 8 日，报名费 7,000 日元，接受水彩等平面作品。作品须在出品前一年内完成，且未曾在公开征集中入选；每人限投一件。

申请前需要核对尺寸、厚度、重量及送件要求，并另计包装和运输费用。U30 Frontier 奖面向 1997 年 4 月 1 日及以后出生的参赛者。


**Reason:** Official SOMPO page verified 2026-09-10. Missing work-age and prior-selection restrictions matter; after -> inclusive date. Link detailed handling schedule instead of claiming delivery is the only hurdle.


### futures_engine.py · 086 · Retain wording

[engines/futures_engine.py:519](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:519)

**Current**

> FACE 2027——征集要项、送件日期与报名表


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 087 · Rewrite

[engines/futures_engine.py:524](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:524)

**Current**

> 东京有三个空间，接受这样的作品


**Replace with**

三家可进一步了解的东京空间


**Reason:** Existence and thematic resemblance do not prove acceptance of her work.


### futures_engine.py · 088 · Rewrite

[engines/futures_engine.py:526](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:526)

**Current**

> 谷中的 HAGI ART 把自己的方向写得很清楚：年轻创作者的个展与联展、艺术书市集，以及关于建筑、文化与日常生活的展览——而且完全不收场地费，整个项目靠楼下的咖啡店养着。它按方案选人，所以要发邮件提方案，不是订档期。
> 
> 吉祥寺的 Gallery KAZE，六天 11 万日元，销售不抽成，40 平方米、20 米挂画墙。今年十月那里有一场水彩个展——青山一树，《水彩でえがく情景》——2027 年的档期大半还空着。按你的价格，这个空间相当于卖出 {_paintings_phrase(110000, zh=True)}。
> 
> Moon Gallery 你已经熟悉了：五天 10 万日元，不抽成，也不需要人守场。


**Replace with**

HAGI ART 的公开介绍涉及展览、艺术书和建筑与日常生活等主题，可作为核对展览提案要求的对象。

Gallery KAZE 与 Moon Gallery 可用于比较租赁展览的费用和服务。费用表应注明查询日期、展期、销售佣金、值守安排及额外收费；某一时点的空档不代表仍可预约。


**Reason:** Move volatile prices/availability into dated facts; do not imply all are equally suitable, or that her Moon terms equal public rates.


### futures_engine.py · 089 · Rewrite

[engines/futures_engine.py:548](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:548)

**Current**

> HAGI ART，谷中——不收场地费；方案寄到 info@hagiso.com，两份 A4 PDF：作品集，以及一份专为这个空间写的展览构想


**Replace with**

HAGI ART：查看展览提案要求与官方联系渠道


**Reason:** Retain exact materials/address only after current route check.


### futures_engine.py · 090 · Rewrite

[engines/futures_engine.py:551](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:551)

**Current**

> Gallery KAZE，吉祥寺——六天 11 万日元，销售不抽成，设备可借


**Replace with**

Gallery KAZE：查看场地、收费和设备说明


**Reason:** Replace unqualified rate promise with maintained source.


### futures_engine.py · 091 · Rewrite

[engines/futures_engine.py:556](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:556)

**Current**

> 以及每年都会再来一次的公开征集


**Replace with**

可留意下一轮的公开征集


**Reason:** Do not promise annual recurrence from a short history.


### futures_engine.py · 092 · Rewrite

[engines/futures_engine.py:559](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:559)

**Current**

> biscuit gallery——它的 grid next 公开征集从 2024 年起每年都办。不收报名费，也不收展位费，面向学生以及大约四十岁以下、此前没有在那里展过的创作者。2026 那一轮的申请是12 月底到 4 月 30 日，展览在八月，所以下一个窗口大约在 12 月打开。


**Replace with**

biscuit gallery 的 grid next 可作为下一轮关注项目。申请资格、作品发表限制和收费情况，需要按当届要项核对。下一轮尚未公布时，仅显示往届报名时间作为参考。


**Reason:** Remove fixed age, fee and opening claims unless current source supports each. Neither past dates nor recent annual pattern confirms next cycle.


### futures_engine.py · 093 · Rewrite

[engines/futures_engine.py:564](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:564)

**Current**

> 同一个市场再往上，这类作品在哪里


**Replace with**

更长期的画廊参照


**Reason:** Remove hierarchy of ceilings and unreachable upper market.


### futures_engine.py · 094 · Rewrite

[engines/futures_engine.py:566](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:566)

**Current**

> Tokyo Gallery + BTAP 从 1950 年开到现在，代理名单上有六位中国艺术家，其中几位用的就是纸上水墨与水彩——同样的材料，出现在这个市场的顶端。徐冰也在这份名单上——这家画廊不是一封陌生来信能够得着的。把它记住，是为了知道天花板长什么样。


**Replace with**

Tokyo Gallery + BTAP 可作为更长期的研究参照：看看它如何介绍纸上作品、安排展览和呈现艺术家的长期创作。媒介相近，只是进一步了解的起点；是否适合合作，还需要比较具体作品与画廊方向。


**Reason:** Avoid making nationality/medium a proxy for fit, or declaring a gallery impossible to approach.


### futures_engine.py · 095 · Rewrite

[engines/futures_engine.py:578](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:578)

**Current**

> 还有第三种安排，比前面两种都划算


**Replace with**

也可以比较提供制作支持的展览项目


**Reason:** Third is universally cheaper is not established.


### futures_engine.py · 096 · Rewrite

[engines/futures_engine.py:580](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:580)

**Current**

> 在租场地和被代理之间，还有一种安排：反过来付钱给艺术家办展的公开征集。TOKAS 提供 15 万日元制作经费，场地不收费；它的公开征集按固定的年度周期走，所以这是可以提前安排的事，不用干等。


**Replace with**

提供制作支持的公开征集，是另一种办展方式。例如 TOKAS-Emerging 的当届要项列有场地和制作支持。它需要经过评选，资助范围与艺术家承担的工作应分别列明。


**Reason:** Support is neither a sales opportunity nor complete risk transfer.


### futures_engine.py · 097 · Retain wording

[engines/futures_engine.py:592](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:592)

**Current**

> TOKAS——各项目的公开征集与申请时间


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 098 · Rewrite

[engines/futures_engine.py:597](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:597)

**Current**

> 这份名单比一本东京画廊名录短得多，短正是它的用处。和十个真正对得上的空间建立关系，比给一百个不对路的空间发信管用。


**Replace with**

下面按合作方式整理了相关机构，便于比较它们的展览、出版或授权业务。


**Reason:** Replace universal ten-versus-hundred slogan. The finished records must actually supply the fit explanation and verified route; do not publish instructions to the system as product copy.


### futures_engine.py · 099 · Retain wording

[engines/futures_engine.py:605](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:605)

**Current**

> 第一封信


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 100 · Rewrite

[engines/futures_engine.py:606](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:606)

**Current**

> 第一次联系，只需要让人容易看到作品。一个链接，同一个系列的五张画，还有一句具体的话，说明为什么选了这一家。给 HAGI ART 的例子：


**Replace with**

下面是一封写给 HAGI ART 的日语联系草稿。使用前需要补齐真实的到访经历或选展理由，并按对方当前要求调整材料。


**Reason:** Clarifies draft status; title alone does not make copy safe to send.


### futures_engine.py · 101 · Rewrite

[engines/futures_engine.py:633](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:633)

**Current**

> 已经画完的作品，再挣一次钱


**Replace with**

现有作品的授权用途


**Reason:** Plain, professional heading.


### futures_engine.py · 102 · Rewrite

[engines/futures_engine.py:634](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:634)

**Current**

> 授权对你有一个别处没有的优势：你手上已经有的画就是现成的。六年每天画下来是好几千张图，原作还是你的，同时还能挣钱。值多少钱，主要看一张图被用在哪里、怎么用：


**Replace with**

你已有的水彩作品，可以按书封、文具、日历等用途整理授权样例。能否授权，需要先确认作品权利和图像文件；费用则取决于具体用途、期限、地域与独家要求。


**Reason:** Do not infer thousands of licensable high-resolution images from years of practice. Remove reuse of commission grid as archive-license price list.


### futures_engine.py · 103 · Retain wording

[engines/futures_engine.py:645](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:645)

**Current**

> 用途


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 104 · Move / correct scope

[engines/futures_engine.py:645](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:645)

**Current**

> 公开费率


**Replace with**

历史制作报价参考（2020 年）


**Reason:** JIA table is commissioned illustration, not current archive-license market rates; preferably relocate to commissions.


### futures_engine.py · 105 · Retain wording

[engines/futures_engine.py:647](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:647)

**Current**

> 杂志内页小图


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 106 · Delete

[engines/futures_engine.py:647](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:647)

**Current**

> 5,000 日元


**Replace with**

删除该行；5,000 日元仅对应特定规格的小幅插图，不能代表所有杂志内页图。


**Reason:** Delete overgeneralized amount, not replace with invented new rate.


### futures_engine.py · 107 · Retain wording

[engines/futures_engine.py:648](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:648)

**Current**

> 书籍封面


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 108 · Retain wording

[engines/futures_engine.py:648](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:648)

**Current**

> 70,000 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 109 · Retain wording

[engines/futures_engine.py:649](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:649)

**Current**

> 杂志封面


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 110 · Retain wording

[engines/futures_engine.py:649](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:649)

**Current**

> 100,000 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 111 · Move / correct scope

[engines/futures_engine.py:650](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:650)

**Current**

> 挂历


**Replace with**

A3 挂历插画，全套 12 幅


**Reason:** 800,000 row is a 12-image commissioned set, not one licensed painting. Relocate with source/date.


### futures_engine.py · 112 · Retain wording

[engines/futures_engine.py:650](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:650)

**Current**

> 800,000 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 113 · Rewrite

[engines/futures_engine.py:653](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:653)

**Current**

> 所以授权条款和费用一样要紧：形式、地域、期限、是否独家、能不能再次使用。在日本公开的费率表上，著作权转让的定价大约是普通授权的两到三倍。只要对方要的是永久权利，就把这一条摆到明面上。


**Replace with**

报价时可同时列出用途、地域、期限、是否独家，以及追加使用的处理方式。长期使用许可和著作权转让涉及不同范围的权利，应在条款中分别写清楚。


**Reason:** Do not equate perpetual license with ownership. JIA multiplier belongs to source detail, not a universal contract rule.


### futures_engine.py · 114 · Rewrite

[engines/futures_engine.py:664](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:664)

**Current**

> 一小组能直接当封面用的画


**Replace with**

从现有作品中挑选书封样例


**Reason:** Avoid turning research on existing assets into a request for ten new paintings.


### futures_engine.py · 115 · Rewrite

[engines/futures_engine.py:665](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:665)

**Current**

> 你的题材本来就贴合图书市场：建筑、氛围、室内、天气、光，还有安静的城市场景。值得专门去应对的，是构图上的要求。封面要放得下字，也要经得起裁切。画一小组竖构图，特意留出安静的区域——天空、雾、水面、墙、阴影，或者上三分之一整片留白。这样艺术总监手上就有了能围着它做封面的图，而作品看上去还是一眼就认得出是你的。五到十张，一个授权作品集的开头就有了。然后把它们放到艺术总监本来就会去看的地方：


**Replace with**

你的建筑、室内和光线题材，可以用来研究书封的呈现方式。先从现有作品中挑几张，试排书名、作者名和必要文字，看看裁切后能否保留画面的重点。需要新作品时，再按具体用途补充。


**Reason:** Keep practical art-direction value; remove promise of commercial fit and unnecessary production.


### futures_engine.py · 116 · Rewrite

[engines/futures_engine.py:686](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:686)

**Current**

> イラストレーションファイルWeb——日本的艺术总监和装帧设计师找插画师的地方，以及申请收录的表格


**Replace with**

イラストレーションファイルWeb：查看插画师资料及申请收录方式


**Reason:** Avoid universal claim about all art directors.


### futures_engine.py · 117 · Rewrite

[engines/futures_engine.py:689](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:689)

**Current**

> amanaimages——日本的图像授权；公开的封面授权价为 33,000–79,200 日元


**Replace with**

amanaimages：查看书封图像的授权范围与报价示例


**Reason:** Buyer-facing price not artist payout.


### futures_engine.py · 118 · Rewrite

[engines/futures_engine.py:692](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:692)

**Current**

> Arcangel——专做书封图像，收插画，付给供稿人净额的 50%


**Replace with**

Arcangel：查看书封图像征集及供稿合同


**Reason:** Net receipts definition and deduction basis must be documented.


### futures_engine.py · 119 · Rewrite

[engines/futures_engine.py:699](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:699)

**Current**

> Bridgeman Studio——接受插画；投三到五张图申请，他们会连同你现在网上的作品一起看。合同分独家与非独家两种，非独家可以同时在别处授权。


**Replace with**

Bridgeman Studio：查看插画申请材料与合同选项


**Reason:** Exclusivity claims should quote current contributor agreement, not imply unrestricted reuse.


### futures_engine.py · 120 · Rewrite

[engines/futures_engine.py:704](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:704)

**Current**

> 这条路可以从你已经有的作品开始，再靠专门为商业用途画的作品往外扩。


**Replace with**

可以先用现有作品了解需求，再根据实际询问决定是否补充新作。


**Reason:** Clear conditional sequence.


### futures_engine.py · 121 · Rewrite

[engines/futures_engine.py:713](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:713)

**Current**

> 一本还没做出来的书


**Replace with**

把已有作品整理成出版提案


**Reason:** More immediately useful than an unmade-book abstraction.


### futures_engine.py · 122 · Rewrite

[engines/futures_engine.py:715](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:715)

**Current**

> 出版这条路上最有力的，是一个清楚到出版社一听就知道怎么卖的选题构想。你已有的画证明你做得出来；方案说明的是这本书到底是什么。这个区别之所以要紧，是因为查过的这几家出版社要的是方案和构想。拿来对照的那本东京建筑画集，五十张画里有四十张是在合同谈定之后才画的。所以一份有力的方案要有：


**Replace with**

出版提案需要让编辑看清这本书的主题、读者和内容结构。你已有的作品可以作为样例；还没完成的部分，则在方案中说明。这样对方能评估选题，而你也不必先把整本书画完。


**Reason:** Remove unverifiable reader response and unidentified comparison book; preserve the valuable reduction in up-front work.


### futures_engine.py · 123 · Rewrite

[engines/futures_engine.py:733](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:733)

**Current**

> 这本书的构想


**Replace with**

主题与书名暂案


**Reason:** More useful proposal field.


### futures_engine.py · 124 · Retain wording

[engines/futures_engine.py:734](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:734)

**Current**

> 这些画为什么属于同一本书


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 125 · Rewrite

[engines/futures_engine.py:735](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:735)

**Current**

> 一段排好顺序的样张


**Replace with**

按阅读顺序编排的样页


**Reason:** Natural publishing Chinese.


### futures_engine.py · 126 · Rewrite

[engines/futures_engine.py:736](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:736)

**Current**

> 几张完成的作品，用来呈现视觉语言


**Replace with**

能体现画面风格的完成作品


**Reason:** 视觉语言 is acceptable but less direct here.


### futures_engine.py · 127 · Retain wording

[engines/futures_engine.py:737](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:737)

**Current**

> 还有哪些要画


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 128 · Retain wording

[engines/futures_engine.py:738](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:738)

**Current**

> 预设的读者


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 129 · Rewrite

[engines/futures_engine.py:739](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:739)

**Current**

> 大致的规模与开本


**Replace with**

预计页数、开本与制作进度


**Reason:** Concrete scope.


### futures_engine.py · 130 · Rewrite

[engines/futures_engine.py:742](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:742)

**Current**

> 即使最后成书用的是新画的作品，你这六年的积累也让这份方案有特别扎实的底子。


**Replace with**

六年的日常创作，为选题、样页和作品编排提供了现成素材。


**Reason:** Specific appreciation without grading her as especially solid.


### futures_engine.py · 131 · Rewrite

[engines/futures_engine.py:748](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:748)

**Current**

> 这笔账


**Replace with**

版税、发行与前期投入


**Reason:** Name what is being compared.


### futures_engine.py · 132 · Rewrite

[engines/futures_engine.py:749](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:749)

**Current**

> 论每本能拿多少，出版是弱的；论发行，它是强的。


**Replace with**

出版社合作与自出版，需要分别比较每本收入、前期投入和发行支持。


**Reason:** Avoid assigning weak/strong universal properties.


### futures_engine.py · 133 · Retain wording

[engines/futures_engine.py:754](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:754)

**Current**

> 


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 134 · Hold for model correction

[engines/futures_engine.py:754](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:754)

**Current**

> 每本你拿到


**Replace with**

每本收入及扣费口径


**Reason:** Publisher royalty and self-publishing contribution are not apples-to-apples until cost basis aligned.


### futures_engine.py · 135 · Rewrite

[engines/futures_engine.py:754](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:754)

**Current**

> 300 本


**Replace with**

售出 300 本的测算


**Reason:** Clarify assumption; do not imply forecast.


### futures_engine.py · 136 · Retain wording

[engines/futures_engine.py:763](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:763)

**Current**

> 出版社出版


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 137 · Retain wording

[engines/futures_engine.py:763](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:763)

**Current**

> _ROY_PER_COPY_ZH


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 138 · Retain wording

[engines/futures_engine.py:764](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:764)

**Current**

> _ROY_300_ZH


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 139 · Retain wording

[engines/futures_engine.py:765](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:765)

**Current**

> 自己出版的精装本


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 140 · Retain wording

[engines/futures_engine.py:765](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:765)

**Current**

> 3,635 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 141 · Retain wording

[engines/futures_engine.py:766](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:766)

**Current**

> 1,090,500 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 142 · Rewrite

[engines/futures_engine.py:769](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:769)

**Current**

> 出版社真正给的是版税之外的那一整套：出印刷的钱、进全国书店、一个 ISBN、制作、库存，还有一条会一直挂在你名字上的出版记录。当这本书除了卖出去，还要带动你手上其他的事时，这些好处才最值。岔口的另一边——自己付钱给印厂，以及一批印量要卖掉多少才回得来——算在“直接卖”那一条里。


**Replace with**

出版社可承担编辑、设计、印制、库存及发行中的一部分或全部工作，具体以合作方案为准。自出版则需要自行安排这些环节。两种方式可以用同一套口径比较：前期现金投入、每本结余、工作量和发行渠道。


**Reason:** No automatic nationwide stocking, ISBN uniqueness, or guaranteed permanent career benefit.


### futures_engine.py · 143 · Rewrite

[engines/futures_engine.py:788](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:788)

**Current**

> 394,500 日元由谁来出


**Replace with**

前期印制费用由谁承担


**Reason:** Do not repeat a provisional model number as a firm invoice.


### futures_engine.py · 144 · Rewrite

[engines/futures_engine.py:790](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:790)

**Current**

> 三家把入口写出来的出版社


**Replace with**

三家出版社，各自的联系方式


**Reason:** MdN has an inquiry route, not an open proposal call.


### futures_engine.py · 145 · Rewrite

[engines/futures_engine.py:798](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:798)

**Current**

> マール社——「いつでも、どなたでも」，也不要求你出过书。方案一旦被采用，由他们出钱出版，并进入全国书店。一个月内回复；寄去的东西不退。


**Replace with**

マール社：可查看公开的出版提案要求、费用承担方式和回复说明。


**Reason:** Submission response not promised by us; retain sourced detail in dated evidence.


### futures_engine.py · 146 · Rewrite

[engines/futures_engine.py:801](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:801)

**Current**

> 青幻舎——只走方案投递专用表单：作品集（作品、活动经历、简介）、方案、图像数据，附件上限 10MB


**Replace with**

青幻舎：可通过出版提案专用表单查看材料要求与附件限制。


**Reason:** Do not assume current 10 MB limit without check.


### futures_engine.py · 147 · Rewrite

[engines/futures_engine.py:804](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:804)

**Current**

> MdN——《东京店构え》系列就是他们出的，所以这一类书本来就在他们的书目里。他们没有公开投稿通道，要从一般咨询表单去问。


**Replace with**

MdN：出版过《東京店構え》等相关题材书籍。目前未确认有公开提案入口，可先查看官方咨询方式。


**Reason:** Proper book title; inquiry is a question, not invitation to send unsolicited large files.


### futures_engine.py · 148 · Rewrite

[engines/futures_engine.py:809](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:809)

**Current**

> 所以这条路上接下来真正有用的一件事，是把一份书的方案做扎实，扎实到只要小改一下就能同时递给这三家。


**Replace with**

可以先整理一份通用的选题说明和样页，再按各出版社的书目与材料要求分别调整。


**Reason:** Do not pretend all three accept same submission.


### futures_engine.py · 149 · Rewrite

[engines/futures_engine.py:819](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:819)

**Current**

> 画和用途，分开计价


**Replace with**

把创作工作与使用范围写清楚


**Reason:** Distinguish quote components without universal mandatory separate invoices.


### futures_engine.py · 150 · Rewrite

[engines/futures_engine.py:821](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:821)

**Current**

> 一次委托拿走的东西，要么由费用补回来，要么得在别处产生价值。全国费率表给了一个有用的底线：


**Replace with**

商业委托可以按创作工作、使用范围和交付条件来比较。历史报价表能提供参考，但需要注明年份、作品规格与适用范围。


**Reason:** No official national minimum; historical evidence not binding floor.


### futures_engine.py · 151 · Retain wording

[engines/futures_engine.py:831](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:831)

**Current**

> 用途


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 152 · Rewrite

[engines/futures_engine.py:831](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:831)

**Current**

> 公开费率


**Replace with**

历史制作报价参考（2020 年）


**Reason:** Current rates cannot be inferred from old table.


### futures_engine.py · 153 · Retain wording

[engines/futures_engine.py:833](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:833)

**Current**

> 书籍封面


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 154 · Retain wording

[engines/futures_engine.py:833](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:833)

**Current**

> 70,000 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 155 · Retain wording

[engines/futures_engine.py:834](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:834)

**Current**

> 杂志封面


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 156 · Retain wording

[engines/futures_engine.py:834](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:834)

**Current**

> 100,000 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 157 · Retain wording

[engines/futures_engine.py:835](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:835)

**Current**

> 内页小图


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 158 · Retain wording

[engines/futures_engine.py:835](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:835)

**Current**

> 5,000 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 159 · Hold for source

[engines/futures_engine.py:836](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:836)

**Current**

> 经手工作的平均值


**Replace with**

删除此行，或另列具名调查的年份、样本和统计口径。


**Reason:** 71,327 has false precision and no visible population; not same kind of evidence as commission guideline.


### futures_engine.py · 160 · Retain wording

[engines/futures_engine.py:836](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:836)

**Current**

> 71,327 日元


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 161 · Rewrite

[engines/futures_engine.py:839](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:839)

**Current**

> 建筑与氛围类的画在封面上有明确需求：文学小说的封面，大量依赖的正是这一类图像。那份费率表的五个媒介档次里，手绘水彩排在第二高。当授权范围扩大、图像被再次使用，或者这次发表把作品带到下一个客户面前时，商业委托才变得更有吸引力。同一张图反复被用时，二次使用可以按原稿费再付一笔，公开的比例依次是 70%、50%、50%、20%。要护住的正是这一部分。


**Replace with**

书籍封面是可以进一步研究的用途。报价时，需要把原稿制作与追加使用分别说明；公开参考表中的金额和比例，也应连同年份、作品规格及适用条件一起展示。


**Reason:** Do not turn a workload rank into a prestige rank or universal formula; cite JIA once in evidence appendix.


### futures_engine.py · 162 · Rewrite

[engines/futures_engine.py:859](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:859)

**Current**

> 在询问到来之前就备好的条款


**Replace with**

可以复用的报价说明


**Reason:** Avoid assumption nobody has approached her.


### futures_engine.py · 163 · Rewrite

[engines/futures_engine.py:861](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:861)

**Current**

> 每一次商业委托，这四项分开报价：


**Replace with**

一份清楚的报价说明，可以包含以下四部分：


**Reason:** Available structure, not dictate to every deal.


### futures_engine.py · 164 · Retain wording

[engines/futures_engine.py:867](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:867)

**Current**

> 绘制费


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 165 · Rewrite

[engines/futures_engine.py:868](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:868)

**Current**

> 做出这张图所需要的工作。


**Replace with**

创作内容、交付文件、修改次数与交付时间。


**Reason:** Specific scope she can reuse.


### futures_engine.py · 166 · Retain wording

[engines/futures_engine.py:869](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:869)

**Current**

> 授权


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 167 · Rewrite

[engines/futures_engine.py:870](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:870)

**Current**

> 可以出现在哪里、用多久、在哪些国家、作什么用途。


**Replace with**

使用媒介、用途、地域、期限及是否独家。


**Reason:** Include exclusivity; clear standard terminology.


### futures_engine.py · 168 · Retain wording

[engines/futures_engine.py:872](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:872)

**Current**

> 追加使用


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 169 · Rewrite

[engines/futures_engine.py:873](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:873)

**Current**

> 同一张图被用到别处时，另计一笔费用。


**Replace with**

增加媒介、延长使用时间或扩大范围时，如何另行约定费用。


**Reason:** Avoid implying every different use automatically has same fee rule.


### futures_engine.py · 170 · Retain wording

[engines/futures_engine.py:875](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:875)

**Current**

> 著作权转让


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 171 · Rewrite

[engines/futures_engine.py:876](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:876)

**Current**

> 客户想永久拥有这些权利时，单独计价，而且高出许多。


**Replace with**

如需转让著作权，单独列明权利范围和对价，并确认作品展示及后续使用安排。


**Reason:** Ownership and indefinite license must not be conflated; final terms need case review.


### futures_engine.py · 172 · Rewrite

[engines/futures_engine.py:884](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:884)

**Current**

> 这样一来，“画一张多少钱”这种含糊的问题，就变成了一个你能稳定报价的问题。


**Replace with**

有了这份说明，收到询问时就可以按项目调整，不必每次从头写。


**Reason:** Concrete time saved.


### futures_engine.py · 173 · Rewrite

[engines/futures_engine.py:890](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:890)

**Current**

> 现在就有两扇有用的门


**Replace with**

两项可查看当届规则的作品征集


**Reason:** Not always currently open.


### futures_engine.py · 174 · Rewrite

[engines/futures_engine.py:896](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:896)

**Current**

> ザ・チョイス——统一 1,500 日元，投一张和投五张一个价。一年办四次，每次换一位评审，入选作品都会进入年度奖。年龄、国籍、职业或业余，全都明确不设限。报名费通过 Peatix 预付，缴费截止在寄件截止的前一天。


**Replace with**

ザ・チョイス：查看当期评审、报名费用、付款与寄件截止时间。


**Reason:** Time-sensitive quantities belong to dated factual fields.


### futures_engine.py · 175 · Rewrite

[engines/futures_engine.py:899](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:899)

**Current**

> HB FILE——7,000 日元，目前是第 37 届，接受已经发表过的作品，所以六年画完的东西本身就是作品集。每位投稿者的档案会在画廊向设计师和出版社开放一年；最高奖是在表参道 HB Gallery 办一周个展。


**Replace with**

HB FILE：查看当届作品集要求、费用、展示方式和奖项。已有作品是否可用，以该届规定为准。


**Reason:** Do not promise complete portfolio from all past work, or stale edition number.


### futures_engine.py · 176 · Rewrite

[engines/futures_engine.py:904](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:904)

**Current**

> 这两条都很便宜，都是把作品放到“会下委托的人”眼前的方式。


**Replace with**

这两项征集可以帮助作品接触编辑与设计从业者。是否值得参加，需要结合当届评审、费用和准备量判断。


**Reason:** ¥7,000 not objectively cheap; competition does not guarantee commission.


### futures_engine.py · 177 · Rewrite

[engines/futures_engine.py:914](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:914)

**Current**

> 几个不错的起点


**Replace with**

可以从哪一步开始


**Reason:** Plain next-action heading.


### futures_engine.py · 178 · Rewrite

[engines/futures_engine.py:923](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:923)

**Current**

> 其中一件有截止日期。其余的都不着急，而且它们大小不一样——两件是一个下午的事，三件是要动手做的活。


**Replace with**

下面按准备工作的先后整理。可以先选一个方向；有截止日期的项目另列出来，方便安排。


**Reason:** Current body has six rows but says five experiments; no need to do every route.


### futures_engine.py · 179 · Rewrite

[engines/futures_engine.py:928](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:928)

**Current**

> 10 月 8 日之前


**Replace with**

有明确截止日期


**Reason:** Date supplied by data, not static heading.


### futures_engine.py · 180 · Rewrite

[engines/futures_engine.py:929](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:929)

**Current**

> FACE 2027——7,000 日元，接受的媒介里写明水彩，尺寸没有下限。


**Replace with**

FACE 2027：先核对作品是否符合当届要求，再决定是否报名。报名截止、费用和送件安排见项目详情。


**Reason:** A calendar exception, not automatic first recommendation.


### futures_engine.py · 181 · Retain wording

[engines/futures_engine.py:931](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:931)

**Current**

> 直接卖


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 182 · Rewrite

[engines/futures_engine.py:932](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:932)

**Current**

> 一个下午：用按需印刷上架一张 A2 海报、一张 A1 海报和一张装裱的 A4 印刷。


**Replace with**

先比较一种印刷品的打样费用与预期售价，再决定是否制作样品。


**Reason:** One product; no unsupported afternoon estimate.


### futures_engine.py · 183 · Retain wording

[engines/futures_engine.py:934](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:934)

**Current**

> 画廊


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 184 · Rewrite

[engines/futures_engine.py:935](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:935)

**Current**

> 一个下午：挑一场展去看，把一个五张同系列作品的链接准备好。


**Replace with**

整理近期个展的介绍、现场照片和一组作品链接，供下一次联系使用。


**Reason:** Useful existing-materials step; visit not magically one afternoon.


### futures_engine.py · 185 · Retain wording

[engines/futures_engine.py:937](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:937)

**Current**

> 图像授权


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 186 · Rewrite

[engines/futures_engine.py:938](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:938)

**Current**

> 要动手做的：头五张竖构图、可以直接当封面用的画。


**Replace with**

从现有作品中挑选几张，试做书封或文具的排版样例。


**Reason:** Replace “头五张” and obligation to make new work.


### futures_engine.py · 187 · Retain wording

[engines/futures_engine.py:940](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:940)

**Current**

> 出版


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 188 · Rewrite

[engines/futures_engine.py:941](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:941)

**Current**

> 要动手做的：把已有的一组作品，写成一页纸的书的构想。


**Replace with**

选一组已有作品，写出一页选题说明，并配上几页样页。


**Reason:** Concrete deliverable.


### futures_engine.py · 189 · Retain wording

[engines/futures_engine.py:943](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:943)

**Current**

> 委托


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 190 · Rewrite

[engines/futures_engine.py:944](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:944)

**Current**

> 要动手做的：一份可以反复用的“费用＋授权”模板，趁还没有人来问先写好。


**Replace with**

准备一份可以复用的报价说明，列明创作内容、使用范围和修改安排。


**Reason:** Do not infer no inquiries yet.


### futures_engine.py · 191 · Rewrite

[engines/futures_engine.py:947](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:947)

**Current**

> 五个实验做下来，会比现在凭空挑选清楚得多。


**Replace with**

先完成与你当前方向最相关的一项，再根据实际反馈决定下一步。


**Reason:** Remove belittling 凭空挑选 and five simultaneous experiments.


### futures_engine.py · 192 · Rewrite

[engines/futures_engine.py:979](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:979)

**Current**

> 这是什么样的一条路


**Replace with**

合作方式


**Reason:** Remove verbose formula repeated five times.


### futures_engine.py · 193 · Rewrite

[engines/futures_engine.py:980](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:980)

**Current**

> 这条路有、别的路没有的


**Replace with**

可以带来什么


**Reason:** Remove unjustified exclusivity.


### futures_engine.py · 194 · Rewrite

[engines/futures_engine.py:981](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:981)

**Current**

> 你要承担的是什么


**Replace with**

需要投入什么


**Reason:** Less burdensome without concealing real tradeoffs.


### futures_engine.py · 195 · Rewrite

[engines/futures_engine.py:1001](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1001)

**Current**

> 作品通过你自己的店铺出去——文案你写、价格你定、包裹你打——钱是一笔一笔进来的，卖一件收一件。明信片、zine、印刷品和原作现在都是这样在走，直接接的委托也是。


**Replace with**

通过自己的店铺销售，可以自行安排产品、定价和上架节奏。明信片、zine、印刷品与原作的销售，可以沿用已有渠道。


**Reason:** No elementary lecture about money arriving one item at a time.


### futures_engine.py · 196 · Rewrite

[engines/futures_engine.py:1017](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1017)

**Current**

> 整个毛利都归你。每卖一张，画廊抽走大约一半；一本 {_BOOK_PRICE:,} 日元的书，出版社分给你 {_ROY_PER_COPY_ZH}，授权那边，是别人按定好的用途一次性付你一笔钱——在这条路上，成本以外的钱全是你的。价格是你定的，不需要替它争取；也没有任何一件事要等申请、等评审、等别人的排期，所以周一做的决定，周五就可能在挣钱。其他四条路没有一条做得到。
> 
> 别的路要先把观众攒起来，这条路一开始就有。观众已经在了，而且已经在看，所以一件新东西当天下午就能到他们眼前，不用安排引荐，也不用等谁点头。


**Replace with**

已有店铺和关注者，让你可以用现有渠道介绍新产品。定价与上架安排也由你掌握。收入需要扣除制作、平台、包装、配送等实际费用，订单多少则需要通过销售记录来判断。


**Reason:** Remove “only this route,” next-Friday earnings, assumed reach and take-home/profit conflation.


### futures_engine.py · 197 · Rewrite

[engines/futures_engine.py:1034](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1034)

**Current**

> 所有环节都还在你手上：上架、拍照、打包、寄件、回客户邮件，还有堆在房间里的货。销量只来自你自己的观众，没有第二个来源，所以一淡就是全线一起淡。批量印刷毛利更高，代价是风险你自己扛——卖不掉的那些，钱是先付掉的。


**Replace with**

上架、拍照、客户沟通和履约仍需要时间。批量印刷通常要先付款并安排库存；按需印刷则需要比较较高的单件费用和供应商的交付质量。


**Reason:** No claim all sales come from followers or all channels decline together.


### futures_engine.py · 198 · Rewrite

[engines/futures_engine.py:1045](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1045)

**Current**

> 画廊出钱办展、抽佣金，并且负责找买家。它自己的收入取决于会回头再买的藏家，所以它介绍给你的人，是它打算长期留住的人——所以代理往往抬的是单张画的价，而不只是多卖几张。


**Replace with**

不同画廊提供的支持有所不同，可能包括策展、作品介绍、销售与藏家联络。合作时需要明确场地费、销售佣金和双方责任。


**Reason:** No inevitable price rise or all collectors repeat.


### futures_engine.py · 199 · Rewrite

[engines/futures_engine.py:1054](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1054)

**Current**

> 真正的区别在于钱的流向：租场地是你付场地费，这条路上是画廊出钱办展。价格会上去还有一层原因——帮你抬价的那个人，自己也靠这个吃饭。
> 
> 另外，你在这条路上站到的位置，会跟着你走到另外四条路上——出版社、艺术总监、授权买家读展览履历的方式是一样的，这份清单上没有第二样东西有这个作用。


**Replace with**

合适的画廊合作，可以增加作品被认真介绍和接触新买家的机会。展览资料也可以用于之后的出版或委托介绍，具体价值取决于展览内容与合作方式。


**Reason:** Specific possible benefit, no universal prestige transfer.


### futures_engine.py · 200 · Rewrite

[engines/futures_engine.py:1067](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1067)

**Current**

> 每一笔销售的大约一半，以及展什么、什么时候展的部分决定权。代理这件事起步也慢：路径是先去看展，再写信，然后等上几个月。而且画廊的注意力跟着它自己的展览计划走，所以它清淡的一年，也是你清淡的一年。


**Replace with**

需要比较销售佣金、费用承担、展期安排及合作范围。建立长期关系可能需要多次交流，时间和结果都因画廊而异。


**Reason:** Remove fatalistic shared quiet year and fixed months-long script.


### futures_engine.py · 201 · Rewrite

[engines/futures_engine.py:1077](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1077)

**Current**

> 安静的钱。一张图按约定的用途授权出去——文具、家居、包装、书封、品牌——生产、铺货、销售都由拿到授权的公司负责。原作自始至终还是你的；交出去的是许可，限定在说好的场合和说好的期限之内。


**Replace with**

图像授权让合作方在约定范围内使用作品，并负责相应产品的制作或发行。报价与条款需要写明用途、期限、地域和独家要求；原作所有权也应单独确认。


**Reason:** “安静的钱” sells passive income; use precise mechanism.


### futures_engine.py · 202 · Rewrite

[engines/futures_engine.py:1086](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1086)

**Current**

> 五条路里，只有这一条能为同一张图反复收钱；其他每一条都是做一件、卖一次。它不要求你另外画新东西，也不会带来公众知名度，所以你要是只想一直画下去、别的事尽量少管，这条路合适。
> 
> 住在哪里、签证是什么，对这条路的影响也最小——买家可以是任何地方的公司，交付的是文件；五条路里，只有这一条在你搬到另一个国家之后还能原样继续。


**Replace with**

现有作品有机会用于不同产品；能否重复授权，取决于已有合同和每次约定的范围。整理作品、沟通用途和审核合同仍需要时间。跨地区合作还需确认适用的合同、税务与当地规定。


**Reason:** Remove false exclusivity, no-publicity promise, and unsafe visa-minimal blanket claim. No inference about her immigration status.


### futures_engine.py · 203 · Rewrite

[engines/futures_engine.py:1100](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1100)

**Current**

> 钱按别人的时间表、别人的销量到账。查到的插画师里，只有一位公开过自己的收入构成：做了二十年授权，客户包括 M&S、John Lewis、联合利华——授权只占她收入的 3%。价值在条款里，而对一批作品签下无限期买断，就等于放弃了日后再次授权它的可能；这是这条路上唯一一种代价以年计、而不是以钱计的错误。


**Replace with**

收入可能来自一次性授权费，也可能按销售结算。不同艺术家的收入构成差别很大，个案只能作为参考。长期或独家条款会影响后续使用，因此需要明确权利范围、期限与终止条件。


**Reason:** One artist’s 3% is not market rate; perpetual transfer and exclusivity not identical.


### futures_engine.py · 204 · Rewrite

[engines/futures_engine.py:1114](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1114)

**Current**

> 书本身就是一件商品——别人是冲着它是一本书才买的，摆在店里、架子上，背后有 ISBN 和发行商。有出版社参与时，印刷的钱和库存由他们承担；你出的是作品，和这本书的构想。


**Replace with**

与出版社合作时，可以由双方约定选题、编辑、制作和发行分工。需要先确认是由出版社承担成本的出版合作，还是包含作者出资的其他模式。


**Reason:** Distinguish supported publishing from author-funded arrangements without assuming contract.


### futures_engine.py · 205 · Rewrite

[engines/futures_engine.py:1122](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1122)

**Current**

> 这是五条路里唯一一条在开始之前就知道价钱的；清单上其他每一扇门，都是先申请，然后等。做出来的东西在其他四条路上也都用得上——画廊、出版社、艺术总监，拿给他们看的是同一本成品书——而书摆在架子上，陌生人会拿起来翻——这些人永远刷不到你的帖子。有出版社参与时，同样不用出钱、家里不堆书，而且发行能进入全国书店；这一点这份清单上别处完全没有。


**Replace with**

出版社可能提供编辑制作、书店发行和库存管理等支持，让作品接触店铺之外的读者。一本内容清楚、编排完整的书，也能作为介绍创作的材料。具体渠道与投入，以对方的合作方案为准。


**Reason:** No guaranteed national distribution or claim self-publishing readers never see posts.


### futures_engine.py · 206 · Rewrite

[engines/futures_engine.py:1139](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1139)

**Current**

> 有出版社参与时，不确定的只有一件事：对方点不点头，而这件事的时间表没有人能控制——一份方案可能压上几个月，最后石沉大海。他们从每本书里抽走的那部分，是这笔交易的另一半，下面的账里有具体数字。自己出版没有等待这回事，代价是钱要先掏，而且在书卖动之前家里一直堆着。


**Replace with**

需要投入提案与样页准备，并等待编辑评估。后续还要确认制作周期、修改安排、版税结算和权利范围。自出版则需要自行安排制作与销售，同样有时间和现金投入。


**Reason:** Acceptance is not only uncertainty; self-publishing not instantaneous.


### futures_engine.py · 207 · Rewrite

[engines/futures_engine.py:1151](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1151)

**Current**

> 杂志插画、书籍封面、委托创作。对方提需求，你交稿，按约定时间付款；费用是按这张图会被用到多广来定的，而不是按你画了多久。


**Replace with**

商业委托通常围绕具体项目展开。费用可综合创作难度、修改量、交付时间和使用范围商议，付款节点也需要事先约定。


**Reason:** Hours and scope both matter; no guaranteed payment sequence.


### futures_engine.py · 208 · Rewrite

[engines/futures_engine.py:1158](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1158)

**Current**

> 五条路里只有这一条每月收入可以预期，也是最不浪漫的一条——这两件事其实是同一件事。这里是先付钱、后有作品；其他每一条都是先把画画出来，之后才谈卖不卖得掉。没有库存，也没有卖不掉的存货堆在房间里。这也是这里唯一一条“先被委托、后动笔”的路——有没有人要，在落第一笔之前就有答案了。


**Replace with**

确认委托后，可以按约定的项目和付款节点安排工作。持续合作的客户有助于提高可预期性，但每月收入仍取决于订单与结算。


**Reason:** Remove guaranteed monthly income, universal prepayment and dismissive “最不浪漫”.


### futures_engine.py · 209 · Rewrite

[engines/futures_engine.py:1170](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1170)

**Current**

> 题材、进度和最终画面不再完全是你的。一张 70,000 日元的封面，和你自己一张原作挣到的差不多，而原作没有附带任何要求。另外，不同客户之间价差极大——所以才有那句话：你拿什么作品集，就接到什么活。


**Replace with**

需要留出沟通、修改和交付的时间，并确认作品能否继续展示或使用。与原作销售比较时，应同时考虑实际结余、投入时间和保留的权利。


**Reason:** Original list price and commission net return not comparable; no shaming portfolio slogan.


### futures_engine.py · 210 · Retain wording

[engines/futures_engine.py:1189](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1189)

**Current**

> 直接卖


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 211 · Rewrite

[engines/futures_engine.py:1199](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1199)

**Current**

> 自己的店，自己定价，成本之上全归你。


**Replace with**

沿用自己的店铺，安排产品和定价。


**Reason:** No implied net-profit guarantee.


### futures_engine.py · 212 · Retain wording

[engines/futures_engine.py:1205](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1205)

**Current**

> 画廊


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 213 · Rewrite

[engines/futures_engine.py:1206](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1206)

**Current**

> 画廊卖你的原作，并且负责找买家。


**Replace with**

比较展览支持、销售服务与合作费用。


**Reason:** Tell her what useful research is inside.


### futures_engine.py · 214 · Retain wording

[engines/futures_engine.py:1212](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1212)

**Current**

> 图像授权


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 215 · Rewrite

[engines/futures_engine.py:1213](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1213)

**Current**

> 有人付钱，使用你已经画好的一张画。


**Replace with**

看看现有作品还可以用于哪些产品。


**Reason:** Preview usefulness.


### futures_engine.py · 216 · Retain wording

[engines/futures_engine.py:1219](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1219)

**Current**

> 出版


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 217 · Rewrite

[engines/futures_engine.py:1220](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1220)

**Current**

> 由出版社把你的作品做成一本书，钱也由他们出。


**Replace with**

把作品整理成选题，了解出版社如何接案。


**Reason:** No cost-bearing promise before contract.


### futures_engine.py · 218 · Retain wording

[engines/futures_engine.py:1226](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1226)

**Current**

> 委托


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### futures_engine.py · 219 · Rewrite

[engines/futures_engine.py:1227](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1227)

**Current**

> 有人付钱请你按要求画一张新的。


**Replace with**

整理作品资料与报价，准备回应项目询问。


**Reason:** No elementary definition; useful content preview.


### futures_engine.py · 220 · Rewrite

[engines/futures_engine.py:1268](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1268)

**Current**

> 五个账号合计约 23.3 万人在看着，店铺已经在跑；价位到 2,200 日元就断了，再往上直接跳到 31,900。


**Replace with**

你已有自己的店铺，也在多个平台积累了关注。这里比较印刷品的制作成本、定价和销售方式。


**Reason:** Remove sum of follows = people watching, and deficiency framing.


### futures_engine.py · 221 · Rewrite

[engines/futures_engine.py:1279](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1279)

**Current**

> {solos} 场个展、{groups} 场联展，最近的一场在原宿的 Galerie LE MONDE。


**Replace with**

已有 {solos} 场个展和 {groups} 场已确认联展，最近一场是 {latest_exhibition}。


**Reason:** Introduce latest_exhibition from the current verified record; omit that clause when unavailable. Counts must not silently become zero. This is a template proposal, not a drop-in source patch.


### futures_engine.py · 222 · Rewrite

[engines/futures_engine.py:1287](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1287)

**Current**

> 一个能卖进室内、酒店餐饮、文具和出版的题材——角色类作品到不了的那些品类。


**Replace with**

建筑、室内与光线题材，可以用于研究书封、文具和空间装饰类的合作。


**Reason:** No claim character artists cannot enter huge overlapping categories.


### futures_engine.py · 223 · Rewrite

[engines/futures_engine.py:1291](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1291)

**Current**

> {zines} 本 zine、{pubs} 本出版物，还有六年每天画下来的画，够从里面做出一本书。


**Replace with**

已有 {zines} 本 zine 和 {pubs} 本出版物，也有六年的水彩日记可供整理。


**Reason:** Counts are source-driven; remove automatic “enough for a book” judgment.


### futures_engine.py · 224 · Rewrite

[engines/futures_engine.py:1295](C:/ScottStuff/GalleryAgentAI/engines/futures_engine.py:1295)

**Current**

> 六年每天按时把画交出来，以及一个日本文学出版社会买来做封面的题材。


**Replace with**

持续的水彩创作，已经积累出可供编辑了解的作品。这里整理介绍材料与报价方式。


**Reason:** Daily self-directed practice is not client deadline performance.


## engines/book_economics_engine.py


### book_economics_engine.py · 001 · Retain wording

[engines/book_economics_engine.py:75](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:75)

**Current**

> 在中国印


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### book_economics_engine.py · 002 · Rewrite

[engines/book_economics_engine.py:76](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:76)

**Current**

> 运抵东京、含运费。这些是报给英语使用者的价格；同一份规格用中文去问，是另一个价格。


**Replace with**

按当前估算包含运抵东京的费用；最终以同一规格的书面报价为准。


**Reason:** Chinese language does not guarantee a lower price; landed terms require confirmation.


### book_economics_engine.py · 003 · Retain wording

[engines/book_economics_engine.py:82](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:82)

**Current**

> 在日本印，数码印刷


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### book_economics_engine.py · 004 · Rewrite

[engines/book_economics_engine.py:83](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:83)

**Current**

> 两周交货，不用过海关——但尺寸上限是 B5，页数约 96 页。


**Replace with**

这项方案按供应商的尺寸、页数与交期范围估算，最终规格和交付时间需另行确认。


**Reason:** B5/96-page route is not equivalent to 128-page hardcover; show spec in comparison.


### book_economics_engine.py · 005 · Retain wording

[engines/book_economics_engine.py:89](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:89)

**Current**

> 在日本印，A4 胶印


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### book_economics_engine.py · 006 · Rewrite

[engines/book_economics_engine.py:90](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:90)

**Current**

> 在日本做全尺寸精装的做法。列在这里，是因为多数人以为只能这样做。


**Replace with**

日本 A4 胶印方案；需核对纸张、页数、装订和交付费用。


**Reason:** Remove assumptions about what most people believe.


### book_economics_engine.py · 007 · Hold for model correction

[engines/book_economics_engine.py:200](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:200)

**Current**

> 同样是印 100 本，如果定价 11,000 日元，卖 41 本就能回本。小批量不是靠多卖救回来的，是靠封底那个价格。


**Replace with**

提高定价会改变收回预付支出所需的销量，也可能影响需求。可以把不同售价作为测算情景，比较各自的条件。


**Reason:** Hardcoded 41 differs from computed value and faulty model; no guaranteed rescue by pricing.


### book_economics_engine.py · 008 · Rewrite

[engines/book_economics_engine.py:211](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:211)

**Current**

> 做一本书要花多少钱，可以在开始之前精确到日元算出来；能卖多快，则完全算不出来。一头是固定的价钱，另一头是没有底的销售速度——要决定的全部就是这个落差，而把这个落差接过去，正是出版社的作用。


**Replace with**

印制成本可以先询价，销量和销售速度则需要通过实际订单了解。这里把预付支出、销售费用和不同销量下的结果放在一起，帮助比较自出版与出版社合作。


**Reason:** Not precise to yen before quote; not all uncertainty unknowable.


### book_economics_engine.py · 009 · Hold for model correction

[engines/book_economics_engine.py:226](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:226)

**Current**

> 钱是能回来的，只是周期长。{_fen(ref['outlay_jpy'])} 换来 {ref['run']} 本；卖到第 {ref['breakeven_direct']} 本这批印量就付清了，剩下的 {left} 本是净赚。准确的说法是「慢」——下面的数字说明的正是它为什么慢。


**Replace with**

达到测算中的销量后，销售回款可覆盖模型列出的预付支出。之后的每笔订单仍可能产生平台、包装和配送费用；最终收益也取决于实际售出数量。


**Reason:** Remove assured recovery, “only slow,” and remaining stock = pure profit.


### book_economics_engine.py · 010 · Rewrite

[engines/book_economics_engine.py:237](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:237)

**Current**

> 这 {_fen(ref['outlay_jpy'])} 由谁来出


**Replace with**

前期费用由谁承担


**Reason:** Avoid promoting provisional number.


### book_economics_engine.py · 011 · Rewrite

[engines/book_economics_engine.py:240](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:240)

**Current**

> 先要付的钱


**Replace with**

预付支出


**Reason:** Natural cash-flow term.


### book_economics_engine.py · 012 · Rewrite

[engines/book_economics_engine.py:241](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:241)

**Current**

> 回本点


**Replace with**

收回预付支出所需销量


**Reason:** Define metric consistently.


### book_economics_engine.py · 013 · Rewrite

[engines/book_economics_engine.py:242](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:242)

**Current**

> 每卖一本


**Replace with**

每本收入与扣费口径


**Reason:** Avoid gross/net mismatch.


### book_economics_engine.py · 014 · Rewrite

[engines/book_economics_engine.py:243](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:243)

**Current**

> 能到达的地方


**Replace with**

发行渠道


**Reason:** Precise heading.


### book_economics_engine.py · 015 · Rewrite

[engines/book_economics_engine.py:244](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:244)

**Current**

> 书放在哪里


**Replace with**

库存与履约


**Reason:** Professional rather than books in bedroom.


### book_economics_engine.py · 016 · Rewrite

[engines/book_economics_engine.py:245](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:245)

**Current**

> 不确定的那一项


**Replace with**

仍需确认的条件


**Reason:** More than one unknown.


### book_economics_engine.py · 017 · Retain wording

[engines/book_economics_engine.py:250](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:250)

**Current**

> 自己出版


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### book_economics_engine.py · 018 · Hold for model correction

[engines/book_economics_engine.py:252](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:252)

**Current**

> {_fen(ref['outlay_jpy'])}——{ref['run']} 本，在中国印，运抵东京


**Replace with**

按所选规格、印量和交付条件计算的预付费用。


**Reason:** Real amount must regenerate from corrected model.


### book_economics_engine.py · 019 · Hold for model correction

[engines/book_economics_engine.py:254](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:254)

**Current**

> {ref['run']} 本里的第 {ref['breakeven_direct']} 本；剩下 {left} 本是净赚


**Replace with**

按实际单笔回款计算，显示收回整批预付支出所需的销量。


**Reason:** Remove remaining copies pure profit.


### book_economics_engine.py · 020 · Hold for model correction

[engines/book_economics_engine.py:256](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:256)

**Current**

> 直接卖出，{_fen(ref['margin_direct_jpy'])}


**Replace with**

按直售价格扣除模型列明的销售费用后计算。


**Reason:** Define costs once; do not subtract prepaid production cost twice.


### book_economics_engine.py · 021 · Rewrite

[engines/book_economics_engine.py:258](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:258)

**Current**

> 自己的店铺、几家寄售的书店、一次一个展位


**Replace with**

自己的店铺，以及已确认接受寄售或参展的渠道。


**Reason:** No assumed consignment acceptance.


### book_economics_engine.py · 022 · Rewrite

[engines/book_economics_engine.py:260](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:260)

**Current**

> {ref['run']} 本精装书堆在房间里，直到卖完


**Replace with**

需要安排库存空间、包装和发货，也可询问仓储或代发服务。


**Reason:** Avoid dramatized books piled in room.


### book_economics_engine.py · 023 · Rewrite

[engines/book_economics_engine.py:262](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:262)

**Current**

> 卖到第 {ref['breakeven_direct']} 本要多久


**Replace with**

实际订单量与销售周期。


**Reason:** Unknown timing without faulty threshold.


### book_economics_engine.py · 024 · Rewrite

[engines/book_economics_engine.py:268](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:268)

**Current**

> 有出版社


**Replace with**

出版社承担制作与发行的合作


**Reason:** Distinguish contract models.


### book_economics_engine.py · 025 · Rewrite

[engines/book_economics_engine.py:270](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:270)

**Current**

> 不用付


**Replace with**

是否需要作者出资，以合作方案为准。


**Reason:** No universal zero-cost guarantee.


### book_economics_engine.py · 026 · Rewrite

[engines/book_economics_engine.py:271](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:271)

**Current**

> 没有要收回的钱


**Replace with**

如无作者预付制作费用，则无需回收这笔制作支出。


**Reason:** Still time/opportunity cost; specify cash item.


### book_economics_engine.py · 027 · Rewrite

[engines/book_economics_engine.py:272](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:272)

**Current**

> 版税。日本的惯例是定价的 {int(ROYALTY_BAND[0] * 100)}–{int(ROYALTY_BAND[1] * 100)}%，在这里大约 {_fen(roy_lo)}–{_fen(roy_hi)}，对比自己直接卖的 {_fen(ref['margin_direct_jpy'])}。这是行业惯例，不是谁开出的条件——目前没有任何出版社报过价。


**Replace with**

版税收入需按合同中的计价基数、比例和结算方式计算。这里的示例只是测算情景，尚无出版社向你提出具体条件。


**Reason:** Do not treat 8–10% as universal Japanese rate or compare gross royalty to inconsistent margin.


### book_economics_engine.py · 028 · Rewrite

[engines/book_economics_engine.py:278](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:278)

**Current**

> 全国的书店


**Replace with**

合同中约定的书店及线上发行渠道。


**Reason:** Nationwide book distribution not guaranteed placement.


### book_economics_engine.py · 029 · Rewrite

[engines/book_economics_engine.py:279](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:279)

**Current**

> 出版社的仓库


**Replace with**

库存由谁保管、退货如何处理，以合同约定为准。


**Reason:** Publisher warehouse not universal.


### book_economics_engine.py · 030 · Rewrite

[engines/book_economics_engine.py:280](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:280)

**Current**

> 对方同不同意


**Replace with**

选题是否采用，以及制作、权利和结算条款。


**Reason:** Acceptance not sole unknown.


### book_economics_engine.py · 031 · Rewrite

[engines/book_economics_engine.py:284](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:284)

**Current**

> Mateusz Urbanowicz 画东京的那两本书——《东京店构え》《东京夜行》——由 MdN 出版，不是自出版，这个系列在日本卖过十万册。自出版没有任何途径能到那个数字；反过来，自出版也不需要等谁点头。这就是这笔交易的全部内容。


**Replace with**

Mateusz Urbanowicz 与 MdN 的合作，可以作为城市水彩出版的案例。值得研究的是选题、样页和发行方式；个案销量不能直接推算你的销量。


**Reason:** Remove false claim self-publishing has no path to 100k; publication example not sales forecast.


### book_economics_engine.py · 032 · Rewrite

[engines/book_economics_engine.py:296](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:296)

**Current**

> 书实际上卖得有多快


**Replace with**

销售速度：目前能参考什么


**Reason:** Distinguish known case from forecast.


### book_economics_engine.py · 033 · Rewrite

[engines/book_economics_engine.py:298](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:298)

**Current**

> 日本艺术书展的中位数是 {FAIR_MEDIAN_LOW}–{FAIR_MEDIAN_HIGH} 本。只靠书展的话，{ref['breakeven_direct']} 本要摆 {fairs_lo}–{fairs_hi} 次摊。


**Replace with**

已有参展者案例可用于了解书展销售，但样本中的销量不能代表整个市场。比较时需注明书展、展期、产品价格、样本数量和统计方式。


**Reason:** Mixed self-selected sample not national art-book-fair median.


### book_economics_engine.py · 034 · Hold for model correction

[engines/book_economics_engine.py:302](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:302)

**Current**

> 东京艺术书展最便宜的展位是 {_fen(FAIR_BOOTH_JPY)}，销售不抽成。按这里的成本，卖 {booth_copies} 本就回本了——第一个小时之内。


**Replace with**

参展费用需要单独计算：展位、交通、运输和值守等支出，再除以每本新增销售带来的净回款。这个数表示覆盖参展费用所需的销量，不能据此推算多久能卖完。


**Reason:** Delete first-hour prediction; distinguish incremental event cost from run cash recovery.


### book_economics_engine.py · 035 · Hold for model correction

[engines/book_economics_engine.py:306](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:306)

**Current**

> 按 70/30 的标准寄售分成，落地成本要低于大约 {_fen(CONSIGNMENT_UNIT_CEILING)} 才有得赚，在这几条路里就是中国印 {ref['run']} 本以上。所以印多少和在哪里卖是同一个决定，不是两个。


**Replace with**

寄售分成会影响每本回款。可以在相同售价和成本条件下，分别测算直售与寄售，再决定印量和渠道。


**Reason:** Fixed ¥1,500 universal threshold does not follow from supplied numbers.


### book_economics_engine.py · 036 · Rewrite

[engines/book_economics_engine.py:329](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:329)

**Current**

> 每一条路的算法


**Replace with**

计算条件与明细


**Reason:** “算法” is internal implementation vocabulary.


### book_economics_engine.py · 037 · Rewrite

[engines/book_economics_engine.py:330](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:330)

**Current**

> 在这份清单上，印一本书是唯一一件事先就能知道价钱的事。其余每一样，都是先申请，然后等。


**Replace with**

每项测算都列明规格、费用来源、查询日期和未计入的支出。


**Reason:** Replace false unique knowable-price assertion.


### book_economics_engine.py · 038 · Rewrite

[engines/book_economics_engine.py:333](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:333)

**Current**

> 回本的数字可以算出来，能卖多少本却算不出来。这里每一个数字都有出处；而销售数字是别人书展的中位数，不是预测。


**Replace with**

这些数字用于比较方案。供应商报价、实际订单及未计入的费用变化后，结果也需要更新。


**Reason:** No “every figure sourced” blanket; disclose limitations at point of use.


## engines/recurring_calendar_engine.py


### recurring_calendar_engine.py · 001 · Rewrite

[engines/recurring_calendar_engine.py:59](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:59)

**Current**

> TOKAS-Emerging（东京都现代美术空间）


**Replace with**

TOKAS-Emerging


**Reason:** Do not misname Tokyo Arts and Space as Museum of Contemporary Art Tokyo.


### recurring_calendar_engine.py · 002 · Rewrite with verified source

[engines/recurring_calendar_engine.py:62](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:62)

**Current**

> 免费场地、15 万日元制作经费，布展与宣传都由他们负责。在日本居住即可，不限国籍，1990 年 4 月 1 日或之后出生。


**Replace with**

2027 年度要项提供免费场地、15 万日元制作支持，以及部分布展、运输和宣传支持。申请者须在日本居住，并于 1991 年 4 月 1 日及以后出生；该轮已截止。下一轮条件以新要项为准。


**Reason:** Official page verified: birth cutoff is 1991, not 1990; support is partial, not all tasks done.


### recurring_calendar_engine.py · 003 · Rewrite

[engines/recurring_calendar_engine.py:73](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:73)

**Current**

> 一份展览提案，和十张能作为一个整体挂在一起的画。


**Replace with**

按当届要求准备展览方案与作品集，说明作品如何在空间中呈现。


**Reason:** Do not invent ten-image universal requirement.


### recurring_calendar_engine.py · 004 · Retain wording

[engines/recurring_calendar_engine.py:84](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:84)

**Current**

> TOKAS OPEN SITE


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### recurring_calendar_engine.py · 005 · Hold for source

[engines/recurring_calendar_engine.py:87](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:87)

**Current**

> 暂停中。TOKAS 本乡馆正在施工，下一次征集要到 2027 年度以后，所以今年二月这一轮不会有。


**Replace with**

下一轮开放情况需以 TOKAS 官方公告为准。


**Reason:** Source archive lists OPEN SITE 11 in February 2026; verify claimed suspension against precise cycle before retaining.


### recurring_calendar_engine.py · 006 · Hold for source

[engines/recurring_calendar_engine.py:91](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:91)

**Current**

> 40 万日元展览经费，不限年龄，接受个展提案。


**Replace with**

制作支持金额、展览形式和申请资格，按当届要项列明。


**Reason:** Separate historical allowance from future promise.


### recurring_calendar_engine.py · 007 · Rewrite

[engines/recurring_calendar_engine.py:95](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:95)

**Current**

> 同一批作品，外加一份「它如何撑起一个空间」的书面构想。


**Replace with**

一组相关作品，以及空间使用和展示方式的说明。


**Reason:** Natural preparation language.


### recurring_calendar_engine.py · 008 · Rewrite

[engines/recurring_calendar_engine.py:107](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:107)

**Current**

> TOKAS 驻地（国内・交流）


**Replace with**

TOKAS 驻留项目（国内／交流）


**Reason:** 驻留 is standard; different programs must be separate entries.


### recurring_calendar_engine.py · 009 · Hold for source

[engines/recurring_calendar_engine.py:111](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:111)

**Current**

> 在墨田驻留 60–90 天并有制作费，或全额资助约 3 个月，前往台北、首尔或赫尔辛基。不限国籍。


**Replace with**

国内驻留与海外交流的地点、时长、经费和资格不同，需分别查看当届要项。


**Reason:** Do not merge several programs into one universally eligible offer.


### recurring_calendar_engine.py · 010 · Rewrite

[engines/recurring_calendar_engine.py:115](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:115)

**Current**

> 一个「为什么要去那里」的理由——那个地方会让作品发生什么变化。


**Replace with**

研究主题、选择该地点的原因，以及计划开展的交流或创作。


**Reason:** Concrete proposal elements; no rhetorical question.


### recurring_calendar_engine.py · 011 · Retain wording

[engines/recurring_calendar_engine.py:125](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:125)

**Current**

> SICF（青山 Spiral）


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### recurring_calendar_engine.py · 012 · Hold for source

[engines/recurring_calendar_engine.py:128](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:128)

**Current**

> 评审制，艺术家可直接报名，不限年龄与国籍。展位费从 48,400 日元起。其中一位拿到大奖——在 Spiral 中庭办个展，外加 50 万日元。


**Replace with**

评审制展示项目。报名费用、展位规格、奖项与资格，需按当届要项核对。


**Reason:** Current event fees and awards need maintained source.


### recurring_calendar_engine.py · 013 · Rewrite

[engines/recurring_calendar_engine.py:132](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:132)

**Current**

> 要能从远处一眼看住的作品——展位首先是被远远看见的。


**Replace with**

一组适合展位尺度的作品，以及展示布局和作品说明。


**Reason:** “一眼看住” is unnatural; do not prescribe spectacle to quiet painter.


### recurring_calendar_engine.py · 014 · Retain wording

[engines/recurring_calendar_engine.py:141](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:141)

**Current**

> Independent Tokyo


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### recurring_calendar_engine.py · 015 · Rewrite

[engines/recurring_calendar_engine.py:144](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:144)

**Current**

> 由主办方筛选，现场有 20–30 位画廊主担任评审——这是画廊发掘新人的公认渠道之一。展位费约 45,000 日元起。


**Replace with**

可用于了解独立艺术家的展示与行业交流机会。参展费用、筛选方式和评审名单需按当届公告确认。


**Reason:** Remove unsupported recognized pipeline and static juror count.


### recurring_calendar_engine.py · 016 · Rewrite

[engines/recurring_calendar_engine.py:148](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:148)

**Current**

> 一面完整连贯的墙，和一句能回答「最近在做什么」的简短说明——现场每一位画廊主都会问这句。


**Replace with**

一组方向连贯的作品，以及一段简短的创作介绍。


**Reason:** No prediction of what every gallery owner asks.


### recurring_calendar_engine.py · 017 · Retain wording

[engines/recurring_calendar_engine.py:160](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:160)

**Current**

> HB Gallery FILE 大赛


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### recurring_calendar_engine.py · 018 · Hold for source

[engines/recurring_calendar_engine.py:164](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:164)

**Current**

> 没有任何资格限制——国籍、年龄、居住地、学生身份都不设门槛。十位特别奖得主，大奖得主各获得表参道的一周个展。


**Replace with**

申请资格、入选名额与获奖后的展览安排，以当届要项为准。


**Reason:** Current sentence ambiguously awards solo shows to all ten; verify categories.


### recurring_calendar_engine.py · 019 · Rewrite

[engines/recurring_calendar_engine.py:168](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:168)

**Current**

> 15–20 张作为一组来选的作品——评审是艺术总监，不是策展人。


**Replace with**

按当届要求整理作品集，并说明作品的关联与应用方向。


**Reason:** Do not generalize jury roles or portfolio count.


### recurring_calendar_engine.py · 020 · Retain wording

[engines/recurring_calendar_engine.py:179](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:179)

**Current**

> biscuit gallery「grid next」


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### recurring_calendar_engine.py · 021 · Rewrite

[engines/recurring_calendar_engine.py:183](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:183)

**Current**

> 免费报名、免费参展，接受学生——其中一位可获得个展。年龄大致在 40 岁以下。


**Replace with**

可查看下一轮的申请资格、收费及入选后的展览安排。


**Reason:** Need latest conditions rather than permanent age/fee promise.


### recurring_calendar_engine.py · 022 · Rewrite

[engines/recurring_calendar_engine.py:187](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:187)

**Current**

> 一张新画，并且在展览之前不发到 Instagram——这个征集只收未发表的作品。


**Replace with**

申请前核对作品的发表限制；如要求未发表，需确认社交平台展示是否包含在限制内。


**Reason:** New painting and Instagram embargo cannot be commanded from assumed rule.


### recurring_calendar_engine.py · 023 · Retain wording

[engines/recurring_calendar_engine.py:194](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:194)

**Current**

> 京都艺术中心 Co-program


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### recurring_calendar_engine.py · 024 · Hold for source

[engines/recurring_calendar_engine.py:197](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:197)

**Current**

> 目前在日本找到的经费最充裕的公开征集——个展最高 100 万日元，外加六周工作室。


**Replace with**

可比较制作支持、空间使用和项目执行要求。金额与支持期限按当届要项列明。


**Reason:** Remove superlative across Japan and fixed unverified support.


### recurring_calendar_engine.py · 025 · Rewrite

[engines/recurring_calendar_engine.py:201](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:201)

**Current**

> 要的是一个项目，而不是作品集——他们资助的是正在发生的创作，不是已完成的东西。


**Replace with**

一份包含创作主题、实施计划、预算和成果呈现方式的项目提案。


**Reason:** Project grants not blanket ban on existing work.


### recurring_calendar_engine.py · 026 · Rewrite

[engines/recurring_calendar_engine.py:212](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:212)

**Current**

> 东京艺术委员会 创业期扶持金


**Replace with**

Arts Council Tokyo「スタートアップ助成」


**Reason:** 创业期扶持金 misleadingly sounds startup-business grant; retain official title.


### recurring_calendar_engine.py · 027 · Rewrite

[engines/recurring_calendar_engine.py:216](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:216)

**Current**

> 在东京举办公开活动最高 30 万日元——这是一笔办事的预算，不是收入。无国籍限制，但要求在东京居住。一年两轮，错过一轮还有下一轮。


**Replace with**

这类资助支持在东京开展的艺术活动。申请资格、补助上限和可计入的费用，应按当轮指南分别确认。


**Reason:** Retain useful project-cost distinction without assuming eligibility or recurring rounds.


### recurring_calendar_engine.py · 028 · Rewrite

[engines/recurring_calendar_engine.py:220](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:220)

**Current**

> 一个本来就打算做的展览——它资助的是这件事本身，不是一个新点子。


**Replace with**

活动方案、实施时间、预算，以及已确认的场地或合作安排。


**Reason:** Avoid invented already-planned-project requirement.


### recurring_calendar_engine.py · 029 · Retain wording

[engines/recurring_calendar_engine.py:231](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:231)

**Current**

> 野村财团 艺术文化助成


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### recurring_calendar_engine.py · 030 · Hold for source

[engines/recurring_calendar_engine.py:234](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:234)

**Current**

> 最高 100 万日元，用于活动本身。无国籍、居住地或年龄限制。国内这一项资助的是在日本进行的活动，所以中日交流展是以日本这一边的部分符合条件。


**Replace with**

需按具体资助类别核对活动地点、申请人资格、经费上限与可支持的项目。


**Reason:** Do not universalize no nationality/age/residence constraints across categories.


### recurring_calendar_engine.py · 031 · Rewrite

[engines/recurring_calendar_engine.py:238](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:238)

**Current**

> 另一边要有个合作方——这个项目的结构就是两个地方。


**Replace with**

按所申请类别准备项目方案；涉及跨地区合作时，说明双方分工与合作安排。


**Reason:** Two-location requirement not established for whole foundation.


### recurring_calendar_engine.py · 032 · Retain wording

[engines/recurring_calendar_engine.py:251](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:251)

**Current**

> 亚洲文化协会 个人奖助


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### recurring_calendar_engine.py · 033 · Rewrite

[engines/recurring_calendar_engine.py:255](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:255)

**Current**

> 最高 3.5 万美元。资格看的是国籍，所以中国护照在哪里都算数——单靠日本的留学签证则不算。它要求五年的创作经历，并且奖助期间要从课业中暂时抽身。


**Replace with**

ACC 的个人奖助支持符合条件的研究与文化交流。申请资格、目的地、时间和在读期间的安排，需按当届指南逐项确认。


**Reason:** Nationality alone does not settle eligibility; current official page does not substantiate blanket five-year rule.


### recurring_calendar_engine.py · 034 · Rewrite

[engines/recurring_calendar_engine.py:259](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:259)

**Current**

> 先要弄清楚的是「休学」这一条，因为留学在留资格本身以在学为前提。外国人在留综合信息中心可以免费咨询这类问题。


**Replace with**

如计划涉及休学或长期离境，需向学校和相关机构确认具体安排。


**Reason:** Do not infer her current visa; no categorical immigration ruling.


### recurring_calendar_engine.py · 035 · Rewrite

[engines/recurring_calendar_engine.py:263](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:263)

**Current**

> 推荐人，以及一份以「月」而不是「周」为单位的计划。三个月是实际需要的准备期——这是清单上最长的一份申请。


**Replace with**

研究计划、拟联系的机构与推荐材料。准备时间取决于项目范围和材料要求。


**Reason:** No universal three-month preparation claim.


### recurring_calendar_engine.py · 036 · Rewrite

[engines/recurring_calendar_engine.py:270](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:270)

**Current**

> 好乐门（Holbein）奖学金


**Replace with**

荷尔拜因（Holbein）奖学金


**Reason:** Correct established Chinese brand spelling; retain Japanese official name if region preference differs.


### recurring_calendar_engine.py · 037 · Hold for source

[engines/recurring_calendar_engine.py:273](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:273)

**Current**

> 一年内价值 30 万日元的画材，来自一家水彩颜料厂商。在日本居住即可，无国籍限制。


**Replace with**

画材支持项目。支持品类、金额、申请资格和材料要求，需查看当届公告。


**Reason:** Do not make medium sufficient for eligibility.


### recurring_calendar_engine.py · 038 · Rewrite

[engines/recurring_calendar_engine.py:277](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:277)

**Current**

> 几乎不需要准备——媒介本身就是最好的理由。


**Replace with**

按当届要求整理作品、创作说明和所需画材。


**Reason:** Remove “almost no preparation” assumption.


### recurring_calendar_engine.py · 039 · Retain wording

[engines/recurring_calendar_engine.py:284](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:284)

**Current**

> 福冈亚洲美术馆 驻地


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### recurring_calendar_engine.py · 040 · Hold for source

[engines/recurring_calendar_engine.py:287](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:287)

**Current**

> 由美术馆主办、以展览收尾的驻地项目。专为在亚洲各地创作的艺术家而设——不限居住地与国籍。


**Replace with**

美术馆驻留项目。需确认当届面向的申请地区、资格、驻留安排与成果要求。


**Reason:** Asian-targeted and unrestricted nationality/residence are not equivalent.


### recurring_calendar_engine.py · 041 · Rewrite

[engines/recurring_calendar_engine.py:291](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:291)

**Current**

> 往返两座城市的创作本身就是申请内容——在两地之间移动对作品做了什么。


**Replace with**

说明研究或创作主题、与当地的关联，以及驻留期间的计划。


**Reason:** Do not assume her practice consists of moving between two cities.


### recurring_calendar_engine.py · 042 · Retain wording

[engines/recurring_calendar_engine.py:301](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:301)

**Current**

> 东京艺术书展 TABF


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### recurring_calendar_engine.py · 043 · Rewrite

[engines/recurring_calendar_engine.py:304](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:304)

**Current**

> 在 zine、艺术家书和买这些东西的人当中占一个展位——这是印刷品的圈子。最便宜的桌子 16,500 日元，销售不抽成。


**Replace with**

艺术书、zine 与独立出版物的展示和销售场合。展位费用、展期和参展要求按当届公告列明。


**Reason:** Cheapest historical booth is not available to all applicants.


### recurring_calendar_engine.py · 044 · Rewrite

[engines/recurring_calendar_engine.py:308](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:308)

**Current**

> 2027 年 1 月这一届已经满了——报名在 2026 年六月就截止了——能进的是再下一届。征集通常在春天开始。


**Replace with**

2027 年 1 月这一届的申请已截止。下一轮开放时间需等官方公布，往届月份仅供准备时参考。


**Reason:** Closed applications not proof fully booked; avoid invented next opportunity.


### recurring_calendar_engine.py · 045 · Rewrite

[engines/recurring_calendar_engine.py:312](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:312)

**Current**

> 一件印好、做完的东西。三个月说的是制作时间；填表只要一个下午。


**Replace with**

可展示和销售的出版物，以及定价、库存、配送和值守计划。


**Reason:** No fixed three-month or afternoon estimate.


### recurring_calendar_engine.py · 046 · Retain wording

[engines/recurring_calendar_engine.py:329](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:329)

**Current**

> Elizabeth Greenshields 基金会


**Reason:** Clear label, proper name or numeric cell. Retain wording; verify factual/numeric fields under the cross-cutting checks.


### recurring_calendar_engine.py · 047 · Hold for source

[engines/recurring_calendar_engine.py:331](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:331)

**Current**

> 具象绘画的首次资助约 1.8 万加元。18–41 岁，明确接受学生申请，且完全没有国籍或居住地要求。


**Replace with**

面向具象艺术创作的资助。年龄、申请资格、支持金额与材料要求，需查看基金会当前说明。


**Reason:** Specific age boundary and unrestricted scope need source check.


### recurring_calendar_engine.py · 048 · Rewrite

[engines/recurring_calendar_engine.py:335](C:/ScottStuff/GalleryAgentAI/engines/recurring_calendar_engine.py:335)

**Current**

> 常年接受申请——没有会错过的截止日期。近期作品的图片，加一段简短的说明：现在在画什么。


**Replace with**

可先整理近期作品图片与创作说明，再按基金会当前申请清单补齐材料。


**Reason:** Rolling does not mean no detailed requirements.


## engines/outreach_kit_engine.py


### outreach_kit_engine.py · 001 · Out of current UI

[engines/outreach_kit_engine.py:67](C:/ScottStuff/GalleryAgentAI/engines/outreach_kit_engine.py:67)

**Current**

> 一个链接——Instagram，或者一个网页相册。来自陌生寄件人的附件，通常不会被打开。


**Reason:** Not rendered by current Saffron. Do not spend the next release polishing unmounted etiquette copy.


### outreach_kit_engine.py · 002 · Out of current UI

[engines/outreach_kit_engine.py:69](C:/ScottStuff/GalleryAgentAI/engines/outreach_kit_engine.py:69)

**Current**

> 五张，来自同一个系列，而不是跨越整个创作的选集。对方要判断的是这批作品能不能撑起一面墙，而不是它能有多少种面貌。


**Reason:** Not rendered by current Saffron. Do not spend the next release polishing unmounted etiquette copy.


### outreach_kit_engine.py · 003 · Out of current UI

[engines/outreach_kit_engine.py:71](C:/ScottStuff/GalleryAgentAI/engines/outreach_kit_engine.py:71)

**Current**

> 写明去看过他们哪一场展的那句话，是整封信里唯一无法伪造的部分，也是会被读两遍的部分。


**Reason:** Not rendered by current Saffron. Do not spend the next release polishing unmounted etiquette copy.


### outreach_kit_engine.py · 004 · Out of current UI

[engines/outreach_kit_engine.py:73](C:/ScottStuff/GalleryAgentAI/engines/outreach_kit_engine.py:73)

**Current**

> 第一封信请求的是“看一下”，不是一次展览。请求展览就成了提案，而提案是可以被否决的。


**Reason:** Not rendered by current Saffron. Do not spend the next release polishing unmounted etiquette copy.


### outreach_kit_engine.py · 005 · Rewrite

[engines/outreach_kit_engine.py:75](C:/ScottStuff/GalleryAgentAI/engines/outreach_kit_engine.py:75)

**Current**

> 十天没有回音，通常意味着信没有被看到，而不是被拒绝。三个月后下一场展开幕时写第二封，寄信人已经是“来过两次的人”。


**Replace with**

暂时没有回复，原因可能很多。是否再次联系，可以结合对方公开的联系说明，以及你是否有新的展览或作品消息来决定。


**Reason:** Silence is not evidence an email was unseen. Never manufacture a second visit or scheduled repeated outreach.


### outreach_kit_engine.py · 006 · Out of current UI

[engines/outreach_kit_engine.py:77](C:/ScottStuff/GalleryAgentAI/engines/outreach_kit_engine.py:77)

**Current**

> 尺寸和价格在对方问起之前不写。没被问就写上，信就变成了一份报价单。


**Reason:** Not rendered by current Saffron. Do not spend the next release polishing unmounted etiquette copy.


### outreach_kit_engine.py · 007 · Out of current UI

[engines/outreach_kit_engine.py:84](C:/ScottStuff/GalleryAgentAI/engines/outreach_kit_engine.py:84)

**Current**

> 第一封信


**Reason:** Not rendered by current Saffron. Do not spend the next release polishing unmounted etiquette copy.


### outreach_kit_engine.py · 008 · Out of current UI

[engines/outreach_kit_engine.py:85](C:/ScottStuff/GalleryAgentAI/engines/outreach_kit_engine.py:85)

**Current**

> 东京的画廊不设投稿箱；进入的方式是先到场，然后写信。有效的第一封信很短——去看过的那场展、三句话的自我介绍、一个链接、五张画。信里没有任何请求，所以没有什么可以被拒绝；而任何一句回复，本身就是一份要求说明。


**Reason:** Not rendered by current Saffron. Do not spend the next release polishing unmounted etiquette copy.


### outreach_kit_engine.py · 009 · Out of current UI

[engines/outreach_kit_engine.py:94](C:/ScottStuff/GalleryAgentAI/engines/outreach_kit_engine.py:94)

**Current**

> 这封写给 HAGI ART——它自己写明的方向就是年轻创作者的个展与联展，而且不收场地费。换掉第一段，正文对任何一家都成立。


**Reason:** Not rendered by current Saffron. Do not spend the next release polishing unmounted etiquette copy.


### outreach_kit_engine.py · 010 · Out of current UI

[engines/outreach_kit_engine.py:98](C:/ScottStuff/GalleryAgentAI/engines/outreach_kit_engine.py:98)

**Current**

> 在东京，这六件事是真的


**Reason:** Not rendered by current Saffron. Do not spend the next release polishing unmounted etiquette copy.
