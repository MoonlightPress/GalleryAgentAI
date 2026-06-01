
# Publishing Into Existing Opportunities v1

Adds a Publishing / Artist Books section using the same model as the zine section.

It does not create a separate page.

It:
1. Adds publishing targets to `compact_opportunities.json`
2. Adds `ui/publishing_opportunity_section.py`
3. Patches `app.py` to render publishing after zines

## Run

```powershell
python run_publishing_into_existing_opportunities_v1.py
```

## Launch

```powershell
python -m streamlit run app.py
```

## Check

```powershell
notepad reports\publishing_opportunities_added.md
```

## Git

```powershell
git add .
git commit -m "add publishing targets to existing opportunity feed"
git push
```
