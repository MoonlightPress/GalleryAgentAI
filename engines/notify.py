"""
notify.py

Tiny, dependency-light Discord webhook notifier so an unattended pipeline run
can announce success/failure to a channel. Designed to be a SAFE no-op when no
webhook is configured (env var ``MOCHI_DISCORD_WEBHOOK`` unset), and to never
raise — a monitoring hook must not be able to crash the thing it monitors.

Usage:
    from engines.notify import notify_discord
    notify_discord("Monthly pass finished: 419 opps live", status="success")

Set the webhook once (PowerShell):
    setx MOCHI_DISCORD_WEBHOOK "https://discord.com/api/webhooks/...."
"""
from __future__ import annotations

import os

# Discord embed sidebar colors (decimal RGB).
_COLORS = {
    "info":    0x5865F2,  # blurple
    "success": 0x57F287,  # green
    "failure": 0xED4245,  # red
}
_EMOJI = {"info": "🔵", "success": "✅", "failure": "❌"}


def build_discord_payload(message: str, status: str = "info") -> dict:
    """Build the JSON body for a Discord webhook POST.

    Unknown status strings fall back to 'info' rather than raising.
    """
    if status not in _COLORS:
        status = "info"
    return {
        "username": "Mochi",
        "embeds": [
            {
                "title": f"{_EMOJI[status]} Mochi pipeline",
                "description": message,
                "color": _COLORS[status],
            }
        ],
    }


def notify_discord(
    message: str,
    status: str = "info",
    *,
    webhook_url: str | None = None,
    poster=None,
    timeout: float = 10.0,
) -> bool:
    """Post a message to Discord. Returns True only if it was actually sent.

    No webhook configured -> safe no-op returning False. Any transport error is
    swallowed (returns False) so the calling pipeline never dies on a failed
    notification. ``poster`` is injectable for testing; defaults to
    ``requests.post``.
    """
    if webhook_url is None:
        webhook_url = os.environ.get("MOCHI_DISCORD_WEBHOOK")
    if not webhook_url:
        return False

    if poster is None:
        import requests  # local import keeps the module import-cheap

        poster = requests.post

    payload = build_discord_payload(message, status)
    try:
        resp = poster(webhook_url, json=payload, timeout=timeout)
        return 200 <= getattr(resp, "status_code", 500) < 300
    except Exception:
        return False
