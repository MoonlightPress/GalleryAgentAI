# Saffron: a more useful, more personal observatory

Review date: 10 September 2026. Scope: the current deployed Saffron and its producing code. This is a proposal and Chinese editorial audit; no application changes or deployment have been made.

## The change I would aim for

Saffron should make three things apparent very quickly: **it remembers the work she has actually made; it has done some difficult research; and it gives her room to choose what matters.**

There is already substantial work here. The five career directions, book-production comparison, recurring calls, exhibition record and prepared Japanese introduction are much more useful than a sparse statistics page. Keep that substance. The biggest improvement is to bring the strongest, most personal finding forward, make the economics trustworthy, and give the Chinese the clarity of an attentive editor.

The emotional effect should come from the quality of that attention. Naming the recent LE MONDE exhibition and showing how its materials could support a publishing proposal says more than telling her she has great potential. Her nationality and location matter when they affect languages, distribution, eligibility or practical arrangements; they should not stand in for her artistic preferences, finances, relationships or ambitions.

Brief visits are a useful design constraint. They do not establish why she visits or how she feels. Build something that offers value during a brief visit and remains useful if she never messages you about it.

## What I reviewed

The current application renders `SaffronV2` for both `#observe` and `#observe2`, despite older documentation describing it as a sandbox. The actual structure is:

| Tab | Mounted content |
|---|---|
| 策略 | Five directions, book economics, publisher comparison, strategy ladders |
| 日历 | Annual view, selected month, recurring calls, grant landscape |
| 概况 | Career record, comparable artists, venue tracker, press |

I inspected the live Chinese and English views, the narrow-screen layout, the source copy and the underlying calculations. The language appendices inventory 436 structured Chinese copy units across four Python sources, strategy ladders and grant data. Eleven of those are outside the current UI and explicitly marked. The remaining interface, exhibition, peer, press and 52 venue rows are reviewed separately.

This is a full editorial pass over current Saffron's authored content and visible supporting sections. It is not independent verification of every one of the 1,185 records in its served opportunity catalogue. Where a recommendation depends on further research, the audit says so. Unmounted legacy collaboration/licensing/collector sections are not presented as defects on the current page.

## 1. Fix the facts and behavior that can undo the whole experience

These are release blockers for the claims they affect. Better typography cannot compensate for a convincing but incorrect answer.

### Book economics: define the question before calculating

The page currently describes recovery of the prepaid print bill. Its calculation divides the entire print bill by a per-copy margin that subtracts printing again. That counts the same printing cost twice for this cash-recovery question.

Using the existing model inputs, with selling costs deliberately excluded for diagnosis:

| Scenario | Existing displayed calculation | Simplified prepaid-cash recovery |
|---|---:|---:|
| 300 copies × ¥1,315; retail ¥4,950 | 109 copies | 80 copies |
| 100 digital copies × ¥3,204; retail ¥4,950 | 184 copies; marked impossible | 65 copies |
| Same digital run; retail ¥11,000 | 41 copies | 30 copies |

**These corrected simplified counts are not recommended sales targets.** They expose the formula error. Real cash recovery must include the actual prepaid costs and the actual cash retained from each sale:

`copies required = ceil(total prepaid costs / (cash received per copy − per-sale costs not already prepaid))`

For example, payment fees, packaging, subsidized shipping and channel deductions change that denominator. Taxes need consistent treatment. Design, proofs, freight and other setup costs need explicit inclusion or exclusion. If the question is accounting profit instead, define inventory and cost recognition separately. Use upward rounding for a whole-copy threshold. Do not call all remaining copies “pure profit.”

Also remove the fixed claim that consignment only works below approximately ¥1,500 per unit. The limit depends on price, the shop's terms and included expenses. A 70/30 split is a scenario, not every venue's contract. The chart should help compare capital tied up, margin and unsold stock; it should never imply that demand has been established.

The currently compared specifications are not equivalent: the Japanese digital option is limited to a smaller format/page count than the full-size hardcover comparison. Put size, pages, binding, paper, proofing and delivery assumptions beside the price. Language ability may help communication; it does not establish a discount from a Chinese printer.

