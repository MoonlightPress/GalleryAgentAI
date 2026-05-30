
# Backup and Encoding Patch

This package does three things:

1. Fixes mojibake risk by setting request encoding from `apparent_encoding`.
2. Creates a deployment readiness audit.
3. Adds a Git backup helper.

## Run

```powershell
python run_backup_and_encoding_patch.py
python project_backup_git_helper.py
git push
```

## Then rerun the working application sequence

```powershell
python run_real_verification.py
python application_link_repair.py
python application_page_crawler.py
python opportunity_type_classifier.py
python application_action_report.py
```

## Check

```powershell
Get-Content reports\application_action_report.md | Select-Object -First 80
notepad reports\deployment_readiness_audit.md
notepad reports\git_backup_report.md
```

## Online deployment note

Deploy the dashboard first. Do not depend on live crawling online until the crawler has caching, rate limits, and safe retry handling.
