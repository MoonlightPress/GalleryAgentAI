# Mochi Pre-Handoff Checklist — external review pass (2026-06-24, night)

**Who wrote this:** an outside review setup (not the core mochi chat), at Scott's request, after a 5-agent
code review + a live-site walk of https://twilightdreamworks.com/mochi/ in Chinese. Scott is **not** sending
this to GEGYjiji tonight. This is the to-do list for the readiness pass.

**How to use this:** the five detailed facet reports live next to this file in `_reviews/`
(`2026-06-24_frontend_ux.md`, `_data_pipeline.md`, `_backend_api.md`, `_architecture.md`, `_launch_deploy.md`).
This file is the consolidated, prioritized action list. Verify each item against the live rendered page, not a
self-reported coverage number — that's the trap that ate a whole day (see §1).

---

## STATUS — overnight pass (2026-06-25, while Scott slept)

**⚠️ NOT YET DEPLOYED — these fixes are committed to source/`main` but the LIVE site still shows the old
build + old backend.** A full rebuild + deploy (and a server-side backend restart) is needed to make them
visible. Do that deliberately and atomically (see §3.4 — the partial-deploy hazard is real; tonight's Saffron
blank came from exactly this).

**Done & verified this pass (committed to `main`):**
- ✅ **§1 Saffron render bug** — already fixed earlier by the mochi session (`localizeDeep` + `lang` threaded +
  4 `had_zh` arrays added). Confirmed in source.
- ✅ **§3.3 Money gate** (`68c5febd`) — the 4 translation engines are now in `PAID_STEPS`; verified the
  unattended maintenance pass can no longer run them. The 6/30 spend risk is closed.
- ✅ **"nothing has links" (calendar + all sections)** (`b2bdec21`) — added a click-through `open` link to every
  `OppCard`. Verified live on the dev server: 43 cards now link out (was ~3 on the page); real hrefs.
- ✅ **§4.6 Closed fair in "best actions"** (`d9444cd1`) — `_ibm_eligible` now excludes `status=closed`.
  Verified: 0 closed items IBM-eligible, 139 legitimate ones still eligible.

**Deliberately NOT done unattended (need supervision, a paid run, or server/SSH) — for the next pass:**
- **Calendar "not a real calendar" feel** — the month grid IS real but small and buried under the long 30-day
  list. This is a design/layout call (make the grid primary? collapse the list?) — left for Scott's eye, not
  guessed at overnight. The English on it is mostly proper-noun titles (`opp.name` with no `name_zh`) + city
  strings; decide per-item whether to localize or leave (most award names are legitimately English).
- **§4.7 Backend `_load_json` crash-safety** — ~40 `json.loads` call sites, several already in try/except.
  A blanket refactor is too risky to do unattended against the serving app. Spec: add `_load_json(path, default)`
  and apply to the hot GET readers first (`/api/opportunities`, `/api/saffron`, `/api/contacts`,
  `/api/peppercorn`, `/api/career_strategy`). Low severity (only bites on an interrupted write).
- **§4.8 Deadline-parser unification** — importing `deadline_normaliser`'s parser into `api.py:_deadline_passed`
  changes what gets hidden; medium risk, wanted supervised + tested.
- **§2.2 Email feedback loop** — the profile-source unification is a code fix, but a refreshed draft needs a
  PAID regen — left for Scott's go.
- **§2.1 Server autonomy + §3.4 nginx/SSL reconcile** — infra/SSH; mochi already offered to set up nginx. Not
  touched (no unattended SSH to production).

---

## 0. The meta-lesson (read first — this is why the translation work looped all day)

The translation engines translate **pipeline data** and then report "100% coverage." That report is true *about
the data file* and **blind to a whole second class of text**: strings hardcoded in the React frontend, and data
fields the components render in the wrong language. So the engine kept declaring victory while the page kept
showing English. **Fix the verification, not just the data:** after any translation/i18n change, do a DOM
English-sweep on the actually-rendered page in zh (a quick `document.querySelectorAll` scan for Latin-heavy text
nodes with no CJK finds it in seconds). Never trust the engine's self-report as the completion gate.

---

## 1. Saffron i18n render bug — translations EXIST, components don't read them (HIGH)