Owner: [book_economics_engine.py](C:/ScottStuff/GalleryAgentAI/engines/book_economics_engine.py:116), plus dependent claims in `futures_engine.py` and `strategy_ladders.js`.

### Chinese calendar: translation currently changes the data

In the same live session, September showed **0 dated entries in Chinese and 53 in English**. The translator recursively changes string values, including month names; the calendar then tries to match them against an English month list.

Keep month numbers, dates, record IDs and status enums independent of display language. Translate labels at rendering time. The same problem affects CRM status display: translated values no longer match the expected status IDs, leaving words such as **冷淡** visible. A venue without a contact record should read **尚无联系记录**, not receive an interpersonal judgment.

The calendar also needs date-type and identity verification. I encountered a CORE result mixed with an unrelated NSF CoRe date, and an “Artist Support Programme” record whose link was “Link in bio” text and whose dates described interviews. Such records should not become application deadlines. Estimated recurring windows, confirmed application deadlines, exhibition dates, interviews and delivery dates need distinct fields and treatments.

Rolling grants must be included in the open-state logic: **今天没有开着的** contradicts a visible **常年开着** entry. Large catalogue counts should move into optional data notes; they do not show how many suitable, verified opportunities she has.

Owners: [SaffronPage.jsx](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronPage.jsx:45), [SaffronV2.jsx](C:/ScottStuff/GalleryAgentAI/frontend/src/components/SaffronV2.jsx:279), calendar normalization and verification engines.

### Rates: restore the missing scope

