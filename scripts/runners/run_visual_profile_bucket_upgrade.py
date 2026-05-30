
from smart_pipeline_runner import run_pipeline

PIPELINE = [
    "artist_visual_profile_v1.py",
    "visual_profile_ingester.py",
    "opportunity_differentiation_engine.py",
    "career_bucket_report.py",
    "final_score_guard.py",
    "pipeline_debug_summary.py",
    "project_folder_audit.py",
]

run_pipeline(PIPELINE)
