"""
backups.py

Timestamped snapshots of the artist's edited data files. Every time she saves
(her statement, goals, answers, exhibition/career logs), we drop a dated copy
into memory/backups/ so an edit can never be silently lost — to a bad deploy, a
corrupt write, or future "serious work" on the project.

Snapshots are best-effort: a backup failure must never block her save.
"""
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


def backup_filename(name: str, now: datetime) -> str:
    """`peppercorn_profile.json` + a time -> `peppercorn_profile.<UTC>.json`."""
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    if "." in name:
        stem, ext = name.rsplit(".", 1)
        return f"{stem}.{stamp}.{ext}"
    return f"{name}.{stamp}"


def snapshot(src, backups_dir, now: datetime) -> Path | None:
    """Copy ``src`` into ``backups_dir`` under a timestamped name.

    Returns the backup path, or None if the source doesn't exist or the copy
    fails for any reason (never raises).
    """
    try:
        src = Path(src)
        if not src.exists():
            return None
        backups_dir = Path(backups_dir)
        backups_dir.mkdir(parents=True, exist_ok=True)
        dest = backups_dir / backup_filename(src.name, now)
        shutil.copy2(src, dest)
        return dest
    except Exception:
        return None
