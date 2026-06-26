# Usage Recording + Session Digests — Design

- **Date:** 2026-06-26
- **Status:** Approved direction, pending spec review
- **Owner:** Mochi / GalleryAgentAI
- **Topic:** See how the artist navigates the app and what kinds of things she interacts with, without flooding Discord.

## Problem

The Discord feed shows almost nothing. Today the frontend already beacons `/api/event`
on every page move, but the backend (`api.py:track_event`) **drops everything except the
`open` event** and pings Discord once when she loads the app. Navigation between pages is
discarded; interactions (follow, apply, hide, card-open, profile edits) are never even
emitted. The system was deliberately narrowed to a single daily "she opened it" ping, and
`engines/visit_tracking.py` is documented as **content-blind** — "records THAT she visited,
never what she looks at."

Scott wants to **watch how she moves through the app live**, and to see **what kinds of things
pull her attention** — but without a flood of per-interaction pings. Navigation should stream
live; interaction detail should arrive as a single wrap-up once she's done.

## Goals

- Keep the existing **live "she's here" ping** when she loads the app (once per visit).
- Post **navigation live** — both the three companion pages (Home / Saffron / Peppercorn)
  **and** the section headers she engages with inside a page (Today's Focus, Immediate Best
  Moves, People, Saffron's tabs, …) — as she moves, so the session can be watched in near-real
  time. Debounced so only genuine landings (≥2s), not scroll-throughs, post.
- Capture **interactions** — follows, applies, hides/"not this", card-opens, profile saves —
  tagged by **category/type only** (zine, gallery, residency, …), **never the named
  opportunity**.
- Deliver the **interaction wrap-up** as **one consolidated digest per visit**, posted
  **~10 minutes after she goes idle** (the session looks done): what she acted on, by type,
  plus where she spent the most time. The navigation itself already went out live; the digest
  is the "what did she do" summary, not a replay of her moves.

## Non-Goals

- No per-*interaction* real-time pings — each follow/apply/hide/card-open does **not** ping
  live; those are batched into the idle digest. (Navigation moves *do* post live, but debounced
  to genuine landings so they're meaningful moves, not the per-scroll flood.)
- No naming of specific opportunities in any message (privacy line Scott chose).
- No in-app analytics page, charts, or dashboard. Discord is the only surface.
- No weekly roll-up (considered, dropped in favour of per-session digests).
- No PII. The only identifier is the existing anonymous `visitor_id` (random UUID in
  `localStorage`).

## Locked Decisions

| Question | Decision |
|---|---|
| Where data surfaces | Discord only |
| Live open ping | Keep, unchanged (once per app load) |
| Navigation delivery | **Live** — companion + section moves posted as they happen |
| Nav granularity | Companion pages **and** within-page section headers |
| Nav noise control | Section pings debounced to genuine landings (≥2s); no per-scroll spam |
| Interaction detail | Category + counts only; never the named opportunity |
| Interaction digest | One per session, flushed ~10 min after last activity |
| Flush mechanism | Backend daemon-thread ticker (reliable when she just closes the tab) |
| Idle threshold | 10 minutes (config constant) |

## Architecture

Three parts: **capture** (frontend → `/api/event`), **durable log** (`usage_events.jsonl`),
and **flush** (backend ticker → interaction digest → Discord). Two kinds of event post to
Discord **live** as they happen — the open ping and every navigation move (companion + section);
the interaction digest is the only delayed message. Every event is also logged.

### 1. Event model

All events POST to the existing `/api/event` endpoint as JSON. Three shapes:

```jsonc
// session start — already sent today; keep firing the live ping AND log it
{ "type": "open", "page": "discover", "visitor_id": "<uuid>" }

// navigation — already sent today but currently DROPPED; now posts LIVE to Discord + logged.
// `section` is new and optional: present for within-page section/tab moves (debounced).
{ "type": "nav", "page": "observe", "from": "discover", "section": "landscape" }

// interaction — NEW; frontend does not emit these yet.
// `category` is the opportunity TYPE, never its name. Omitted where N/A (e.g. profile save).
{ "type": "action", "action": "follow", "category": "zine", "visitor_id": "<uuid>" }
```

`action` values (v1 set): `follow`, `unfollow`, `apply`, `hide` ("not this"/suppress),
`open_card` (expand an opportunity), `profile_save` (Peppercorn), `saffron_answer`.

Every logged event is stamped server-side with `ts` (UTC ISO) and `visitor_id` (carried from
the client, or the most recent open's id within the session) so the flusher can group by
visitor and order by time. Server receive-time is the source of truth for dwell/ordering —
clients send no timestamps.

### 2. Capture — frontend (`frontend/src/`)

- **Companion nav:** already emitted in `App.jsx` (the `nav` beacon). No change to emission;
  the change is purely that the backend stops discarding it.
- **Section headers (within-page):** an `IntersectionObserver` watches each major section's
  container on the discover page (Today's Focus, Open Calls / `OpportunitiesSection`, People /
  `RelationshipTargets`, etc.). A section counts as "viewed" when it is ≥50% visible for ≥2s;
  fire one `nav` event `{page:'discover', section:<key>}` per entry, deduping consecutive
  repeats so scrolling past doesn't spam. Saffron/Peppercorn tab switches are state changes —
  emit the same `nav` shape `{page, section:<tab>}` directly from the tab handler (no observer
  needed).
- **Interactions:** add a tiny shared helper `track(action, {category})` in
  `frontend/src/` (thin wrapper over the same `fetch('/api/event', {keepalive:true})` the nav
  beacon already uses). Call it at the ~5 interaction handlers — follow/unfollow toggle, mark
  Applied, hide/"not this", card expand, profile/answer save. Exact handler locations are
  identified during planning. All calls are best-effort and never block or throw into the UI.

### 3. Durable log (`memory/usage_events.jsonl`)

Append-only, one JSON object per line. Append (not read-modify-write) so concurrent writes
never clobber, and the buffer survives a backend restart. Volume is tiny (a few visits/week).
Lives next to `visit_log.json` under `DATA_DIR` (`memory/`).

A small per-visitor flush marker is kept in the existing `visit_log.json` (e.g.
`last_digest_ts` per `visitor_id`) so a session is reported **exactly once** and a restart
can't double-post.

### 4. Flush — backend ticker + report builder

- **Ticker:** a daemon thread started at FastAPI startup. Wakes every `TICK_SECONDS` (60s),
  reads the event log, groups events by `visitor_id`, and finds the latest session whose last
  event is older than `IDLE_MINUTES` (10) and whose end-time is newer than that visitor's
  `last_digest_ts`. For each such session it builds a digest, posts it via `notify_discord`,
  and advances `last_digest_ts`. A daemon thread (not asyncio) keeps the blocking
  `requests.post` in `notify_discord` simple and isolated. Any exception is swallowed and
  logged — the ticker must never crash the API.
- **Report builder:** a new pure module `engines/usage_report.py`, structured like
  `visit_tracking.py` (no I/O, no network — fully unit-testable). The digest is the
  **interaction wrap-up**. Given a list of events for one session it computes:
  - **interaction counts** by `action` and by `category` (the primary content)
  - **dwell** per page/section from consecutive timestamps → "most time on X"
  - a brief one-line **flow recap** (the moves already went out live; this is just context)
  - session duration and a returning/new + day-number header
  and formats the Discord message string.

A session boundary = a gap > `IDLE_MINUTES` between consecutive events for a visitor (same
threshold as the flush trigger, so "the session that just went idle" and "the session in the
digest" are the same run).

### 5. Live pings — open + navigation (`track_event`)

`track_event` posts live for **two** event types and logs all three:

- `open` → keep current behaviour: register the visit, mark new/returning, and
  `notify_discord` the "📊 … opened Mochi … on <page>" line immediately.
- `nav` → `notify_discord` the move immediately. `describe_event` already formats nav as
  `Home → People`; extend it to append the section when present (e.g. `Saffron → Landscape`).
  The client-side debounce ensures these are genuine landings, not scroll spam.
- `action` → log only, no live ping (these are summarised in the delayed digest).

The open ping only fires once per app load, so it stays low-volume. The current code ignores
the once-per-day `_notify` flag and pings on every open — fine here. The digest keys off the
**log**, not these live pings, so nothing is double-reported.

### Example — what lands in Discord

**Live, as she moves** (each a separate message; section pings debounced to real landings):

```
📊 A returning visitor opened Mochi · day 4 · on Home
Home → Today's Focus
Today's Focus → People
People → Saffron
Saffron → Landscape
Saffron → Money
```

**Then ~10 min after she stops, one digest** (interactions, not a replay of the moves):

```
🧵 Session wrap-up — returning · day 4 · ~7 min
most time on: Saffron
followed 2 (1 zine, 1 gallery) · applied 1 (art book fair) · hid 1 (watercolour soc) · opened 4 cards
flow: Home → People → Saffron (Landscape, Money)
```

## Components & Interfaces

| Unit | Responsibility | Depends on |
|---|---|---|
| `frontend/src/App.jsx` (nav beacon) | emit `open` + `nav` (companion). Already exists. | `/api/event` |
| `frontend` `track()` helper + observers | emit within-page `nav` (sections/tabs) and `action` events | `/api/event` |
| `POST /api/event` (`api.py`) | live ping for `open` + `nav`; append every event to log | `notify`, `visit_tracking`, log file |
| `memory/usage_events.jsonl` | durable append-only event stream | — |
| ticker thread (`api.py` startup) | flush idle sessions exactly once | log file, `usage_report`, `notify`, `visit_log.json` |
| `engines/usage_report.py` (new, pure) | reconstruct a session + format digest | — |
| `engines/notify.py` | post to Discord | env webhook |
| `engines/visit_tracking.py` | open-ping wording + new/returning + day count | — |

## Data Flow

1. She loads the app → `open` → live ping fires **and** event appended to log.
2. She moves around → `nav` (companion + section) → posts **live** **and** appended to log;
   `action` events (follow/apply/hide/card-open/save) → appended to log only, no live ping.
3. She stops. ~10 min later the ticker sees the session idle → builds the interaction digest →
   posts once → stamps `last_digest_ts`.

## Error Handling

- All frontend emits are best-effort (`keepalive`, `.catch(()=>{})`); never block the UI.
- `/api/event` log append is wrapped; a failure returns `{ok:true}` and is silently dropped —
  tracking must never fail the page.
- Ticker catches all exceptions per tick; a bad tick is logged and the loop continues.
- `notify_discord` is already a safe no-op when `MOCHI_DISCORD_WEBHOOK` is unset.

## Privacy Posture

The system moves from strictly content-blind to **flow-and-category aware, still name-blind**:
it records which pages/sections she engages and the *types* of opportunities she acts on,
never the specific named opportunity. `engines/visit_tracking.py`'s module docstring (and the
`/api/event` comment) must be updated to state this new posture explicitly, so it doesn't read
as a regression of the documented "content-blind" intent.

## Config Knobs (constants, easily changed)

- `IDLE_MINUTES = 10` — idle gap that ends a session / triggers flush.
- `TICK_SECONDS = 60` — ticker wake interval.
- `SECTION_DWELL_MS = 2000`, `SECTION_VISIBLE_RATIO = 0.5` — section-view debounce.

## Testing

- `engines/usage_report.py`: unit tests (Python) over crafted event lists — flow ordering,
  dwell/most-time-on, session splitting on the idle gap, category/count rollups, empty/odd
  inputs degrade safely. Mirrors `tests/test_visit_tracking.py`.
- Flush dedup: a session is digested once; a second tick over the same events posts nothing.
- `notify_discord` is already injectable (`poster=`) for assert-without-network.
- Frontend: the `track()` helper is best-effort and side-effect-only; covered by a light unit
  test that it posts the expected shape and swallows errors.

## Out of Scope / Future

- On-demand `GET /api/usage_report` endpoint (easy add later; not needed for v1).
- Guaranteed delivery via deploy cron if she's away for long stretches (the builder is already
  a pure function the existing cron could call).
- Named-opportunity detail or an in-app analytics view — only if Scott later wants to cross
  those lines.
