# Saffron Chinese audit — grant detail

Source: `frontend/src/data/saffron_insights.js`, `GRANT_LANDSCAPE`. All Chinese leaves in this object were read. Current Saffron renders only named items (0–3); item 4 is internal research, not visible copy. Dates/amounts retained for wording are still time-sensitive and require the source checks in the brief. No claim is made that every grant has been independently reverified.

TOKAS 2027 correction: [official call](https://www.tokyoartsandspace.jp/archive/application/2026/20260616-331.html). ACC purpose/eligibility: [official 2027 guidelines](https://www.asianculturalcouncil.org/grant-opportunities).


## where_to_start_zh — Rewrite / verify conditions

**Current:** TOKAS-Emerging 是最合适的一个，而且不问国籍——只要你住在日本，且出生于 1990 年 4 月 1 日或之后。它给的是 TOKAS 本乡的一个个展，再加 15 万日元的制作支持。2027 年度征集已于 2026 年 7 月 31 日截止；下一轮时间尚未公布。


**Replace with:** TOKAS-Emerging 可作为机构个展的研究对象。2027 年度报名已截止；下面保留当届条件供准备时参考，下一轮以官方新公告为准。

**Reason:** Remove 最合适 and premature eligibility assurance; closed opportunity is not immediate start.


## items.0.country_zh — Retain wording; recheck dated facts

**Current:** 日本（东京）


## items.0.amount_zh — Rewrite / verify conditions

**Current:** TOKAS 本乡的个展 ＋ 15 万日元制作支持


**Replace with:** 2027 年度：免费展览空间与 15 万日元制作支持，另有部分布展、运输及宣传支持。

**Reason:** Official page says partial assistance; note date and tax treatment in detail.


## items.0.eligibility_zh — Rewrite / verify conditions

**Current:** 住在日本（日本在住），且 1990 年 4 月 1 日或之后出生。没有国籍要求——2026 年 9 月 8 日核实。


**Replace with:** 2027 年度要求在日本居住，且于 1991 年 4 月 1 日及以后出生，并能承担准备、实施与撤展等责任。其他条件见官方要项。

**Reason:** 2026-09-10 official check: 1991, not 1990. Do not carry fixed birth cutoff into later cycles.


## items.0.deadline_zh — Retain wording; recheck dated facts

**Current:** 2027 年度征集于 2026 年 6 月 26 日至 7 月 31 日开放，现已截止；下一轮尚未公布


## items.0.why_apply_zh — Rewrite / verify conditions

**Current:** 在一个公立机构做一个个展，带制作费，而且条件里没有一句话提到你来自哪里。


**Replace with:** 入选后可在 TOKAS 本乡举办个展，并获得制作与展示方面的支持。

**Reason:** Do not continually frame Chinese identity as barrier or personal exemption.


## items.0.tip_zh — Rewrite / verify conditions

**Current:** TOKAS 和东京艺术委员会是两个不同的机构，各有各的入口、各自开放，尽管同属一个基金会。没有「合并申请」这回事。


**Replace with:** TOKAS 与 Arts Council Tokyo 的项目分别申请，各自的时间、材料和支持范围需要单独核对。

**Reason:** Remove defensive response to imaginary 合并申请 misunderstanding.


## items.1.country_zh — Retain wording; recheck dated facts

**Current:** 日本（东京）


## items.1.amount_zh — Rewrite / verify conditions

**Current:** 个人最高 30 万日元，且须在符合条件的补助经费范围内


**Replace with:** 个人申请最高 30 万日元；实际额度及可计入的费用，以当轮指南为准。

**Reason:** Plain language; source refresh required for current cycle.


## items.1.eligibility_zh — Rewrite / verify conditions

**Current:** 住在东京都内的个人。没有国籍条款。有一件事没有任何地方写明：留学签证算不算「居住」。在为它做任何准备之前，值得先打一通电话（03-6256-8431）。


**Replace with:** 需要核对东京都内居住、艺术活动经历及项目实施等要求。涉及个人情况的部分，可向主办方确认。

**Reason:** Do not invent special doubt that a student visa is not residence or assert she has that status.


## items.1.deadline_zh — Retain wording; recheck dated facts

**Current:** 第二轮截止：2026 年 9 月 24 日 18:00（日本时间）


## items.1.why_apply_zh — Rewrite / verify conditions

**Current:** 它资助的是你自己组织的项目，而不是去投别人的征集——和这页上其他所有东西都不同。


**Replace with:** 可用于符合条件的自主策划艺术活动，例如展览项目。

**Reason:** Remove unique-on-page claim and preserve project-cost purpose.


## items.1.tip_zh — Rewrite / verify conditions

**Current:** 个人申请的资助上限为 30 万日元，且不得超过符合条件的补助对象经费。编制预算前请核对详细指南。


**Replace with:** 准备预算时，按指南分别列出可补助与需自行承担的费用。

**Reason:** Useful, specific action without bureaucratic redundancy.


## items.2.country_zh — Rewrite / verify conditions

**Current:** 美国（面向亚洲艺术家）


**Replace with:** 亚洲及美国的文化交流

**Reason:** Not simply United States for Asian artists; destinations governed by program.


## items.2.amount_zh — Rewrite / verify conditions

**Current:** 最高 35,000 美元，一笔发放、预算由你自己安排，为期 1–6 个月


**Replace with:** 个人奖助的金额、期限和支付安排，以 2027 年度官方指南为准。

**Reason:** Hold unsupported lump-sum claim; do not translate guessed payout mechanism.


## items.2.eligibility_zh — Rewrite / verify conditions

**Current:** 需要属于官方列出的 26 个国家或地区（包括美国）之一的国籍或永久居留权——中国大陆在列，这一关你过。申请人须年满 21 岁，并有五年专业经历。在读期间可以申请，但在受资助的奖学金期间必须办理休学，且不得修读大学课程或从事教学。


**Replace with:** 中国大陆属于当届资格名单中的地区。国籍或永久居留只是条件之一，还需核对年龄、目的地及学习和工作安排。奖助期间的课程与教学限制，见官方指南。

**Reason:** Remove “这一关你过” and unsupported universal five-year rule; applicant eligibility cannot be inferred from nationality alone.


## items.2.deadline_zh — Retain wording; recheck dated facts

**Current:** 2027 年度：2026 年 10 月 1 日 至 11 月 10 日 09:59（美东时间）


## items.2.why_apply_zh — Rewrite / verify conditions

**Current:** 这是这页上唯一一个你在国籍上直接过关的，金额也是最大的。


**Replace with:** 适合研究与文化交流计划，可以比较目的地、交流对象和所需时间。

**Reason:** Neither biggest nor only nationality fit is decision-worthy or established.


## items.2.tip_zh — Rewrite / verify conditions

**Current:** 它资助的是「去看」，不是「去做」。ACC 明确说明不资助创作与办展，只支持开放式的考察研究。以「做出一批作品」为目标写的申请，正是他们会拒绝的那种。


**Replace with:** 申请内容应围绕研究与文化交流展开，并说明希望了解的问题、交流对象和计划活动。作品制作经费或办展经费需另找适用项目。

**Reason:** Replace 去看/去做 slogan and prediction of rejection with accurate program purpose.


## items.3.country_zh — Retain wording; recheck dated facts

**Current:** 中国


## items.3.amount_zh — Rewrite / verify conditions

**Current:** 最高 10 万元人民币


**Replace with:** 支持金额与类别，以当届项目指南为准。

**Reason:** Verify exact category, not overall foundation.


## items.3.eligibility_zh — Rewrite / verify conditions

**Current:** 面向中国公民，以户籍为准。需要单位推荐函，或三位副高级以上的内地专家推荐。水彩（粉）画是列明的类别。


**Replace with:** 需按具体资助类别核对国籍、户籍、推荐材料及作品要求。

**Reason:** Current text collapses category-specific rules; hold for verification.


## items.3.deadline_zh — Retain wording; recheck dated facts

**Current:** 2027 年度已于 2026 年 6 月 15 日截止


## items.3.why_apply_zh — Rewrite / verify conditions

**Current:** 这是这页上唯一一条核实过、确实存在的中国国籍途径。


**Replace with:** 可作为国内创作资助的研究对象，先比较作品要求与自己的项目是否相符。

**Reason:** No only-China-route overclaim.


## items.3.tip_zh — Rewrite / verify conditions

**Current:** 门槛不低：成品尺寸至少 1.5 米 × 1.5 米；走美术创作这条线的话，作品要交给国内国有美术馆收藏。这和你现在的画法是两回事。


**Replace with:** 作品尺寸、材料、成果提交及收藏安排，会影响项目准备量，需先按对应类别核对。

**Reason:** “这和你现在的画法是两回事” judges practice; dimensions need exact applicable guide.


## items.4.category_note_zh — Out of current UI

**Current:** 已核实：这两扇门对你是关的


## items.4.note_zh — Out of current UI

**Current:** 有两扇门看上去开着，其实并没有开。文化厅的「新进艺术家海外研修制度」要求日本国籍或永久居留资格，表格里还要求附证明文件。国际交流基金会唯一面向个人的艺术类项目，要求日本或东盟国家的国籍或永久居留权。两项均于 2026 年 9 月 8 日核实。写在这里，是免得你白花一个月才发现。
