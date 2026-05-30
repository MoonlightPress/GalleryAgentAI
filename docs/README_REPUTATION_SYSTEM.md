
# Mochi Reputation System Upgrade

This upgrade models:
- artistic reputation
- momentum waves
- social proof
- downstream legitimacy

The system now thinks about:
- how opportunities affect future opportunities
- how small wins compound
- what creates artistic credibility
- which spaces create downstream trust

It adds:
- reputation modeling
- momentum waves
- social proof strategy
- prestige compounding logic

RUN:

python patch_pipeline_reputation.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py

DEPLOY:

git add .
git commit -m "add reputation system"
git push
