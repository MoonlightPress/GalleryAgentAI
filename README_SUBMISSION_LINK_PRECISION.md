
# Submission Link Precision Patch

Fixes:
- Google Maps links being classified as submission links.
- Social/media links being included.
- Action report only showing counts instead of actual links.

## Run

```powershell
python run_submission_link_precision_patch.py
```

## Check

```powershell
Get-Content reports\actionable_opportunities.md | Select-Object -First 140
```
