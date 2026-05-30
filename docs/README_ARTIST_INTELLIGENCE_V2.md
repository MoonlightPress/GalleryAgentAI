
# Artist Intelligence v2

This patch moves the system from "opportunity list" toward "career ecosystem intelligence."

## Adds

- peer artist references
- publisher/platform matches
- ecosystem clusters
- bridge from ecosystems to current opportunities
- `reports/ecosystem_report.md`

## Run

```powershell
python patch_artist_intelligence_v2_pipeline.py
python run_artist_intelligence_v2.py
python run_full_mochi_pipeline.py
```

## Check

```powershell
notepad reports\ecosystem_report.md
notepad reports\career_bucket_report.md
```

## Deploy

```powershell
git add .
git commit -m "add artist ecosystem intelligence"
git push
```
