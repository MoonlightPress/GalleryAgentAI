# Mochi Found Something New — Design

- **Date:** 2026-07-05
- **Status:** Approved direction, pending spec review
- **Owner:** Mochi / GalleryAgentAI
- **Topic:** Surface a notice when the pipeline adds new opportunities, so the artist doesn't have to notice silently-updated lists herself.

## Problem

`run_full_mochi_pipeline.py` runs (currently ~monthly) add new opportunities to
`deploy_data/compact_opportunities.json`, but nothing on the frontend tells her
anything changed — she'd only notice by scrolling and recognizing an
unfamiliar card. `StatusBar.jsx` (rendered on all three companion pages,
persistent per the Three Companions spec) is currently a literal empty
decorative div with a comment inviting exactly this kind of addition.

Each opportunity already carries an `imported_at` date (e.g. `"2026-05-31"`,
set when the pipeline first ingests it) — no new pipeline step is needed to
know something is new; the data already exists.

## Goals

- A count-based notice ("🐾 Mochi found 3 new things this week") in the
  StatusBar, visible on all three pages, when the pipeline has added
  opportunities recently.
- A small "New" badge on individual opportunity cards (`OppCard.jsx`) next to
  the existing confidence dot, for opportunities imported recently — a
  passive signal while browsing, independent of the banner.
- A dismiss (×) on the banner so it doesn't sit there forever once she's
  seen it, without losing track of a *later* batch of new opportunities.

## Non-Goals

- No new pipeline step, no `date_discovered` engine, no diff/delta tracking
  of what exactly changed between runs — `imported_at` already answers "is
  this new," which is all that's needed.
- No cross-device sync for the dismiss state. Dismissing on her phone won't
  dismiss it on her desktop — acceptable for a single-user internal tool;
  the underlying "is this new" signal (the card badges) stays identical on
  every device regardless of dismissal.
- No listing of specific new opportunity names in the banner itself — she
  browses the normal sections to see them, same as always.

## Architecture

Two independent signals, one shared underlying fact:

### 1. `is_new` — stateless, server-computed, identical everywhere

A pure, testable helper (new function, colocated with other small serving
helpers in `api.py` near `_opp_id()`):

```python
NEW_WINDOW_DAYS = 7

def is_new_opportunity(imported_at, now=None, window_days=NEW_WINDOW_DAYS) -> bool:
    """True if imported_at parses to a date within window_days of now.
    Malformed/missing imported_at -> False. Never raises."""
```

Wherever `/api/opportunities` builds each served opportunity dict (next to
where `"id": _opp_id(opp)` is set), add `"is_new": is_new_opportunity(opp.get("imported_at"))`.
One extra boolean per opportunity, computed once per request — no caching
needed given the low request volume this app sees.

`window_days=7` matches the current ~monthly pipeline cadence: a notice
window of about a week after each run, then quiet until the next one.

### 2. Banner dismiss — per-device, additive on top of `is_new`

`OppCard.jsx` reads `opp.is_new` directly — no dismiss logic, always shows
the badge for any opportunity flagged new, on every device. This is the
passive "still recent" signal while browsing.

`StatusBar.jsx` is the one place dismissal applies:

- On mount, count opportunities where `is_new && !dismissedIds.has(id)` across
  all sections of the already-fetched opportunities payload (reads from the
  shared `apiCache` `App.jsx` already warms via `getCache('/api/opportunities')`,
  falling back to its own fetch on a cache miss).
- Renders "🐾 Mochi found {N} new thing{s} this week" plus a small × when
  `N > 0`.
- Clicking × stores the **currently-new opportunity ids** (not a raw count)
  into `localStorage` under `mochi_new_dismissed`. On every load, prune that
  stored set down to only ids that are still present AND still `is_new` in
  the current payload — keeps it small and self-cleaning as items age past
  the 7-day window naturally.
- If a later pipeline run adds opportunities not in the dismissed set, the
  banner reappears counting only those — a previously-dismissed batch stays
  dismissed.

## Data Flow

1. Pipeline run adds opportunities to `compact_opportunities.json` with
   today's `imported_at`.
2. Next `/api/opportunities` request computes `is_new` per item server-side.
3. `OppCard` shows the badge for any `is_new` item, unconditionally.
4. `StatusBar` computes `is_new && !dismissed` count from the same payload
   and shows/hides its banner accordingly; a dismiss click persists the
   current new-id set to `localStorage` so the banner quiets down for that
   batch specifically.

## Error Handling

- `is_new_opportunity()` never raises — bad/missing `imported_at` just means
  "not new," consistent with the rest of this app's serving code (best-effort,
  never fail the page over a data quirk).
- `StatusBar`'s `localStorage` read/write is wrapped best-effort (matching
  the existing pattern in `App.jsx`'s `mochi_intro_dismissed` and `OppCard.jsx`'s
  `mochi_card_feedback`) — a `localStorage` failure just means dismissal
  doesn't persist, not a broken page.
- Cache-miss fallback fetch in `StatusBar` degrades to showing nothing
  (no banner) rather than blocking render if the fetch fails.

## Testing

- `is_new_opportunity()`: fresh date → True; 8-days-old → False; exactly
  7-days-old boundary; missing/malformed `imported_at` → False; degrades
  safely on garbage input (mirrors `_format_dwell`'s test style).
- Frontend: a light unit test on the pure "compute dismissable new count"
  logic if it's extracted as a standalone function (matching the existing
  `frontend/src/utils/*.test.js` pattern) rather than tested through full
  component rendering, since this repo has no component/DOM test harness.

## Out of Scope / Future

- Per-device dismiss sync, if that ever becomes a real pain point.
- Naming specific new opportunities in the banner text itself.
- A dedicated pipeline-run-metadata endpoint (last-run timestamp, exact
  delta) — `imported_at`-based recency has been sufficient so far.
