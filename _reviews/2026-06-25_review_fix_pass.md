# 2026-06-25 — Mochi's Atelier: Four-Angle Review + Fix Pass (ops record)

**Keeper:** Crema (Ops). **Status:** fixes in flight (3 agents). **This file is the handshake for the verification agent — read it before checking anything.**

> Context that reframes everything below: this is **GEGYjiji's PRIVATE dashboard** — audience of one,
> never shared publicly. Scott's bar: *"this is for the girl I love. I need it to stand up to that metric."*
> Two late corrections from Scott landed mid-pass and are load-bearing:
> 1. **Her real following is 26,000 (2.6万), NOT 90,000 / 9万.** The data was wrong; every derived claim must be recomputed.
> 2. **Private, single-user.** All share / OG / SEO / unfurl findings are MOOT and were dropped from scope.

---

## Section 1 — Baseline (restore point)

- Committed her runtime data and pushed a clean baseline **before** any fix work, per Scott.
- Baseline commit on `main`: **`c41f2a80`** ("checkpoint: her runtime data ... before review-fix pass"), pushed to `origin/main` (`3405e640..c41f2a80`).
- If a fix goes wrong, `c41f2a80` is the known-good point.
- Rule honored: **no `git add .`** in this repo (a tracked `.env` with the Discord webhook + Anthropic key exists). All staging was explicit-path.

## Section 2 — How the review was done (so findings are trustworthy)

- The live app is a **client-rendered SPA**; a static fetch returns only `<title>`. Per the standing project rule, everything was verified against the **rendered** page, not an engine's self-report.
- Playwright MCP was wedged; the page was rendered with **headless Chrome** (`--dump-dom` + `--screenshot`, desktop 1440 + mobile 390). Artifacts (scratchpad, not committed): `mochi_rendered.html`, `mochi_desktop.png`, `mochi_mobile.png`.
- Four reviewers, four angles, all held to Scott's metric: **Crema** (ops/does-it-work), **Flint** (tech/perf/a11y), **Lore** (writing/voice/bilingual), **Pip** (first-run/emotional). All four independently landed on **"close, not yet."**

## Section 3 — Findings (convergent), re-weighted for "private / audience of one"

Severity reflects the private-dashboard reframe.

