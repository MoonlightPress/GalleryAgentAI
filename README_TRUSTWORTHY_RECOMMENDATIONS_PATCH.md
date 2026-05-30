
# Trustworthy Recommendations Patch

This patch improves the recommendation output rather than adding another engine.

## It does

- Removes legacy illustrator/painter wording from opportunity text.
- Hides junk sources like Facebook / Instagram / Pinterest / Continue Reading.
- Forces each opportunity into one primary strategic bucket.
- Generates `reports/strategic_action_report.md`.
- Stops the same five opportunities from dominating every category.

## Run

```powershell
python patch_trustworthy_recommendations_pipeline.py
python run_trustworthy_recommendations_patch.py
```

## Check

```powershell
notepad reports\strategic_action_report.md
notepad reports\recommendation_trust_cleaner_report.md
```

Then:

```powershell
python run_full_mochi_pipeline.py
```
