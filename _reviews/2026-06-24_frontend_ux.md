# Frontend / UX Review — 2026-06-24

**Facet:** Frontend / UX quality and the artist's lived experience (GEGYjiji — 26, watercolor painter, Tokyo, Chinese/Japanese, highly driven but easily emotionally overwhelmed).
**Scope:** canonical `frontend/` (port 5177; ran on 5178 because 5177 was occupied). NOT `frontend2/`, NOT Streamlit `app.py`.
**Mode:** READ-ONLY. Ran tests, lint, production build, the FastAPI backend (`api.py` on :8001), the Vite dev server, and rendered the live app in Playwright at desktop (1280px) and mobile (390px). No code edited, no paid pipeline run.

---

## Summary

The three companion pages all render correctly. The recent rules-of-hooks refactors are clean — no hook-order bugs remain, no render breakage, no console errors on any page, and Saffron is additionally protected by a per-tab `SectionErrorBoundary`. Tests (15), lint (0 errors, 1 trivial warning), and the production build all pass.

The two headline launch risks are **not** code defects but **experience defects**, and they cut directly against this specific artist:

1. **The Mochi browse page is an endurance scroll** — measured **8,969px desktop / 22,618px mobile**, 11 stacked card sections, 52 cards on first paint before any "show more". The product's stated promise ("exactly three actions today") is delivered (Today's Focus is 3 cards) and then immediately buried under ~49 more cards plus a duplicated strongest-picks band. For an easily-overwhelmed user this is the single biggest UX liability.

2. **An entire Saffron tab renders English-only for a Chinese-first user.** The default language is zh (correct for GEGYjiji), but the Pricing Intelligence section and parts of the Revenue/Timeline sections show Chinese headers over English bodies — a jarring mixed-language wall on the "收入" (money) tab.

Two documented concerns are **stale/resolved**: the "390px StatusBar overflow → 659px" no longer exists (StatusBar is now a 5px accent), and there is no body-level horizontal overflow at 390px.

Net: nothing here is a hard *technical* blocker, but the endurance-scroll directly contradicts the product's core emotional promise and should be addressed before this goes to the real user it was built for.

---

## What I verified (with evidence)

**Tooling (all green):**
- `npm test` → **15 / 15 pass** (freshness, feedbackBehavior, recommendationQuality, relationshipTargets).
- `npm run build` → **succeeds**, 52 modules, code-split chunks (`index` 390kB, `SaffronPage` 148kB lazy, `PeppercornPage` 47kB lazy). Note: hero PNGs are huge — `mochi_hero` 1.98MB, three others ~2.8–2.9MB each (~10.6MB of un-optimized PNG shipped). Build warning that `/mochi_hero.png` resolves at runtime (it does — used as a CSS `background-image` for the old StatusBar thumb that no longer renders; harmless but dead).
- `npm run lint` → **0 errors, 1 warning**: unused `eslint-disable` directive at `frontend/src/components/PeppercornPage.jsx:1302`.

**Live render (Playwright, backend serving 416 real opportunities):**
- Backend healthy: `/api/today`, `/api/opportunities`, `/api/saffron`, `/api/career_strategy` all return valid JSON. `/api/opportunities` sections: immediate_best_moves 6, open_calls 12, publication_editorial 2, competitions_awards 37, zines_and_print 29, relationship_targets 20, **watch_list 310** (total 416).
- **Peppercorn (default page, zh):** renders cleanly, no errors, full-bleed hero, collapsible sections, dismissible intro. Screenshot: `.playwright-mcp/pep_desktop_zh.jpeg` (copied to repo cwd as `pep_desktop_zh.jpeg`). docHeight 2,385px — calm.
- **Mochi browse (zh, desktop):** docHeight **8,969px**, 11 sections, **52 cards** before "show more". Screenshot: `mochi_desktop_full.jpeg`.
- **Mochi browse (zh, mobile 390px):** docHeight **22,618px**. `scrollWidth` 375 (< 390) → **no horizontal document overflow**. Only `.quick-nav-*` exceeds the viewport, and that bar is intentionally horizontally scrollable.
- **StatusBar:** DOM has `.status-accent` (height **5px**); the old `.status-bar` element is **absent**. The documented 390px → 659px overflow cannot occur.
- **Saffron (zh, desktop):** docHeight 5,635px, 6 tabs, no error boundary triggered, no console errors. Clicked through tabs; all render. Screenshots: `saffron_desktop_profile.jpeg`, `saffron_money_zh_english_leak.jpeg`.
- **Console:** 0 errors / 0 warnings on every page navigated.
- **i18n probe (zh, money tab):** 12 paragraph-level text blocks contained zero CJK characters (pure English) while the UI was in Chinese — programmatically detected, samples captured (see Issue 4).

