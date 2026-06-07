#!/usr/bin/env python3
"""
Mochi scheduler — runs whichever tier is due based on memory/last_run.json.

Tiers and cadence:
  daily   (>= 20 h)  — deadline checks, status updates, digest
  weekly  (>= 6 d)   — URL verification, submission crawling, light discovery
  monthly (>= 28 d)  — full 74-step pipeline, deep research, expansion

Usage:
  python scripts/scheduler.py
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).parent.parent.resolve()
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from smart_pipeline_runner import run_pipeline  # noqa: E402

LAST_RUN_PATH = ROOT / "memory" / "last_run.json"

THRESHOLDS = {
    "daily":   timedelta(hours=20),
    "weekly":  timedelta(days=6),
    "monthly": timedelta(days=28),
}

# ── Daily: fast status pass, no heavy API calls ──────────────────────────────
DAILY_PIPELINE = [
    "deadline_extraction_engine.py",
    "opportunity_status_engine.py",
    "opportunity_decay_engine.py",
    "daily_digest_report.py",
    "daily_quest_generator.py",
]

# ── Weekly: verification + submission crawling + light discovery ──────────────
WEEKLY_PIPELINE = [
    "targeted_verification_weekly.py",   # HEAD+GET check on all opps (replaces url_verification_engine)
    "deep_verification_agent.py",        # Claude extracts contact/fees/process from venue pages
    "verification_report_engine.py",     # recomputes verification_status from all fields
    "submission_link_hunter.py",
    "submission_strategy_engine.py",
    "submission_timeline_engine.py",
    "painting_discovery_engine.py",
    "discovery_engine.py",
    "rumor_mill_engine.py",
    "research_priority_engine.py",
    "global_research_queue_builder.py",
    "daily_digest_report.py",
    "daily_quest_generator.py",
]

# ── Monthly: full pipeline (run_full_mochi_pipeline.py, all 74 steps) ─────────
MONTHLY_SCRIPT = ROOT / "run_full_mochi_pipeline.py"


# ── last_run helpers ──────────────────────────────────────────────────────────

def load_last_run() -> dict:
    if LAST_RUN_PATH.exists():
        raw = json.loads(LAST_RUN_PATH.read_text(encoding="utf-8"))
        return {k: datetime.fromisoformat(v) for k, v in raw.items()}
    return {}


def save_last_run(last_run: dict) -> None:
    LAST_RUN_PATH.parent.mkdir(parents=True, exist_ok=True)
    LAST_RUN_PATH.write_text(
        json.dumps({k: v.isoformat() for k, v in last_run.items()}, indent=2),
        encoding="utf-8",
    )


def is_due(tier: str, last_run: dict, now: datetime) -> bool:
    if tier not in last_run:
        return True
    return (now - last_run[tier]) >= THRESHOLDS[tier]


# ── tier runner ───────────────────────────────────────────────────────────────

def run_tier(tier: str, last_run: dict, now: datetime) -> bool:
    print(f"\n{'='*70}")
    print(f"SCHEDULER  {tier.upper()} TIER  {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*70}\n")

    try:
        if tier == "monthly":
            result = subprocess.run([sys.executable, str(MONTHLY_SCRIPT)])
            if result.returncode != 0:
                raise SystemExit(f"monthly pipeline exited {result.returncode}")
        elif tier == "weekly":
            run_pipeline(WEEKLY_PIPELINE)
        elif tier == "daily":
            run_pipeline(DAILY_PIPELINE)
    except SystemExit as exc:
        print(f"\nSCHEDULER: {tier} FAILED — {exc}", file=sys.stderr)
        return False

    last_run[tier] = now
    save_last_run(last_run)
    print(f"\nSCHEDULER: {tier} complete — last_run updated")
    return True


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    now = datetime.now()
    last_run = load_last_run()

    # Evaluate all three tiers before running so the summary is printed first
    due = [tier for tier in ("daily", "weekly", "monthly") if is_due(tier, last_run, now)]

    if not due:
        print("SCHEDULER: nothing due.")
        for tier in ("daily", "weekly", "monthly"):
            if tier in last_run:
                elapsed = now - last_run[tier]
                remaining = THRESHOLDS[tier] - elapsed
                hours = remaining.total_seconds() / 3600
                print(f"  {tier:8s}  next due in {hours:.1f}h")
        return

    print(f"SCHEDULER: tiers due — {', '.join(due)}")

    for tier in due:
        # Skip daily/weekly if monthly is about to run — monthly covers both
        if tier in ("daily", "weekly") and "monthly" in due:
            print(f"SCHEDULER: skipping {tier} (monthly run covers it)")
            last_run[tier] = now
            save_last_run(last_run)
            continue
        success = run_tier(tier, last_run, now)
        if not success:
            sys.exit(1)

    print("\nSCHEDULER: all due tiers complete.")


if __name__ == "__main__":
    main()
