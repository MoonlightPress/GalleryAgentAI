# UX Pass + Alternate Build — Progress Tracker

**Started:** 2026-06-13 (overnight session)
**Goal:** Full UX pass on the three companion pages, findings documented separately,
then an alternate frontend build (`frontend2/`) that dramatically improves on the
current one WITHOUT touching the working `frontend/`.

**User intent (verbatim spirit):** This is for the artist he loves. All reports say
"good" — he needs *perfect*. Undeniable, fully self-explanatory. The new build should
make the current version look obsolete. Document everything as we go so a token reset
never leaves unfinished docs/analysis/builds. Multiple parallel agents authorized.

---

## Resume-here state (update after every milestone)

- [x] Project understood (CLAUDE.md, memory, api.py read, all frontend components read/skimmed)
- [x] Servers: FastAPI already running :8001; Vite started :5177 (proxy /api → 8001)
- [x] Full-page screenshots captured: `C:\Users\ScotA\AppData\Local\Temp\mochi_shots\*.png`
      (mochi_full, saffron_full, pepper_full + _top variants; default lang renders zh)
- [x] Close-up screenshots (EN lang, detail panel open, calendar view, expanded sections)
- [x] `01_UX_FINDINGS.md` — complete audit DONE
- [x] `02_REDESIGN_SPEC.md` — design spec DONE
- [x] `05_API_AUDIT.md` — agent-verified /api/today root cause + email coverage counts DONE
- [x] `04_LOGIC_EFFECTIVENESS.md` — DONE (agent-written; 7/13 IBM copy-paste ready,
      no follow-up loop, scheduler never ran, Tier-4 leak, top-5 ranked fixes)
- [x] `frontend2/` scaffolded AND RUNNING on :5178 (npm installed, smoke-tested, zero console errors)
- [x] Shared shell v2 DONE: hash router (router.js), CompanionBand (animals = nav, voice
      lines), StatusStrip (sticky, honest signals), atelier.css design system,
      utils (api.js / deadlines.js / fitWords.js), i18n local-registry (i18n/local.js)
- [x] Mochi page v2 BUILT AND VERIFIED (4:55am): zero console errors; Copy email
      → clipboard contains venue-appropriate Japanese draft; details expand in
      place w/ checklist + tabbed drafts + copy; stale drawer present; focus area
      contains only future dates (2026/2027); mobile 390px layout verified clean.
      Shots: v2_mochi_top/full/detail/toast/drawer/mobile.png
- [x] Saffron page v2 BUILT AND VERIFIED (run-2 agent, ~5:05am): synthesis +
      journey stones + field bars + perch + FieldNotes library; zero console
      errors incl. clicking all 7 stones and all 24 note cards; see agent report
      at bottom of this file. Known gap: server-side strings (blocking_now, step
      details) are English-only — backend localization, noted for later.
- [x] Peppercorn page v2 BUILT AND VERIFIED (run-2 agent, ~5:10am): page root +
      peppercorn.css; Wondering→Insight→Knows→RecordBook→Milestones; zero console
      errors; save round-trip tested through the UI (goal added→persisted→removed);
      existing profile data renders. See agent report at bottom of this file.
- [x] Backend fixes applied (see 05_API_AUDIT.md "FIXES APPLIED"): /api/today
      staleness gates + 90k→26k follower fix in engines + generated data.
      ✅ API RESTARTED 4:54am — fix verified live: quick_win UTRECHT deadline
      blanked (evergreen), stretch_goal now "FY2026 Life with Art Grant"
      (June 29, 2026 — real and future) instead of dead Nov-2025 fellowship.
- ALL THREE PAGE AGENTS DIED AT SESSION TOKEN LIMIT (resets 4:30am Asia/Tokyo).
  An in-session cron (job 6acd497d, every 2h at :53) will resume this work at
  4:53am IF this Claude session stays open. Next session: verify Mochi page
  visually, finish Saffron+Peppercorn page roots from their existing components,
  restart API, screenshot all pages old-vs-new, write 03_BEFORE_AFTER.md.
- [x] Side-by-side screenshots copied to reports/ux_pass_2026-06/shots/ (10 files)
- [x] `03_BEFORE_AFTER.md` — DONE
- [x] Overnight continuation cron set (job 6acd497d, every 2h at :53, session-only)
- [x] Final summary delivered + committed as a928cb40; overnight cron deleted (work complete)

## Key facts discovered (so a fresh session doesn't re-derive)

- Frontend: `frontend/src` — App.jsx routes 3 pages by state: discover (Mochi),
  observe (Saffron), refine (Peppercorn). i18n: zh/ja/en via translations.js (2576 lines).
- Backend: `api.py` (2511 lines) — endpoints: /api/opportunities (bucketed sections),
  /api/today (3 focus slots), /api/feedback, /api/submissions, /api/contacts,
  /api/saffron, /api/career_strategy.
