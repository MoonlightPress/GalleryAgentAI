
from smart_pipeline_runner import run_pipeline

PIPELINE = [
    "artist_project_builder.py",
    "project_submission_mapper.py",
    "pipeline_debug_summary.py",
]

run_pipeline(PIPELINE)
