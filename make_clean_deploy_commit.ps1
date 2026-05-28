python project_health_check.py
python run_full_mochi_pipeline.py
python safe_deploy_check.py

git status
git add app.py deploy_data memory reports static *.py project_manifest.json .streamlit/config.toml
git commit -m "update mochi intelligence app"
git push
