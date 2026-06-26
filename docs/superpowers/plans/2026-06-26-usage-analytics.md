# Usage Recording + Session Digests — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stream navigation live to Discord (companion pages + in-page section landings) and post one consolidated interaction digest ~10 min after she goes idle, recording every event to a durable log — without flooding the webhook or naming any specific opportunity.

**Architecture:** Frontend emits `open`/`nav`/`action` events to the existing `/api/event`. The backend appends every event to `memory/usage_events.jsonl`, live-pings Discord for `open` and `nav`, and logs `action` silently. A daemon-thread ticker reads the log each minute and flushes any session idle >10 min as a single digest built by the pure module `engines/usage_report.py`.

**Tech Stack:** Python 3.11 / FastAPI (`api.py`), React + Vite (`frontend/`), Discord webhook via `engines/notify.py`. Python tests use `unittest` (run with `pytest`); frontend tests use Node's built-in `node:test`.

**Spec:** `docs/superpowers/specs/2026-06-26-usage-analytics-design.md`

## Global Constraints

- **Best-effort only:** no tracking path may break the page or crash the API. Every emit, log write, and ticker iteration is wrapped and silently degrades.
- **Name-blind:** never write or send a specific opportunity name/id in a tracking event or digest. Interactions carry `category` (the opportunity *type*) only.
- **Discord is the only surface.** No in-app analytics view. No PII beyond the existing anonymous `visitor_id` (random UUID in `localStorage`, key `mochi_vid`).
- **Config constants (exact values):** `IDLE_MINUTES = 10`, `TICK_SECONDS = 60`, `SECTION_DWELL_MS = 2000`, `SECTION_VISIBLE_RATIO = 0.5`.
- **Follow existing patterns:** Python tests mirror `tests/test_visit_tracking.py` (unittest classes); frontend tests mirror `frontend/src/**/*.test.js` (node:test). Timestamps are UTC ISO-8601 (`datetime.now(timezone.utc).isoformat()`).
- **Frequent commits:** one commit per task.

---

### Task 1: Session math in `engines/usage_report.py`

**Files:**
- Create: `engines/usage_report.py`
- Test: `tests/test_usage_report.py`

**Interfaces:**
- Produces:
  - `PAGE_LABELS: dict[str,str]`, `SECTION_LABELS: dict[str,str]`
  - `split_sessions(events: list[dict], idle_minutes: int = 10) -> list[list[dict]]`
  - `sessions_to_flush(events, now: datetime, last_flushed_iso: str | None = None, idle_minutes: int = 10) -> list[tuple[list[dict], datetime]]`
  - `dwell_by_page(events) -> dict[str,float]`
  - `most_time_on(events) -> str | None`
  - `_parse_ts(value) -> datetime | None`, `_timed(events) -> list[tuple[datetime,dict]]`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_usage_report.py
import unittest
from datetime import datetime, timezone, timedelta

from engines.usage_report import (
    split_sessions, sessions_to_flush, dwell_by_page, most_time_on,
)

T0 = datetime(2026, 6, 26, 10, 0, 0, tzinfo=timezone.utc)


def _ev(mins, **kw):
    """Event helper: ts = T0 + mins minutes."""
    e = {"ts": (T0 + timedelta(minutes=mins)).isoformat()}
    e.update(kw)
    return e


class SplitSessionsTests(unittest.TestCase):
    def test_single_run_is_one_session(self):
        evs = [_ev(0, type="open", page="discover"), _ev(2, type="nav", page="observe")]
        self.assertEqual(len(split_sessions(evs, idle_minutes=10)), 1)

    def test_gap_over_idle_splits(self):
        evs = [_ev(0, type="open"), _ev(2, type="nav"), _ev(20, type="nav")]
        sessions = split_sessions(evs, idle_minutes=10)
        self.assertEqual(len(sessions), 2)
        self.assertEqual(len(sessions[0]), 2)

    def test_unparseable_ts_dropped(self):
        evs = [_ev(0, type="open"), {"type": "nav", "ts": "garbage"}]
        self.assertEqual(len(split_sessions(evs)[0]), 1)

    def test_empty(self):
        self.assertEqual(split_sessions([]), [])


class SessionsToFlushTests(unittest.TestCase):
    def test_idle_session_is_flushed(self):
        evs = [_ev(0, type="open"), _ev(3, type="nav")]
        now = T0 + timedelta(minutes=20)        # 17 min after last event
        out = sessions_to_flush(evs, now, None, idle_minutes=10)
        self.assertEqual(len(out), 1)

    def test_active_session_not_flushed(self):
        evs = [_ev(0, type="open"), _ev(3, type="nav")]
        now = T0 + timedelta(minutes=5)         # only 2 min idle
        self.assertEqual(sessions_to_flush(evs, now, None, idle_minutes=10), [])

    def test_already_flushed_session_skipped(self):
        evs = [_ev(0, type="open"), _ev(3, type="nav")]
        now = T0 + timedelta(minutes=20)
        end_iso = (T0 + timedelta(minutes=3)).isoformat()
        self.assertEqual(sessions_to_flush(evs, now, end_iso, idle_minutes=10), [])


