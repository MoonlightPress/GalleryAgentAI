
from smart_pipeline_runner import run_pipeline

PIPELINE = [
    "recommendation_trust_cleaner.py",
    "exclusive_strategy_bucket_engine.py",
    "strategic_action_report.py",
    "pipeline_debug_summary.py",
]

run_pipeline(PIPELINE)
