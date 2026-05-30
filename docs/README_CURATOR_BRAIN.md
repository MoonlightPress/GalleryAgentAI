
# Mochi Curator Brain Upgrade

This upgrade pushes the system from:
- recommendation engine

toward:
- curatorial intelligence

It adds:
- curator personality modeling
- long-term career path analysis
- serendipity recommendations
- anti-commercial filtering
- trajectory thinking

The system now asks:
"What artistic world does this belong to?"
and:
"What kind of artist career does this help build?"

RUN:

python patch_pipeline_curator_brain.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py

DEPLOY:

git add .
git commit -m "add curator brain intelligence"
git push