class DwellTests(unittest.TestCase):
    def test_most_time_on_picks_longest_page(self):
        evs = [_ev(0, type="open", page="discover"),
               _ev(1, type="nav", page="observe"),
               _ev(9, type="nav", page="discover")]  # 8 min on Saffron
        self.assertEqual(most_time_on(evs), "Saffron")

    def test_most_time_on_empty_is_none(self):
        self.assertIsNone(most_time_on([]))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_usage_report.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'engines.usage_report'`

- [ ] **Step 3: Write minimal implementation**

```python
# engines/usage_report.py
"""
usage_report.py

Pure, dependency-light helpers that turn a stream of usage events into a
per-session Discord digest. No I/O and no network — fully unit-testable. The
impure shell (reading the log, posting to Discord) lives in api.py.

Name-blind by contract: events carry an opportunity *category* (the type), never
the named opportunity. Nothing here ever sees or emits an opportunity name.
"""
from __future__ import annotations

from datetime import datetime

PAGE_LABELS = {
    "discover": "Home",
    "observe": "Saffron",
    "refine": "Peppercorn",
}

SECTION_LABELS = {
    "today_focus": "Today's Focus",
    "open_calls": "Open Calls",
    "people": "People",
    "tracker": "Tracker",
    "calendar": "Calendar",
}


def _parse_ts(value):
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def _timed(events):
    """Sorted ``[(dt, event), ...]`` for events with a parseable ``ts``."""
    out = []
    for e in events or []:
        t = _parse_ts(e.get("ts"))
        if t is not None:
            out.append((t, e))
    out.sort(key=lambda x: x[0])
    return out


def split_sessions(events, idle_minutes=10):
    """Split time-ordered events into sessions, breaking on gaps > idle_minutes."""
    timed = _timed(events)
    sessions, current, last = [], [], None
    for t, e in timed:
        if last is not None and (t - last).total_seconds() > idle_minutes * 60:
            sessions.append([x for _, x in current])
            current = []
        current.append((t, e))
        last = t
    if current:
        sessions.append([x for _, x in current])
    return sessions


def sessions_to_flush(events, now, last_flushed_iso=None, idle_minutes=10):
    """Sessions that have gone idle (>idle_minutes since their last event) and end
    after ``last_flushed_iso``. Returns ``[(session_events, end_dt), ...]`` so each
    can be digested exactly once."""
    last_flushed = _parse_ts(last_flushed_iso) if last_flushed_iso else None
    out = []
    for sess in split_sessions(events, idle_minutes):
        timed = _timed(sess)
        if not timed:
            continue
        end = timed[-1][0]
        if (now - end).total_seconds() <= idle_minutes * 60:
            continue  # still active
        if last_flushed is not None and end <= last_flushed:
            continue  # already reported
        out.append((sess, end))
    return out


def dwell_by_page(events):
    """Seconds attributed to each companion page (time until the next event)."""
    timed = _timed(events)
    out = {}
    for (t0, e0), (t1, _e1) in zip(timed, timed[1:]):
        secs = (t1 - t0).total_seconds()
        if secs <= 0:
            continue
        label = PAGE_LABELS.get(e0.get("page"), e0.get("page") or "?")
        out[label] = out.get(label, 0) + secs
    return out


def most_time_on(events):
    d = dwell_by_page(events)
    if not d:
        return None
    return max(d, key=d.get)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_usage_report.py -v`
Expected: PASS (all tests in `SplitSessionsTests`, `SessionsToFlushTests`, `DwellTests`)

- [ ] **Step 5: Commit**

```bash
git add engines/usage_report.py tests/test_usage_report.py
git commit -m "feat(usage): session split + idle-flush + dwell math"
```

---

### Task 2: Digest formatting in `engines/usage_report.py`

**Files:**
- Modify: `engines/usage_report.py`
- Test: `tests/test_usage_report.py`

**Interfaces:**
- Consumes: `_timed`, `_location` helpers; `PAGE_LABELS`, `SECTION_LABELS` from Task 1.
- Produces:
  - `ACTION_LABELS: dict[str,str]`
  - `interaction_counts(events) -> dict[str, dict]` — `{action: {"total": int, "by_category": {cat: int}}}`
  - `format_flow(events) -> str`
  - `duration_minutes(events) -> int`
  - `build_digest(events, returning: bool | None = None, day: int | None = None) -> str`

- [ ] **Step 1: Write the failing test**

```python
# Append to tests/test_usage_report.py (add imports at top of file)
from engines.usage_report import (
    interaction_counts, format_flow, build_digest, duration_minutes,
)


