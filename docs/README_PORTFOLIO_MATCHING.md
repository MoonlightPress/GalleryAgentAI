
# Mochi Portfolio Matching Upgrade

This upgrade matches opportunities against specific bodies of work.

Instead of:
"Send her portfolio."

The system now asks:
"Which body of work should she send?"

It adds:
- portfolio body definitions
- opportunity-to-portfolio matching
- body-of-work recommendations
- generated portfolio pitch reports
- Portfolio Matching UI panel

## Run

```powershell
python patch_pipeline_portfolio_matching.py
python patch_app_portfolio_matching.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

## Deploy

```powershell
git add .
git commit -m "add portfolio matching system"
git push
```