The JIA **¥800,000** calendar example refers to an **A3 calendar with 12 illustrations**. It is not a reference fee for licensing one existing image. The published page is dated January 2020 and describes negotiated, experience-based reference figures. Present it as historical commissioning context, with its scope; obtain actual usage-specific evidence for archive licensing. [JIA remuneration reference](https://jpn-illust.com/guarantee.html)

Separate original asking prices, actual completed sales, gross project fees, royalties, licensing fees and cash retained. A listed ¥31,900–115,500 original does not establish her net income per painting. A sold-out label does not establish transaction details. A fee for twelve images cannot be compared with one original without explaining the work and rights involved.

The print-on-demand table also needs reconciliation: ¥1,465 divided by ¥3,000 is about 48.8%, not the displayed 44%; ¥2,268 divided by ¥5,000 is about 45.4%, not 43%. If a different denominator or additional expense explains those percentages, show it. Otherwise recalculate from shared numeric fields.

### Eligibility: attach rules to a particular cycle

The current TOKAS text uses a 1990 birth cutoff. The official 2027 call uses **1 April 1991 and later**, and that application cycle closed in July 2026. It can be a preparation reference, not a currently open recommendation. [TOKAS-Emerging 2027 call](https://www.tokyoartsandspace.jp/archive/application/2026/20260616-331.html)

FACE 2027's U30 cutoff includes **1 April 1997**. “After” is not equivalent to “on or after.” Its fee, dates and work requirements also belong to that cycle. [FACE 2027 official call](https://www.sompo-museum.org/news/2026/face2027/)

ACC's current guidance concerns research and cultural exchange, with program-specific eligibility and activity restrictions. Remove the unsupported blanket five-year requirement unless a current applicable source establishes it. Chinese nationality alone does not confirm full eligibility. [ACC grant guidelines](https://www.asianculturalcouncil.org/grant-opportunities)

Do not turn these observations into generalized immigration or contract advice. A useful entry says which documented conditions apply and which applicant-specific facts remain unknown.

## 2. Make the first screen prove that the page is for her

The current opening spends attention explaining routes in general before showing its best evidence. At the inspected 390 × 844 viewport, the hero occupied about 192 px, companion navigation extended to y≈291, and the opening text began around y≈466. The first route header began around y≈783; the “first steps” section began around y≈1,560. There was no observed horizontal overflow, but useful specificity arrived late.

I would keep the illustration, companion navigation and familiar tabs, then replace the long introductory argument with one short personal observation and one prepared finding.

**Opening draft, using the current exhibition record:**

> **现有作品，还可以怎样被看见**
>
> 原宿 Galerie LE MONDE 的个展刚在 9 月结束。从持续的水彩日记，到出版物和展览，你已经积累了不同形式的作品资料。
>
> 这里把出版、画廊合作和图像授权放在一起，比较各自能用上哪些现有材料，以及需要补充什么。

English sense: the recent exhibition, sustained diary and publications give her material that can serve several purposes; Saffron compares how those materials could be used. The dates must come from current records and change when the “recent” wording expires. This is recognition, not a claim that the gallery represents her or that its clients are hers.

Immediately below, show **one substantive finding with its evidence**, not three generic compliments. The best candidate is the book comparison, once corrected and brought to a common specification:

> **下一本画集：先比较规格、预付支出和销售方式**
>
> 自费印制与出版社合作，承担的工作和库存不同。下面把费用、发行安排和目前能确认的条件放在同一张对照里。

Only use that introduction when the promised comparison is actually complete. A future finished finding could be more specific: which measured specification reduces cash exposure, what is sacrificed, and which sales assumption would change the conclusion. Avoid presenting the existing ¥109-copy story with softer language.

Give her an immediate route into **画集与成本 / 图像授权 / 展览资料** as in-page content links, while preserving the animal navigation. No modal, onboarding form or required goal selection should interrupt the first visit.

## 3. Design for three amounts of attention

| Time available | What she should be able to get |
|---|---|
| About 5 seconds | A recognizable reference to her work and one useful finding headline |
| About 1 minute | The finding's implication, a few credible figures or examples, and the next useful document |
| About 10 minutes | Sources, assumptions, tradeoffs, comparable examples and prepared material she can reuse |

The longer view must contain real work. Progressive disclosure should organize that work, not conceal an empty answer.

Keep all five current directions, but make collapsed cards informative. Each should show its purpose and one decision-relevant distinction. For example, publishing can preview **谁承担制作与库存**; licensing can preview **已有作品的使用范围与报价依据**. Avoid five equally weighted promotional taglines implying five new obligations.

Inside each direction, use a consistent order: what this could offer; the most relevant evidence; time/cost/rights tradeoffs; a prepared next resource; sources and unresolved questions. Retain useful bespoke material such as the Japanese letter and book chart. Avoid adding repeated generic essays just to fill a template.

## 4. Do the research that saves her work

### A price study she can actually use

Prepare a compact comparison of genuinely comparable watercolors, reproductions and art books. The important distinction is product and career context, not a similar follower count. A useful record includes:

- Artist and seller; direct source and date checked.
- Medium, dimensions, paper, edition, signature, framing and year.
- Current asking price; separately identified evidence of a completed sale, if available.
- Shipping/tax treatment and known channel deductions.
- Why it is comparable, and the main limitation of the comparison.

Then state a modest conclusion: what price positions are represented, where her existing range sits, and which proposed product lacks good evidence. The gap between a ¥2,200 item and a ¥31,900 original is a hypothesis to investigate, not proof that she needs a middle-priced product. Do not suggest a new edition until production quality, audience interest and delivery work have been considered.

Keep private sales information optional. The page should deliver useful public research without requiring her to reveal finances or complete a questionnaire first.

### A book decision sheet

Use one explicit target specification and obtain comparable current quotes or identify the differences. Show small-run exposure, larger-run exposure, samples, freight, storage, direct sale and venue-specific consignment. Add publisher route, proposal requirements, evidenced distribution and relevant books from the publisher's own catalogue.

Include a draft sequence or sample spread using existing material only when available and authorized. An editable cost sheet and a prepared proposal outline would save more time than another essay about publishing. Label unsent drafts clearly. Do not claim a publisher necessarily pays every cost or guarantees national distribution.

### A licensing brief tied to the actual paintings

Choose a small set of relevant uses—such as a book jacket, stationery or a calendar—and explain why specific existing works could suit them. Check reproduction quality, crop requirements and existing rights before treating the archive as immediately licensable.

Research the client's actual visual work and public approach route. For each promising lead, supply a cited example, fit explanation, named submission/contact method where published, and a concise draft inquiry. Price evidence must match the number of images, use, duration, territory, exclusivity and revision work. Do not manufacture contacts or imply a mockup is an existing commercial relationship.

### A compact exhibition and publication packet

Use the existing record to prepare a reusable selection: recent exhibition details, a short accurate biography, relevant works, publications and a Japanese introduction. This is where the LE MONDE show becomes practically useful instead of merely being acknowledged.

For peers, explain one transferable practice per artist: a specific book format, exhibition presentation, distribution route or documented collaboration. Ten loosely comparable successful people can feel like a ranking. A few properly explained cases can answer a real question.

For venues and press, perform the next verification step before surfacing an action. All 52 venue rows have replacement wording in the audit, but replacing “send a DM” with “check submissions” is only an interim correction. The finished product should supply the verified route wherever public evidence permits. Consolidate duplicates and move lower-confidence entries out of the main view.

## 5. Replace the career ladder's verdicts with usable sequences

The current ladders contain real insight about reusable materials, but several dependencies and thresholds are editorial inventions. A certain number of press features is not a universal prerequisite for representation. A follower count does not establish sales readiness. Missing data does not establish that she has never done something.

Preserve the useful ordering while separating **已有资料**, **可以补充**, and **尚未确认**. Do not award a score for her career or make a voluntary path look like a course she is behind on.

For a book-oriented path, a sensible optional sequence is:

1. Select an existing body of work and draft a short sequence.
2. Compare two feasible specifications using evidence gathered by Saffron.
3. Review a sample or proof before committing to production.
4. Choose a publishing or self-publishing route based on cost exposure and distribution.

For licensing, first establish a suitable work selection and reproduction/rights information, then use a prepared client-specific inquiry. For a gallery relationship, first reuse accurate exhibition material and check the venue's public approach policy. These are practical dependencies, not universal career stages.

Saffron can show these sequences as optional context. When there is a verified, timely action, let her carry it into Mochi's existing action workflow. Do not create another five-item daily checklist on Saffron.

## 6. Refine the aesthetic around reading

Keep the warm paper, watercolor scene, bird, serif headings and quiet atmosphere. The established illustration is an asset. This does not need more decoration or a new palette.

The most valuable visual changes are:

- Reduce the combined hero/navigation/introduction height enough to reveal a concrete finding in the initial mobile view. Preserve recognizable art and usable navigation; validate on a real narrow viewport rather than relying on a desktop crop.
- Use roughly 16–17 px for substantive Chinese body copy and 14–15 px for meaningful secondary text. Current card explanations can drop to 12–12.5 px. Short technical footnotes may be smaller, but essential caveats and conclusions should not be.
- Use an upright Chinese body face with generous line height. Reserve serif emphasis for short headings; remove italic styling from paragraphs and avoid pale text for facts she must evaluate.
- Give the main finding a clearer hierarchy than the supporting cards. Distinguish sections through spacing, type and restrained paper treatment rather than five equally prominent boxes.
- On mobile, show each cost scenario as a labelled stack or card. Do not shrink a wide financial table until its assumptions become unreadable.
- Keep source links near the claim and provide a compact source date. Put methodology in a disclosure, while keeping uncertainty that changes the decision visible.
- Check keyboard focus, expanded-state semantics, reduced motion and the nighttime palette. The dark navigation can remain atmospheric, but labels and selected state still need clear contrast.

The test is whether the page feels like a thoughtfully prepared studio reference she can use. Extra ornament cannot create that feeling by itself.

## 7. Make the Chinese specific, natural and nonjudgmental

The main language problem is not grammar alone. English arguments were often carried into Chinese with their metaphors, certainty and implied assessment intact. Phrases about doors, ladders, ceilings and “running a business” can make a personal resource sound like a translated startup strategy memo.

Use direct Chinese, one idea at a time. Recognize concrete work. Describe tradeoffs without ranking her worth or assuming she wants every route. Keep **你** where it sounds natural; warmth does not require speaking about her in the third person.

| Current | Proposed direction |
|---|---|
| 你已经有一套跑起来的创作和生意 | 你从 2020 年开始持续画水彩日记，也已经有了出版物、个展和自己的店铺。 |
| 2,200 到 31,900 日元之间的空档 | 印刷品与原作之间，可以尝试什么价位 |
| 小批量不是靠多卖救回来的，是靠封底那个价格。 | Compare actual costs and selling assumptions; replace only after correcting the calculation. |
| 冷淡 | 尚无联系记录, when there is no contact record |
| 这一关你过 | State the applicable condition; do not announce complete eligibility. |

The appendices provide exact original wording, proposed replacements and reasons. Some revisions deliberately remove an unsupported assertion without supplying another. **Those are safe interim drafts, not an excuse to publish a page full of “needs checking.”** Complete the research and replace the uncertainty with a sourced answer where possible. Keep only unresolved questions that genuinely affect the choice.

Do not polish Chinese while leaving an inaccurate English claim intact. Both languages must express the same facts, scope and uncertainty. Preserve official Japanese names and titles; do not invent Chinese names for events or institutions.

## 8. Implementation order and ownership

| Priority | Deliverable | Primary owners |
|---|---|---|
| P0 | Correct book cash model and all dependent claims; reconcile rate scopes and percentages | `book_economics_engine.py`, `futures_engine.py`, `strategy_ladders.js` |
| P0 | Language-independent dates/statuses/IDs; calendar parity; quarantine invalid dates and links | `SaffronV2.jsx`, shared translation code, normalization/verification engines |
| P0 | Current-cycle eligibility; remove unsupported factual guarantees | `recurring_calendar_engine.py`, `saffron_insights.js`, source verification |
| P1 | First-screen personal observation and one completed research finding | `SaffronV2.jsx`, `futures_engine.py`, shared current artist record |
| P1 | Apply Chinese editorial decisions and synchronize English | All five copy owners in appendices; `translations.js`; named sections in `SaffronPage.jsx` |
| P1 | Mobile hierarchy, readable type, useful collapsed previews | Existing Saffron component styles |
| P2 | Finish the focused book, price and licensing research sheets; reusable materials | Existing research/content workflow, with dated primary evidence |
| P2 | Replace unsupported ladder thresholds; curate venue/peer/press details | `strategy_ladders.js`, verified records and mounted overview sections |

Use the canonical `frontend/`. Fix generating rules before regenerating derived JSON; do not hand-patch generated content. Author-maintained copy can be edited at its source. Use stable IDs for translations and links rather than English sentence or person-name equality. Preserve the distinction between a gallery's official URL and a search fallback.

The record should also reconcile across sections: exhibition count must not be labelled as group-show count; the newest show should not coexist with an older “latest” note; press counts should agree; two exhibitions with unknown types should remain unknown. Distinguish recorded, inferred and absent information.

Before release, verify these concrete outcomes:

1. Switching Chinese/English preserves the same calendar entries, selected month and CRM states. Locale is allowed to change presentation only.
2. Pure arithmetic checks cover direct/consignment scenarios, per-sale costs, zero or negative receipts, whole-copy rounding and recovery beyond the print run. Every displayed dependent number agrees.
3. A narrow-screen visit exposes a specific, evidenced finding promptly; all five directions remain accessible, with readable figures and keyboard-operable disclosures.
4. No unsupported guarantee survives merely in the other language, a ladder detail or an empty state. Mixed English peer descriptions and stale exact-match exhibition translations are resolved.
5. Every prominently recommended opportunity has a matching official identity, working route, correct date type and visible status. Estimated windows are not labelled open.

Run the repository's required frontend checks when changes are implemented, and inspect the resulting Chinese UI. This review itself did not change the app or run a paid pipeline.

## What would make the next visit feel different

The strongest next release would contain a corrected book comparison, an opening that recognizes the recent exhibition, a concise prepared asset she can actually use, and Chinese that sounds like it was written for her. That is a larger practical improvement than adding another section.

The measure of success is that she can leave having learned something useful or saved herself some work. A reply, a long session or a particular emotional response should not be built into that measure.
