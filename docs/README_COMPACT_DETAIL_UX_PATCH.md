
# Mochi Compact Detail UX Patch

This patch improves the opportunity detail view.

## Adds

- compact 3-panel detail renderer
- compact score/verification metrics
- career-bucket badges
- source/open button
- micro outreach draft
- better scanability
- less scrolling

## Run

```powershell
python run_compact_detail_patch.py
python -m streamlit run app.py
```

## Check

Click an opportunity and confirm the detail area is now:

- header
- metrics row
- three compact panels:
  - Venue / Source
  - Submission / Action
  - Why This Fits

## Deploy

```powershell
git add .
git commit -m "add compact opportunity detail view"
git push
```