class InteractionCountsTests(unittest.TestCase):
    def test_counts_by_action_and_category(self):
        evs = [
            _ev(0, type="action", action="follow", category="zine"),
            _ev(1, type="action", action="follow", category="gallery"),
            _ev(2, type="action", action="applied", category="fair_popup"),
            _ev(3, type="nav", page="observe"),  # ignored
        ]
        c = interaction_counts(evs)
        self.assertEqual(c["follow"]["total"], 2)
        self.assertEqual(c["follow"]["by_category"], {"zine": 1, "gallery": 1})
        self.assertEqual(c["applied"]["total"], 1)
        self.assertNotIn("nav", c)


class FlowTests(unittest.TestCase):
    def test_flow_dedupes_consecutive_and_uses_labels(self):
        evs = [
            _ev(0, type="open", page="discover"),
            _ev(1, type="nav", page="discover", section="people"),
            _ev(2, type="nav", page="discover", section="people"),  # dup
            _ev(3, type="nav", page="observe"),
        ]
        self.assertEqual(format_flow(evs), "Home → People → Saffron")


class BuildDigestTests(unittest.TestCase):
    def test_digest_has_header_dwell_counts_flow(self):
        evs = [
            _ev(0, type="open", page="discover"),
            _ev(1, type="nav", page="observe"),
            _ev(8, type="action", action="follow", category="zine"),
        ]
        text = build_digest(evs)
        self.assertIn("Session wrap-up", text)
        self.assertIn("most time on: Saffron", text)
        self.assertIn("followed 1 (1 zine)", text)
        self.assertIn("flow:", text)

    def test_digest_with_no_interactions_omits_counts_line(self):
        evs = [_ev(0, type="open", page="discover"), _ev(2, type="nav", page="observe")]
        text = build_digest(evs)
        self.assertIn("Session wrap-up", text)
        self.assertNotIn("followed", text)

    def test_empty_events_degrade_safely(self):
        self.assertIsInstance(build_digest([]), str)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_usage_report.py -v`
Expected: FAIL — `ImportError: cannot import name 'interaction_counts'`

- [ ] **Step 3: Write minimal implementation**

```python
# Append to engines/usage_report.py

ACTION_LABELS = {
    "follow": "followed",
    "applied": "applied",
    "maybe_later": "saved for later",
    "not_for_me": "hid",
    "open_card": "opened",
    "profile_save": "edited profile",
    "saffron_answer": "answered a question",
}


def _location(e):
    if e.get("section"):
        return SECTION_LABELS.get(e["section"], str(e["section"]).replace("_", " ").title())
    return PAGE_LABELS.get(e.get("page"), e.get("page") or "?")


def interaction_counts(events):
    counts = {}
    for e in events or []:
        if e.get("type") != "action":
            continue
        action = e.get("action") or "other"
        slot = counts.setdefault(action, {"total": 0, "by_category": {}})
        slot["total"] += 1
        cat = e.get("category")
        if cat:
            slot["by_category"][cat] = slot["by_category"].get(cat, 0) + 1
    return counts


def format_flow(events):
    seq = []
    for _t, e in _timed(events):
        if e.get("type") not in ("open", "nav"):
            continue
        loc = _location(e)
        if not seq or seq[-1] != loc:
            seq.append(loc)
    return " → ".join(seq)


def duration_minutes(events):
    timed = _timed(events)
    if len(timed) < 2:
        return 0
    return max(0, round((timed[-1][0] - timed[0][0]).total_seconds() / 60))


def build_digest(events, returning=None, day=None):
    who = "returning" if returning is True else "new" if returning is False else "visit"
    head = f"🧵 Session wrap-up — {who}"
    if day:
        head += f" · day {day}"
    head += f" · ~{duration_minutes(events)} min"
    lines = [head]

    mt = most_time_on(events)
    if mt:
        lines.append(f"most time on: {mt}")

    counts = interaction_counts(events)
    if counts:
        parts = []
        for action, slot in counts.items():
            seg = f"{ACTION_LABELS.get(action, action)} {slot['total']}"
            if slot["by_category"]:
                cats = ", ".join(f"{n} {c}" for c, n in slot["by_category"].items())
                seg += f" ({cats})"
            parts.append(seg)
        lines.append(" · ".join(parts))

    flow = format_flow(events)
    if flow:
        lines.append(f"flow: {flow}")

    return "\n".join(lines)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_usage_report.py -v`
Expected: PASS (all classes)

- [ ] **Step 5: Commit**

```bash
git add engines/usage_report.py tests/test_usage_report.py
git commit -m "feat(usage): build per-session digest text"
```

---

### Task 3: Section support in `describe_event`

**Files:**
- Modify: `engines/visit_tracking.py:51-56` (the `nav` branch of `describe_event`)
- Test: `tests/test_visit_tracking.py`

**Interfaces:**
- Consumes: existing `describe_event(event, day=None, returning=None)`.
- Produces: `nav` events with a `section` render as `↳ <SectionLabel>`; existing companion-nav behavior unchanged.

- [ ] **Step 1: Write the failing test**

```python
# Add to tests/test_visit_tracking.py inside DescribeEventTests
    def test_nav_with_section_shows_subarrow_label(self):
        text, _ = describe_event({"type": "nav", "page": "discover", "section": "people"})
        self.assertEqual(text, "↳ People")

    def test_nav_with_unknown_section_titlecases(self):
        text, _ = describe_event({"type": "nav", "page": "observe", "section": "money_runway"})
        self.assertIn("Money Runway", text)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_visit_tracking.py -k section -v`
Expected: FAIL — returns `"→ Home"` (current code ignores `section`)

- [ ] **Step 3: Write minimal implementation**

Add a section-label map near `PAGE_LABELS` (top of `engines/visit_tracking.py`, after line 17):

```python
SECTION_LABELS = {
    "today_focus": "Today's Focus",
    "open_calls": "Open Calls",
    "people": "People",
    "tracker": "Tracker",
    "calendar": "Calendar",
}


