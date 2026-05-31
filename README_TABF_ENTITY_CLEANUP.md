
# TABF Entity Cleanup

Cleans noisy TABF entities and ranks publishers / book ecosystem signals.

## Run

```powershell
python run_tabf_entity_cleanup.py
```

## Check

```powershell
notepad reports\tabf_clean_entities.md
notepad reports\tabf_ranked_publishers.md
notepad reports\tabf_nin_overlap.md
```

Outputs:

```text
memory/tabf_clean_entities.json
memory/tabf_ranked_publishers.json
memory/tabf_nin_overlap.json
reports/tabf_clean_entities.md
reports/tabf_ranked_publishers.md
reports/tabf_nin_overlap.md
```
