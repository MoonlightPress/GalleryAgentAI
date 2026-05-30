
# Mochi Final Guardrails Fix

This fixes the problem you just saw:

- top 15 all still 10/10
- candidate sample still says `not gated`
- junk candidates still visible in debug output

## Run

```powershell
python patch_final_guard_pipeline.py
python run_full_mochi_pipeline.py
python pipeline_debug_summary.py
notepad reports\pipeline_debug_summary.md
```

## Expected result

Top opportunities should no longer all be 10/10.

Candidate debug should show approved/rejected samples separately.

Junk like Instagram / Pinterest / TikTok should be rejected.

## Deploy

```powershell
git add .
git commit -m "add final score and candidate guardrails"
git push
```
