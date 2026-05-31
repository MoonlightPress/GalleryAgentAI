
# Tokyo Zine Crawler v1

Single-purpose crawler for the Book / Zine Path.

It searches for:

- zine shops
- artist-book stores
- photobook stores
- independent bookstores
- risograph studios
- zine fairs
- small press publishers
- consignment targets

## Run

```powershell
python run_tokyo_zine_crawler_v1.py
```

## Check

```powershell
notepad reports\tokyo_zine_ecosystem.md
notepad reports\zine_section_summary.md
```

## Outputs

```text
memory/tokyo_zine_ecosystem.json
memory/zine_section_summary.json

deploy_data/tokyo_zine_ecosystem.json
deploy_data/zine_section_summary.json

reports/tokyo_zine_ecosystem.md
reports/zine_section_summary.md
```

## Git

```powershell
git add .
git commit -m "add Tokyo zine ecosystem crawler and section summary"
git push
```

## Warning

Search-discovered entries need human verification. The crawler intentionally prioritizes coverage over perfect certainty.
