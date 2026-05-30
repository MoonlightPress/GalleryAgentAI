
# Mochi Artist Image Review Upgrade

This adds an Artist Images panel.

It lets you:
- view cataloged images
- assign images to portfolio clusters
- edit cluster notes
- generate a visual profile draft
- apply the draft to the master artist profile

## Run

```powershell
python patch_pipeline_artist_review.py
python patch_app_artist_image_review.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

## Workflow

1. Create:

```text
artist_images/
```

2. Put images inside it, optionally in folders.

3. Run:

```powershell
python image_catalog_builder.py
```

4. Use the Artist Images panel.

5. Generate the visual profile draft.

6. Apply it:

```powershell
python artist_profile_apply_draft.py
python run_full_mochi_pipeline.py
```
