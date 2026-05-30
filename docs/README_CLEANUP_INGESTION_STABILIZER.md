
# Mochi Cleanup + Ingestion Stabilizer

Fixes:
- Windows filename crash from `Aperture | Photography`
- weak candidate filtering
- junk candidate links
- unsafe pipeline order

Run:

```powershell
python patch_safe_filenames.py
python patch_pipeline_cleanup_stabilizer.py
python run_ingestion_only.py
python run_scoring_only.py
python run_reports_only.py
python -m streamlit run app.py
```

Deploy:

```powershell
git add .
git commit -m "stabilize ingestion and pipeline"
git push
```
