
from smart_pipeline_runner import run_pipeline

PIPELINE = [
    "smart_cover_letter_engine.py",
    "submission_timeline_engine.py",
    "strategy_explainer_generator.py",
    "final_score_guard.py",
    "pipeline_debug_summary.py",
    "opportunity_status_engine.py",
]

run_pipeline(PIPELINE)
