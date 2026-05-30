
# Mochi Evidence Upgrade

This package makes recommendations more defensible.

It adds:
- evidence extraction from scraped pages
- claim validation
- evidence quality fields
- evidence-based score caps
- source dossiers for every opportunity

The system now separates:
- inferred fit
- sourced evidence
- missing proof
- verified claims

## Run

```powershell
python patch_pipeline_evidence.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

## Outputs

- `memory/evidence_records.json`
- `reports/evidence_score_guard.md`
- `reports/source_dossiers/`
- `reports/claim_validation_report.md`

## Why this matters

This stops weakly sourced recommendations from becoming inflated 10/10s.
