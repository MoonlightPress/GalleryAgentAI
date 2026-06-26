# Sterling — money facet review (Revenue / Pricing / Grants / Licensing / Publication)

**Date:** 2026-06-26 · **Surface:** live money tab (收入 under 观察·山楂), walked in zh (Playwright) + source.
**Tone verdict (gold standard):** PRESERVED. No regression. Every revenue stream is `leaving_on_table: false`; no "缺口 / gap / leaving on the table / should be earning" anywhere in the live money tab; the `sf.sec.oppGap`/`sf.revenue.summary` strings in `translations.js` were re-de-pressured ("可以探索的方向 / Open Directions", "都不急，也都不是必须"). Pricing/revenue copy is calm and affirming. Licensing lead correctly moved out of the subheader (`SaffronPage.jsx:1376`) and reads right. Revenue links resolve to real platforms only (`REVENUE_PLATFORM_URL`, `SaffronPage.jsx:449` → SUZURI→suzuri.jp, Booth.pm→booth.pm) — no word-searches. SUZURI/BASE are consistent inside this tab (SUZURI framed as optional hands-off merch with no income figure; the retired "¥30–80k/mo + 90k Twitter" claim is gone from here).

---

## TIER 0 — money inaccuracy she'd see

**T0.1 — Pricing-section subtitle is stale: shows ¥37,000–135,000, which both overshoots her real catalog AND contradicts its own body cards.**
- **Surface:** 定价情报 (Pricing Intelligence) header subtitle, visible even while collapsed. Live capture rendered: `定价情报 ¥37,000–135,000 原作 · ¥3,000–12,000 版画`.
- **File:line:** `frontend/src/i18n/translations.js:370` (zh `sf.sum.pricing`), mirrored `:1281` (ja), `:2322` (en). Rendered as the section `summary` at `frontend/src/components/SaffronPage.jsx:1842`.
- **The contradiction:** the body range cards directly below render the corrected data — originals **¥30,000 – ¥115,000**, prints **¥3,000 – ¥15,000** (`frontend/src/data/saffron_insights.js:856` and `:861`). So the subtitle and the cards inches below disagree on the same screen.
- **Why it's wrong vs her real catalog:** her real originals are **¥31,900–¥115,500 (three ¥115,500 pieces SOLD OUT)**. The stale subtitle's **¥37,000 floor** sits *above* her cheapest real original (¥31,900) — it would tell her her entry pieces are underpriced when they aren't — and its **¥135,000 ceiling is a phantom** ~¥19,500 above the highest price any buyer has actually paid (¥115,500). The body cards (¥30k–115k) are accurate to her catalog; the subtitle is the only inaccurate number, and it's the most-glanced one.
- **Fix:** update `sf.sum.pricing` (all three langs) to match the body / her catalog — e.g. `¥30,000–115,000 原作 · ¥3,000–15,000 版画`. Better still, lead with her real product mix (originals + zines, ¥1,200–2,800) since she has **no print line**; a print range she doesn't sell shouldn't headline her money summary.
- **Why it matters:** this is exactly the T0.2 fix from the 2026-06-25 review — the data file was corrected, but the `translations.js` subtitle was never updated, so the wrong number is live. Two different prices for the same work on one screen reads as the dashboard not knowing her catalog — the precise "estimate wearing the costume of a fact" failure the money pass was built to kill.

---

## TIER 1 — visible defect on a money section

**T1.1 — Licensing "entries" that are explanations, not brands, render as clickable Google-search links.**
- **Surface:** 授权版图 (Licensing), third group "为什么你的受众让你具备授权潜力". Rows like `收入区间（实际） ↗`, `如何被主动联系 vs. 如何主动提案 ↗`, `实际时间线 ↗`, and the category-2 rows `书籍封面插画（集英社…） ↗`, `生活方式品牌（化妆品、茶饮…） ↗` are explainer headings, but each is wrapped as an external link.
- **File:line:** `frontend/src/components/SaffronPage.jsx:1385-1390` — `href={entry.website || entry.url || sfSearch(entry.name)}`. The `LICENSING_LANDSCAPE` data (`saffron_insights.js:4-116`) has **no `website`/`url` on any entry**, and `sfSearch` (`SaffronPage.jsx:425`) returns `google.com/search?q=…`. So every licensing row links to a web search of its own label — including non-brand headings.
- **Fix:** only render the `↗` link for entries that are real outlets with a URL; render the explainer rows (audience threshold, revenue ranges, how-to, timeline, and the two category descriptions) as plain text.
- **Why:** clicking "收入区间（实际）" and being thrown to a Google results page reads as broken/unfinished on a section that is otherwise her best, most concrete money guidance.

