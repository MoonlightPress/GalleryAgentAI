# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Read [`CURRENT_STATE.md`](CURRENT_STATE.md) first.** It is the single source of truth for what's
> live *right now* — which frontend is current, how to run the app, what's mid-build. This file covers
> the durable *why*; `CURRENT_STATE.md` covers the volatile *what*. If they disagree, `CURRENT_STATE.md` wins.

## What This Project Is

**Mochi** is an AI-assisted artist career support system. The repo is named GalleryAgentAI; the project is named Mochi.

It was built for a real watercolor painter — not a hypothetical user. Her work: urban environments, architecture, memory, absence, atmosphere, quiet observation. That specificity shaped every major architectural decision. When the machine got something wrong, there was a real person to notice.

The central question Mochi must answer is: **"What should this artist do next?"** — not "What exists?" Artists don't lack information. They drown in it. The bottleneck is prioritization and decision-making.

The system is advisory. Humans make all decisions. The system never conducts outreach automatically.

Artist profile lives in `memory/artist_master_profile.json` and `artist_dossier.md`.

## Read Before Touching Code

The Bible files in `docs/bible/` are the canonical reference for why things exist. Read them before making architectural changes. They document 11 phases of development and 14 hard-won lessons, including which ideas failed and why.

The `docs/` numbered files (`00_START_HERE.md` through `09_INSTRUCTIONS_FOR_CLAUDE.md`) are the onboarding sequence.

## Running the App

The live app is a **React (Vite) frontend served by a FastAPI backend.** Streamlit `app.py` is the **retired** original dashboard — kept for reference only, no longer the product.

```powershell
# Current app — starts backend + frontend together, opens http://localhost:5177
start_mochi.bat
#   api.py     -> FastAPI backend on 127.0.0.1:8001 (python api.py)
#   frontend/  -> Vite dev server on :5177 (npm run dev), proxies /api -> :8001

# Active full pipeline (72-step, searches root + engines/ + ui/)
python run_full_mochi_pipeline.py

# Legacy 11-step pipeline (original, still functional)
python council_pipeline_agent.py

# Historical artist research
python run_historical_artist_pipeline.py

# Retired Streamlit dashboard (reference only)
python -m streamlit run app.py
```

### Which frontend is current

There are two React apps — **do not let this confuse you (it confused Codex):**

- **`frontend/` (port 5177) is the canonical, current frontend.** `start_mochi.bat` launches it. Active work lands here — most recently `40ab9737 "Port Mochi UX improvements to current frontend"`.
- **`frontend2/` (port 5178) is the v2 UX-rework sandbox** (`start_mochi_v2.bat`). Its UX improvements were already **ported back into `frontend/`**. Treat it as an experiment that fed the canonical app, not a second product.

Both apps already implement all three companion pages (Mochi / Peppercorn / Saffron). **Work in `frontend/` unless explicitly told otherwise.**

**Required `.env` at project root:**
```
ANTHROPIC_API_KEY=sk-ant-api03-...
TAVILY_API_KEY=tvly-dev-...
```

Install: `pip install -r requirements.txt`

