
# Painting Discovery Package

This fixes the empty "Native Painting / Works on Paper" section.

## Run

```powershell
python patch_painting_discovery_pipeline.py
python run_painting_discovery.py
```

## Check

```powershell
notepad reports\painting_discovery_report.md
notepad reports\painting_quality_gate_report.md
notepad reports\native_painting_action_report.md
notepad reports\native_medium_rankings.md
```

Then:

```powershell
python run_full_mochi_pipeline.py
```
