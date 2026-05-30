
# Mochi Publication + Deadline Intelligence Upgrade

This improves the weak part of the data:
- deadlines
- submission timing
- how often they publish
- whether details are actually actionable

## Images

Put individual images here:

```text
artist_images/
```

Recommended:

```text
artist_images/architecture_memory/
artist_images/daily_life/
artist_images/printed_matter/
artist_images/uncategorized/
```

Individual images are better than collage/gallery files.

## Run

```powershell
python patch_pipeline_publication_deadline.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

## Outputs

- `memory/publication_frequency.json`
- `memory/deadline_evidence.json`
- `reports/publication_frequency_report.md`
- `reports/deadline_evidence_report.md`
- `reports/detail_confidence_report.md`
- `reports/verified_detail_merge_report.md`

## What changes

Each opportunity gets:
- `publication_frequency`
- `publication_frequency_confidence`
- `deadline_evidence`
- `detail_confidence_score`
- `detail_confidence_grade`
- `detail_missing_fields`

This makes weak opportunities visibly weak and better-documented opportunities more persuasive.
