
# Report Writer Filename Fix

This fixes:

```text
OSError: Invalid argument: reports\portfolio_pitches\Aperture | Photography.md
```

## Run

```powershell
python patch_report_writer_filenames.py
python run_remaining_reports.py
```

Then:

```powershell
python run_full_mochi_pipeline.py
```

If clean:

```powershell
git add .
git commit -m "fix report writer filenames"
git push
```
