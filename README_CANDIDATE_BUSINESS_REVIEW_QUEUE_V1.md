
# Candidate Business Review Queue v1

This creates a fast review workflow for turning search queries into verified zine / artist-book business records.

## Run

```powershell
python run_candidate_business_review_queue_v1.py
```

## Check

```powershell
notepad reports\candidate_business_review_queue.md
notepad memory\candidate_business_decisions.json
notepad reports\verified_zine_businesses.md
```

## Workflow

1. Open `reports/candidate_business_review_queue.md`
2. Open the Maps/Search links.
3. Fill approved businesses into:

```text
memory/candidate_business_decisions.json
```

4. Run:

```powershell
python approved_business_ingest.py
python business_review_dashboard_export.py
```

## Decision values

```text
approved
rejected
skipped
```

## Outputs

```text
memory/candidate_business_review_queue.json
memory/candidate_business_decisions.json
memory/verified_zine_businesses.json

deploy_data/candidate_business_review_queue.json
deploy_data/verified_zine_businesses.json

reports/candidate_business_review_queue.md
reports/verified_zine_businesses.md
```

## Git

```powershell
git add .
git commit -m "add candidate business review queue for zine ecosystem"
git push
```
