
# Application Page Crawler v1

This improves precision after submission links are discovered.

## Run

```powershell
python run_application_page_crawler.py
```

## Check

```powershell
Get-Content reports\application_action_report.md | Select-Object -First 180
```

It ranks submission links, filters exhibition/schedule false positives, crawls the best pages, and extracts dates, emails, and requirement terms.
