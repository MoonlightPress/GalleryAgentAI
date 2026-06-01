
from smart_pipeline_runner import run_pipeline

PIPELINE = [
    "opportunity_truth_checker.py",
    "score_explanation_alignment.py",
    "career_path_ranker.py",
    "pipeline_debug_summary.py",
]

run_pipeline(PIPELINE)
