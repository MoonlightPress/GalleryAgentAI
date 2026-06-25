# Frontend diagnostic — `frontend/` (canonical, port 5177)

Read-only audit, 2026-06-25. No source edited. Scope: `frontend/src` (Mochi / Saffron / Peppercorn).
Toolchain: `npm run lint` = 0 errors / 1 warning (pre-existing), `npm test` = 20/20 pass,
`npm run build` = success with 1 asset warning. Details under "Build / lint / test".

Severity legend: **P0** blocker for a Chinese-artist handoff · **P1** real bug, visible ·
**P2** minor / polish · **P3** cleanup.

---

## P0 — Japanese is shipped but unreachable; English leaks if it were reachable

**P0 — `日本語` cannot be selected; the entire `ja` layer is dead-coded.**
The language switcher iterates `LANGUAGES`, which is `['zh', 'en']` only.
Evidence: `src/i18n/translations.js:3228` → `export const LANGUAGES = ['zh', 'en']`;
consumed at `src/components/Nav.jsx:35` (`LANGUAGES.map(...)`). A full `ja` dictionary exists
(`dicts = { zh, ja, en }`, translations.js:3232) and *every* component branches on `lang === 'ja'`
(`_ja` fields, `name_ja`, `locF`, etc.), but none of it is ever reachable from the UI.
The task brief says the app supports 中文 / English / 日本語 — it does not expose 日本語.
*Fix: either add `'ja'` to `LANGUAGES` + a `LANGUAGE_LABELS.ja` (and finish the ja gaps below), or
formally drop ja and stop maintaining the dead `_ja` data/dict.*

**P0 — 95 i18n keys present in `en`/`zh` are MISSING from the `ja` block → English leak in ja.**
Quantified by key-diff of the three dict blocks (zh lines 5–1138, ja 1139–2139, en 2140–end):
`en`/`zh` each have ~986/1022 keys; **`ja` has 891** (95 fewer than en). Fallback chain is `ja → en`
(translations.js:2,3236), so each missing key renders **English** in Japanese mode. The gap clusters
include the entire **`sf.cr.*` correction UI (17 keys)** the brief called out — `sf.cr.addShow.btn/venue/year/
saved/title`, `sf.cr.alreadyDid`, `sf.cr.city/country/confirmed/mentioned/hedge/jwsYear/cancel`,
`sf.cr.type.{group,solo,institutional,international}` — plus `sf.actStatus.*` (15),
`pp.crm.*` (lookUp, saveNote, yourNotes, add*…), `pp.event.*`, `pp.goals.accomplish*`, `pp.syn.*`,
`pp.intro.*`, `sf.intro.body`, `sf.label.whereToStart`, `mochi.intro.body`, `mochi.poem.0–3`,
`opps.strongest.title/desc`, `status.updated`. (Only blocked from view today by the P0 above.)
*Fix: add the 95 missing keys to the `ja` block (list reproducible via a zh/ja key-diff).*

> Note: `zh` has **0** keys missing vs `en` — Chinese coverage of the static dict is complete. The
> leaks below are *data-field* leaks (raw English values rendered without a `_zh`/loc swap), not dict gaps.

---

## P1 — English data fields rendered raw (leak in 中文)

**P1 — `TrackerSection` renders the raw English outcome.**
`src/components/TrackerSection.jsx:53` → `<span ...>{a.outcome}</span>` prints `pending` / `accepted` /
`rejected` etc. verbatim. The same value is translated everywhere else via `t('pp.outcome.'+x)`.
*Fix: `{tfb(t, 'pp.outcome.' + a.outcome, a.outcome)}`.*

**P1 — `OppDetailPanel` contact note rendered raw.**
`src/components/OppDetailPanel.jsx:232` → `<p ...>{opp.contact_note}</p>` (no `loc()` swap), while
its siblings use `loc('overview')`, `loc('why_it_fits')`, etc. English `contact_note` shows in zh/ja.
*Fix: `{loc('contact_note')}` (and ensure `contact_note_zh/_ja` are produced upstream).*

**P1 — Saffron "gaps · strengths" summary is hardcoded English.**
`src/components/SaffronPage.jsx:1607` (`OpportunityGap`) →
`` const summary = `${data.gaps.length} gaps · ${data.strengths.length} strengths` ``.
The collapsed-section summary line shows "N gaps · M strengths" in English regardless of language.
*Fix: route through `t('sf.sum.oppGap', {...})`.* (Same pattern, lower stakes, at
`CareerPosition` 326, `CareerBenchmarks` 611, `StrategicPathway` 500, `InstagramStrategy` 540,
`PublicationLandscape` 858, `LongTermScenarios` 913 — those interpolate `Instagram`/counts only, mostly OK.)

