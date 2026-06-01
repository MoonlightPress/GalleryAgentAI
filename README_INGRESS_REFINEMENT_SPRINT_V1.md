
# Ingress Refinement Sprint v1

Focuses on better opportunity data, not visuals.

It does three things:

1. Refines gallery candidates and removes obvious false positives.
2. Expands art fairs / illustration markets / artist markets.
3. Attempts field extraction for deadline, fee, email, and application route.

## Requires

Run after:

```powershell
python run_opportunity_intelligence_sprint_v1.py
```

## Run

```powershell
python run_ingress_refinement_sprint_v1.py
```

## Check

```powershell
notepad reports\gallery_candidates_refined.md
notepad reports\art_fair_candidates.md
notepad reports\verified_opportunity_fields.md
```

## Outputs

```text
memory/gallery_candidates_refined.json
memory/art_fair_candidates.json
memory/verified_opportunity_fields.json

deploy_data/verified_opportunity_fields.json

reports/gallery_candidates_refined.md
reports/art_fair_candidates.md
reports/verified_opportunity_fields.md
```

## Git

```powershell
git add .
git commit -m "refine ingress feeds with gallery quality art fairs and verification fields"
git push
```