This is the root cause of the all-day loop. The `_zh`/`_ja` data is present and correct in
`frontend/src/data/saffron_insights.js`; two components render the raw English fields instead of the localized
ones. The localization helper already exists in the same file:

- `frontend/src/components/SaffronPage.jsx:1045` — `locF(item, field, lang)` (returns `field_zh`/`field_ja` when present).

**`CareerTimeline({ t })` (SaffronPage.jsx:1459)** — component doesn't even receive `lang`; thread it in (or call
`useLanguage()` inside), then route these through `locF`:
- `1463 {d.overall_assessment}` → `locF(d, 'overall_assessment', lang)` — `overall_assessment_zh` exists ✅
- `1484 {peer.comparable_age}` → `locF(peer, 'comparable_age', lang)` — `comparable_age_zh` exists (×4) ✅
- `1489 {peer.comparison}` → `locF(peer, 'comparison', lang)` — `comparison_zh` exists (×4) ✅
- `1487 {h}` (the `peer.at_stage.had.map(...)` bullet list) → **`had_zh` is MISSING (count 0 in the data).**
  This is the ONLY genuinely-untranslated piece in the block. Add `had_zh` arrays to the 4 peers in
  `saffron_insights.js` (peer blocks ~lines 776, 790, 804, 818), then render the zh array when `lang==='zh'`.

**`PricingIntelligence({ t })` (SaffronPage.jsx:1501)** — also doesn't receive `lang`; thread it in, then:
- `1506 {d.source_note}` → `locF(d, 'source_note', lang)` — `source_note_zh` exists ✅
- `1512 {range.label}` → localize — `label_zh` exists (×5) ✅
- `1516 {range.note}` → localize — `note_zh` exists (×20) ✅
- `1518 {range.sweet_spot}` → localize — `sweet_spot_zh` exists ✅
- `1529 {f.factor}` (and the rest of `what_affects_price`) → localize, **but `factor_zh` count is only 1** in the
  data — verify every factor has a `factor_zh`/`note_zh`; some may still need translating. CHECK, don't assume.

**Verify:** build + serve, switch to zh, DOM-sweep the 观察/Saffron page for any remaining Latin-heavy text. The
discovery (发现) and 对话/Peppercorn pages are already clean except legitimate proper nouns (venue/magazine names).

---

## 2. Durability — will it still serve HER, unattended, a month from now? (HIGH, her-facing)

These are the two that actually undercut the product promise. Everything below §2 is secondary.

1. **Server autonomy / staleness.** Production is currently **laptop-driven** — the only proven refresh is a
   Windows Scheduled Task on Scott's laptop that SCPs JSON up. Laptop off → data silently goes stale, with no
   on-screen signal. And `last_run.json` reads `status: failed` (2026-06-23) — the refresh loop's last run
   failed. **Action:** confirm/install the server-side cron (`deploy/setup_server_pipeline.sh` → `mochi-pipeline.sh`)
   and verify it actually runs, OR consciously accept laptop-driven AND add a "data last updated / may be stale"
   banner so she's never silently looking at frozen data. Investigate why 6/23 failed.

