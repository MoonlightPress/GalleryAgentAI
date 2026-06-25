# Backend API diagnostic — `api.py` + engines

_Read-only review, 2026-06-25. No code changed. Scope: `api.py` (FastAPI) and the
engines it imports (`regen.py`, `profile_sync.py`, `backups.py`, `visit_tracking.py`,
`notify.py`, `ibm_email_writer.py`). Tests run; no paid steps, no SSH._

`python -c "import api"` succeeds. Test suite: **115 pass / 3 fail** (`python -m
unittest discover -s tests`, 118 total) — the 3 failures are the known pre-existing
`deadline_normaliser` / `targeted_verification_agent` ones, root-caused below (G1).

---

## CRITICAL

**(none that crash the live app in normal use.)** The headline risk is data integrity,
not a 500 — see H1/H2. Listed by realistic severity below.

---

## HIGH

### H1 — Most GET endpoints still do a raw `json.loads()` that 500s on a corrupt/half-written file
The crash-safe `_load_json()` helper (api.py:57) is used by only ~8 readers. **~40 call
sites still do `json.loads(path.read_text(...))` directly** and will raise (→ 500) if the
file is mid-write or truncated. The "api.py guards every file read" note in
CURRENT_STATE.md is now **stale** — it's half-true.
- Evidence (GET readers that 500 on a corrupt file):
  `/api/submissions` api.py:1152; `/api/contacts/update` :1304; `/api/contacts/{name}` :1337;
  `/api/contacts/lookup` :1363; `/api/career_events` :2839; `/api/exhibition_log` :2891;
  `/api/issues` :3222; `/api/today` :3058, :3100; and the whole `/api/saffron` body
  (:1387, :1476, :1545, :2089, :2678, :2690, :2720). `_load_suppressed` :155 and
  `_load_suppressed_categories` :162 feed `/api/opportunities`, so a corrupt
  `suppressed_opportunities.json` 500s the **main** board.
- One-line fix: route every `json.loads(p.read_text())` through `_load_json(p, default)`
  (it already exists and is the intended guard).

### H2 — Every write is non-atomic, and the per-edit backup is taken *after* the write
No write path uses temp-file + `os.replace`. `_save_her_data` (api.py:110) does
`path.write_text(...)` then `snapshot(...)`. If the process dies mid-`write_text`
(deploy restart, kill, disk-full), the live file is left truncated **and** the next
backup snapshots the already-corrupt file. Combined with H1, a single interrupted save
can both corrupt her data and 500 the page that reads it.
- Evidence: api.py:115-116 (write-then-backup, no temp file); `grep` for
  `os.replace|NamedTemporaryFile|.tmp` in api.py / backups.py → none.
- One-line fix: write to `path.with_suffix(".tmp")`, `os.replace()` into place, and take
  the backup of the *previous* good file before overwriting (or snapshot before write).

### H3 — Concurrent-edit clobber on the shared profile / log files (read-modify-write, no locking)
`POST /api/peppercorn` (api.py:2757) reads `artist_master_profile.json` (:2771),
mutates, writes. `POST /api/saffron_answer` (:2787), `/api/membership` (:2920),
`/api/career_events` (:2843), `/api/contacts*` (:1253/1300/1332) all do the same
read-modify-write on shared files with no lock. Two near-simultaneous requests = last
writer wins, the other edit is silently lost. Single-user app so low *probability*, but
`/api/event` fires a beacon on every nav and the regen subprocess also rewrites
`compact_opportunities.json` — interleaving is possible.
- Evidence: api.py:2771-2774 (peppercorn read→write), 2920-2940 (membership),
  2843-2852 (career_events); writer rewrite api.py-spawned `ibm_email_writer.py:310`.
- One-line fix: serialize her-data writes behind a single `threading.Lock` (or an
  `asyncio.Lock`) around the read-modify-write block.

### H4 — Pre-existing test failures are real spec/impl drift, not flaky
The 3 failing tests assert a **venue-exemption** rule that was specced and tested but
never implemented in the engines:
- `classify_deadline()` (deadline_normaliser.py:128) has **no `category` parameter**;
  the tests call it with `category=...` → `TypeError` (test_deadline_normaliser.py:104,110).
