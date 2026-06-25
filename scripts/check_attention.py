"""check_attention.py — aggregate everything that needs the maintainer's eyes.

Writes reports/NEEDS_ATTENTION.md when there is anything to act on:
  - open user-reported issues (memory/user_reported_issues.json — her reports)
  - a failed last pipeline run (memory/last_run.json)
Deletes the file when everything is clear, so its existence IS the warning.

Run automatically at the end of run_weekly_pipeline.bat. To act on it:
open Claude Code in this repo and say "work through reports/NEEDS_ATTENTION.md".

It also fires a best-effort Discord alert (via engines/notify.py → MOCHI_DISCORD_WEBHOOK)
when the last pipeline run FAILED, so a silent failure — like last_run.json="failed"
on 2026-06-23, which went unnoticed and let her data go stale — surfaces immediately.
The Discord call is wrapped so a notifier problem can never crash this check.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
OUT = ROOT / "reports" / "NEEDS_ATTENTION.md"


def build_failure_message(last_run: dict) -> str:
    """Human-readable Discord alert text for a failed pipeline run."""
    ts = last_run.get("last_run", "") or "unknown time"
    host = last_run.get("host", "")
    where = f" on {host}" if host else ""
    return (
        f"Mochi pipeline run FAILED{where} at {ts}. "
        f"Her data is going stale — check the newest log in logs/pipeline_runs/ "
        f"and reports/NEEDS_ATTENTION.md."
    )


def alert_on_failed_run(last_run: dict, notifier=None) -> bool:
    """Fire a Discord failure alert if last_run failed. Best-effort: any error is
    swallowed so a notifier problem can NEVER crash the attention check.

    ``notifier`` is injectable for testing; defaults to engines.notify.notify_discord.
    Returns True only if a failure alert was actually dispatched (notifier returned
    truthy), False otherwise (run not failed, or notifier no-op / error).
    """
    if not last_run or last_run.get("status") != "failed":
        return False
    try:
        if notifier is None:
            from engines.notify import notify_discord as notifier
        return bool(notifier(build_failure_message(last_run), status="failure"))
    except Exception:
        return False


def _load_last_run() -> dict:
    p = ROOT / "memory" / "last_run.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


issues = []
p = ROOT / "memory" / "user_reported_issues.json"
if p.exists():
    issues = [r for r in json.loads(p.read_text(encoding="utf-8")) if r.get("status") == "open"]

def main() -> int:
    issues = []
    p = ROOT / "memory" / "user_reported_issues.json"
    if p.exists():
        issues = [r for r in json.loads(p.read_text(encoding="utf-8")) if r.get("status") == "open"]

    last_run = _load_last_run()
    run_failed = last_run.get("status") == "failed"

    # Best-effort Discord alert on a failed run (silent failures let her data go stale).
    alert_on_failed_run(last_run)

    if not issues and not run_failed:
        if OUT.exists():
            OUT.unlink()
        print("check_attention: all clear")
        return 0

    lines = [
        "# NEEDS ATTENTION — generated " + datetime.now().isoformat(timespec="minutes"),
        "",
        "This file exists because something needs a maintainer. To act on it, open",
        "Claude Code in this repo and say: **work through reports/NEEDS_ATTENTION.md**.",
        "When an item is resolved, set its status to 'resolved' in",
        "memory/user_reported_issues.json — this file regenerates on the next check.",
        "",
    ]
    if run_failed:
        lines += ["## Pipeline", "- The last scheduled pipeline run FAILED — check the newest log in logs/pipeline_runs/", ""]
    if issues:
        lines += [f"## Reports from the artist ({len(issues)} open)", ""]
        for r in issues:
            lines += [f"- **{r.get('ts','')[:16]}** · page: {r.get('page','?')} · lang: {r.get('lang','?')} · id `{r.get('id')}`",
                      f"  > {r.get('text','')}", ""]

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"check_attention: WROTE {OUT} ({len(issues)} open issues, run_failed={run_failed})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
