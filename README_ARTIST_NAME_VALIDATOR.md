
# Artist Name Validator v1

Cleans artist/entity data by rejecting awards, institutions, locations, sentence fragments, and fake names.

## Run

```powershell
python run_artist_name_validator.py
```

## Check

```powershell
notepad reports\artist_name_validation_report.md
notepad reports\validated_opportunity_credibility.md
```

Outputs:

```text
memory/validated_artist_biographies.json
memory/validated_artist_profiles.json
memory/validated_opportunity_credibility.json
reports/artist_name_validation_report.md
reports/validated_opportunity_credibility.md
```
