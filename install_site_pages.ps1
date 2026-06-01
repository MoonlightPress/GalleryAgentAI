
# Run from your project root.
# Adjust $componentsDir and $dataDir if your project uses different folders.

$componentsDir = "src\components\career"
$dataDir = "deploy_data"

New-Item -ItemType Directory -Force -Path $componentsDir | Out-Null
New-Item -ItemType Directory -Force -Path $dataDir | Out-Null

Copy-Item "CareerPathsHome.jsx" "$componentsDir\CareerPathsHome.jsx" -Force
Copy-Item "ZineCategoryPage.jsx" "$componentsDir\ZineCategoryPage.jsx" -Force
Copy-Item "PublishingCategoryPage.jsx" "$componentsDir\PublishingCategoryPage.jsx" -Force

python publishing_category_seed.py

Copy-Item "memory\publishing_category_targets.json" "$dataDir\publishing_category_targets.json" -Force
Copy-Item "memory\publishing_website_section.json" "$dataDir\publishing_website_section.json" -Force

Write-Host "Installed career site components and publishing data."
Write-Host "Now import the components into your app/router."