- `_deadline_is_real()` (targeted_verification_agent.py:81) doesn't exempt relationship
  categories, so a past-dated `bookstore_gallery` returns False where the test expects
  True (test_targeted_verification_agent.py:23).
- Impact on the live app: **none today** — api.py implements the exemption itself via
  `_RELATIONSHIP_CATS` + `_deadline_passed`/`shape_card` (api.py:265, 800-849, 696). So
  the serving layer is correct; the *pipeline* engines lag. The failures are a latent
  data-quality gap (a past-dated consignment venue can get wrongly demoted at pipeline
  time), not a crash.
- One-line fix: add a `category=None` param to `classify_deadline` and a relationship-cat
  early-return to `_deadline_is_real`, mirroring api.py's `_RELATIONSHIP_CATS`.

---

## MEDIUM

### M1 — `POST /api/feedback` is the one her-data writer that does NOT use `_save_her_data` (no backup)
It writes `feedback.json`, `suppressed_opportunities.json`, and **auto-creates
submission-log entries** with raw `write_text` and raw `json.loads` reads (api.py:1009,
1020, 1026, 1047, 1068). So the "Applied" action mutates her submission log with neither
the crash-safe read nor the timestamped backup that every other her-edit path now has.
- One-line fix: read via `_load_json`, write via `_save_her_data(SUBMISSIONS_PATH, ...)`.

### M2 — `suppress_category` and the contact POST/PATCH writers bypass the backup helper too
`/api/feedback/suppress-category` (api.py:1137) and `/api/contacts` add/update/patch
(api.py:1288, 1320, 1355) write with raw `write_text`, not `_save_her_data` — no backup,
non-atomic. Inconsistent with the durability story those backups were added for.
- One-line fix: route through `_save_her_data`.

### M3 — Regen can run only if the box has `anthropic` + a key; failure is silent-by-design but unobservable
`spawn_draft_regen` (regen.py:31) always returns the spawn result, not the run result —
`regen_started: true` only means the subprocess launched. The child
(`ibm_email_writer.py`) `sys.exit(1)` if `ANTHROPIC_API_KEY` is missing (writer:251-253)
and the only trace is `reports/regen_last_run.log`. CURRENT_STATE notes server regen is
"NOT yet exercised by a real edit; verify" — confirmed: there is **no readback** to the
API or UI of whether the regen actually wrote drafts. A keyless box looks identical to a
success from the response.
- Edge: the writer clears `email_drafts_stale` only on `errors == 0` (writer:315). A
  partial failure correctly leaves it stale — good. But if the spawn *itself* fails
  (no `python`, bad cwd), `email_drafts_stale` stays True forever and every subsequent
  edit re-spawns a doomed full re-targeting run.
- One-line fix: surface the tail of `regen_last_run.log` (or a `last_regen_status.json`)
  on a health/status endpoint so a silent keyless failure is visible.

### M4 — Regen rewrites the exact 2.7MB file the API caches, non-atomically
`ibm_email_writer.py:310` does a full non-atomic `json.dumps` rewrite of
`deploy_data/compact_opportunities.json`. The API caches that file by mtime
(`load_opportunities`, api.py:872-881) and re-reads on mtime change. A request landing
mid-rewrite → `_load_json` returns `[]` → the board momentarily serves **empty** (or, for
the raw-`json.loads` saffron path at :1476/:2461, a 500). Self-heals next request, but the
window is real on a slow disk.
- One-line fix: writer should write `.tmp` + `os.replace` (also fixes H2 for this file).

### M5 — `ibm_email_writer.py` uses cwd-relative paths
`OPP_PATH = Path("deploy_data/...")`, `PROFILE_PATH = Path("memory/...")`
(writer:29-30). Works only because the API passes `cwd=Path(__file__).parent`
(api.py:2778). Any other caller (cron, manual run from another dir, a future scheduler)
silently reads/writes the wrong (or empty) files. Brittle coupling.
- One-line fix: anchor to `Path(__file__).resolve().parent.parent` like api.py does.

