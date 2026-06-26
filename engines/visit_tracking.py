"""
visit_tracking.py

Usage signal for the app: live "she opened it" / "she moved here" wording, plus
new-vs-returning detection and a running day/visit count. The system is now
flow- and category-aware (which page/section she engages, the *types* of
opportunity she acts on) but remains NAME-BLIND — it never records the specific
named opportunity. The per-session interaction digest is built in
engines/usage_report.py; this module only formats the live ping lines.
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
}


def _page_label(page) -> str:
    if not page:
        return "?"
    return PAGE_LABELS.get(page, str(page).replace("_", " ").title())


def _section_label(section) -> str:
    return SECTION_LABELS.get(section, str(section).replace("_", " ").title())


def describe_event(event: dict, day: int | None = None,
                   returning: bool | None = None) -> tuple[str, str]:
    """Turn a navigation event into ``(message, status)`` for the Discord feed.

    Event types: ``open`` (session start), ``nav`` (page change), ``action``
    (a meaningful action like a profile edit). Unknown shapes degrade to a
    safe generic string rather than raising.

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

    return "👀 activity", "info"


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
