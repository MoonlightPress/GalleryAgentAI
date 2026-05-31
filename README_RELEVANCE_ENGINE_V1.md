
# Relevance Engine v1

Fixes the main scoring flaw: keyword density was making garbage entities look important.

## Run

```powershell
python run_relevance_engine_v1.py
```

## Check

```powershell
notepad reports\relevance_scores.md
notepad reports\opportunity_evidence_cards.md
```

Outputs:

```text
memory/relevance_scores.json
memory/opportunity_evidence_cards.json
deploy_data/relevance_scores.json
deploy_data/opportunity_evidence_cards.json
reports/relevance_scores.md
reports/opportunity_evidence_cards.md
```
