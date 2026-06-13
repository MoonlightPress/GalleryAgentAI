"""check_attention.py — aggregate everything that needs the maintainer's eyes.

Writes reports/NEEDS_ATTENTION.md when there is anything to act on:
  - open user-reported issues (memory/user_reported_issues.json — her reports)
  - a failed last pipeline run (memory/last_run.json)
Deletes the file when everything is clear, so its existence IS the warning.

Run automatically at the end of run_weekly_pipeline.bat. To act on it:
open Claude Code in this repo and say "work through reports/NEEDS_ATTENTION.md".
"""
import json
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent.parent
OUT = ROOT / "reports" / "NEEDS_ATTENTION.md"

issues = []
p = ROOT / "memory" / "user_reported_issues.json"
if p.exists():
    issues = [r for r in json.loads(p.read_text(encoding="utf-8")) if r.get("status") == "open"]

run_failed = False
p = ROOT / "memory" / "last_run.json"
if p.exists():
    run_failed = json.loads(p.read_text(encoding="utf-8")).get("status") == "failed"

if not issues and not run_failed:
    if OUT.exists():
        OUT.unlink()
    print("check_attention: all clear")
    raise SystemExit(0)

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
