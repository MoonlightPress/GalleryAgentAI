
# Mochi Project Organizer

Run:

```powershell
python run_project_organizer.py
```

Check:

```powershell
notepad reports\project_organization_report.md
```

Find files later:

```powershell
python project_file_finder.py discovery
python project_file_finder.py compact
python project_file_finder.py visual
```

Undo if needed:

```powershell
python restore_organized_files.py
```

This moves misplaced Python files out of `reports/`, moves runner scripts into `scripts/runners/`, moves patch/fix scripts into `scripts/patches/`, archives zips, and creates root shortcuts for common runners.
