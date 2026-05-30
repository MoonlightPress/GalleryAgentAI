
# Mochi Visual Profile + Career Buckets

This package adds the visual profile from the Instagram/image review and creates strategic opportunity buckets.

## Adds

- `artist_visual_profile_v1.py`
- `opportunity_differentiation_engine.py`
- `career_bucket_report.py`
- `project_folder_audit.py`
- `patch_visual_profile_bucket_pipeline.py`
- `run_visual_profile_bucket_upgrade.py`

## What it does

- writes Nin's visual profile into JSON automatically
- adds `visual_fit_score`
- adds `career_buckets`
- adds `primary_bucket`
- adds `differentiated_score`
- creates `memory/opportunity_buckets.json`
- creates `reports/career_bucket_report.md`
- creates `reports/project_folder_audit.md`

## Run

```powershell
python patch_visual_profile_bucket_pipeline.py
python run_visual_profile_bucket_upgrade.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

## Check

```powershell
notepad reports\career_bucket_report.md
notepad reports\project_folder_audit.md
notepad reports\pipeline_debug_summary.md
```

## Deploy

```powershell
git add .
git commit -m "add visual profile and career buckets"
git push
```
