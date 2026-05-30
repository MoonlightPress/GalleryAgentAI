
# Mochi Pipeline Compatibility Fix

This fixes the current error:

```text
can't open file deep_match_scoring_engine.py
```

The pipeline referenced an old script name. This patch makes the runner safer:

- skips missing optional scripts
- uses `artist_profile_scoring_engine.py` if `deep_match_scoring_engine.py` is missing
- keeps required scripts strict
- provides a core-only runner if the full pipeline is still messy

## Run

```powershell
python patch_pipeline_compatibility.py
python run_full_mochi_pipeline.py
python pipeline_debug_summary.py
notepad reports\pipeline_debug_summary.md
```

## If full pipeline is still too messy

```powershell
python run_required_core_only.py
python -m streamlit run app.py
```

## Deploy if good

```powershell
git add .
git commit -m "fix pipeline compatibility"
git push
```
