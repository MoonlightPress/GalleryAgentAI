
# Source Purity Layer

This fixes the problem where rewritten text makes photography sources look like watercolor opportunities.

## Adds fields

```json
native_medium: painting | photography | mixed | unknown
translation_candidate: true / false
source_purity_score: number
```

## Run

```powershell
python patch_source_purity_pipeline.py
python run_source_purity_upgrade.py
```

## Check

```powershell
notepad reports\source_medium_audit.md
notepad reports\translation_candidates.md
notepad reports\source_purity_enforcer_report.md
notepad reports\native_medium_rankings.md
```

Then:

```powershell
python run_full_mochi_pipeline.py
```
