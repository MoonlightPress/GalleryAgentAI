
# Zine Website Top Section v1

This package gets the Zine / Artist Books category ready for the website.

It does three things:

1. Curates the noisy normalized opportunities into a clean website-facing zine target list.
2. Creates a top-of-section summary with benefits, practical plan, and good samples.
3. Exports JSON for the dashboard.

## Run

```powershell
python run_zine_website_top_section_v1.py
```

## Check

```powershell
notepad reports\zine_category_targets.md
notepad reports\zine_website_top_section.md
```

## Website data

```text
deploy_data/zine_category_targets.json
deploy_data/zine_website_top_section.json
```

## Optional React stub

```text
zine_react_component_stub.jsx
```

Use this as a guide if you want a top-section component.

## Git

```powershell
git add .
git commit -m "add website-ready zine category top section"
git push
```