def _section_label(section) -> str:
    return SECTION_LABELS.get(section, str(section).replace("_", " ").title())
```

Replace the `nav` branch (currently lines 51-56):

```python
    if etype == "nav":
        section = event.get("section")
        if section:
            return f"↳ {_section_label(section)}", "info"
        to = _page_label(event.get("page"))
        frm = event.get("from")
        if frm:
            return f"{_page_label(frm)} → {to}", "info"
        return f"→ {to}", "info"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_visit_tracking.py -v`
Expected: PASS — new section tests pass and all existing `DescribeEventTests` still pass.

- [ ] **Step 5: Commit**

```bash
git add engines/visit_tracking.py tests/test_visit_tracking.py
git commit -m "feat(usage): describe_event renders within-page section moves"
```

---

### Task 4: Backend `/api/event` — durable log + live nav ping

**Files:**
- Modify: `api.py:49-50` (add config constants after `DATA_DIR`/`DEPLOY_DIR`)
- Modify: `api.py:3329-3362` (rewrite `track_event`)
- Create helper `_append_usage_event` in `api.py` (near `track_event`)
- Test: `tests/test_usage_endpoint.py`

**Interfaces:**
- Consumes: `describe_event` (Task 3), `register_visit`, `mark_visitor`, `notify_discord`.
- Produces: `_append_usage_event(event: dict, path: Path | None = None) -> None`; `/api/event` logs all events, live-pings `open` + `nav`, logs `action` silently. New constants `USAGE_EVENTS_PATH`, `USAGE_STATE_PATH`, `IDLE_MINUTES`, `TICK_SECONDS`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_usage_endpoint.py
import json
import unittest
from pathlib import Path
import tempfile

import api


class AppendUsageEventTests(unittest.TestCase):
    def test_appends_one_json_line_with_ts(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "usage_events.jsonl"
            api._append_usage_event({"type": "nav", "page": "observe"}, path=path)
            api._append_usage_event({"type": "action", "action": "follow"}, path=path)
            lines = path.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 2)
            rec = json.loads(lines[0])
            self.assertEqual(rec["type"], "nav")
            self.assertIn("ts", rec)          # server-stamped

    def test_bad_path_does_not_raise(self):
        # A failed append must never propagate (tracking is best-effort).
        api._append_usage_event({"type": "nav"}, path=Path("/nonexistent-dir/x/y.jsonl"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_usage_endpoint.py -v`
Expected: FAIL — `AttributeError: module 'api' has no attribute '_append_usage_event'`

- [ ] **Step 3: Write minimal implementation**

Add constants after `api.py:50`:

```python
USAGE_EVENTS_PATH = DATA_DIR / "usage_events.jsonl"
USAGE_STATE_PATH  = DATA_DIR / "usage_state.json"
IDLE_MINUTES      = 10
TICK_SECONDS      = 60
```

Add the append helper just above `track_event` (api.py:3329):

```python
def _append_usage_event(event, path=None) -> None:
    """Append one usage event as a JSON line. Server-stamps ``ts``. Best-effort:
    a failure here must never fail the page (see /api/event)."""
    path = path or USAGE_EVENTS_PATH
    try:
        rec = dict(event or {})
        rec["ts"] = datetime.now(timezone.utc).isoformat()
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _read_usage_events(path=None):
    """Read the append log into a list of event dicts. Missing file -> []."""
    path = path or USAGE_EVENTS_PATH
    out = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:
                    continue
    except FileNotFoundError:
        return []
    except Exception:
        return []
    return out
```

Replace the body of `track_event` (api.py:3339-3362) with:

```python
    try:
        event = await request.json()
    except Exception:
        event = {}
    etype = (event or {}).get("type")

    # Durable record for the idle digest — every event, best-effort.
    _append_usage_event(event)

    if etype == "open":
        vpath = DATA_DIR / "visit_log.json"
        try:
            log = json.loads(vpath.read_text(encoding="utf-8")) if vpath.exists() else {}
        except Exception:
            log = {}
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log, _notify, day = register_visit(log, today)
        log, returning = mark_visitor(log, event.get("visitor_id"))
        try:
            _atomic_write_json(vpath, log)
        except Exception:
            pass
        text, status = describe_event(event, day=day, returning=returning)
        notify_discord(text, status=status)

    elif etype == "nav":
        # Navigation streams live (companion moves + debounced section landings).
        text, status = describe_event(event)
        notify_discord(text, status=status)

    # type == "action": logged only; summarised later in the idle digest.
    return {"ok": True}
```

