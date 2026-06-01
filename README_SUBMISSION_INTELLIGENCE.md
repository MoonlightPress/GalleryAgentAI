
# Submission Intelligence Package

This reads discovered submission/action pages and extracts:

- page title
- text excerpt
- emails
- date candidates
- deadline guess
- fee candidates
- requirements
- artist readiness score

## Run

```powershell
python run_submission_intelligence.py
```

## Check

```powershell
notepad reports\submission_intelligence_report.md
notepad reports\artist_readiness_report.md
```

This depends on the previous link-saver package having already generated:

```text
memory/submission_targets.json
```
