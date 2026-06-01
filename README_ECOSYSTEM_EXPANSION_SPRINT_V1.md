
# Ecosystem Expansion Sprint v1

This focuses on the categories that are proving useful:

- Galleries
- Open Calls / Competitions
- Art Fairs / Creator Events
- Zines / Art Books

It ignores, for now:

- Publishing
- Cafés
- Licensing

## Requires

Run after:

```powershell
python run_ingress_refinement_sprint_v1.py
```

## Run

```powershell
python run_ecosystem_expansion_sprint_v1.py
```

## Check

```powershell
notepad reports\gallery_ecosystem.md
notepad reports\fair_ecosystem.md
notepad reports\open_call_verification.md
notepad reports\opportunity_rankings.md
notepad reports\ecosystem_battle_plans.md
```

## Outputs

```text
memory/gallery_ecosystem.json
memory/fair_ecosystem.json
memory/verified_open_calls.json
memory/opportunity_rankings.json
memory/ecosystem_battle_plans.json

deploy_data/opportunity_rankings.json
deploy_data/ecosystem_battle_plans.json

reports/gallery_ecosystem.md
reports/fair_ecosystem.md
reports/open_call_verification.md
reports/opportunity_rankings.md
reports/ecosystem_battle_plans.md
```

## Git

```powershell
git add .
git commit -m "add ecosystem expansion for galleries fairs calls and zines"
git push
```
