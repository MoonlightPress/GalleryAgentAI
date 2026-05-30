
# Mochi Global Opportunity Upgrade

This package adds international/global opportunities and two new homepage sections:

- Global Targets
- Publication Targets

It also adds:
- global opportunity seed data
- global expansion script
- global research queue
- strategy feed rebalance

## Install

Unzip into:

```text
C:\ScottStuff\GalleryAgentAI
```

## Run

```powershell
python patch_full_pipeline_global.py
python patch_strategy_homepage_global_sections.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

## Deploy

```powershell
git add app.py deploy_data memory reports *.py global_opportunity_seeds.json strategy_homepage_components.py
git commit -m "add global opportunity expansion"
git push
```

## Restore local opportunity file if needed

```powershell
copy deploy_data\compact_opportunities_before_global_expansion.json deploy_data\compact_opportunities.json
```
