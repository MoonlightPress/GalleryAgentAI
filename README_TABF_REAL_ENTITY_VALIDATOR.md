
# TABF Real Entity Validator

Validates cleaned TABF entities and prepares a contact-harvesting queue.

## Run

```powershell
python run_tabf_real_entity_validator.py
```

## Check

```powershell
notepad reports\tabf_validated_entities.md
notepad reports\tabf_contact_queue.md
notepad reports\tabf_validated_overlap.md
```

Outputs:

```text
memory/tabf_validated_entities.json
memory/tabf_contact_queue.json
memory/tabf_validated_overlap.json
reports/tabf_validated_entities.md
reports/tabf_contact_queue.md
reports/tabf_validated_overlap.md
```
