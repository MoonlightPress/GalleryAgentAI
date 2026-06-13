# Maintenance pipeline — the full pipeline MINUS every step that spends money.
# Zero Tavily searches, zero Claude calls: re-verifies URLs and deadlines (plain
# HTTP), re-normalises dates, re-scores, re-buckets, regenerates reports, applies
# feedback/preferences. Safe to schedule weekly without watching a quota.
#
# Discovery of NEW opportunities (the Tavily engines) and fresh email drafts
# (the Claude engines) only happen in run_full_mochi_pipeline.py, run by choice.
from smart_pipeline_runner import run_pipeline
from run_full_mochi_pipeline import PIPELINE, PAID_STEPS

MAINTENANCE = [s for s in PIPELINE if s not in PAID_STEPS]

if __name__ == "__main__":
    print(f"Maintenance pipeline: {len(MAINTENANCE)} free steps "
          f"({len(PIPELINE) - len(MAINTENANCE)} paid steps skipped)")
    run_pipeline(MAINTENANCE)
