
# Mochi Truth Alignment Patch

This fixes the problem where the score says 10/10 but the explanation says "it doesn't fit."

## Adds

- `opportunity_truth_checker.py`
- `score_explanation_alignment.py`
- `career_path_ranker.py`

## Run

```powershell
python patch_truth_alignment_pipeline.py
python run_truth_alignment.py
```

## Check

```powershell
notepad reports\opportunity_truth_checker_report.md
notepad reports\score_explanation_alignment.md
notepad reports\watercolor_career_path_rankings.md
```

Then:

```powershell
python run_full_mochi_pipeline.py
```
