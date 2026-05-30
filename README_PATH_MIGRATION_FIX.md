
# Mochi Path Migration Fix

The project organizer moved files into:

- `engines/`
- `ui/`
- `scripts/runners/`
- `scripts/patches/`

Old runners still look for scripts in the root folder.

This patch adds `smart_pipeline_runner.py`, which searches the new folders automatically.

## Run

```powershell
python patch_runners_for_new_paths.py
python run_path_migration_check.py
```

Then try:

```powershell
python run_discovery_expansion.py
```

Then:

```powershell
python run_full_mochi_pipeline.py
```

## If clean

```powershell
git add .
git commit -m "repair paths after project organization"
git push
```
