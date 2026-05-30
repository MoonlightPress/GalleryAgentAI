
from smart_pipeline_runner import run_pipeline

PIPELINE = [
    "next_project_engine.py",
    "next_email_engine.py",
    "next_exhibition_engine.py",
    "pipeline_debug_summary.py",
]

run_pipeline(PIPELINE)
