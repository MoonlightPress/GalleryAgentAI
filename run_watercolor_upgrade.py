
from smart_pipeline_runner import run_pipeline

PIPELINE = [
    "watercolor_artist_profile_engine.py",
    "watercolor_source_expander.py",
    "watercolor_opportunity_converter.py",
    "watercolor_project_rebuilder.py",
    "pipeline_debug_summary.py",
]

run_pipeline(PIPELINE)
