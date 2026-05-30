
import json
import os
import time
from pathlib import Path

PIPELINE = [
    "python deep_crawl_engine.py",
    "python opportunity_signal_extractor.py",
    "python candidate_quality_gate.py",
    "python approved_candidate_importer.py",
    "python url_verification_engine.py",
    "python evidence_extraction_engine.py",
    "python evidence_score_guard.py",
]

OUT_PATH = "logs/live_refresh_log.txt"

def log(message):
    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)

    with open(OUT_PATH, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def main():

    log("=" * 60)
    log("STARTING LIVE REFRESH")
    log(time.strftime("%Y-%m-%d %H:%M:%S"))

    for cmd in PIPELINE:

        log(f"RUNNING: {cmd}")

        code = os.system(cmd)

        log(f"EXIT CODE: {code}")

    log("LIVE REFRESH COMPLETE")
    log("")

    print(f"Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
