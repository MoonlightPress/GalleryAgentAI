# 2026-06-25 — Saffron + Whole-Site Review: consolidated punch-list

**Keeper:** Crema (Ops). **Scope:** the WHOLE site (Mochi 发现 / Saffron 观察 / Peppercorn 对话), Saffron-weighted — Scott's call, after the first pass reviewed only Mochi. Six reviewers: Pip (emotional), Sterling (money, reconciled vs her real BASE shop), Flint (tech), Crema (whole-site integration), Domino (UX/visual), Lore (copy/zh+ja).

> Private dashboard for GEGYjiji — audience of one. Facts: ~26k Instagram (NOT 90k), ~90k Twitter (real). Bar: "stand up to the girl I love."
> **Method caveat:** live render was blocked (playwright wedged; api.py out of bounds), so all six reasoned from source + data + the two translation stores. **A final headless-Chrome bilingual walk (zh AND ja, every tab) is the right last check before handoff** — every reviewer flagged this.

## Top-line verdict

The site **holds together as one coherent product and largely stands up** — the worrying things are real but bounded, and the through-line is consistent: *the bones, values, and reasoning are sound; the failures are all "the page doesn't yet reflect the truth"* (wrong product mix, under-priced sales, a stray name, equal weight for unequal things). Cross-tab facts that scared us (26k, SUZURI/BASE) are genuinely reconciled. Chinese (her default) is clean. **Not yet ship-ready** because of the money-accuracy and data-integrity items in Tier 0.

---

## TIER 0 — Fix before she sees it (truth / trust / harm)

**T0.1 — Money: kill the phantom-print "money left on the table" deficit. [Sterling]**
The Saffron money tab runs a "print editions ¥3–12k / quarterly releases" revenue stream and books its *absence* as lost income — the bulk of the "¥60–180k/month you're leaving on the table" headline. Ground truth from her BASE shop: **she has no print line and never has** (she sells originals + ¥1,980 zines + ¥1,100–1,980 postcard sets). It invents a baseline she never had, then charges her for missing it. Fix: reframe prints as an *optional* new tier (justified honestly — her sold-out originals prove demand), recompute the headline without the phantom line, retarget the consignment advice to zines/originals she actually stocks. Files: `data/saffron_insights.js` (REVENUE_STREAMS + summary assessment).

**T0.2 — Money: correct the pricing center *upward*. [Sterling, vs real catalog]**
Her real originals: **¥31,900–¥115,500, with three ¥115,500 pieces SOLD OUT** (revealed demand at the top). Dashboard says floor ¥37k, "sweet spot ¥50–80k" — which would tell her to price her flagship work ~¥35k *under* what buyers already paid. Fix: floor → ¥30k, sweet spot → ¥70–90k, cite the sold-out ¥115,500 sales as evidence, and loosen the over-cautious "¥960k/yr is a stretch" hedge (at her demonstrated prices ¥840k–1.39M/yr; ¥960k is the midpoint). Keep a light hedge on *consistency* only. File: `data/saffron_insights.js` (PRICING_INTELLIGENCE).

**T0.3 — Money: reconcile the SUZURI contradiction. [Sterling]**
Cached Discover SUZURI panel still shows the retired *"With 90k Twitter followers… ¥30–80k/month"* (`deploy_data/compact_opportunities.json:12749`) — contradicts the in-app ¥10–30k and re-anchors income to the wrong platform. Fix: regenerate that card's `three_bullets` to ¥10–30k and drop the 90k anchor, or suppress the SUZURI Discover card so only the corrected in-app section speaks. One SUZURI number site-wide.

**T0.4 — Money: fix the stale/fabricated Japanese SUZURI strings. [Sterling + Lore]**
`data/saffron_insights.js` ja siblings are leftovers that contradict EN/zh and invent claims: `why_now_ja:415` asserts *"0.1% of 26k → stable passive income"* (fabricated conversion math, cut it); `action_ja:417` is a pushy directive vs the EN "optional"; `description_ja:512` still names SUZURI as the gap (EN/zh say BASE); the ¥960k `why_now_ja:453` dropped its hedge; and the brand is mistyped **"SUSURI"** in several places (413/415/486…). Fix: retranslate the three ja fields to match corrected EN intent (optional hands-off merch), restore the hedge, SUSURI→SUZURI globally.

