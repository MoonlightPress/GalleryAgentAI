
# Opportunity Normalizer v1

Turns noisy extracted candidates into canonical opportunities.

Example:

```text
タコシェ article
TACO ché official site
Tacoche shop page
```

becomes:

```text
Tacoche
```

## Run

```powershell
python run_opportunity_normalizer_v1.py
```

## Check

```powershell
notepad reports\normalized_opportunities.md
notepad reports\opportunity_summary.md
notepad memory\normalized_opportunity_decisions.json
```

## Outputs

```text
memory/normalized_opportunities.json
memory/normalized_opportunity_summary.json
memory/normalized_opportunity_decisions.json

reports/normalized_opportunities.md
reports/opportunity_summary.md

deploy_data/normalized_opportunities.json
deploy_data/normalized_opportunity_summary.json
deploy_data/normalized_opportunity_decisions.json
```

## Git

```powershell
git add .
git commit -m "add opportunity normalization and zine ecosystem summary"
git push
```
