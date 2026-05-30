
# Config Path Repair

The organizer moved JSON config files into `data/config/`.

Older engines still expect files like:

- `source_targets.json`
- `global_photo_source_pack.json`

in the root folder.

This patch copies needed configs back to root so the existing pipeline works again.

## Run

```powershell
python run_config_path_repair.py
python run_discovery_expansion.py
python run_full_mochi_pipeline.py
```

## Check

```powershell
notepad reports\config_path_repair_report.md
notepad reports\pipeline_debug_summary.md
```
