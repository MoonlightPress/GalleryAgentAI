
from smart_pipeline_runner import run_pipeline

PIPELINE = [
    "visual_dna_extractor.py",
    "dna_recommendation_booster.py",
    "dna_project_refiner.py",
    "pipeline_debug_summary.py",
]

run_pipeline(PIPELINE)
