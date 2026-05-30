
# Mochi Live Refresh + Visual Similarity Upgrade

This improves:
- live ingestion freshness
- visual similarity ranking
- stale opportunity decay
- institution graphing

It adds:
- live refresh scheduler
- visual similarity scoring
- institution reputation graph
- stale opportunity decay

RUN:

python patch_pipeline_live_refresh.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py

OPTIONAL LIVE REFRESH:

python live_refresh_scheduler.py