### M6 — `webhook_deploy` runs `bash deploy_from_git.sh` on push; signature check is **skipped entirely if the secret env var is unset**
api.py:3240-3251: if `MOCHI_WEBHOOK_SECRET` is empty, the `X-Hub-Signature-256` check is
bypassed and **any** unauthenticated POST with `X-GitHub-Event: push` triggers a deploy
shell script (RCE-adjacent — it runs whatever `deploy_from_git.sh` pulls). The HMAC path
itself is correct (constant-time `compare_digest`, api.py:3246), but "no secret ⇒ no
auth" is fail-open.
- Evidence: api.py:3233 (`WEBHOOK_SECRET = os.environ.get(..., "")`), 3243 (`if
  WEBHOOK_SECRET:` guards the whole check).
- One-line fix: if `WEBHOOK_SECRET` is empty, **reject** the webhook (403) instead of
  deploying; require the secret to be set in prod.

---

## LOW

### L1 — CORS allow-list has no production origin
api.py:36-40 lists only `localhost`/`127.0.0.1:517x`. Prod is
`twilightdreamworks.com/mochi`. This works today only because nginx serves the React app
and the API same-origin (the browser never sends a cross-origin XHR), so CORS never
engages. If the frontend is ever served from a different host, every call breaks. Low risk
because `allow_credentials` is unset (default False), so no credential exposure.
- One-line fix: add the prod origin to `allow_origins` (or document the same-origin
  assumption).

### L2 — `market_stats` score tiers double-count the boundary
api.py:2545-2546: `top_tier = score > 8`, `mid_tier = 5 <= score <= 8`. A score of exactly
8 lands in mid (fine), but the labels imply `>8 / 5-8 / <5` which is self-consistent — no
gap or overlap actually. **Re-checked: not a bug.** Noted only to record it was inspected.

### L3 — `_load_json` default is `None`, and a few `_load_json` callers then call `.get`/iterate
`/api/tracker` (api.py:2950-2956) does `_load_json(DATA_DIR/"feedback.json", [])` — passes
a default, safe. But `/api/saffron` `_load_json(_pp_path, {})` etc. all pass defaults too,
so this is currently fine. The risk is future callers copying `_load_json(path)` with no
default and then `.get()`-ing `None`. Cosmetic/defensive.
- One-line fix: make the `default` parameter required, or default it to `{}`.

### L4 — `/api/career_strategy` 404s instead of degrading
api.py:3254-3259 raises 404 if `career_strategy_report.json` is absent. Every other reader
degrades to an empty default. Minor inconsistency; the report is regenerated by
`_refresh_career_strategy` on most her-edits so it usually exists.
- One-line fix: return `_load_json(path, {})` with a `generated: false` flag instead of 404.

---

## What is actually solid (verified, not flagged)
- `_load_json` (api.py:57), `backups.snapshot` (backups.py:27), `notify_discord`
  (notify.py:48), `visit_tracking` (register/describe) all correctly swallow errors and
  never raise — the engine helpers are well-built.
- `/api/event` page keys (`discover`/`observe`/`refine`) match `PAGE_LABELS`
  (visit_tracking.py:13) — the telemetry feed is consistent end-to-end.
- The webhook HMAC comparison uses constant-time `compare_digest` (api.py:3246) — correct
  when the secret IS set (see M6 for the fail-open caveat).
- `profile_sync.apply_peppercorn_edits` correctly treats an empty statement as "no edit"
  (profile_sync.py:27-29), so clearing the box can't wipe her real statement.
- The serving layer's deadline/relationship-venue handling (`_deadline_passed`,
  `_RELATIONSHIP_CATS`, `shape_card`) is correct and is why H4's engine drift doesn't
  reach the UI.

---

## Priority order to fix
1. **H1 + H2** together (route GET readers through `_load_json`; make `_save_her_data`
   atomic + back up the prior good file) — kills the corrupt-file-→-500 and the
   corrupt-write-→-lost-data class in one pass.
2. **M6** — close the fail-open webhook (reject when no secret).
3. **H3 / M1 / M2** — one write-lock + route the stragglers through `_save_her_data`.
4. **M3 / M4 / M5** — make regen observable + atomic + cwd-independent.
5. **H4** — implement the venue exemption in the two pipeline engines so the 3 tests pass.