| # | Finding | Found by | Severity | Status |
|---|---------|----------|----------|--------|
| F1 | **English leaks into the zh view** — first card shows `📅 Twice-yearly (spring/autumn) — watch @mo…`. ~199/522 cards have English `deadline` with no `deadline_zh`; `OppCard.loc()` falls through to English. Also `Check source` placeholder (~10×), `Tier 2` jargon. | Flint, Lore | **Critical** (she reads it daily) | Fix in flight (Data + Frontend) |
| F2 | **Follower count wrong: 9万/90,000 → real 26,000.** Baked into ~35 spots in `compact_opportunities.json` + many `Memory/*.json`; derived claims wrong (e.g. Kamome "150× the minimum" → ~43×). | Scott (correction) | **Critical** (dashboard lies to her) | Fix in flight (Data + Infra/generator) |
| F3 | **Voice talks ABOUT her, not TO her** — ~57 cards use `她`/`GEGYjiji` vs 17 `你`. On her own private tool this reads as a dossier. | Lore, Pip (both #1 emotional fix) | **High** | Fix in flight (Data patch + Infra/generator prompt) |
| F4 | **Deadlines invisible on card faces** — `OppCard.jsx` never renders `opp.deadline`; competitions/open-calls show no dates. | Crema | **High** (core ops promise) | Fix in flight (Frontend) |
| F5 | **Today's Focus mis-ranks + under-renders** — promises 3, shows 2; leads with a no-deadline zine shop; buries ZINEフェス東京 (closes **6/27**, 2 days out). | Crema, Pip | **High** | Fix in flight (Frontend) |
| F6 | **Triage state doesn't persist** — `useState(null)`, never hydrated; POST keys on `title||name||id` but suppress uses `opp.id` (id mismatch). | Crema, Flint | **Medium** (daily driver) | Fix in flight (Frontend) |
| F7 | **Perf on her phone** — hero is a **1.98 MB PNG**; **403 KB JS served uncompressed** (nginx gzip off, verified). ~2.4 MB → ~0.4 MB achievable. | Flint | **Medium** | Fix in flight (Frontend asset + Infra nginx) |
| F8 | **Overwhelm: bare counts** (关注列表 302, etc.) read as "how behind you are"; threat-framed urgency (`不可逾期`). Studio value: reward action, never shame rest. | Pip | **Medium** | Fix in flight (Frontend counts + Data urgency copy) |
| F9 | `<html lang="en">` on Chinese content. | Flint | **Low** | Fix in flight (Frontend) |
| F10 | **Long-tail quality cliff** — 294/522 cards fall to templated pipeline-speak that even leaks engine instructions ("建议在推荐前进行核实", "因其属于结构化机会类别"). | Lore | **Low/Med** | Fix in flight (Data rewrite + Infra generator) |
| — | Poems are **correct and well-chosen** (Su Shi / Wang Wei / Bai Juyi / Wei Yingwu, attributions verified). Scott asked to **add more** if convenient. | Lore | n/a | Adding (Frontend) |

**Dropped as MOOT (private dashboard):** OG/social-unfurl meta, share-preview, SEO, "is it creepy/automated."

## Section 4 — Fix pass: agent assignments + file-ownership boundaries

Split by **disjoint file ownership** so the three agents cannot collide. Agents EDIT ONLY; the orchestrator integrates, runs the authoritative build/test/lint, then commits & pushes per verified chunk. None of the agents commit.

- **Agent A — DATA (content).** Zone: `deploy_data/compact_opportunities.json` (live) + `Memory/*.json` (source). Tasks: F2 (26k + recompute), F3 (你-not-她 in why-it-fits copy), F1 partial (kill `Check source`/`Tier 2`, add `deadline_zh`/`location_zh`), F8 partial (soften `不可逾期`), F10 partial (rewrite template lines). Must keep JSON parseable.
- **Agent B — FRONTEND.** Zone: `frontend/` only (never `frontend2/`). Tasks: F4 (deadline on card face, reuse `formatDeadlineStr`), F1 (harden `loc()`/`locF` so it NEVER echoes raw English/sentinels — the documented fix pattern), F5 (Today's Focus rank-by-urgency + render promised count), F6 (localStorage hydration + single stable id), F8 (soften counts on home), F9 (`lang=zh` + toggle), F7 (hero `<picture>`+WebP, dims, fetchpriority), poems (+3–4), F10 (suppress template render). Must pass `npm test` / `build` / `lint`.
- **Agent C — INFRA/PYTHON.** Zone: `deploy/**`, `engines/**`, pipeline runners (`api.py` only if required). Tasks: F7 (nginx gzip/brotli — note: **manual SSH re-apply required**), stale-data alerting (wire `engines/notify.py` to fire on failed run), **durable generator fixes** (F2 follower count read from profile, F3 second-person + no-jargon in the copy-gen prompt) so a future regen doesn't reintroduce F2/F3/F10.

## Section 5 — Verification checklist (for the checking agent)

Verify against the **rendered** page (headless Chrome, both zh and English toggle, desktop + 390px mobile), not source self-report. Then:

- [ ] **F1:** Grep the rendered DOM for any Latin-script run inside zh cards (deadline/location). Confirm NO `Check source`, NO `Tier`, NO raw recurrence English ("Twice-yearly", "Rolling consignment", "watch @…") in the zh view. Confirm `loc()`/`locF` cannot fall through to English even for a field with no `_zh` (test by temporarily removing a `_zh` — renderer should show a localized fallback, not English).
- [ ] **F2:** `grep -rn "9万\|90,000\|90000\|90k"` across `deploy_data/` and `Memory/` → **zero** her-facing hits. Confirm "倍/×" multiplier claims recomputed from 26,000 (or made qualitative). Confirm `Memory/artist_master_profile.json` root number = 26,000.
- [ ] **F3:** `grep -n "GEGYjiji\|她"` in the why-it-fits/reasoning fields of `compact_opportunities.json` → only acceptable in titles/proper-noun context, not in the voice. Spot-check 5 cards render in second person in both languages.
- [ ] **F4/F5:** Card faces show a localized deadline; urgent (<7d) styled. Today's Focus renders the promised count and leads with the soonest real deadline (ZINEフェス 6/27 should surface, not be buried).
- [ ] **F6:** Mark a card 已申请, reload → state persists. Confirm one stable id used for POST + persistence + suppression (no `title||name||id` vs `opp.id` split).
- [ ] **F7:** `curl -H "Accept-Encoding: gzip" <js url> -w "%{size_download}"` → materially smaller than 403 KB (after server re-apply). Hero served as WebP, < ~400 KB, with width/height + `fetchpriority`. **nginx change needs manual SSH re-apply — confirm with Scott it was applied to prod.**
- [ ] **F8:** Home/today surface shows no anxiety-inducing bare counts; `不可逾期` reframed to gentle opportunity copy.
- [ ] **F9:** `<html lang="zh">`; toggling language updates it.
- [ ] **Poems:** new entries correctly attributed, picked up by rotation (array-length-driven, not a stale constant).
- [ ] **Build gate:** `cd frontend && npm test && npm run build && npm run lint` green (one known pre-existing Peppercorn unused-disable warning is acceptable). Relevant `engines/` tests green.

## Section 6 — Systemic root causes (fix the cause, not the symptom)

The verification agent should confirm these are addressed at the source, because several are **recurring** (per CURRENT_STATE this is at least the third English-leak: Saffron timeline → money tab → now deadlines):

1. **i18n coverage is not enforced.** Root cause of F1/F10: the pipeline emits her-facing free-text fields (deadline, location, why-it-fits) **without guaranteed `_zh`**, and the renderer's fallback **echoes the English source** instead of routing through the translation layer. *Durable fix:* (a) generator must emit `_zh` (and `_ja`) for every her-facing free-text field, and (b) `loc()`/`locF` must NEVER return raw source — always a localized value or empty. Consider a CI/test assertion: "no her-facing field renders Latin script in zh mode."
2. **No output sanitizer between pipeline and her view.** `Check source`, `Tier 2`, "建议在推荐前进行核实" are internal strings that reached production copy. *Durable fix:* a final gate that strips internal taxonomy/placeholder/meta-instruction tokens before data is served.
3. **Profile is not the single source of truth for derived copy.** F2 happened because the follower count was baked into copy instead of read from `artist_master_profile.json` at generation time. *Durable fix:* generator reads stats from the profile; never hardcode.
4. **Generation prompt under-constrained on voice.** F3 recurs every regen because the copy prompt doesn't fix person/address. *Durable fix:* prompt enforces second person + no jargon (Agent C).
5. **Silent pipeline failure.** `last_run.json` = failed (6/23) went unnoticed → data quietly rots on a tool she relies on. *Durable fix:* Discord alert on failed/incomplete run (Agent C).
6. **Asset/build hygiene.** PNG-not-WebP hero + gzip-off are repeatable regressions. *Durable fix:* document the asset pipeline + nginx config as part of deploy, and re-verify after each deploy.

## Section 7 — Fix results (FILLED IN AS AGENTS REPORT — currently PENDING)

- **Agent A (Data): ✅ DONE (crashed mid-flight at tool-use 73 — "connection closed" — but substantive work completed first; verified by the orchestrator, not trusted).** JSON re-validated as parseable after the crash.
  - Instagram count **90k/9万 → 26k** (45 "26k" present). Voice **她 → 你** complete (0 third-person `她`, 200 `你`; no `GEGYjiji的…` reasoning constructions remain). `Check source` placeholder **removed** (0).
  - **Verified-as-correct residuals (left intentionally):** `HK$90,000` is a real grant amount; **"90k Twitter followers" is her real Twitter count — Scott confirmed 2026-06-25 "leave Twitter as-is."** Only Instagram was wrong.
  - **`Tier N` jargon (6 hits) left:** all in internal, non-rendered fields (`quick_action`/`bucket_fix_note`/`next_cycle_note` — none referenced in `frontend/src`); she never sees them, and Agent C banned `Tier` in generated copy going forward.
  - **`deadline_zh` NOT added (the one skipped item — agent crashed before it).** Mitigated: Agent B's hardened `locF` suppresses English free-text in the zh view, so no leak. Open enhancement: translate the ~recurrence deadline phrases to zh so those cards can *show* a deadline rather than hide it.
- **Agent B (Frontend): ✅ DONE.** 38/38 tests (21 new), build clean, lint 0 errors. F4 card-face deadlines (urgent <7d styled); **F1 hardened `locF`** (new `utils/localize.js` — suppresses English in zh/ja, routes sentinels Unknown→待确认 / rolling→常年开放, never echoes placeholders) applied in OppCard/OppDetailPanel/TodaysFocus; F5 Today's Focus reranked by urgency + count-accurate subtitle; F6 triage persists via `localStorage` keyed by single stable `oppKey()` (POST+persist+suppress unified); F8 raw counts removed from home headers; F9 `<html lang="zh-Hans">` + live toggle; **F7 hero WebP 1.89 MB → 0.12 MB** via `<picture>` + dims + fetchpriority; **+4 poems** (Du Mu 泊秦淮, Meng Haoran 宿建德江, Wang Wei 鹿柴, Zhang Ji 枫桥夜泊; POEM_COUNT now derived from dict). Note: live-browser walk not done (frontend-only bounds); behavior covered by DOM-text unit tests.
- **Integration gate (orchestrator, authoritative):** frontend **38/38 + build clean (main bundle 406 kB → 133 kB gzip) + lint 0 errors**; python **166/166 OK**. Both JSON data files valid.
- **Commits + push:** committed in 4 chunks (data / frontend / infra+pipeline / this record) and pushed to `origin/main`.
- **NOT deployed to prod** — Scott's call. Deploy = `bash deploy.sh` **+ manual SSH re-apply of `deploy/nginx-mochi.conf`** (gzip won't take effect otherwise).
- **Outstanding / honest gaps for a future pass:** (1) zh translations for recurrence deadline phrases (so they show, not hide); (2) the visual **uniformity / hierarchy** problem — every card renders identically regardless of importance; "give cards hierarchy" is the highest-leverage *visual* change but was out of scope here; (3) a live rendered-page walk in both languages before any handoff.
- **Agent B (Frontend):** _pending_
- **Agent C (Infra/Python): ✅ DONE (not committed).** 166/166 tests green.
  - **nginx gzip** added inside `server {}` of `deploy/nginx-mochi.conf` (gzip on, comp_level 5, min_length 1024, types js/css/json/svg/plain, `gzip_vary on`). Brotli deliberately omitted (no `ngx_brotli` on the stock Lightsail nginx — would fail `nginx -t`). **REQUIRES MANUAL SSH RE-APPLY to take effect on prod** (deploy.sh only reloads, doesn't install the config).
  - **Stale-data alerting:** wired existing `engines/notify.py` into BOTH failure paths — `scripts/check_attention.py` (laptop, refactored to pure testable `build_failure_message`/`alert_on_failed_run`) and `deploy/mochi-pipeline.sh` (server cron). Fires a Discord message on `last_run.json status="failed"`. +7 tests.
  - **Durable generator fixes (latent — apply on NEXT regen, no data regenerated):** new `follower_count_str()` helper in `engines/profile_sync.py` reads the count from the profile (+6 tests, incl. a regression guard it never returns "90"); `engines/why_it_fits_engine.py` now pulls the count from `artist_master_profile.json` AND its prompt enforces second person + forbids third-person/name, internal taxonomy ("Tier"/"bucket"/"score"), and meta-leaks ("建议在推荐前进行核实"); `engines/ibm_email_writer.py` uses the helper too.
  - **KEY SYSTEMIC FINDING:** there is **no hardcoded `90,000`/`9万`/`90k` anywhere in `engines/`** — the live engines already used ~26k. **The 90k came from previously-GENERATED data, not engine code.** ⇒ root cause #3 (profile-as-source-of-truth) is now enforced in code; the remaining 90k cleanup is purely the Data agent's job on the baked JSON.
  - Files: `deploy/nginx-mochi.conf`, `deploy/mochi-pipeline.sh`, `scripts/check_attention.py`, `engines/profile_sync.py`, `engines/why_it_fits_engine.py`, `engines/ibm_email_writer.py`, `tests/test_check_attention_alert.py` (new), `tests/test_profile_sync.py`.
- **Integration build/test/lint:** _pending_
- **Commits + push:** _pending_
- **Outstanding for Scott:** nginx re-apply on prod (manual SSH); decide whether to deploy this pass to her live site.

---
*Crema keeps this current. When each agent reports, its results + any residual items move into Section 7, and any new systemic cause goes into Section 6. Nothing is "done" until Section 5 is checked against the rendered page.*
