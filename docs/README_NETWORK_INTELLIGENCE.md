
# Mochi Network Intelligence Upgrade

This upgrade teaches the system to think in ecosystems instead of isolated opportunities.

It adds:
- institution similarity mapping
- adjacent discovery paths
- ecosystem clustering
- recommendation neighborhood analysis
- adjacent-space discovery

Instead of:
"This opportunity is good."

The system now asks:
"What OTHER spaces belong to this ecosystem?"

RUN:

python patch_pipeline_network.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py

DEPLOY:

git add .
git commit -m "add network intelligence"
git push
