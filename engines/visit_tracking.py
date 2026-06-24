"""
visit_tracking.py

Coarse usage signal for the app: decide whether to send a once-per-day "she
opened it" notification, and keep a small running count of days active / total
visits. Deliberately content-blind — it records THAT she visited and how often
she comes back, never what she looks at.
"""
from __future__ import annotations


# Friendly labels for the internal page keys used by the frontend.
PAGE_LABELS = {
    "discover": "Home",
    "observe": "Saffron",
    "refine": "Peppercorn",
}


def _page_label(page) -> str:
    if not page:
        return "?"
    return PAGE_LABELS.get(page, str(page).replace("_", " ").title())


def describe_event(event: dict, day: int | None = None) -> tuple[str, str]:
    """Turn a navigation event into ``(message, status)`` for the Discord feed.

    Event types: ``open`` (session start), ``nav`` (page change), ``action``
    (a meaningful action like a profile edit). Unknown shapes degrade to a
    safe generic string rather than raising.
    """
    event = event or {}
    etype = event.get("type")

    if etype == "open":
        label = _page_label(event.get("page"))
        day_part = f" — day {day}" if day else ""
        return f"📊 GEGYjiji opened Mochi{day_part} (on {label})", "info"

    if etype == "nav":
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
