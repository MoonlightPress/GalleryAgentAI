
# Mochi Relationship Upgrade

Adds:
- relationship memory
- curator tracking
- momentum scoring
- CRM progression

INSTALL:

Unzip into:

C:\ScottStuff\GalleryAgentAI

RUN:

python patch_pipeline_relationship.py
python patch_app_relationship.py

python run_full_mochi_pipeline.py

python -m streamlit run app.py

DEPLOY:

git add .
git commit -m "add relationship momentum system"
git push
