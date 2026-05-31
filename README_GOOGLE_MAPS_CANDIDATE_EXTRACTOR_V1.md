
# Google Maps Candidate Extractor v1

This fixes the previous problem.

Before:

```text
search query → review queue
```

Now:

```text
search query → extracted business-like candidates → review queue → verified businesses
```

## Run

```powershell
python run_google_maps_candidate_extractor_v1.py
```

## Check

```powershell
notepad reports\extracted_business_candidates.md
notepad memory\extracted_business_decisions.json
```

## Review workflow

1. Open `reports\extracted_business_candidates.md`
2. For each promising candidate, open the Maps check URL.
3. Edit `memory\extracted_business_decisions.json`.
4. Change decision from `skipped` to `approved` or `rejected`.
5. Run:

```powershell
python ingest_extracted_business_decisions.py
python extracted_business_site_export.py
```

## Outputs

```text
memory/extracted_business_candidates.json
memory/extracted_business_decisions.json
memory/verified_zine_businesses.json

reports/extracted_business_candidates.md
reports/verified_zine_businesses.md

deploy_data/extracted_business_candidates.json
deploy_data/verified_zine_businesses.json
```

## Git

```powershell
git add .
git commit -m "add business candidate extractor for zine ecosystem"
git push
```
