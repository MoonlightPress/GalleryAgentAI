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
