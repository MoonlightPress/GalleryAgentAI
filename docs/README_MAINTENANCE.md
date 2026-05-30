# Mochi Maintenance Tools

First run:

```powershell
python project_health_check.py
python safe_deploy_check.py
```

Clean deploy:

```powershell
.\make_clean_deploy_commit.ps1
```

Archive junk later:

```powershell
python archive_unused_files.py
```

This does not delete files. It moves junk into `_archive/<timestamp>/`.