---

## TIER 2 — accuracy / usefulness

**T2.1 — Real licensing brands link to name-searches instead of their own sites.**
- **Surface/file:** same mechanism as T1.1. `Hobonichi`, `Midori (Designphil)`, `Stalogy`, `Mark's Inc.` all fall through to `sfSearch(entry.name)`.
- **Fix:** add real `website` fields to those entries — hobonichi.co.jp (ほぼ日), designphil.co.jp (Midori), marks-tokyo-edge / marks.jp (Mark's), stalogy.com. These are exactly the brands she'd want to reach; a one-hop link to the real site (where licensing/contact lives) is the difference between "real guidance" and "a search box."
- **Why:** the licensing copy itself is strong and specific (correct fee bands — Hobonichi ¥50k–500k/use, Midori ¥30k–200k, royalties 3–8%; DM-inbound mechanics). The links undersell content that's already accurate.

**T2.2 — The Tokyo grant entry conflates a commercial award with government grants and links to a search.**
- **Surface:** 资助资源 (Grant Landscape), entry "Tokyo Metropolitan Government Arts Grants (TACT)".
- **File:line:** `saffron_insights.js:338-361`. "(TACT)" is not a recognized acronym for Tokyo public arts funding; `deadline` points at `tokyo-midtown-award.jp` (Tokyo Midtown Award is a **commercial** Mitsui design competition, not a metropolitan-government grant) alongside `tokyoartsandspace.jp`. The `apply` field carries no domain, so `grantHref` (`SaffronPage.jsx:432`) falls to a Google search of the (wrong) name.
- **Fix:** rename to the real funders — **Arts Council Tokyo** (artscouncil-tokyo.jp/en/grants — note the live Discover board already links the genuine "FY2026 Life with Art Grant" there) and/or **TOKAS** (tokyoartsandspace.jp) — drop the Tokyo Midtown Award reference and the TACT acronym, and put a real domain in `apply` so the link resolves. Amount band (¥100k–1M) is fine.
- **Why:** it's the one grant entry that names the wrong institution; the other four (ACC ~$3,000/mo, Japan Foundation ¥500k–3M, Bunka-cho overseas study, China Arts Foundation) resolve to real domains and are honestly hedged ("Typically…", "check …").

**T2.3 — Verify "China Arts Foundation International" is a real, reachable program.**
- **File:line:** `saffron_insights.js:363-386`. Heavily hedged ("amount varies", "availability varies by political climate", apply "via Chinese embassy cultural attaché") and has no domain. It's the most speculative entry in an otherwise concrete list; if it can't be tied to a real grant body, it's filler dressed as an opportunity.
- **Fix:** confirm the entity, or replace with a verifiable overseas-Chinese-artist program (e.g. China National Arts Fund 国家艺术基金 routes) or drop it. Keep the honest-uncertainty tone.

---

## TIER 3 — nits

**T3.1 — Prints subtitle ¥3,000–12,000 vs body ¥3,000–15,000.** Same stale-subtitle source as T0.1 (`translations.js:370` vs `saffron_insights.js:861`); fold into the T0.1 fix. Minor on its own because she has no print line.

**T3.2 — Publication Landscape is accurate but thin.** Renders her two real works (Colour Diary 2021 + contributor to *defined Definition 02*) and text-only tiers/targets (no bad links) — consistent with the press kit, no money inaccuracy. Usefulness could rise by ordering `top_targets` to her actual nearest path (self-published zine → art-book consignment → publisher), but this is engine-fed (`data.publication_landscape`), so it's a generator nit, not a copy bug.
