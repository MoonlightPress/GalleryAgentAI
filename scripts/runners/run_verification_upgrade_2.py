
from smart_pipeline_runner import run_pipeline

run_pipeline([
"artist_profile_purge.py",
"opportunity_verification_engine.py",
"bucket_deduplicator.py",
"pipeline_debug_summary.py"
])
