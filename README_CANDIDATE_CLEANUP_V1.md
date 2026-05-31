# Candidate Cleanup v1

Cleans extracted business candidates into:
- strong leads
- review leads
- event/article leads
- auto-rejects

## Run

```powershell
python run_candidate_cleanup_v1.py
```

## Check

```powershell
notepad reports\clean_business_candidates.md
notepad reports\clean_candidate_summary.md
notepad memory\clean_business_decisions.json
```

## Review

Change good records in `memory\clean_business_decisions.json` from `"skipped"` to `"approved"`, then run:

```powershell
python ingest_clean_business_decisions.py
python clean_candidate_summary.py
python clean_candidate_dashboard_export.py
```

## Git

```powershell
git add .
git commit -m "add cleanup pipeline for zine business candidates"
git push
```
