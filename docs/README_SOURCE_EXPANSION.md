
# Mochi Source Expansion Pack

This adds a broader discovery base.

It includes:
- photobook publishers
- artist book fairs
- photo open calls
- Japan art-book spaces
- source coverage reporting
- source type score weighting

Run:

```powershell
python patch_pipeline_source_expansion.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

Outputs:
- `reports/source_coverage_report.md`
