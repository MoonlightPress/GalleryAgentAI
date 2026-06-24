"""
regen.py

Fire-and-forget launcher for the email-draft writer. Used by the API to
auto-regenerate her drafts the moment she edits her profile, without blocking
the save request and without ever letting a launch failure surface to her.

Why a subprocess (not an in-process call): the writer makes a series of Claude
API calls that can take a while; spawning it detached keeps the save instant and
isolates a crash from the web server.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

_WRITER = "engines/ibm_email_writer.py"
_DEFAULT_LOG = "reports/regen_last_run.log"


def build_regen_command(limit: int | None = None) -> list[str]:
    """The command that runs the draft writer under the current interpreter."""
    cmd = [sys.executable, _WRITER]
    if limit is not None:
        cmd += ["--limit", str(limit)]
    return cmd


def spawn_draft_regen(
    *,
    limit: int | None = None,
    cwd: str | None = None,
    log_path: str | None = None,
    runner=None,
) -> bool:
    """Launch the draft writer in the background. Returns True if it was spawned.

    Any failure to spawn is swallowed (returns False) so an auto-regen can never
    break the save it was triggered by. Output is appended to a log file so an
    unattended run leaves a trace.
    """
    if runner is None:
        runner = subprocess.Popen

    try:
        log_target = log_path if log_path is not None else _DEFAULT_LOG
        log_dir = os.path.dirname(log_target)
        if log_dir:
            Path(log_dir).mkdir(parents=True, exist_ok=True)
        log_fh = open(log_target, "a", encoding="utf-8")
        runner(
            build_regen_command(limit),
            cwd=cwd,
            stdout=log_fh,
            stderr=subprocess.STDOUT,
        )
        return True
    except Exception:
        return False
