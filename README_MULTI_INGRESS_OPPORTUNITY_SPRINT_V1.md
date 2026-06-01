
# Multi-Ingress Opportunity Sprint v1

Hits four high-signal categories at once:

- Open Calls / Contests
- Art Book & Zine Fairs
- Residencies
- Publishing / Small Press

It reuses the existing opportunity-feed model.

## Run

```powershell
python run_multi_ingress_opportunity_sprint_v1.py
```

## Check

```powershell
notepad reports\multi_ingress_raw_candidates.md
notepad reports\multi_ingress_opportunities_added.md
```

## Output

```text
memory/multi_ingress_seed_queries.json
memory/multi_ingress_raw_candidates.json
memory/compact_opportunities.json

deploy_data/compact_opportunities.json

reports/multi_ingress_seed_queries.md
reports/multi_ingress_raw_candidates.md
reports/multi_ingress_opportunities_added.md
```

## Launch

```powershell
python -m streamlit run app.py
```

## Git

```powershell
git add .
git commit -m "add multi-category opportunity ingress sprint"
git push
```
