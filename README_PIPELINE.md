# Mochi Intelligence Pipeline Upgrade

Add these files to project root:
- opportunity_enrichment_pipeline.py
- venue_intelligence_builder.py
- research_queue_report.py
- inquiry_draft_generator.py
- run_intelligence_pipeline.py

Requires previous files:
- opportunity_report_engine.py
- memory/artist_master_profile.json

Run:
```powershell
python run_intelligence_pipeline.py
python -m streamlit run app.py
```

Creates:
- enriched deploy_data/compact_opportunities.json
- venue files in memory/venues/
- research queue in memory/research_queue.json
- readable queue in reports/research_queue.md
- detailed reports in reports/opportunities/
- inquiry drafts in reports/inquiry_drafts/

Deploy:
```powershell
git add app.py deploy_data memory reports *.py
git commit -m "add intelligence pipeline and verification workflow"
git push
```