2. **Her feedback loop is silently broken.** Editing her artist statement in Peppercorn does **not** refresh email
   drafts — two independent breaks: Peppercorn saves to `memory/peppercorn_profile.json` (api.py ~2540) while
   `engines/ibm_email_writer.py` reads `memory/artist_master_profile.json` (lines 27, 38–44), AND the writer is
   write-once (only fills missing `email_ja`/`email_en`, line ~258). **Action:** unify the profile source and let
   a statement edit trigger a draft regen (paid step — needs Scott's go). The "Draft — review before sending"
   label mitigates the trust risk for launch but the mechanism is still broken.

---

## 3. His-risk — close before "set and forget" (MEDIUM, not her-facing)

3. **Money gate.** `PAID_STEPS` is incomplete: the Claude-using translation engines
   (`content_translation_engine`, `saffron_translation_engine`, `contact_translation_engine`,
   `opp_strategy_translation_engine`) are in the live pipeline but NOT in `PAID_STEPS`. A cache saves steady-state,
   but any source-prose change before the **enabled Windows Scheduled Task `MochiWeeklyPipeline`** fires (next ≈
   Thu 2026-06-30) means silent, unattended Claude spend. **Action:** add those engines to `PAID_STEPS`, or
   disable the scheduled task until gated. Also: `scripts/scheduler.py` + `deep_verification_agent.py` (the real
   Claude/Tavily spenders) are **orphaned/unreachable** — archive or banner them so they can't be misfired.

4. **Deploy fragility.** Tonight's Saffron blank screen was a **partial-deploy 404** on the code-split chunk
   `SaffronPage-<hash>.js` (index.html referenced a hash that wasn't uploaded). Also `install.sh` installs
   `deploy/nginx.conf` (app at `/`, no SSL) while the live config is `deploy/nginx-mochi.conf` (`/mochi`, SSL) and
   the Vite build is hard-baked to `base:'/mochi/'` — a full `install.sh` redeploy would **white-screen the site
   and drop SSL.** A non-technical user can't recover from a blank page. **Action:** make deploy ship all hashed
   chunks atomically; reconcile/retire `nginx.conf` so only `nginx-mochi.conf` can be installed; confirm
   `MOCHI_WEBHOOK_SECRET` is set on the server (api.py:2932 skips signature verification when it's empty).

---

## 4. Content & robustness cleanup (LOW / cosmetic)

5. **Duplicate paragraphs.** Several cards render the short summary and the "why it fits" paragraph as the *same*
   text (e.g. TOKYO ART BOOK FAIR 2026, 2026国际水墨艺术大展, OPEN World Exhibition, several competitions). Looks
   like a missing distinct "why-it-fits" falling back to the summary. Backfill or hide the duplicate.

6. **Stale fair in a top section.** "Zine & Book フェス in 神保町" (held Jan 18–19 2026) appears in the
   best-actions / strongest band. `_ibm_eligible` (api.py ~291) blocks `permanently_closed`/`closed_this_cycle`
   but not plain `status:"closed"`, and its date-range deadline isn't parsed. One-line fix to exclude `closed`.

7. **Backend crash-safety.** Missing-file reads are guarded, but most hot GET readers in `api.py`
   (`/api/opportunities`, `/api/saffron`, `/api/contacts`, `/api/peppercorn`, `/api/career_strategy`) aren't
   try/except-wrapped — a file that *exists but is malformed* (e.g. an interrupted self-write) → `JSONDecodeError`
   → HTTP 500 on every page load. Add a small `_load_json` helper that returns graceful empties on parse errors.

8. **Serve-time deadline parser is weaker than the canonical one.** `_deadline_passed()` (api.py ~648–691) misses
   formats the normaliser handles (English month-year, m/d/y, 2-digit year, ordinals, ranges). Today it's saved by
   the stored `deadline_past` flag, but that depends on the monthly pass staying fresh. Import the
   `deadline_normaliser` parser into `api.py` so there's one parser — free, offline.

---

## 5. Verified GOOD — do NOT re-chase

- Discovery (发现) opens **on action** with exactly **three** Today's Focus picks — the core promise holds.
- Actionable surface is **data-trustworthy**: 0 past-deadline non-relationship items leak into ready/strongest;
  0 photography, 0 listing-artifacts. (Past-deadline-in-actionable = a handful, all correctly badged
  `closed_or_stale`, none reaching the ready tier.)
- 对话/Peppercorn renders correctly and is fully translated to zh; warm, right tone.
- The old "390px StatusBar overflow → 659px" is **gone** (StatusBar is now a 5px accent div).
- Hook-order refactors are clean; 15/15 frontend tests pass; build clean; console clean on working pages.
- Secrets hygiene clean (`.env` untracked, keys present, `.gitignore` correct).
- `deploy.sh` correctly ships `frontend/` (the old `frontend2/`-sandbox trap is fixed).
- The readiness contract (backend `actionability_status`/`review_flags`/`recommendation_reasons` → frontend) is
  coherent end-to-end with no field drift.

---

## Suggested order for tomorrow's pass

1. §1 Saffron i18n render bug (+ `had_zh`) — finishes the translation story for real, with a DOM-sweep verify.
2. §3.3 money gate / scheduled-task — time-sensitive (fires ≈6/30).
3. §2 durability (server autonomy + email feedback loop) — the two things gating "ready for her."
4. §3.4 deploy fragility (atomic chunks + nginx reconcile).
5. §4 content/robustness cleanup.

*Tone reminder: this is for one real, easily-overwhelmed artist. Bias every fix toward calm, current, and
trustworthy over feature-complete.*
