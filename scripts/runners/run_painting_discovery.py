
from smart_pipeline_runner import run_pipeline

PIPELINE=[
    "painting_discovery_engine.py",
    "painting_quality_gate.py",
    "painting_action_report.py",
    "native_medium_ranker.py",
    "pipeline_debug_summary.py"
]

run_pipeline(PIPELINE)