Update the `track_event` docstring (api.py:3331-3338) to state the new posture:

```python
    """Usage signal. Records every event to usage_events.jsonl for the idle
    digest. Posts LIVE to Discord for `open` (she's here) and `nav` (her moves,
    companion + debounced section landings). `action` events are logged silently
    and summarised in the per-session digest the ticker posts ~10 min after she
    goes idle. Flow- and category-aware, never names a specific opportunity.
    Best-effort — never fails the page over a tracking hiccup."""
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_usage_endpoint.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add api.py tests/test_usage_endpoint.py
git commit -m "feat(usage): log every event; live-ping nav; action logged silently"
```

---

### Task 5: Backend digest ticker

**Files:**
- Modify: `engines/usage_report.py` (add `run_flush`)
- Modify: `api.py` (add `_flush_tick` + startup thread, near `track_event`)
- Test: `tests/test_usage_report.py`

**Interfaces:**
- Consumes: `sessions_to_flush`, `build_digest` (Tasks 1-2); `_read_usage_events`, `USAGE_STATE_PATH` (Task 4); `notify_discord`, `_load_json`, `_atomic_write_json`.
- Produces: `run_flush(events, now, state: dict, notifier) -> tuple[dict, int]` (new state, count posted); `_flush_tick(now=None)` shell; daemon thread started at FastAPI startup.

- [ ] **Step 1: Write the failing test**

```python
# Append to tests/test_usage_report.py
from engines.usage_report import run_flush


class RunFlushTests(unittest.TestCase):
    def _events(self):
        return [
            _ev(0, type="open", page="discover", visitor_id="v1"),
            _ev(3, type="action", action="follow", category="zine", visitor_id="v1"),
        ]

    def test_posts_one_digest_for_idle_session(self):
        posted = []
        now = T0 + timedelta(minutes=20)
        state, count = run_flush(self._events(), now, {}, notifier=posted.append)
        self.assertEqual(count, 1)
        self.assertEqual(len(posted), 1)
        self.assertIn("Session wrap-up", posted[0])
        self.assertIn("v1", state)

    def test_second_run_does_not_repost(self):
        now = T0 + timedelta(minutes=20)
        state, _ = run_flush(self._events(), now, {}, notifier=lambda m: None)
        posted = []
        state2, count = run_flush(self._events(), now, state, notifier=posted.append)
        self.assertEqual(count, 0)
        self.assertEqual(posted, [])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_usage_report.py -k RunFlush -v`
Expected: FAIL — `ImportError: cannot import name 'run_flush'`

- [ ] **Step 3: Write minimal implementation**

Append to `engines/usage_report.py`:

```python
def run_flush(events, now, state, notifier):
    """Post a digest for each newly-idle session, grouped per visitor. Returns
    ``(new_state, count_posted)``. ``state`` maps visitor_id -> last-flushed ISO.
    ``notifier(message: str)`` is injected (api.py passes notify_discord)."""
    from collections import defaultdict

    by_visitor = defaultdict(list)
    for e in events or []:
        by_visitor[e.get("visitor_id") or "anon"].append(e)

    new_state = dict(state or {})
    posted = 0
    for vid, evs in by_visitor.items():
        for sess, end in sessions_to_flush(evs, now, new_state.get(vid)):
            notifier(build_digest(sess))
            new_state[vid] = end.isoformat()
            posted += 1
    return new_state, posted
```

Add to `api.py` just below `_read_usage_events`:

```python
def _flush_tick(now=None):
    """One ticker iteration: flush any idle session to Discord exactly once."""
    from engines.usage_report import run_flush

    now = now or datetime.now(timezone.utc)
    events = _read_usage_events()
    state = _load_json(USAGE_STATE_PATH, {})
    new_state, posted = run_flush(events, now, state, notify_discord)
    if posted:
        try:
            _atomic_write_json(USAGE_STATE_PATH, new_state)
        except Exception:
            pass


@app.on_event("startup")
def _start_usage_ticker():
    """Daemon thread that flushes idle-session digests. A thread (not asyncio)
    keeps the blocking notify_discord POST off the event loop. Never crashes the
    API — every tick is guarded."""
    import threading
    import time

    def _loop():
        while True:
            time.sleep(TICK_SECONDS)
            try:
                _flush_tick()
            except Exception:
                pass

    threading.Thread(target=_loop, daemon=True, name="usage-digest-ticker").start()
```