**Tests:** the frontend has unit tests — `cd frontend && npm test` (Node's built-in runner over `src/**/*.test.js`: `freshness`, `feedbackBehavior`, `recommendationQuality`). The Python pipeline side has no formal test suite — validate by running pipelines and inspecting JSON output in `memory/`.

## Architecture

The architecture is a sequence of failures corrected. Each layer exists because the previous one proved insufficient. Do not remove a layer without understanding what problem it was solving.

| Layer | Purpose | Why It Exists | Maturity |
|---|---|---|---|
| Discovery | Find opportunities | Oldest layer — foundation | 80% |
| Ranking | Sort by relevance | Discovery produced too much noise | — |
| Artist DNA | Understand the artist | Generic models produced weak recommendations | 80% |
| Watercolor | Protect painters from photography flood | Visual similarity ≠ professional similarity | 75% |
| Source Purity | Distinguish real opportunities from noise | Archives/catalogs masqueraded as opportunities | 70% |
| Truth Alignment | Anchor scores to evidence | Ranking confidence drifted from reality | 70% |
| Verification | Confirm reality (site alive, submissions open) | Ranked opportunities were often unactionable | 30% |
| Reporting | Communicate findings | — | over-proliferated |
| Career | Transform opportunities into strategy | Opportunities alone ≠ career direction | 20% |
| CRM | Remember relationships | Careers are built through relationships | 5% |

**Overall maturity: 55–65%.** The project is beyond prototype, not yet production-ready.

**Highest priority unfinished system: Verification.** A perfectly ranked opportunity that is closed or unreachable is worthless.

### Active Pipeline

`run_full_mochi_pipeline.py` is the current pipeline (~101 steps in the `PIPELINE` list). It uses `smart_pipeline_runner.py` to resolve scripts across: root → `engines/` → `ui/` → `scripts/runners` → `scripts/patches`. Note: `smart_pipeline_runner.py` has no checkpoint/resume — a killed run leaves no ledger; see `project_system_audit_jul2026` memory for the resume workaround.

`council_pipeline_agent.py` is the legacy 11-step pipeline — still functional, now superseded.

### State Management

All state is JSON files under `memory/`. No database. Key files:

- `memory/opportunities.json` — master opportunity list
- `memory/contact_memory.json` — CRM / contact tracking
- `memory/artist_master_profile.json` — structured artist profile
- `memory/verified/` — quality-verified subset

### The Data Patch Rule

**Any manual fix to a JSON data file must be accompanied by a corresponding engine rule that would produce the same fix automatically on a fresh pipeline run. No exceptions.** If a data patch cannot be expressed as an engine rule, document why in `reports/patch_exceptions.md`. The goal is that **deleting all JSON files and running the pipeline from scratch should produce correct results.**

Before hand-editing a JSON file, determine whether the pipeline regenerates it:
- **Pipeline-generated (patches get overwritten — a rule is required):** `deploy_data/compact_opportunities.json`, `memory/opportunities.json`, `memory/enriched_opportunities.json`, the generated `Memory/*.json` (e.g. `career_strategy_report.json`, `exclusive_strategy_buckets.json`) and `reports/*.md`.
- **Source / app-state (hand-editing is legitimate — no rule needed):** `memory/artist_master_profile.json`, `memory/peppercorn_profile.json`, `memory/contact_memory.json`, `memory/submission_log.json`, `memory/exhibition_log.json`. But any *derived* field computed from these still needs a rule (don't patch the derived value — fix the deriving engine).

See `reports/algorithm_vs_patch_audit.md` for the worked classification of recent commits. `exclusive_primary_bucket` **is** engine-owned: `engines/exclusive_strategy_bucket_engine.py` runs in the pipeline, computes each entry's bucket via `choose_bucket()`, and writes it back onto `compact_opportunities.json`. To pin a specific entry's bucket, set its `bucket_override` field (a value in `BUCKET_ORDER`) — the engine honors it deterministically. Never hand-edit `exclusive_primary_bucket` directly; the engine overwrites it.

### Key Directories

- `engines/` — ~60 specialized reasoning engines; many pipeline steps live here
- `ui/` — Streamlit component modules for the **retired** `app.py` (legacy)
- `docs/bible/` — canonical project history and philosophy
- `docs/` — onboarding sequence, README files, pipeline docs
- `archive/dead_code/` — moved dead code (do not delete, do not modify)
- `scripts/patches/` — one-shot migration scripts (likely already run)

### Claude API Usage

Agents call Claude via the Anthropic SDK. Model calls are not cached by default — adding `cache_control` to high-frequency prompts reduces cost significantly. Most agent files include `sys.stdout.reconfigure(encoding='utf-8')` due to Windows terminal encoding requirements.

### UI

The **React `frontend/`** is production, served by `api.py`. Streamlit `app.py` is retired. Each React component carries its own CSS; the legacy `styles/generated_visual_upgrade.css` applies only to the retired `app.py`.

## UI Vision

**The north star for all future UI development is the Three Companions architecture.** Full specification: `docs/bible/Bible08.txt`. Reference mockups: `Content/ChatGPT Image May 24, 2026, 09_07_39 PM.png` and `09_07_43 PM.png`.

**Status:** the three-companion shell is now **built** in React. `frontend/` has Mochi's page (Today's Focus + opportunity sections), `PeppercornPage.jsx`, and `SaffronPage.jsx`; `frontend2/` is the v2 rework of the same. The current phase is **stabilizing and refining** these pages, not greenfield building. The spec below remains the north star — treat it as the bar the existing pages are measured against.

### The Three Companions

The system has three pages, each anchored by a companion animal. **The animals are the navigation** — clicking a companion illustration takes you to their page. There are no text tabs, no labelled buttons. Mochi's status bar persists across all three pages as the emotional anchor of the system.

| Companion | Page | Mode | Answers |
|---|---|---|---|
| **Mochi** (cat) | Action | Opportunity hunting, legwork done, ready to act | "What should I do today?" |
| **Peppercorn** (mouse) | Input | Artist goals, statement, preferences, feedback | "Is this system understanding me correctly?" |
| **Saffron** (bird) | Observatory | Market view, statistics, comparable artists, context | "What does the bigger picture look like?" |

**Mochi's status bar** persists across all three pages as the intended emotional anchor. **Current reality (2026-07-06):** the original mood panel ("Mochi is happy and full", buddy stats, sticky note) was removed as not earning its space; `StatusBar.jsx` now renders a thin accent plus a dismissable "🐾 Mochi found N new things this week" banner. Two open notes: the persistent-mood anchor described below no longer exists in code (restore-or-retire is an open product decision), and the new-opportunities banner currently sits at the *bottom* of the page where it's easy to miss — moving it near Today's Focus is queued UI work.

### Mochi — The Cat (Page 1: Action)

**Today's Focus structure — always exactly three items:**
1. **Quick Win** (5 min) — Tier 1 action. Something completable right now: a message sent, a deadline confirmed, a consignment venue checked.
2. **High Impact Move** (30-60 min) — Tier 2-3 action. The most important thing today: drafting an intro email, preparing a submission, researching an open call.
3. **Stretch Goal** (longer term) — Tier 4 action. One step toward a future target: RWS criteria research, artist statement draft, portfolio body prep.


Mochi has done the legwork while the artist was away. The pipeline has run. Opportunities are sorted. Emails are drafted. When the artist arrives, three things are ready.

- **Personality:** Watchful, patient, precise. Does not chase carelessly. Produces three options, not fifty.
- **Content:** Today's Focus (always exactly 3 actions), Immediate Best Moves (open calls + relationship targets), submission queue, next email drafts, watch list
- **Palette:** Warmest of the three — cream, amber, ochre, aged paper. The existing Mochi illustration (grey tabby, desk, art supplies) is correct.
- **Tone:** *"Mochi found three things worth your attention today."* / *"Nothing urgent. Come back tomorrow."*

This page is implemented in the React `frontend/` (Today's Focus + Immediate Best Moves + opportunity sections). The retired `app.py` was the original prototype.

### Peppercorn — The Mouse (Page 2: Reflection)

Peppercorn is a black mouse. He is where the artist's voice enters the system. Without this page the system is a monologue. He asks quiet questions and remembers the answers.

- **Personality:** Small, thorough, shy but persistent. Notices what the artist lingered on, skipped, pushed away.
- **Content:** Artist statement, monthly goals, career phase, recommendation feedback ("not this kind / more like this"), portfolio body definitions, preference review, private notes
- **Visual style:** TBD. Do not invent palettes or illustration details. Start from the character — black mouse, small, curious, private — when the time comes to design.
- **Tone:** *"Does this kind of opportunity feel right to you?"* / *"You skipped five gallery calls last month. Should I stop surfacing them?"*

This page is implemented: `frontend/src/components/PeppercornPage.jsx` (and `frontend2/src/pages/peppercorn/`). The visual-design guidance above is still the bar to refine it against — the existing styling is working, not necessarily final.

### Saffron — The Bird (Page 3: Context)

Saffron is a red or yellow bird. She sees patterns the artist cannot see from the ground. Non-interventionist. Reports without judging.

- **Personality:** Observant, patient, long-horizon. Perches and watches. Does not advise — describes.
- **Content:** Comparable artists, opportunity landscape, market context, career statistics, score trends, peer activity
- **Visual style:** TBD. Do not invent palettes or illustration details. Start from the character — red or yellow bird, perched high, wide view, observant — when the time comes to design.
- **Tone:** *"From up here, here are three artists doing similar work in Tokyo right now."* / *"TOKAS has run its open call every May for the past four years."*

This page is implemented: `frontend/src/components/SaffronPage.jsx` (and `frontend2/src/pages/saffron/`). The visual-design guidance above is still the bar to refine it against — the existing styling is working, not necessarily final.

### The Aesthetic (All Three Pages)

Warm watercolor atelier overall. The CSS design tokens from `mochi_app.py` (archived) — `--paper`, `--ink`, `--muted`, `--gold`, `--leaf`, `--rose` — are confirmed for Mochi's page. Georgia serif headings throughout. No hard edges, no cold greys, nothing that feels like a SaaS dashboard.

**Peppercorn and Saffron's visual styles are TBD.** Do not invent palettes, illustration styles, or page layouts for them. Their physical identities are fixed (black mouse; red or yellow bird). Everything else waits for a real design pass.

### What This Means for Code

- The three-companion structure supersedes the six-card single-page layout described in earlier versions of this file
- Mochi's page is the React `frontend/` (Today's Focus) — do not conflate it with the whole system
- Peppercorn is the missing feedback loop; nothing should be built that assumes the system knows the artist's preferences without it
- Saffron is the missing market context; statistics and analytics belong there, not on Mochi's action page
- The Mochi status bar persists across all three pages
- Today's Focus is always three items — the pipeline must surface exactly three actionable items, not a ranked list of fifty
- Never introduce cold blue/grey colour schemes, dense tables, or aggressive CTAs on any of the three pages
- Empty states get warm copy and a small illustration, not "No data found"

## Career Strategy Framework

GEGYjiji's career is structured in four tiers. **Her current phase is computed dynamically** from her real record and lives in `memory/career_strategy_report.json` (`current_phase`, `readiness_scores`) — as of 2026-07-06 that is **Tier 3 established, building toward Tier 4** (evidence: 8 confirmed group shows, 2 solo shows, an institutional show, an international show, 2 publications; tier_3_readiness = 1.0, tier_4_readiness = 0.85). **Do not hardcode her tier** — engines that surface "what to do today" should read the report so scoring tracks her real progress. (This corrects an earlier hardcoded "Tier 1-2" that predated her exhibition record being entered.)

| Tier | Label | What It Is | Status (computed) |
|---|---|---|---|
| **1** | Ambient Visibility | Zine shops, bookshop consignment, café prints, art book fairs, self-publishing. Low-barrier presence-building — work enters circulation without requiring pitching. | **Established** |
| **2** | Networking | Group shows, artist-run spaces, open calls at accessible Tokyo galleries, community events. Active relationship-building with the people who will matter in 3-5 years. | **Established** |
| **3** | Credibility | Small institutional shows (TOKAS, BankART1929, Youkobo), juried open calls (Jinny Street, Belladonna, Shoto Museum), Japan Watercolor Society. CV weight. | **Established (100% readiness)** |
| **4** | Prestige Targets | Royal Watercolour Society, American Watercolor Society, Cité Internationale des Arts, Asian Cultural Council, Printed Matter, Offprint. For the deep-work year at 30 and beyond. | Building toward (85% readiness) |

**Scoring rule:** opportunity fit to her current level is a gentle re-rank term, not a hard multiplier. Tiers 1-2 are always fully in reach (level-fit 1.0); Tier 3/4 fit *rises* with her readiness — `_level_fit` in `api.py` maps to roughly **[0.85, 1.15]×** (0.85 + 0.30·fit), so level-appropriate opportunities lift and stretch ones sink without hiding anything. (This replaced an older hard ×1.3–1.4 multiplier — the "Saffron hybrid reframe.") Tier 4 entries are always routed to `stretch_targets` — they must **never** appear in Immediate Best Moves / Today's Focus. Tier 4 exists to be tracked and prepared for, not acted on now.

**Why this matters for code:** Any engine that surfaces "what to do today" must respect the current phase. Recommending an RWS open exhibition to a 26-year-old building her first exhibition history is worse than useless — it sets the wrong expectation and wastes attention. The tier framework is the primary guard against this.

The full tier definitions live in `memory/artist_master_profile.json` under `career_strategy`.

## Critical Lessons (Do Not Repeat)

- **More opportunities ≠ more value.** 3 excellent > 100 mediocre. Don't optimize for volume.
- **Photography floods painting.** Visual/thematic similarity between watercolor and photography is real but the professional ecosystems are entirely separate. The Watercolor Layer exists to enforce this. Do not weaken it.
- **Score inflation is real.** The system has repeatedly grown more confident while growing less accurate. Evidence must outweigh prediction.
- **Reports multiply faster than insight.** Do not add a report unless it solves a specific problem. Do not measure progress by report count.
- **Verification > ranking.** Always. A closed opportunity with a perfect score is useless.
- **Actionability is the product.** Every feature should be evaluated against: "Does this help the artist decide what to do next?" If no, it's probably unnecessary.

## Artist Social Media

- Instagram: @gegyjiji — https://www.instagram.com/gegyjiji/ (~26k followers, daily watercolor diary)
- Twitter/X account exists (@GegYjiji, ~90k followers) but do NOT reference in outreach emails. Instagram only. (The ~90k figure is Twitter, NOT Instagram — a longstanding mix-up; Instagram is ~26k.)

## Development Posture

The current phase is **consolidation, not expansion.** The roadmap priority order is:

1. Audit (done)
2. Stabilize
3. Improve verification
4. Improve submission discovery
5. Build CRM
6. Build artist career operating system

Do not add features, new scoring layers, or new reports until stabilization is complete.
