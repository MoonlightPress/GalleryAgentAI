
# Application Link Repair

This fixes the zero-link problem by deriving `submission_links` and `ranked_submission_links` directly from `memory/verified_opportunities.json`, and by adding known application links for key targets.

## Run

```powershell
python run_repaired_application_pipeline.py
```

## Check

```powershell
python -c "import json;d=json.load(open('memory/application_page_results.json',encoding='utf-8'));print(len(d[0].get('ranked_submission_links',[])))"
python -c "import json;d=json.load(open('memory/typed_opportunities.json',encoding='utf-8'));print(len(d[0].get('ranked_submission_links',[])))"
Get-Content reports\application_action_report.md | Select-Object -First 140
```