> Note: `_load_json` exists in `api.py` (used by `/api/tracker`). If its signature is `_load_json(path, default)`, the call above matches. Verify before running.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_usage_report.py -k RunFlush -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add engines/usage_report.py api.py tests/test_usage_report.py
git commit -m "feat(usage): idle-session digest ticker"
```

---

### Task 6: Frontend `track()` helper

**Files:**
- Create: `frontend/src/utils/track.js`
- Modify: `frontend/src/App.jsx:63-94` (use `track`, drop inline visitor_id)
- Test: `frontend/src/utils/track.test.js`

**Interfaces:**
- Produces: `track(event: object) -> void` — attaches the anonymous `visitor_id` from `localStorage` (`mochi_vid`) and POSTs to `/api/event` with `keepalive`. Best-effort; swallows all errors.

- [ ] **Step 1: Write the failing test**

```js
// frontend/src/utils/track.test.js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { track } from './track.js'

function withStubs(run) {
  const store = {}
  global.localStorage = {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v) },
  }
  global.crypto = { randomUUID: () => 'test-uuid' }
  const calls = []
  global.fetch = (url, opts) => { calls.push({ url, opts }); return Promise.resolve() }
  try { return run(calls) } finally {
    delete global.fetch; delete global.localStorage; delete global.crypto
  }
}

test('posts event to /api/event with visitor_id attached', () => {
  withStubs((calls) => {
    track({ type: 'action', action: 'follow', category: 'zine' })
    assert.equal(calls.length, 1)
    assert.equal(calls[0].url, '/api/event')
    const body = JSON.parse(calls[0].opts.body)
    assert.equal(body.type, 'action')
    assert.equal(body.action, 'follow')
    assert.equal(body.visitor_id, 'test-uuid')
    assert.equal(calls[0].opts.keepalive, true)
  })
})

