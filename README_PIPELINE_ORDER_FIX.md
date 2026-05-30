
# Pipeline Order Fix

Your `application_page_results.json` and `typed_opportunities.json` had zero ranked links because the application crawler was being run after stale/empty intermediate files.

This patch gives you one correct runner:

```powershell
python run_fixed_application_pipeline.py
```

Then check:

```powershell
python -c "import json;d=json.load(open('memory/application_page_results.json',encoding='utf-8'));print(len(d[0].get('ranked_submission_links',[])))"
python -c "import json;d=json.load(open('memory/typed_opportunities.json',encoding='utf-8'));print(len(d[0].get('ranked_submission_links',[])))"
Get-Content reports\application_action_report.md | Select-Object -First 120
```

Expected: both counts should be nonzero for TOKYO ART BOOK FAIR.
