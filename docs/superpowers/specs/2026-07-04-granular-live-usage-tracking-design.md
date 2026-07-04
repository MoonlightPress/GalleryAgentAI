# Granular Live Usage Tracking — Design

- **Date:** 2026-07-04
- **Status:** Approved direction, pending spec review
- **Owner:** Mochi / GalleryAgentAI
- **Topic:** Extend the June 26 usage-analytics build (`docs/superpowers/specs/2026-06-26-usage-analytics-design.md`) with finer-grained click/dwell/exit detail, delivered live, plus better bot classification.

## Problem

The June 26 build gave live nav pings (companion + section moves) and a single idle-session
digest with duration, most-time-on-page, and interaction counts by category. That's a real
improvement but still leaves gaps:

- Only ~6 hand-picked actions fire a tracking event (`follow`/`unfollow`/`apply`/`hide`/
  `open_card`/`profile_save`/`saffron_answer`). Plenty of interactive UI — filters/sort,
  external link click-through, watch-list toggles, Peppercorn goal/portfolio edits,
  exhibition-log entries — isn't wired up at all.
- Interaction detail only ever arrives batched in the idle digest, ~10 minutes after the
  fact. There's no way to watch what she's doing as she does it.
- Dwell time is inferred server-side from gaps between consecutive events. The final page
  she was on before closing the tab has no real end-time — it's simply invisible.
- The bot/device classification (`_classify_client`) is computed only to decorate the
  Discord message text and is thrown away — never stored, never usable later.
- The `visitor_id` itself is under-explained: it's a random UUID a browser generates once
  and keeps in `localStorage`. Seeing the same ID from two different geos in one day (the
  Korea → Tokyo case) almost always means the same physical browser changed networks
  (VPN, roaming, travel) — not a different person — but nothing today makes that
  reasoning available to a reader of the feed.

## Goals

- Expand the set of curated actions tracked so "what she clicks" covers meaningfully more
  of the app, not just follow/apply/hide/card-open.
- Post **every** tracked action live to Discord as it happens (not batched into the
  digest). Keep the existing idle-session digest too, as a short recap bookend.
- Add a `leave` event fired on tab hide/close so dwell time — including the last page
  before she closes the tab — is real, client-measured time, not a server-side inference.
- Persist the bot/device classification onto every logged event (not just Discord text),
  and strengthen it with a hosting/proxy/datacenter signal from the geo lookup, so bots
  that don't self-identify via User-Agent are still catchable.

## Non-Goals

- **No dashboard this round.** Discord stays the only surface. Revisit only if the
  channel becomes too noisy to read.
- **No cross-session geo-change auto-flagging.** The Korea/Tokyo pattern is not detected
  or annotated automatically — geo shows per-event exactly as it does today. A human
  reading the feed draws that conclusion themselves.
- **No "her vs. a friend on her device" identification.** There is no login system, and
  building one solely for this would be new infrastructure beyond what was asked for.
  `visitor_id` remains an anonymous per-browser marker. The identity improvement in scope
  is better bot/hosting detection, not human identity discrimination.
- No naming of specific opportunities in any message (unchanged from June 26).
- No PII beyond what's already logged (IP, UA, geo label — unchanged posture).

## Architecture

Builds directly on the June 26 pipeline (frontend `track()` → `POST /api/event` →
`usage_events.jsonl` → live Discord ping + idle-session digest). Three additions:

### 1. Expanded action set

New `action` values added to the v1 set (`follow`, `unfollow`, `apply`, `hide`,
`open_card`, `profile_save`, `saffron_answer`):

- `filter_change` / `sort_change` — `category` carries the filter/sort key, not a value
  (e.g. `"deadline"`, `"tier"`), consistent with the existing never-log-specifics posture.
- `external_link_click` — she opened the actual opportunity URL (`OppCard.jsx:280`,
  currently untracked). Strong signal, no destination URL logged, only `category`.
- `watchlist_add` / `watchlist_remove`.
- Peppercorn: goal edit, portfolio-body edit, preference-review answer (extending the
  existing `profile_save`/`saffron_answer` pattern to a couple more Peppercorn actions).
- `exhibition_log_add`.