test('swallows fetch errors (best-effort)', () => {
  withStubs((calls) => {
    global.fetch = () => { throw new Error('network down') }
    assert.doesNotThrow(() => track({ type: 'nav', page: 'observe' }))
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd frontend && node --test src/utils/track.test.js`
Expected: FAIL — cannot resolve `./track.js`

- [ ] **Step 3: Write minimal implementation**

```js
// frontend/src/utils/track.js
// Best-effort UX beacon. Posts a usage event to /api/event with the anonymous,
// stable per-browser visitor id attached. Never throws into the UI.

function visitorId() {
  try {
    let v = localStorage.getItem('mochi_vid')
    if (!v) {
      v = (typeof crypto !== 'undefined' && crypto.randomUUID)
        ? crypto.randomUUID()
        : String(Date.now()) + Math.random().toString(36).slice(2)
      localStorage.setItem('mochi_vid', v)
    }
    return v
  } catch {
    return null
  }
}

export function track(event) {
  const vid = visitorId()
  const body = vid ? { ...event, visitor_id: vid } : { ...event }
  try {
    fetch('/api/event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      keepalive: true,
    }).catch(() => {})
  } catch {
    /* ignore — tracking is best-effort */
  }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd frontend && node --test src/utils/track.test.js`
Expected: PASS (both tests)

- [ ] **Step 5: Refactor `App.jsx` to use it**

In `frontend/src/App.jsx`, add the import near the other util imports:

```js
import { track } from './utils/track'
```

Replace the body of the beacon `useEffect` (lines 70-93) with:

```js
  useEffect(() => {
    const from = prevPage.current
    prevPage.current = page
    track(from === null ? { type: 'open', page } : { type: 'nav', page, from })
  }, [page])
```

(The `visitor_id` is now attached inside `track`; the inline localStorage block and `fetch` are removed. Leave the `prevPage` ref declaration above the effect intact.)

- [ ] **Step 6: Verify the suite still passes**

Run: `cd frontend && npm test`
Expected: PASS (existing `freshness`, `feedbackBehavior`, `recommendationQuality` + new `track`)

- [ ] **Step 7: Commit**

```bash
git add frontend/src/utils/track.js frontend/src/utils/track.test.js frontend/src/App.jsx
git commit -m "feat(usage): track() beacon helper; App.jsx uses it"
```

---

### Task 7: Live section-view tracking on the discover page

**Files:**
- Create: `frontend/src/components/TrackedSection.jsx`
- Modify: `frontend/src/App.jsx:105-117` (wrap discover sections)

**Interfaces:**
- Consumes: `track` (Task 6).
- Produces: `<TrackedSection section="...">{children}</TrackedSection>` — fires `track({type:'nav', page:'discover', section})` once per mount when the section is ≥`SECTION_VISIBLE_RATIO` visible for ≥`SECTION_DWELL_MS`.

- [ ] **Step 1: Write the component**

```jsx
// frontend/src/components/TrackedSection.jsx
import { useEffect, useRef } from 'react'
import { track } from '../utils/track'

const SECTION_DWELL_MS = 2000
const SECTION_VISIBLE_RATIO = 0.5

// Fires one nav event when the wrapped section is genuinely landed on (visible
// past the ratio for the dwell time), so scrolling past doesn't spam. Once per
// mount. Layout-neutral: a plain block wrapper with no margin of its own.
export default function TrackedSection({ section, children }) {
  const ref = useRef(null)
  const firedRef = useRef(false)
  const timerRef = useRef(null)

  useEffect(() => {
    const el = ref.current
    if (!el || typeof IntersectionObserver === 'undefined') return
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && entry.intersectionRatio >= SECTION_VISIBLE_RATIO) {
          if (!firedRef.current && timerRef.current == null) {
            timerRef.current = setTimeout(() => {
              firedRef.current = true
              timerRef.current = null
              track({ type: 'nav', page: 'discover', section })
            }, SECTION_DWELL_MS)
          }
        } else if (timerRef.current != null) {
          clearTimeout(timerRef.current)
          timerRef.current = null
        }
      },
      { threshold: [SECTION_VISIBLE_RATIO] },
    )
    obs.observe(el)
    return () => {
      obs.disconnect()
      if (timerRef.current != null) clearTimeout(timerRef.current)
    }
  }, [section])

  return <div ref={ref} className="tracked-section">{children}</div>
}
```

- [ ] **Step 2: Wire it into `App.jsx`**

Add the import:

```js
import TrackedSection from './components/TrackedSection'
```

Wrap the discover sections (lines 105-117). Replace:

```jsx
        {page === 'discover' && <TodaysFocus />}
        {page === 'discover' && <ViewToggle view={view} setView={setView} />}
        {page === 'discover' && view === 'cards'    && <OpportunitiesSection />}
        {page === 'discover' && view === 'cards'    && (
          <div className="opps-root">
            <RelationshipTargets />
          </div>
        )}
        {page === 'discover' && view === 'cards'    && <TrackerSection />}
```

with:

```jsx
        {page === 'discover' && <TrackedSection section="today_focus"><TodaysFocus /></TrackedSection>}
        {page === 'discover' && <ViewToggle view={view} setView={setView} />}
        {page === 'discover' && view === 'cards'    && <TrackedSection section="open_calls"><OpportunitiesSection /></TrackedSection>}
        {page === 'discover' && view === 'cards'    && (
          <TrackedSection section="people">
            <div className="opps-root">
              <RelationshipTargets />
            </div>
          </TrackedSection>
        )}
        {page === 'discover' && view === 'cards'    && <TrackedSection section="tracker"><TrackerSection /></TrackedSection>}
```

- [ ] **Step 3: Visually verify the discover layout is unchanged**

Run: `start_mochi.bat` (or `cd frontend && npm run dev`), open http://localhost:5177.
Expected: discover page renders identically (spacing between Today's Focus / Open Calls / People / Tracker unchanged). If a gap shifted, add to the relevant CSS: `.tracked-section { display: contents }` is NOT allowed (breaks the observer) — instead ensure `.tracked-section { margin: 0 }` and move any needed spacing onto the inner section, then re-verify.

- [ ] **Step 4: Confirm events fire**

With the dev app open and DevTools → Network filtered to `event`: scroll so a section sits on screen >2s. Expected: a POST `/api/event` with body `{"type":"nav","page":"discover","section":"open_calls",...}`. If `MOCHI_DISCORD_WEBHOOK` is set, the move appears in Discord as `↳ Open Calls`.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/TrackedSection.jsx frontend/src/App.jsx
git commit -m "feat(usage): live section-view tracking on discover"
```

---

### Task 8: Instrument card interactions in `OppCard`

**Files:**
- Modify: `frontend/src/components/OppCard.jsx` (import `track`; `handleFeedback` at 154-165; details button at 266-271)

**Interfaces:**
- Consumes: `track` (Task 6).
- Produces: `action` events `{type:'action', action, category}` for `follow|applied|maybe_later|not_for_me` and `open_card`, each tagged with `opp.category`.

- [ ] **Step 1: Add the import**

In `frontend/src/components/OppCard.jsx`, after line 8 (`import { oppKey } ...`):

```js
import { track } from '../utils/track'
```

- [ ] **Step 2: Track feedback selections**

In `handleFeedback` (line 159, inside `if (next) {`), add as the first line of the block:

```js
    if (next) {
      track({ type: 'action', action: next, category: opp.category })
      await saveFeedback(opp, next)
```

(`next` is one of `follow|applied|maybe_later|not_for_me`; toggling a choice off — `next === null` — does not emit, by design.)

- [ ] **Step 3: Track card opens**

Replace the Details button `onClick` (line 268):

```jsx
          <button
            className={`opp-btn-details${isOpen ? ' opp-btn-details--active' : ''}`}
            onClick={() => {
              if (!isOpen) track({ type: 'action', action: 'open_card', category: opp.category })
              onDetails()
            }}
          >
```

- [ ] **Step 4: Verify**

Run: `cd frontend && npm test` (no regressions), then in the dev app click a card's ★/✓/✕ and "Details" with Network filtered to `event`.
Expected: POST `/api/event` bodies like `{"type":"action","action":"follow","category":"zine_print",...}` and `{"type":"action","action":"open_card",...}`.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/OppCard.jsx
git commit -m "feat(usage): track card feedback + card-open (category-tagged)"
```

---

### Task 9: Instrument profile + Saffron-answer saves

**Files:**
- Modify: `frontend/src/components/PeppercornPage.jsx` (import `track`; `saveSection` at 1879-1908)

**Interfaces:**
- Consumes: `track` (Task 6).
- Produces: an `action` event on a successful save — `saffron_answer` when the update is solely `saffron_answers` (the Saffron-questions editor routes through here via `onSave`), else `profile_save`. No category (not opportunity-scoped).

- [ ] **Step 1: Add the import**

At the top of `frontend/src/components/PeppercornPage.jsx`, with the other imports:

```js
import { track } from '../utils/track'
```

- [ ] **Step 2: Track on successful save**

In `saveSection` (line 1902, immediately after `setIsSaved(true)`), add:

```js
      setIsSaved(true)
      const _keys = Object.keys(updates || {})
      track({
        type: 'action',
        action: (_keys.length === 1 && _keys[0] === 'saffron_answers') ? 'saffron_answer' : 'profile_save',
      })
```

- [ ] **Step 3: Verify**

Run: `cd frontend && npm test` (no regressions), then in the dev app save a Peppercorn field and answer a Saffron question (Network filtered to `event`).
Expected: `{"type":"action","action":"profile_save",...}` for a field edit and `{"type":"action","action":"saffron_answer",...}` for a question answer.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/PeppercornPage.jsx
git commit -m "feat(usage): track profile + saffron-answer saves"
```

---

### Task 10: Privacy docstring update + full verification

**Files:**
- Modify: `engines/visit_tracking.py:1-8` (module docstring)

- [ ] **Step 1: Update the module docstring**

Replace the `visit_tracking.py` docstring (lines 1-8) so it no longer claims strict content-blindness — the system now records flow + interaction *types* (never names):

```python
"""
visit_tracking.py

Usage signal for the app: live "she opened it" / "she moved here" wording, plus
new-vs-returning detection and a running day/visit count. The system is now
flow- and category-aware (which page/section she engages, the *types* of
opportunity she acts on) but remains NAME-BLIND — it never records the specific
named opportunity. The per-session interaction digest is built in
engines/usage_report.py; this module only formats the live ping lines.
"""
```

- [ ] **Step 2: Run the full Python suite**

Run: `python -m pytest tests/test_usage_report.py tests/test_usage_endpoint.py tests/test_visit_tracking.py -v`
Expected: PASS (all classes across the three files).

- [ ] **Step 3: Run the full frontend suite**

Run: `cd frontend && npm test`
Expected: PASS (freshness, feedbackBehavior, recommendationQuality, track).

- [ ] **Step 4: End-to-end smoke (real app)**

With `MOCHI_DISCORD_WEBHOOK` set, run `start_mochi.bat`. Open the app, move between companion pages and discover sections, follow/apply/hide a couple of cards, then leave it idle.
Expected: companion + section moves appear live in Discord (`Home → Saffron`, `↳ Open Calls`); ~10-11 min after the last action a single `🧵 Session wrap-up …` digest appears with counts by category and "most time on". Confirm `memory/usage_events.jsonl` is accumulating lines and `memory/usage_state.json` gains the visitor's last-flushed timestamp after the flush.

- [ ] **Step 5: Commit**

```bash
git add engines/visit_tracking.py
git commit -m "docs(usage): visit_tracking docstring reflects name-blind flow tracking"
```

---

## Self-Review

**Spec coverage:**
- Live open ping — Task 4 (preserved). ✓
- Live navigation, companion — Task 4 (nav branch) + Task 6 (App.jsx emits). ✓
- Live navigation, within-page sections, debounced — Task 3 (render) + Task 7 (observer). ✓
- Interactions captured, category-only — Tasks 8 (cards: follow/apply/maybe/hide/open) + 9 (profile/saffron). ✓
- Durable append log — Task 4. ✓
- Idle 10-min flush via backend ticker, exactly-once — Tasks 1 (`sessions_to_flush`) + 5 (`run_flush`, ticker). ✓
- Digest content (counts by type, most-time-on, flow recap) — Task 2. ✓
- Privacy posture update — Task 10. ✓
- Config knobs (IDLE_MINUTES, TICK_SECONDS, SECTION_DWELL_MS, SECTION_VISIBLE_RATIO) — Tasks 4 + 7. ✓
- Error handling (best-effort everywhere) — Tasks 4, 5, 6, 7. ✓

**Type consistency:** `track(event)` shape (`{type, ...}`) is consistent across App.jsx, TrackedSection, OppCard, PeppercornPage. Event fields (`type`, `page`, `from`, `section`, `action`, `category`, `visitor_id`, `ts`) match between the emitters, `_append_usage_event`, and `usage_report` consumers. `run_flush`/`sessions_to_flush`/`build_digest` signatures match their call sites.

**Out of scope (fast-follow, not in this plan):** Saffron/Peppercorn sub-tab live tracking (one `track({type:'nav', page, section})` per tab handler once those handlers are instrumented); on-demand `GET /api/usage_report`; deploy-cron delivery for long absences.