Screenshot files were written by the Playwright MCP server into `C:/ScottStuff/ArcadiaAI/.playwright-mcp/` and the ArcadiaAI cwd (`pep_desktop_zh.jpeg`, `mochi_desktop_full.jpeg`, `saffron_desktop_profile.jpeg`, `saffron_money_zh_english_leak.jpeg`) — they are review artifacts from this session, not part of the GalleryAgentAI repo.

---

## Issues found

### Issue 1 — Mochi browse page is an endurance scroll (contradicts "exactly three actions")
- **Severity: Major** (experience, not crash)
- **Location:** `frontend/src/App.jsx:62-90` (renders TodaysFocus + OpportunitiesSection + RelationshipTargets stacked); `frontend/src/components/OpportunitiesSection.jsx:13-21, 92-119` (7-section `SECTION_ORDER` + StrongestPicks + Press all stacked).
- **Evidence:** Measured 8,969px desktop / 22,618px mobile; 11 sections; 52 cards on first paint. Backend serves 416 opps incl. a 310-item watch_list and a 37-item competitions list. The strongest-picks band (`strongestPicks(actionSections, 6)`) pulls its 6 cards *from the same sections rendered below it*, so the top of the page duplicates cards the user then scrolls past again (visible in `mochi_desktop_full.jpeg`: UTRECHT, MOUNT ZINE, Strange Gallery, Komonso Roastery recur across bands).
- **Why it matters for this user:** the product thesis (CLAUDE.md: "Produces three options, not fifty"; "3 excellent > 100 mediocre") is the whole point for an artist who "drowns" in possibility. The 3-card Today's Focus is correct, then undermined by ~49 cards of accumulated possibility immediately below it.
- **Suggested fix (no new features — consolidation, per the project's posture):** On the Mochi action page, default to **Today's Focus + Strongest Picks only**, and collapse the seven category grids behind the existing QuickNav / a "browse everything" affordance (the section components already support lazy reveal). Drop the duplication by excluding strongest-picks items from their source grids, or hide the source grids by default. Keep the 310-item watch_list off the action page entirely (it belongs behind a deliberate click). This is a layout/default change, not a rebuild.

### Issue 2 — Default landing page is Peppercorn (input), not Mochi (action)
- **Severity: Minor**
- **Location:** `frontend/src/App.jsx:63` — `const [page, setPage] = useState('refine')`.
- **Evidence:** On load the active companion is 对话/refine (Peppercorn). The Bible/CLAUDE.md frames Mochi (action, "What should I do today?") as the home/anchor; Peppercorn is the reflection/input page.
- **Why it matters:** the first thing the artist sees is a form-heavy "tell the system about yourself" page rather than "here are three things ready for you." For an overwhelmable user, opening on legwork-done reassurance is gentler than opening on a questionnaire.
- **Suggested fix:** default `page` to `'discover'` unless there's a deliberate onboarding reason to land on Peppercorn first. If intentional for first-run, gate it on whether the profile/statement is empty.

### Issue 3 — Saffron Pricing Intelligence & Timeline render English-only in zh/ja
- **Severity: Major** (for a Chinese-first user)
- **Location:** data `frontend/src/data/saffron_insights.js:831-871` (`PRICING_INTELLIGENCE`) and `CAREER_TIMELINE` — their `source_note`, `note`, `rule`, `why`, `current_gap`, `factor`, and per-range `note`/`sweet_spot` fields have **no `_zh`/`_ja` variants**. Render `frontend/src/components/SaffronPage.jsx:1500-1552` (`PricingIntelligence`) and `:1458-1494` (`CareerTimeline`) read those raw fields directly (`f.note`, `range.note`, `d.source_note`) — they do **not** go through `locF()` or the `deepTranslate`/`SF_ZH` path the other money-tab sections use.
- **Evidence:** In zh mode, 12 English-only paragraph blocks detected on the money tab; section *title*/*summary* ARE translated (`定价情报`/`価格情報` at translations.js:348-349, 1185-1186), producing a Chinese header over an all-English body (`saffron_money_zh_english_leak.jpeg`). Sample: "Based on Sterling & Associates assessment data…", "F4–F8 scale (24–38cm)…", "Same piece sells for 2–3× more at a gallery opening…".
- **Suggested fix:** Either route `PricingIntelligence`/`CareerTimeline` through `locF(item, 'note', lang)` and add `note_zh`/`note_ja` (and the other fields) to the data file the way `LICENSING_LANDSCAPE`/`GRANT_LANDSCAPE` already do (251 `_zh`/`_ja` keys exist there as the pattern), or add these static strings to `SF_ZH`/the `_i18n` map. Until then, the entire pricing strategy is unreadable to her.

### Issue 4 — Revenue/Saffron mixed-language qualifier strings in zh
- **Severity: Minor**
- **Location:** `frontend/src/data/saffron_insights.js` `REVENUE_STREAMS` value/qualifier fields rendered in `RevenueStreams`; visible as e.g. "SUZURI (被动收入) ¥10,000–30,000/month **with active promotion**" and "Booth.pm ¥10,000–25,000 **lower traffic, higher margin**".
- **Evidence:** `saffron_money_zh_english_leak.jpeg` — stream body prose is translated but the inline English qualifier after the amount is not.
- **Suggested fix:** add `_zh`/`_ja` for the amount-qualifier field, or move the qualifier into the already-translated note.

### Issue 5 — Revenue cards still lead with SUZURI/Booth.pm, not her actual BASE shop
- **Severity: Minor (content/data, flagged for the data owner — not a frontend code fix)**
- **Location:** `frontend/src/data/saffron_insights.js` `REVENUE_STREAMS` ordering.
- **Evidence:** CURRENT_STATE (2026-06-24) says revenue was "corrected to her actual BASE shop (gegyjiji.base.shop, not SUZURI)." The "从何入手 / Where to start" callout correctly references the BASE shop, but the revenue-stream cards below still lead with **SUZURI** as the first card and **Booth.pm** second; BASE appears only inside the SUZURI card's prose. The correction landed in the callout but not in the card list/order.
- **Suggested fix:** make BASE the first/primary revenue-stream card; demote SUZURI/Booth.pm to alternatives, consistent with the documented correction.

### Issue 6 — Standalone "条帖子" / "件の投稿" labels
- **Severity: Minor**
- **Location:** `frontend/src/i18n/translations.js:644` (zh `sf.label.posts` = "条帖子"), `:1634` (ja = "件の投稿"); used in `SaffronPage.jsx:362, 528`.
- **Assessment:** In every live usage they are preceded by a number (`{s.posts} 条帖子` → "1234 条帖子", `{p.posts} 件の投稿` → "1234 件の投稿"), which is **natural** Chinese/Japanese. They would only read awkwardly if ever shown without a preceding count. Lower priority than CURRENT_STATE implies; cosmetic at most.

### Issue 7 — Unused eslint-disable + dead StatusBar CSS/asset
- **Severity: Minor (cleanliness)**
- **Location:** `frontend/src/components/PeppercornPage.jsx:1302` (unused `react-hooks/exhaustive-deps` disable — the lint warning); `frontend/src/components/StatusBar.css:10-215` (~200 lines of `.status-bar` styling for markup that no longer renders); the 4 hero PNGs (~10.6MB) ship unoptimized.
- **Suggested fix:** remove the stale disable directive; delete dead `.status-bar*` CSS; convert hero PNGs to WebP (the repo already used WebP for the reverted section headers, so the pipeline exists).

---

## Hook-order / render-correctness verdict (the explicit smoke-test ask)

**Clean.** I specifically inspected the two refactor targets:
- `TodaysFocus`, `SaffronPage`, `PeppercornPage` and every sub-component call all their hooks unconditionally at the top, before any early `return` (e.g. `SaffronPage` calls `useState`/`useEffect`/`useMemo` then returns; `PeppercornPage` sub-sections call `useState`/`useEffect` before their `SectionShell` return). No conditional or post-return hooks found.
- The `set-state-in-effect` patterns are deliberately suppressed and legitimate (async-data → editable-local-state sync).
- Saffron wraps its tab content in `SectionErrorBoundary key={tab}` — a render failure in any one section degrades to a warm inline message instead of blanking the page.
- Live: Peppercorn, Saffron (all 6 tabs), and Mochi all rendered with **0 console errors / 0 warnings**. No empty/broken states observed; loading and empty states are warm (`tf.noItems` = "Nothing urgent. Come back tomorrow.").

The CURRENT_STATE worry "verify Peppercorn/Saffron still render after the hook-order changes" is **satisfied** — they render correctly.

---

## Launch verdict for this facet

**Conditional go.** No technical blockers: it builds, tests pass, all three pages render correctly in both languages with zero console errors, and the previously-feared StatusBar overflow is gone. But two issues land squarely on the person this app was built for and should be fixed before she sees it: (1) the Mochi action page must stop being an 8,969px / 22,618px endurance scroll — it currently betrays the "exactly three actions" promise that is the product's entire reason to exist; and (2) the Saffron money tab must not show her an all-English wall in Chinese mode. Issue 1 is the one I'd block a *real-user* launch on for an easily-overwhelmed artist; Issue 3 is a strong should-fix. Everything else is minor/cleanup.
