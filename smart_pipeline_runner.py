
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Per-run ledger: which steps ran, their status, return code and duration.
# Written after EVERY step so a killed run leaves a usable record — the
# 2026-07-27 run died on Tavily quota mid-pipeline and left nothing; the only
# options were "restart all 101 steps" or hand-surgery. Scott's ask (audit
# 2026-07-06): "know when something goes wrong and where."
LEDGER_PATH = Path("memory/pipeline_ledger.json")

# Concurrency lock. The weekly scheduled task fires at 9:00 AM regardless of
# what else is touching the data — nothing prevented two pipelines (or a
# pipeline and interactive engine runs) interleaving writes to the same JSON
# files, and a torn compact_opportunities.json write was observed 2026-07-28.
# Staleness is age-based, NOT pid-probing: os.kill(pid, 0) on Windows
# TERMINATES the target process, so we never probe pids.
LOCK_PATH = Path("memory/pipeline.lock")
LOCK_STALE_HOURS = 12  # a full paid run takes ~6h; anything older is a corpse


def _acquire_lock(lock_path):
    lock_path = Path(lock_path)
    if lock_path.exists():
        started = None
        try:
            started = datetime.fromisoformat(
                json.loads(lock_path.read_text(encoding="utf-8"))["started_at"])
        except (OSError, json.JSONDecodeError, KeyError, ValueError, TypeError):
            pass  # unreadable lock -> treated as stale below
        if started is not None:
            age_h = (datetime.now() - started).total_seconds() / 3600
            if age_h < LOCK_STALE_HOURS:
                raise SystemExit(
                    f"A pipeline is already running (lock {lock_path}, started "
                    f"{started.isoformat()}). Refusing to run concurrently — "
                    f"interleaved writes corrupt the JSON data files. If that "
                    f"run is dead, delete the lock file and retry.")
            print(f"Stale lock ({age_h:.1f}h old) — replacing it.")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(json.dumps(
        {"pid": os.getpid(), "started_at": datetime.now().isoformat()}),
        encoding="utf-8")


def _release_lock(lock_path):
    try:
        Path(lock_path).unlink()
    except OSError:
        pass

SEARCH_DIRS = [
    Path("."),
    Path("engines"),
    Path("ui"),
    Path("scripts/runners"),
    Path("scripts/patches"),
    Path("reports"),
]

OPTIONAL_SCRIPTS = {
    "strategy_explainer_generator.py",
    "deep_match_scoring_engine.py",
    "rumor_mill_engine.py",
}


def find_script(script, search_dirs=None):
    script_path = Path(script)

    if script_path.exists():
        return script_path

    for folder in (search_dirs or SEARCH_DIRS):
        candidate = folder / script
        if candidate.exists():
            return candidate

    return None


def parse_step(step):
    """Split a PIPELINE entry into (script, args).

    An entry may carry flags — "rumor_mill_engine.py --max 300" — so engine
    options are reachable from inside the pipeline. Resolution and the
    optional-script check always use the script name alone."""
    parts = str(step).split()
    if not parts:
        return "", []
    return parts[0], parts[1:]


def _load_resume_skips(ledger_path):
    """Steps to skip: the ones the last INCOMPLETE run finished. A ledger from
    a run that completed is never resumed-over — that would turn a --resume
    invocation into a silent no-op forever."""
    try:
        prior = json.loads(Path(ledger_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return set()
    if prior.get("completed"):
        return set()
    return {e["step"] for e in prior.get("steps", []) if e.get("status") == "ok"}


def run_pipeline(pipeline, resume=False, ledger_path=LEDGER_PATH,
                 search_dirs=None, lock_path=LOCK_PATH):
    _acquire_lock(lock_path)
    try:
        _run_pipeline_locked(pipeline, resume, ledger_path, search_dirs)
    finally:
        _release_lock(lock_path)


def _run_pipeline_locked(pipeline, resume, ledger_path, search_dirs):
    skip = _load_resume_skips(ledger_path) if resume else set()
    if skip:
        print(f"RESUME: skipping {len(skip)} step(s) the previous run finished")

    ledger = {"started_at": datetime.now().isoformat(),
              "resume": bool(skip), "completed": False, "steps": []}

    def record(step, status, returncode=None, duration=0.0):
        ledger["steps"].append({"step": step, "status": status,
                                "returncode": returncode,
                                "duration_s": round(float(duration), 2)})
        Path(ledger_path).parent.mkdir(parents=True, exist_ok=True)
        Path(ledger_path).write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")

    for step in pipeline:
        script, args = parse_step(step)

        if step in skip:
            print(f"SKIP (resume — already completed): {step}")
            record(step, "skipped_resume")
            continue

        print()
        print("=" * 70)
        print("RUNNING:", step)
        print("=" * 70)

        resolved = find_script(script, search_dirs)

        if resolved is None:
            if script in OPTIONAL_SCRIPTS:
                print(f"SKIP optional missing script: {script}")
                record(step, "skipped_missing_optional")
                continue
            record(step, "failed_missing")
            raise SystemExit(f"FAILED required missing script: {script}")

        t0 = time.monotonic()
        result = subprocess.run([sys.executable, str(resolved), *args])
        elapsed = time.monotonic() - t0

        if result.returncode != 0:
            record(step, "failed", result.returncode, elapsed)
            raise SystemExit(f"FAILED: {script} (see {ledger_path}; "
                             f"rerun with --resume to continue from here)")

        record(step, "ok", 0, elapsed)

    ledger["completed"] = True
    ledger["finished_at"] = datetime.now().isoformat()
    Path(ledger_path).write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")

    print()
    print("PIPELINE COMPLETE")