Exact call sites (`OpportunitiesSection.jsx`, `RelationshipTargets.jsx`,
`OppDetailPanel.jsx`, `DeadlineCalendar.jsx`, `PeppercornPage.jsx`) get identified and
wired during planning — this list defines *what* gets tracked, not the literal diff.
Kept as curated, hand-wired `track()` calls (matching the existing pattern) rather than a
generic delegated click listener, so labels stay precise and intentional.

### 2. `leave` event — real exit/dwell

Client-side, a page/section-enter timestamp is already implicitly known (nav events fire
on entry). Add a `leave` event fired from a `visibilitychange` (tab hidden) and `pagehide`
listener, sent via `navigator.sendBeacon` (survives tab close, unlike a normal fetch):

```jsonc
{ "type": "leave", "page": "discover", "section": "landscape", "dwell_ms": 47000 }
```

`dwell_ms` is computed client-side (now − last-entry-timestamp), so it's accurate even for
the final page before the tab closes — today's biggest blind spot. Posts live, same as nav.

### 3. Live-first delivery

`track_event` (`api.py:3448-3498`) changes so `action` events post to Discord immediately
(via `notify_discord`), the same as `open`/`nav` do today, instead of being log-only. The
existing idle-session digest (`engines/usage_report.py`) is unchanged and keeps posting
~10 min after she goes idle, as a recap (duration, most-time-on, flow, counts) — both
surfaces coexist; the live pings are the moment-by-moment stream, the digest is the
summary bookend.

No batching/collapsing of rapid bursts in v1 — every event posts as its own message. If
the channel proves too noisy in practice, a debounce/collapse pass is a small follow-up,
not a blocker for this round.

### 4. Bot/device classification persisted + strengthened

- `_classify_client()` (`api.py:3417-3436`) result is written onto the logged JSONL record
  (new `device`/`is_bot` fields), not just formatted into the Discord string. Makes it
  queryable later without re-deriving from raw UA.
- `engines/geoip.py`'s `geo_label()` call to `ip-api.com` adds `proxy` and `hosting` to
  its requested `fields` (already fetching `status,country,countryCode,city`). When
  either is true, the event is tagged `likely_bot_hosting: true` alongside the existing
  UA-substring classification — catches bots/scrapers that use a plain UA but run from a
  datacenter/hosting IP. Still descriptive-only: nothing is filtered or suppressed, it's
  additional signal for a human reading the feed.

## Data Flow

1. She interacts with a tracked element → `track()` fires → `POST /api/event` → event is
   appended to `usage_events.jsonl` (now including `device`/`is_bot`/`likely_bot_hosting`)
   **and** posted live to Discord immediately.
2. She hides/closes the tab → `leave` beacon fires with real `dwell_ms` → logged + posted
   live.
3. ~10 min after her last event, the existing ticker flushes the idle-session digest as
   before (unchanged mechanism), giving a recap on top of the live stream.

## Error Handling

Unchanged posture from June 26: all frontend emits are best-effort
(`keepalive`/`sendBeacon`, swallow errors, never block the UI); `/api/event` log append
and Discord post are wrapped so a failure never surfaces to the page; ticker/digest logic
is untouched by this work.

## Config Knobs

No new config constants — reuses `IDLE_MINUTES`, `TICK_SECONDS` from the June 26 build.

## Testing

- `engines/geoip.py`: extend existing tests (if any) to cover the new `proxy`/`hosting`
  fields degrading safely when absent from the API response.
- `_classify_client()`: unit test that `device`/`is_bot`/`likely_bot_hosting` land on the
  persisted event record, not just the Discord string.
- Frontend: `leave` beacon fires on `visibilitychange`/`pagehide` with a plausible
  `dwell_ms`; covered by a light unit test similar to the existing `track()` helper test.
- Manual: confirm a full session (open → nav → a few new actions → leave) produces the
  expected sequence of live Discord messages, then the existing digest recap.

## Out of Scope / Future

- Debounce/collapse for rapid action bursts, if live-Discord volume proves too noisy.
- A dashboard, if Discord stops being a good surface for this level of detail.
- Cross-session geo-change flagging (Korea/Tokyo pattern) — deferred, not ruled out.
