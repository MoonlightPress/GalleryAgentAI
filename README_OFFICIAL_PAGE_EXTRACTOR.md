
# Official Page Extractor

This is the first serious extraction pass for actionable targets.

It checks the top 6 partially researched opportunities and extracts:

- emails
- dates/deadlines
- fees
- requirement signals
- eligibility clues
- relevant contact/application links

## Run

```powershell
python run_official_page_extractor.py
```

## Check

```powershell
notepad reports\official_page_extraction_report.md
notepad reports\actionable_now_refined.md
```

Outputs:

```text
memory/official_page_extractions.json
memory/actionable_targets_refined.json
reports/official_page_extraction_report.md
reports/actionable_now_refined.md
```
