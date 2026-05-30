
# Mochi Strategy Homepage Upgrade

Install:
Unzip into C:\ScottStuff\GalleryAgentAI

Run:
python patch_full_pipeline_strategy.py
python patch_app_strategy_homepage.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py

Deploy:
git add app.py strategy_homepage_components.py run_full_mochi_pipeline.py memory deploy_data reports static
git commit -m "add strategic homepage"
git push

Restore if needed:
copy app_before_strategy_homepage_patch.py app.py