- Design tokens in `frontend/src/index.css`: --paper #FFFAF3, --parchment #EDE5D2,
  --ink #3d2b20, --gold #c49a3e, --leaf #7a9e7e, --rose #d4897a. Georgia serif.
- SaffronPage.jsx = 1584 lines, **24 stacked accordion sections** (almost all collapsed
  by default) → violates "reports multiply faster than insight."
- PeppercornPage.jsx = 2021 lines — carousel of progress arcs + ~10 accordion sections.
- Hero illustrations exist and are beautiful (cat at desk / mouse in mousehole / bird
  at window). Nav is text buttons — vision says *the animals are the navigation*.
- Mochi page = hero + Today's Focus (3 cards) + 7 card-grid sections + press section.

## Decisions made

- Alternate build lives in `frontend2/` (new folder, port 5178), current app untouched.
- Findings = separate docs in this folder, not inline in build.

## If resuming after token reset

1. Read this file fully.
2. Check checklist above; continue at first unchecked item.
3. Vite for old app: `cd frontend && npm run dev` (:5177). API: `python api.py` (:8001).
4. Screenshots dir: `C:\Users\ScotA\AppData\Local\Temp\mochi_shots`

## Saffron page agent report (run 2)

- Built `frontend2/src/pages/saffron/SaffronPage.jsx` (real page root, replaced 284-byte placeholder): hero band (saffron_hero.png + voice line) -> "From up here" synthesis (3 prose beats from /api/saffron: career_position, pathway.blocking_now verbatim, market_landscape; 3 key numbers: confirmed shows / ready-now (actionability tier=high) / deadlines this month from timing_intelligence.monthly_counts) -> The Journey (7 pathway.steps as CSS stepping stones, done=leaf, blocking=gold+scaled with Saffron's note, click-to-detail, defaults to blocking step) -> The Field (category bars, Tokyo/international split bar, actionability pills) -> Perch row (top 4 peer_artists cards) -> existing FieldNotes library. Every section wrapped in NoteBoundary (reused export from FieldNotes.jsx).
- Files touched: `SaffronPage.jsx` (rewritten), `strings.js` (added v2.saffron.journey.title/sub, field.cats/split/tokyo/intl/act, perch.sub/caveat in en/zh/ja). No CSS changes needed — run-1 saffron.css already covered all classes.
- Verified via Playwright on :5178 — `v2_saffron_check.png`, `v2_saffron_full.png`, `v2_saffron_mobile.png` (390x844), plus interaction pass (all 7 stones + all 24 note cards clicked): zero console errors. Note: an initial 500 came from `peppercorn/peppercorn.css` missing (other agent's file, appeared mid-run); not a saffron issue and resolved on re-check.
- Known gaps: pathway.blocking_now / step details / peer fit_reason / actionability labels render verbatim from the API (English-only — server doesn't localize these); peers beyond the top 4 are only reachable via Field Notes (Career Timeline note); "deadlines this month" counts parsed deadlines only (rolling/unknown excluded).

## Peppercorn page agent report (run 2)

- **Built** `frontend2/src/pages/peppercorn/PeppercornPage.jsx` (page root, replacing the 285-byte placeholder) and **created** `peppercorn.css` (page-scoped styles for every `pep-*` class used by the run-1 components; atelier tokens only, no invented palette).
- **Section order per spec**: hero band (340px, `peppercorn_hero.png`, voice line) → The Wondering (opening move, 8 pebbles) → DismissalInsightBanner (simplified v1 port via `api.feedbackInsights()` / `api.suppressCategory()`, client-side 3+ dismissal threshold — currently hidden, dismissals map is empty) → What Peppercorn Knows → The Record Book → Milestones strip.
- **Save contract** mirrors v1 exactly: optimistic local merge then `POST /api/peppercorn` with the full merged profile; toast on save/error. Milestones derive from `live_counts` + statement length + answered question count (1/3 shows · 2/3 pubs · 26k→50k IG · statement: draft · 2/8 questions) — no rings, no fake progress.
- **Error isolation**: each section wrapped in a small class-component boundary (`PepBoundary`) with a quiet fallback line; one bad shape can't blank the page. Added `v2.peppercorn.section.error` to strings.js (en/zh/ja).
- **Verified with Playwright**: `v2_peppercorn_check.png` (1440×950), `v2_peppercorn_full.png` (full page, 2998px), `v2_peppercorn_mobile.png` (390×844) in `%TEMP%\mochi_shots` — zero console errors on all three; saved profile data renders (statement, 2 goals, tiers 1+2, geo, answered questions). One visual polish iteration applied (milestone accent bars, option chip alignment).
- **Save round-trip tested via UI**: added goal "test goal (auto)" → confirmed in fresh `GET /api/peppercorn` → removed via UI → confirmed gone. Files touched: only inside `frontend2/src/pages/peppercorn/` (+ this report).
