
# Real Artist Biography Extractor

This patch tries to stop treating awards, institutions, and menu fragments as artists.

It extracts biography-like blocks and filters profiles down to more plausible human artists.

## Run

```powershell
python run_real_artist_biography_extractor.py
```

## Check

```powershell
notepad reports\artist_biographies.md
notepad reports\real_artist_profiles.md
notepad reports\biography_opportunity_summary.md
```

Outputs:

```text
memory/artist_biographies.json
memory/real_artist_profiles.json
reports/artist_biographies.md
reports/real_artist_profiles.md
reports/biography_opportunity_summary.md
```
