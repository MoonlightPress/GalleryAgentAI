"""Finish tonight's pipeline run if it didn't finish on its own, then publish.

Written 2026-08-20 to be fired blind by a scheduled task at 06:00, hours after
everyone went to bed. It must be safe in all three states it might wake up into:

  1. The run COMPLETED  -> publish if the site is stale, then exit.
  2. The run is STILL RUNNING -> do nothing at all and exit.
  3. The run DIED partway -> resume it, then publish.

State 2 is the dangerous one. The pipeline's own lock goes stale after 12h, so by
06:00 a run that started at 09:49 would look abandoned to it and a second copy
would start on top of the first. So we check the live pid ourselves and refuse.

REGISTERING IT: use the FULL interpreter path, not "python". A scheduled task
does not inherit your PATH, so -Execute "python" fails with 0x80070002 (file not
found) and the task reports success-at-launching-nothing. That happened on the
2026-08-21 05:15 run; it was harmless only because the pipeline had already
finished. Use (Get-Command python).Source.

Publishing is atomic (scp to .new, prove it parses on the server, then mv) and
only happens for a COMPLETED run — half-finished data is un-deduped and
un-bucketed, and stale-but-correct beats fresh-but-broken.
"""
import ctypes
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "memory" / "pipeline.lock"
LOGDIR = ROOT / "logs" / "pipeline_runs"
KEY = ROOT / "Web" / "LightsailDefaultKey-us-east-1.pem"
HOST = "ubuntu@18.206.62.200"
SSH = ["-i", str(KEY), "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=20"]
DEST = "/opt/mochi/deploy_data/compact_opportunities.json"

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001


def say(msg):
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    print(line, flush=True)
    with (LOGDIR / "finish_pipeline_run.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def pid_alive(pid):
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
    if not h:
        return False
    code = ctypes.c_ulong()
    ok = ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(code))
    ctypes.windll.kernel32.CloseHandle(h)
    return bool(ok) and code.value == 259


def latest_log():
    logs = sorted(LOGDIR.glob("full_*.log"), key=lambda p: p.stat().st_mtime)
    return logs[-1] if logs else None


def completed(log):
    return bool(log) and "PIPELINE COMPLETE" in log.read_text(
        encoding="utf-8", errors="replace")


def publish():
    compact = ROOT / "deploy_data" / "compact_opportunities.json"
    r = subprocess.run(["scp", *SSH, str(compact), f"{HOST}:{DEST}.new"],
                       capture_output=True, text=True, timeout=900)
    if r.returncode != 0:
        say(f"scp FAILED: {r.stderr.strip()[:200]}")
        return False
    check = (f"python3 -c 'import json; json.load(open(\"{DEST}.new\"))' "
             f"&& mv {DEST}.new {DEST}")
    r = subprocess.run(["ssh", *SSH, HOST, check],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        say(f"server validate/mv FAILED: {r.stderr.strip()[:200]}")
        return False
    extras = [p for p in (ROOT / "memory" / "career_strategy_report.json",
                          ROOT / "memory" / "peer_artists.json") if p.exists()]
    if extras:
        subprocess.run(["scp", *SSH, *map(str, extras), f"{HOST}:/opt/mochi/memory/"],
                       capture_output=True, text=True, timeout=600)
    say("PUBLISHED — her site now has tonight's data")
    return True


def main():
    LOGDIR.mkdir(parents=True, exist_ok=True)
    say("--- finish_pipeline_run waking up ---")

    # State 2: a run is genuinely still going. Never start a second one.
    if LOCK.exists():
        try:
            pid = json.loads(LOCK.read_text(encoding="utf-8")).get("pid")
        except Exception:
            pid = None
        if pid and pid_alive(pid):
            say(f"pipeline pid {pid} is STILL RUNNING — leaving it alone")
            return
        say("lock present but its pid is dead — clearing stale lock")
        LOCK.unlink(missing_ok=True)

    log = latest_log()

    # State 1: already finished. Publish only if we have not already.
    if completed(log):
        say(f"run already completed ({log.name}) — publishing to be safe")
        publish()
        return

    # State 3: died partway. Resume, holding the machine awake for it.
    say(f"run did NOT complete ({log.name if log else 'no log'}) — resuming")
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    out = LOGDIR / f"full_{stamp}_autoresume.log"
    try:
        with out.open("w", encoding="utf-8") as fh:
            rc = subprocess.run(
                [sys.executable, "run_full_mochi_pipeline.py", "--resume"],
                cwd=str(ROOT), stdout=fh, stderr=subprocess.STDOUT).returncode
        say(f"resume finished rc={rc}, log={out.name}")
        if completed(out):
            publish()
        else:
            say("still not complete — NOT publishing; her site keeps good data")
    finally:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)


if __name__ == "__main__":
    main()
