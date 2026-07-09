"""
visit_tracking.py

Usage signal for the app: live "she opened it" / "she moved here" wording, plus
new-vs-returning detection and a running day/visit count. The system is
flow- and category-aware (which page/section she engages, the *types* of
opportunity she acts on) and, since 2026-07-05 (Scott's call), also names the
specific opportunity/contact an action refers to when the frontend sends one.
The per-session interaction digest is built in engines/usage_report.py; this
module only formats the live ping lines.
"""
from __future__ import annotations


# Friendly labels for the internal page keys used by the frontend.
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
    # Saffron tabs
    "strategy": "Strategy",
    "profile": "Profile",
    "relationships": "Relationships",
    "money": "Money",
    "career_position": "Career Position",
    "long_term_scenarios": "Long-term Scenarios",
    "career_unlock_tree": "Career Unlock Tree",
    # Peppercorn accordion sections
    "artist-statement": "Artist Statement",
    "saffron-questions": "Saffron's Questions",
    "career-goals": "Career Goals",
    "preferences": "Preferences",
    "exhibition-log": "Exhibition Log",
    "submission-log": "Submission Log",
    "venue-log": "Venue Log",
    "contacts": "Contacts",
}


def _page_label(page) -> str:
    if not page:
        return "?"
    return PAGE_LABELS.get(page, str(page).replace("_", " ").title())


def _section_label(section) -> str:
    return SECTION_LABELS.get(section, str(section).replace("_", " ").title())


def visitor_label(known: dict, visitor_id) -> str:
    """Friendly display name for a visitor_id (e.g. "Nin's phone"), or "" if
    not in the curated known-visitors map. Purely a readability aid so Scott
    doesn't have to memorize raw UUID prefixes — the map only ever contains
    ids he has explicitly confirmed himself; nothing here infers identity."""
    if not visitor_id:
        return ""
    return (known or {}).get(visitor_id) or ""


def _format_dwell(ms) -> str:
    """47000 -> '47s', 192000 -> '3m 12s', 120000 -> '2m'. Never raises —
    a malformed/missing dwell degrades to a generic word rather than crashing
    the live ping."""
    try:
        seconds = max(0, int(ms) // 1000)
    except (TypeError, ValueError):
        return "a moment"
    if seconds < 60:
        return f"{seconds}s"
    minutes, secs = divmod(seconds, 60)
    return f"{minutes}m {secs}s" if secs else f"{minutes}m"


def describe_event(event: dict, day: int | None = None,
                   returning: bool | None = None) -> tuple[str, str]:
    """Turn a navigation event into ``(message, status)`` for the Discord feed.

    Event types: ``open`` (session start), ``nav`` (page change), ``action``
    (a meaningful action like a profile edit), ``leave`` (she hid/closed the
    tab — reports real, client-measured dwell time on the page she was on).
    Unknown shapes degrade to a safe generic string rather than raising.

    ``returning`` (when known) makes the open message say whether this is a
    repeat visitor or a new one — so a scattered one-off hit is distinguishable
    from someone actually coming back. ``None`` keeps the old generic wording.
    """
    event = event or {}
    etype = event.get("type")

    if etype == "open":
        who = ("A returning visitor" if returning is True
               else "A new visitor" if returning is False
               else "GEGYjiji")
        label = _page_label(event.get("page"))
        day_part = f" · day {day}" if day else ""
        vid = str(event.get("visitor_id") or "")[:6]
        vid_part = f" · id {vid}" if vid else ""
        return f"📊 {who} opened Mochi{day_part} · on {label}{vid_part}", "info"

    if etype == "nav":
        section = event.get("section")
        if section:
            return f"↳ {_section_label(section)}", "info"
        to = _page_label(event.get("page"))
        frm = event.get("from")
        if frm:
            return f"{_page_label(frm)} → {to}", "info"
        return f"→ {to}", "info"

    if etype == "action":
        return f"✏️ {event.get('action', 'did something')}", "info"

    if etype == "leave":
        label = _page_label(event.get("page"))
        section = event.get("section")
        where = f"{label} · {_section_label(section)}" if section else label
        return f"↩ left {where} · {_format_dwell(event.get('dwell_ms'))}", "info"

    if etype == "return":
        # Pairs with `leave`. Its absence is what made the log unreadable: two
        # leaves in a row with no open between them looked like a bug.
        label = _page_label(event.get("page"))
        return f"↪ back on {label} · away {_format_dwell(event.get('away_ms'))}", "info"

    return "👀 activity", "info"


_SURFACE_LABELS = {
    "today_focus": "Today's Focus",
    "strongest_picks": "Immediate Best Moves",
    "deadline_calendar": "Deadline Calendar",
    "relationship_targets": "Relationship Targets",
    "opportunity_card": "",
}

_ROLE_LABELS = {
    "quick_win": "Quick Win",
    "high_impact": "High Impact",
    "stretch_goal": "Stretch Goal",
}


def _surface_label(surface) -> str:
    """'today_focus' -> "Today's Focus"; 'browse:institutional' -> 'browse · institutional'."""
    s = str(surface or "")
    if not s:
        return ""
    if s.startswith("browse:"):
        return f"browse · {s.split(':', 1)[1]}"
    return _SURFACE_LABELS.get(s, s.replace("_", " "))


def action_detail(event: dict) -> str:
    """The part of a click line after the action verb: which opportunity, its
    category, and the surface she clicked it on. Surface is the field that was
    missing — an ``open_card`` from Today's Focus and one from the browse list
    were byte-identical in the feed. Never raises; unknown shapes shrink."""
    event = event or {}
    name = event.get("name")
    ctx = event.get("category") or event.get("section") or ""
    where = _surface_label(event.get("surface"))
    role = _ROLE_LABELS.get(str(event.get("role") or ""), "")
    link = event.get("link_type")

    parts = []
    if name and ctx:
        parts.append(f"{name} ({ctx})")
    elif name or ctx:
        parts.append(str(name or ctx))
    if where:
        parts.append(f"{where} / {role}" if role else where)
    if link:
        parts.append(str(link))
    return " · ".join(parts)


def _as_int(value, default=0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def mark_visitor(log: dict, visitor_id) -> tuple[dict, bool]:
    """Track distinct anonymous visitor ids so the feed can say 'returning' vs
    'new'. Returns ``(updated_log, returning)``. A missing id is treated as new
    and not stored. Content-blind: an opaque id, never anything about her."""
    log = dict(log or {})
    if not visitor_id:
        return log, False
    seen = log.get("visitor_ids")
    if not isinstance(seen, list):
        seen = []
    returning = visitor_id in seen
    if not returning:
        seen.append(visitor_id)
        log["visitor_ids"] = seen
    return log, returning


def register_visit(log: dict, today: str) -> tuple[dict, bool, int]:
    """Record a visit. Returns ``(updated_log, notify, day_number)``.

    ``notify`` is True only on the first visit of a given day, so a Discord
    ping fires at most once per day. ``day_number`` is how many distinct days
    she has opened the app (1 on the very first day).
    """
    log = dict(log or {})

    log["total_visits"] = _as_int(log.get("total_visits")) + 1
    if not log.get("first_seen"):
        log["first_seen"] = today

    already_today = log.get("last_notified_date") == today
    if already_today:
        return log, False, _as_int(log.get("days_active"), 1)

    days_active = _as_int(log.get("days_active")) + 1
    log["days_active"] = days_active
    log["last_notified_date"] = today
    return log, True, days_active
