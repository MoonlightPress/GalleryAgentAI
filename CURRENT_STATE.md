# CURRENT_STATE.md — single source of truth

**Read this first.** `CLAUDE.md` and `AGENTS.md` cover the durable *why* of the project; this file
covers the volatile *what's true right now*. When the two disagree, this file wins —
and whoever notices the drift should fix it here. Keep this file short.

_Last updated: 2026-06-19_

## The live app

- **Frontend:** React (Vite) in **`frontend/`** → http://localhost:5177
- **Backend:** **`api.py`** (FastAPI/uvicorn) → http://127.0.0.1:8001 (Vite proxies `/api` → :8001)
- **Launch both:** `start_mochi.bat`
- Streamlit **`app.py` is retired** — reference only, not the product. (`launch_mochi.bat` still
  opens it; ignore that launcher.)

## Which frontend is current — IMPORTANT

There are two React apps. This is the thing that has caused confusion:

- **`frontend/` (port 5177) is the canonical, current frontend.** Do all work here unless told otherwise.
- **`frontend2/` (port 5178) is the v2 UX-rework sandbox** (`start_mochi_v2.bat`). Its UX improvements
  were already **ported back into `frontend/`** (commit `40ab9737`, 2026-06-18). Treat it as a finished
  experiment that fed the canonical app, not a second product.

Both apps implement all three companion pages (Mochi / Peppercorn / Saffron).

## Tests

- Frontend: `cd frontend && npm test` (Node's built-in test runner over `src/**/*.test.js`).
- Python pipeline: no formal suite — validate by running the pipeline and inspecting `memory/` JSON.

## Recent completed work

- **Read-only readiness honesty audit** (Codex, 2026-06-19; scope commit `2b522695`): audited all
  380 cached opportunities in `deploy_data/compact_opportunities.json` with `assess_actionability`.
  No ready-status leaks and no strongest-picks leaks were found for URL error/bad/missing,
  closed/permanently closed, or non-relationship `deadline_past` conditions. Distribution:
  `ready=99`, `check_before_acting=67`, `review=130`, `closed_or_stale=84`. Native-medium unknown is
  `224/380` (`58.9%`), limiting artist-fit quality until medium tagging is improved. No generated JSON
  edits, no live web/Tavily checks, no paid pipeline run.
- **Backend readiness contract** (Codex, 2026-06-19; commit `50e0bfd7`): added tested backend
  `actionability_status`, `review_flags`, and `recommendation_reasons` shaping via
  `recommendation_readiness.py`; `api.py` now emits these fields and the current `frontend/` consumes
  them instead of treating browser heuristics as canonical. Browse strongest picks now keeps 6
  candidates for curated breadth. No generated JSON edits, no live web/Tavily checks, no `frontend2/`,
  no retired Streamlit.
- **Photography surfacing fix** (Codex, 2026-06-19): pure photography opportunities are blocked at
  the current app API boundary and rejected by the future bucket engine rule. This fixes cached
  `photo_open_call` / `native_medium: photography` rows appearing in the watch list for a watercolor
  painter. No generated JSON edits, no live web/Tavily checks, no `frontend2/`, no retired Streamlit.
- **Read-only strongest-picks audit** (Codex, 2026-06-19; scope commit `c1cb5cad`): inspected
  existing `/api/opportunities`, `deploy_data/compact_opportunities.json`, and the current frontend
  helper only. No generated JSON edits, no live web/Tavily checks, no paid pipeline run. Main finding:
  current strongest picks mostly satisfy cached readiness signals, but backend readiness fields are
  still needed because the frontend helper can treat contact-verified `needs_reverification` items as
  ready and because browse breadth must label/order uncertain items rather than delete them.
- **Mochi recommendation quality pass** (Codex, 2026-06-19): `frontend/src/utils/recommendationQuality.js`
  and `recommendationQuality.test.js` are complete. Mochi now derives internal readiness/fit signals,
  surfaces a small "strongest picks" band, sorts section cards through that quality layer, and lets
  feedback influence the current board without showing numeric scores to the artist.

## In flight (work not finished — don't assume it's done)

- **Read-only verification-layer audit** (Codex, 2026-06-19): inventory verification scripts/engines,
  map pipeline wiring and written fields, confirm non-ok URL quarantine under readiness/strongest-picks,
  and recommend one canonical verification path. Cached data/code inspection only: no Tavily/live web,
  no paid pipeline run, no generated JSON edits, no `frontend2/`, no retired Streamlit, no CRM/contact
  work. If later hardening is needed, it will be a separate tests-first scope.

## Working together (Claude + Codex)

- Both agents read their own guide (`CLAUDE.md` / `AGENTS.md`) **plus this file**. This file is the
  shared handshake — update it when something material changes (which frontend is current, how to run,
  what's mid-build) so neither agent re-derives stale state from scratch.
- Don't develop the same feature in both `frontend/` and `frontend2/`. `frontend/` is the one.
- Before making non-trivial changes, record the intended scope here if it could affect another agent's
  work. Keep notes short but concrete: active files, why the work is in-bounds, and how it will be
  verified. When the work finishes, move the note to Recent completed work with the commit hash.
- Project-boundary checks should reference this file plus `AGENTS.md` / `CLAUDE.md`: current live app,
  retired Streamlit status, the data patch rule, consolidation-over-expansion posture, and the rule
  that `frontend2/` is a sandbox, not a second product.