**P1 — `OppCard` effort fallback is dead; raw key can reach screen.**
`src/components/OppCard.jsx:143` → `{t(\`card.effort.${...}\`) || opp.effort}`. `t()` returns the *key
string* (truthy) when unmapped, so `|| opp.effort` never fires; an unmapped effort renders the literal
key `card.effort.high`. *Fix: use `tfb(t, \`card.effort.${x}\`, opp.effort)` (the codebase's own helper).*

---

## P2 — Robustness / runtime-error risk

**P2 — `OpportunitiesSection` crashes if the payload lacks `sections`.**
`src/components/OpportunitiesSection.jsx:68` destructures `const { sections, meta } = data` then
`Object.entries(sections)` at line 76. A `{}` / malformed `/api/opportunities` response → `Cannot
convert undefined to object`. (`api.py` normally guards reads, so low-probability, but unguarded here.)
*Fix: `const { sections = {}, meta } = data`.*

**P2 — `SaffronPage` `useMemo(deepTranslate)` assumes well-formed payload.**
`SaffronPage.jsx:2099` runs `deepTranslate(rawData, txMap)` over the whole payload; individual section
components then index deep fields (e.g. `data.career_position.social.find(...)` at 325,
`data.market_stats` paths). A `SectionErrorBoundary` (268, wraps each tab) catches render throws, so a
missing slice degrades to an inline "A section failed to render" card rather than a white screen —
acceptable, but the boundary message itself is **hardcoded English** (`SaffronPage.jsx:275`).
*Fix: localize the boundary copy; consider optional-chaining the hottest field accesses.*

**P2 — `OppDetailPanel` email tab defaults to `ja` for every viewer.**
`OppDetailPanel.jsx:60` → `useState('ja')`. A Chinese user opening details sees the Japanese draft tab
first. Minor, but contradicts the zh-first posture. *Fix: default `emailTab` from `lang`.*

---

## P3 — Cleanup / dead code (incl. the build warning)

**P3 — Build warning: `/mochi_hero.png` referenced in dead CSS.**
`npm run build` emits: *"/mochi_hero.png referenced in /mochi_hero.png didn't resolve at build time".*
Source: `src/components/StatusBar.css:36` → `background-image: url('/mochi_hero.png')`. The path is
root-absolute, so with Vite `base:'/mochi/'` it would resolve to `/mochi_hero.png` (404 in prod, the
file isn't published there) — **but** `StatusBar.jsx` now renders only `<div class="status-accent">`
(StatusBar.jsx:7), so the whole legacy stylesheet (`.status-bar`, `.status-cat-thumb`, mini-calendar,
sticky-note — StatusBar.css:10–215) is **dead**. Harmless today; the warning is real.
*Fix: delete the dead selectors (lines 10–215), keeping only `.status-accent`.*

**P3 — "Known StatusBar mobile overflow" appears already resolved.**
CURRENT_STATE flags a 390px overflow where `StatusBar` expanded the doc to 659px. That came from the
old panel; `StatusBar` now renders a 5px accent div only (StatusBar.jsx:6–8) with no width content, so
the overflow source is gone. Re-verify in a browser, then strike it from the backlog.

**P3 — Pre-existing lint warning (not introduced here).**
`PeppercornPage.jsx:1308` — "Unused eslint-disable directive (react-hooks/exhaustive-deps)". Documented
in CURRENT_STATE; `--fix` removes it. 0 errors otherwise.

---

## Items the brief asked about — verified OK

- **`/api/event` beacon (App.jsx:70–82):** endpoint exists (`api.py:2806 @app.post("/api/event")`),
  call is `keepalive` + double-guarded `try/.catch(()=>{})`. Cannot break the UI. Fine.
- **`TrackerSection.jsx`:** returns `null` until data and when both lists empty (lines 19–22) — no
  forever-spinner, no null crash. Only issue is the raw `outcome` (P1 above).
- **`GapCorrectionForm` + `ReadinessCorrection` (SaffronPage 1786–1918):** POST to real endpoints
  (`/api/exhibition_log` 2895, `/api/membership` 2920); both `onChanged?.()`-refetch; network failures
  swallowed. Logic sound. Their only defect is the missing **ja** `sf.cr.*` keys (P0 above).
- **"drafts updating" message (PeppercornPage 1778–1782):** reads `regen_started` from the POST response,
  shows `t('pp.draftsUpdating')` for 5s. Guarded with `try/catch`. Fine.
- **`OppCard`/`OppDetailPanel` `isDistinct` guards (OppCard:170, OppDetailPanel:251):** correct — hides
  `why_card`/`why_it_fits` when identical to summary/overview; `textGuards` unit tests pass (5/5).
- **All `fetch('/api/...')` endpoints exist in `api.py`** (cross-checked the 13 distinct paths against
  the route list lines 977–3254): `/api/opportunities, /api/feedback[/insights,/suppress-category],
  /api/submissions, /api/contacts[/update,/{name},/lookup], /api/saffron[_answer], /api/peppercorn,
  /api/event, /api/career_events[/{id}], /api/exhibition_log[/{id}], /api/membership, /api/tracker,
  /api/today, /api/career_strategy`. **No dead/again-fetched endpoints found.**
- **`localizeDeep` (SaffronPage 26–37)** correctly swaps `_zh`/`_ja` siblings for the static
  `saffron_insights.js` constants, including array siblings like `credibility_signals_zh` and nested
  `had_zh`/`label_zh`. CareerTimeline / PricingIntelligence / Grant / Revenue / Licensing **do** get
  localized — the earlier pre-handoff "renders raw English" note is no longer reproducible in this build
  (those data constants now carry full `_zh`/`_ja`). Re-confirm visually once ja is selectable.

## Build / lint / test (pre-existing vs new)

- `npm run lint` → **0 errors, 1 warning**, pre-existing (PeppercornPage:1308), documented in CURRENT_STATE.
- `npm test` → **20/20 pass** (feedbackBehavior, freshness, recommendationQuality, relationshipTargets,
  textGuards).
- `npm run build` → **succeeds**; one asset warning (`/mochi_hero.png`, P3 above). Hero PNGs are very
  large (1.9–2.9 MB each, ~10.5 MB raw across the four) — heavy first-paint on mobile; consider WebP.
  Main bundle 400 kB / 131 kB gz, Saffron 167 kB / 57 kB gz (lazy) — acceptable.
