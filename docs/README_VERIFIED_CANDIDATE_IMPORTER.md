
# Mochi Verified Candidate Importer v2

This improves the ingestion gate.

It adds:
- candidate quality scoring
- fit keyword checks
- reject keyword checks
- deduplication
- approved candidate import
- rejected candidate log
- review report

## Run

```powershell
python patch_pipeline_candidate_quality.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

## Outputs

- `ingestion/approved_candidates.json`
- `ingestion/rejected_candidates.json`
- `reports/candidate_review_report.md`

This prevents weak scraped pages from polluting the live app.
