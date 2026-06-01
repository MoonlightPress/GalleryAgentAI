
from smart_pipeline_runner import run_pipeline

PIPELINE = [
    "source_medium_classifier.py",
    "translation_candidate_detector.py",
    "source_purity_enforcer.py",
    "native_medium_ranker.py",
    "pipeline_debug_summary.py",
]

run_pipeline(PIPELINE)
