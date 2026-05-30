
# Mochi Safe Filename Collision Fix

This fixes the current error:

```text
TypeError: safe_filename() got an unexpected keyword argument 'max_len'
```

The cause is duplicate/old filename helper code.

## Run

```powershell
python patch_filename_collision.py
python filename_audit.py
python run_report_core_after_filename_fix.py
```

Then run the full pipeline again:

```powershell
python run_full_mochi_pipeline.py
```

## If it works

```powershell
git add .
git commit -m "fix filename helper collision"
git push
```
