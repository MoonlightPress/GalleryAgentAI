
# Opportunity Type Patch

Adds practical opportunity categories:

- gallery_submission
- open_exhibition
- competition
- book_fair
- zine_fair
- publication
- residency
- contact_only
- unknown

## Run

```powershell
python run_opportunity_type_patch.py
```

## Check

```powershell
Get-Content reports\opportunity_buckets.md | Select-Object -First 160
Get-Content reports\application_action_report.md | Select-Object -First 120
```
