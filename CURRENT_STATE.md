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

## In flight (work not finished — don't assume it's done)

- **`frontend/src/utils/recommendationQuality.test.js`** (Codex, TDD red test): imports a
  `recommendationQuality.js` that does **not exist yet**. The test suite currently shows 1 failure
  for this reason. The implementation still needs to be written. Until then, this file is intentionally
  uncommitted.

## Working together (Claude + Codex)

- Both agents read their own guide (`CLAUDE.md` / `AGENTS.md`) **plus this file**. This file is the
  shared handshake — update it when something material changes (which frontend is current, how to run,
  what's mid-build) so neither agent re-derives stale state from scratch.
- Don't develop the same feature in both `frontend/` and `frontend2/`. `frontend/` is the one.