**T0.5 — Data integrity: remove the "Nin" cross-project bleed. [Crema] — PENDING SCOTT'S GO**
`Memory/artist_master_profile.json:454` `photography_note` reads *"Nin is also a photographer…"* — a name from the Arcadia project, in GEGYjiji's canonical profile. It feeds scoring (un-penalizes photography calls for the wrong reason) and could surface in generated copy. The profile is the root every tab derives from. Fix: remove/restate without the name; re-verify the photography-scoring rationale. *(Held pending Scott's instruction — sensitive.)*

**T0.6 — Cross-tab: unify the group-show count. [Crema] (latent, but a trust-killer)**
Saffron computes `1 + profile-confirmed + logged`, **deduped + excluding a re-logged "Tide from China"** (`api.py:1652-1664`); Peppercorn computes `1 + all logged group shows`, **no dedup/exclusion** (`PeppercornPage.jsx:741-742`). Both read 1 today, so it's invisible — but the moment she logs a show, the two tabs show **different versions of her own record**, and Saffron's whole "where you stand" narrative keys off its number. Fix: one shared count (an `/api` field both tabs read).

---

## TIER 1 — Emotional safety (Saffron) [Pip]

Saffron is genuinely *kinder* than expected — the real guard holds (CareerBenchmarks hides her weakest dimension; the shaming peer-timeline was deleted). Remaining wounds:

**T1.1 — Drop the numeric "第 2 级 / Level 2" badge + ~17% progress bar from the visible readiness card.** A videogame ranking her at her own life; the number wins the glance even though the copy around it is warm. Keep the *named* phase ("人脉与根基"), the strengths line, and one next door; move the numeric ladder into the already-collapsed detail. Files: `SaffronPage.jsx` (CareerReadiness ~1959), `engines/career_strategy_engine.py` (`_career_level`).

**T1.2 — Fix the milestone rings.** IG 26k renders as "52% to 50k" — taking her genuine strength and showing it half-empty, contradicting the app's own "继续增长是加分项，而非必需." Remove the rings or convert to a "you're here" marker, never a sub-50% fill for a dimension the app calls a strength. (`CareerPosition`/`MilestoneRing`).

