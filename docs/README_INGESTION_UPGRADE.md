
# Mochi Ingestion Upgrade

This is the important next step.

It adds:
- web page fetching
- source scraping
- candidate extraction
- URL verification
- score sanity caps
- artist visual profile ingestion template

## Install

Unzip into:

```text
C:\ScottStuff\GalleryAgentAI
```

## Run

```powershell
python patch_pipeline_ingestion.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

## Important

The scraper is conservative. It creates unverified candidates and caps weakly verified scores.

It will not magically make perfect data. It gives you:
- new source pages
- new candidates
- verification reports
- score sanity reports

## Visual profile workflow

1. Give ChatGPT a batch of her images.
2. Ask for a visual profile.
3. Paste the result into `artist_visual_profile_template.json`.
4. Run:

```powershell
python visual_profile_ingester.py
python run_full_mochi_pipeline.py
```

## Reports created

- `reports/url_verification_report.md`
- `reports/score_sanity_report.md`
- `reports/artist_visual_profile_report.md`
- `ingestion/scraped_pages.json`
- `ingestion/opportunity_candidates.json`
