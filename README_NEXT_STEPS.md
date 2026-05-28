# Mochi Next Upgrade

Files:
- memory/artist_master_profile.json
- memory/artist_research_profile.md
- artist_deep_research_prompt.md
- opportunity_report_engine.py
- upgrade_opportunity_scores.py

Run:
```powershell
python upgrade_opportunity_scores.py
python opportunity_report_engine.py
python -m streamlit run app.py
```

Deploy:
```powershell
git add app.py deploy_data memory opportunity_report_engine.py upgrade_opportunity_scores.py reports artist_deep_research_prompt.md
git commit -m "add artist profile and opportunity report engine"
git push
```
