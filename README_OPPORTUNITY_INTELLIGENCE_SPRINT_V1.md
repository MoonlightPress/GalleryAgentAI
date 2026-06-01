
# Opportunity Intelligence Sprint v1

This keeps the path clear:

1. Refine ingress feeds.
2. Canonicalize duplicates.
3. Add gallery discovery.
4. Enrich best records.
5. Add fit/actionability/risk scores.
6. Add enriched opportunities to the existing feed.

## Requires

Run this after:

```powershell
python run_multi_ingress_opportunity_sprint_v1.py
```

## Run

```powershell
python run_opportunity_intelligence_sprint_v1.py
```

## Check

```powershell
notepad reports\canonical_opportunities.md
notepad reports\gallery_candidates.md
notepad reports\enriched_opportunities.md
notepad reports\enriched_opportunities_added.md
```

## Launch

```powershell
python -m streamlit run app.py
```

## Git

```powershell
git add .
git commit -m "add opportunity intelligence sprint with canonicalization enrichment and gallery discovery"
git push
```
