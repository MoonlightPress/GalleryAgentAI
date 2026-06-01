
from smart_pipeline_runner import run_pipeline

PIPELINE = [
    "source_registry_builder.py",
    "source_discovery_expansion.py",
    "quality_gate_relaxer.py",
    "pipeline_debug_summary.py",
]

run_pipeline(PIPELINE)
