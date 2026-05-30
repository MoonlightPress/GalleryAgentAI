
# Mochi Next Moves Package

This is the practical value layer.

It answers:

- What should she make?
- What should she submit?
- Who should she contact first?
- What are the next visibility targets?

## Adds

- `next_project_engine.py`
- `next_email_engine.py`
- `next_exhibition_engine.py`
- `reports/next_projects.md`
- `reports/next_emails.md`
- `reports/next_exhibitions.md`
- `drafts/next_emails/`

## Run

```powershell
python patch_next_moves_pipeline.py
python run_next_moves.py
```

## Check

```powershell
notepad reports\next_projects.md
notepad reports\next_emails.md
notepad reports\next_exhibitions.md
```

Then:

```powershell
python run_full_mochi_pipeline.py
```
