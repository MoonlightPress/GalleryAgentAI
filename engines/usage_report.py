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
