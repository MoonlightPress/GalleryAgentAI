
# Zines Into Existing Opportunities v1

This is the correct integration for the current Streamlit app.

It does **not** create a new page.

It converts the curated zine targets into the same compact opportunity format already used by `app.py`.

## Run

From project root:

```powershell
python run_zines_into_existing_opportunities_v1.py
```

## What it reads

```text
memory/zine_category_targets.json
```

or:

```text
deploy_data/zine_category_targets.json
```

## What it writes

```text
memory/compact_opportunities.json
deploy_data/compact_opportunities.json
reports/zine_opportunities_added.md
```

## Result

The existing app loads:

```python
deploy_data/compact_opportunities.json
```

so the zine opportunities should appear in the current opportunity feed.

## Check

```powershell
notepad reports\zine_opportunities_added.md
```

Then run the site the usual way:

```powershell
streamlit run app.py
```

## Upload

```powershell
git add .
git commit -m "add zine targets to existing opportunity feed"
git push
```
