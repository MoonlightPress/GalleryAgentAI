
# Mochi Fit Audit Upgrade

This adds a recommendation diagnostic layer.

It answers:
- Why is this high?
- Is the score justified?
- Is this inflated?
- Is this underrated?
- What evidence supports the recommendation?
- What fields are still missing?

## Install

Unzip into:

```text
C:\ScottStuff\GalleryAgentAI
```

## Run

```powershell
python patch_pipeline_fit_audit.py
python patch_app_fit_audit.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

## Deploy

```powershell
git add .
git commit -m "add fit audit diagnostics"
git push
```
