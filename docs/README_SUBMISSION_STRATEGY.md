
# Mochi Submission Strategy Upgrade

This upgrade teaches the system:
- HOW to approach each opportunity
- what emotional tone to use
- what kind of submission strategy fits
- how aggressive or restrained outreach should be

It adds:
- strategy modeling
- tone modeling
- smart cover letter generation
- submission pacing
- strategic outreach sequencing

RUN:

python patch_pipeline_submission_strategy.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py

DEPLOY:

git add .
git commit -m "add submission strategy intelligence"
git push
