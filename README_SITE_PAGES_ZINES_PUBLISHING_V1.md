
# Site Pages: Zines + Publishing v1

This package puts the Zine section on the site and adds a first Publishing section.

## Run from project root

Unzip this package into your project root, then run:

```powershell
.\install_site_pages.ps1
```

## Add to app

Use:

```text
site_integration_example.jsx
```

as the pattern for your actual router/page.

Components copied to:

```text
src/components/career/CareerPathsHome.jsx
src/components/career/ZineCategoryPage.jsx
src/components/career/PublishingCategoryPage.jsx
```

Publishing data generated to:

```text
deploy_data/publishing_category_targets.json
deploy_data/publishing_website_section.json
```

Existing required zine data:

```text
deploy_data/category_metrics.json
deploy_data/zine_website_section_final.json
```

## Upload

```powershell
.\upload_git_commands.ps1
```
