
# Tokyo Zine Business Collector v1

Place-first collector for the zine / artist-book ecosystem.

This does not try to scrape random web pages. It builds:

- known business targets
- discovery search queue
- shop/fair/studio fields
- consignment/submission fields
- zine section business summary
- dashboard exports

## Run

```powershell
python run_tokyo_zine_business_collector_v1.py
```

## Check

```powershell
notepad reports\tokyo_zine_businesses.md
notepad reports\zine_business_section_summary.md
```

## Outputs

```text
memory/tokyo_zine_businesses.json
memory/zine_business_section_summary.json

deploy_data/tokyo_zine_businesses.json
deploy_data/zine_business_section_summary.json

reports/tokyo_zine_businesses.md
reports/zine_business_section_summary.md
```

## Git

```powershell
git add .
git commit -m "add Tokyo zine business collector and section summary"
git push
```