**T1.3 — Retire red from the dream-paths.** LongTermScenarios stamps her three possible lives with `高/中/低` in green/amber/**red**. Relabel as fit/alignment ("最契合/契合/可选"); no dream gets a red tag.

**T1.4 — Reframe money "缺口/gap" badges → "机会/opportunity."** On a sensitive user the revenue "缺口" badges + "leaving 20–40% on the table" read as quantified failure. (Folds into T0.1's recompute.)

---

## TIER 2 — Language (her default zh is otherwise clean) [Lore]

**T2.1 — Translate the recurrence/rolling deadline phrases on Saffron's calendar.** `SaffronPage.jsx:718` renders `o.deadline` raw, so "Rolling" / "Twice-yearly (spring/autumn)" show English on the most-scanned ops surface — the last real zh leak. Add a ~15-entry phrase map (Rolling→常年开放, etc.), mirroring Mochi's `utils/localize.js` sentinel handling. *(The ja string bugs are in T0.4.)*

---

## TIER 3 — UX / visual [Domino]

**T3.1 — Install visible importance hierarchy (the #1 site-wide craft fix — answers "all the cards look the same").** Everything below Today's Focus renders at equal weight; a strong, deadline-imminent, perfect-fit pick looks pixel-identical to watch-list filler. You ALREADY built the answer in `TodaysFocus` (role cards: 3px colored top-accent + warm bg + heavier title). Copy that pattern onto `OppCard` (strong/urgent variants) and onto the *primary* section header on each surface. Almost pure CSS; the ranking data exists. Files: `OppCard.{jsx,css}`, `OpportunitiesSection.{jsx,css}`, model = `TodaysFocus.{jsx,css}`.

**T3.2 — Saffron + Peppercorn heroes don't shrink on mobile.** Mochi collapses to 190px; the other two stay 56vh (~470px of image before content on a phone). Add the same mobile media query to `.saffron-hero-img` and `.pp-mouse-img`.

**T3.3 — Delete dead code.** `SectionCards.jsx` (orphaned, has fake-clickable links that `preventDefault`), the orphaned `CAREER_TIMELINE` constant in `saffron_insights.js` (also holds the only surviving 3rd-person "GEGYjiji" voice + the banned unfavorable peer comparison), and the ~180 lines of dead `StatusBar.css`.

---

## TIER 4 — Tech robustness [Flint + Crema]

**T4.1 — Per-section error boundary on Saffron.** Currently one `SectionErrorBoundary` wraps the whole tab (`SaffronPage.jsx:2266`), so one throwing section blanks the entire tab. Wrap each section (class already reusable). Best robustness-per-line on the site.

**T4.2 — Statement round-trip + derived-field pollution.** Peppercorn stores the artist statement as three copies of the same string and propagates only `synthesized_en`, so zh/ja can drift from her edits (Crema C2); and a derived `live_counts` field gets written back into `peppercorn_profile.json` on every save via blind full-document overwrite (Flint). Fix: one canonical statement field translated on save; strip derived keys before/at POST.

**T4.3 — Nav mental-model seam.** Tabs are verbs (发现/观察/对话) but companions introduce themselves by name (Mochi/Saffron/Peppercorn). Add the name beside the verb (e.g. "观察 · 红雀"). [Crema C4]

---

## Handoff caveats (not bugs)
- The Peppercorn→master data loop is **wired but not yet exercised on prod** (Crema C5 / CURRENT_STATE).
- Do the **headless-Chrome bilingual walk (zh + ja, all tabs)** before sending it to her — source-reading verified *which* strings reach her, not the live pixels.

## ADDED 2026-06-25 (Scott) — Card copy: stop asserting taste/aesthetic fit it can't substantiate

Scott's real meaning behind "all the cards look the same" was **the text, not the visuals**: every card just *describes* a venue, so the board reads as a directory. And worse — where the copy DOES say more, it **fabricates aesthetic-fit certainty**. Concrete example: the Mograg card claims *"highest aesthetic match in the database"*, but the actual gallery is ugly/outsider contemporary art — the engine never saw the work; it inferred "fit" from tags and dressed the guess as a verdict. Same disease as the money page (estimate wearing the costume of a fact). And the fit-model wrongly assumes she only likes pretty/quiet work — Scott: "I don't know her taste… she likes ugly stuff like bread thief (パンどろぼう)."

**The standard (agreed in principle, applies to the card-copy pass AND the generator):**
1. **Never assert aesthetic/taste fit the system can't source.** No "highest match", "perfect fit", "your aesthetic" verdicts derived from tags. Hedge ("contemporary/outsider-leaning — worth a look if you want to judge it") or drop.
2. **Lead with verifiable, actionable facts** — takes un-repped artists, fee/free, medium shown, deadline, audience type. Demote description to a supporting clause.
3. **End on a concrete next move**, never "visit their site to get a feel."
4. **Hand her the taste judgment** — present options to assess, don't pre-decide what she'll like.
5. **Generator rule:** the copy engine must be told it may not output aesthetic/taste claims without a source; default to facts + action.

**Status:** DONE (2026-06-25), committed `2902cfca` + `c8271854`. 26 first-seen cards fully rewritten to facts + one concrete action (EN/zh/ja); 125 more swept clean of unearned aesthetic/taste verdicts + filler actions; 0 residual taste verdicts in any language. Generator (`why_it_fits_engine.py`) hardened so a regen can't reintroduce the fabrication. REMAINING: the long-tail `why_it_fits` paragraphs beyond the 26 are de-fabricated but still description-led — a full regeneration is the real fix for long-tail quality, and needs Scott's explicit go before any paid run.

## ROUND 2 — LIVE PASS (2026-06-25, post-deploy) — full team on full alert, IN PROGRESS

After deploy, a live cross-checked pass (Scott's directive: "cross-check the whole site WITH CONTEXT, don't grade pieces in isolation"). Findings to fix in a COORDINATED pass (the level model needs ONE coherent solution, not piecemeal):

1. **Career LEVEL model is self-contradictory (4 ways) — #1.** Live `/api/career_strategy` returns **"Level 4 (Prestige)"**; phase says **"Tier 3 established"**; profile readiness bars show **"almost to Tier 3" + "Tier 4 half full"**; unlock tree shows **"Tier 2."** Four representations, none agree, and "Level 4" overshoots ("Tier 3 established → representation" is the truth). Likely fix: collapse all four into ONE coherent statement; kill the numeric tier game (also the creepy/shaming part).
2. **Profile (Saffron) tab needs a full design overhaul** (Scott: "the whole profile page sucks"). Domino owns the redesign proposal.
3. **No links** on act-now / build-toward / watch-list items — looks actionable, isn't. (Domino called out to catch this class; Flint to root-cause.)
4. **Saffron sounds surveillant** — surfaces her AGE ("age 30 / ~4 years away / deep-work year around 30"). Principle: companions may use what she tells them, never parade inferred personal facts. Remove age/countdown framing → neutral horizons. (Pip leads, Lore on the strings.)
5. **LongTermScenarios still on the OLD model** — "need more group shows / first solo within reach / by 30" residue contradicting her real solo+museum+international record. (Lore.)
6. **Instagram count is HARD-CODED (~26k) and already stale** (she's +1000 since build). Stop presenting a brittle precise number; single-source or soften to "established & growing." (Flint.)
7. **Posting cadence is unrealistic** — daily/post-often. She's in school. Use ~1 painting + 1 process video / month. (Lore.)
8. **No licensing advice** — Scott wants real, concrete licensing guidance (calendars, stationery, postcards, lifestyle/JP-stationery brands); her work suits it. (Sterling proposes.)
9. zh + ja leaks, voice, and any other cross-surface contradiction (whole team).

10. **⚠️ SYSTEMIC: two-source-of-truth split — today's data-file fixes may NOT be live.** The live bundle renders `frontend/src/i18n/translations.js` + hard-coded strings in `SaffronPage.jsx`, NOT just `saffron_insights.js`. Sterling confirmed the money de-pressuring did NOT fully hold live: `saffron_insights.js` is clean, but `translations.js` still shows "Opportunity Gap Analysis / 机会缺口分析", "should be earning… leaving on the table / 错过的部分 / 見逃している部分" (`sf.revenue.summary`, `sf.sec.oppGap`/`sf.sub.oppGap`), hard-coded 26k (`pp.ig.count`/`pp.ig.analysis` + ~7 literals in SaffronPage.jsx), and "next milestone 50k / curators not watching." **Action: re-verify EVERY today-fix against translations.js + SaffronPage.jsx hard-coded strings, not the data file.** (Pip's emotional fixes, Lore's voice fixes, etc. may have the same split.)
11. **Licensing exists in source but isn't live** — rich `LICENSING_LANDSCAPE` in saffron_insights.js (Hobonichi/Midori/Mark's/Stalogy, ¥30k–500k bands, inbound-DM mechanics) but the live `sf.licensing.summary` is the old one-liner. Ship it + surface concrete guidance (calendars, postcards, washi/stickers, notebook/planner covers; first deal = be findable + a one-PDF lookbook when asked).
12. **Add more "open questions" behind a "more" button** (Scott) — progressive disclosure; only questions that change the advice. (Domino, profile redesign.)
13. **Grants/age:** Sterling confirmed grants are eligibility-by-nationality/residency, NOT age — no age-eligibility copy, so no overlap with the age-creepiness concern. Clean.

**PRESERVE (Scott-approved):** the MONEY section tone — *"this is something you can do if you feel like it, but you're already doing great."* It's the GOLD-STANDARD register; bring the profile/career copy UP to it and do NOT regress it in any fix.
**VIEWPORTS:** verify at BOTH phone (~390px) AND tablet/laptop (~1024–1440px).

**Plan:** team reports → ONE coordinated fix (esp. a single coherent level/career-position model + profile redesign, matching the money-section tone) → redeploy → live re-verify in zh AND ja, both viewports.

## What's genuinely good (don't undo)
26k consistent everywhere; 90k Twitter kept off consumer surfaces; SUZURI/BASE reconciled; the data loop closes in code; pricing *logic* validated against her real catalog; Today's Focus hierarchy; the Peppercorn/Saffron questions are the best writing on the site (warm, second-person, explain *why*); kindness guards (favorable-only benchmarks, deleted peer-timeline, doors-not-deficits gap copy) hold in zh.

---
*Status: all six reviews folded in. Nothing edited yet — this is the punch-list. T0.5 (Nin) awaits Scott's go. Recommended fix order: Tier 0 → Tier 1 → Tier 2, then 3/4 as time allows.*
