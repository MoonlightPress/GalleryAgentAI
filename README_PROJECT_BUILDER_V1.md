
# Project Builder v1

This moves the system from:

"Where should she submit?"

to:

"What should she submit?"

## Adds

- `artist_project_builder.py`
- `project_submission_mapper.py`
- `reports/artist_project_concepts.md`
- `reports/project_submission_map.md`

## Run

```powershell
python patch_project_builder_pipeline.py
python run_project_builder_v1.py
```

## Check

```powershell
notepad reports\artist_project_concepts.md
notepad reports\project_submission_map.md
```

Then full pipeline:

```powershell
python run_full_mochi_pipeline.py
```
