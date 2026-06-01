
# Category Metrics v1

Adds concrete metrics to the Zines / Artist Books website section.

It produces:

- category comparison metrics
- zine-specific path score
- cost/timeline estimates
- final website section JSON
- battle plan with phase targets

## Run

```powershell
python run_category_metrics_v1.py
```

## Check

```powershell
notepad reports\category_metrics.md
notepad reports\zine_battle_plan_metrics.md
notepad reports\zine_website_section_final.md
```

## Website data

```text
deploy_data/category_metrics.json
deploy_data/zine_battle_plan_metrics.json
deploy_data/zine_website_section_final.json
```

## Git

```powershell
git add .
git commit -m "add category metrics and final zine website section"
git push
```
