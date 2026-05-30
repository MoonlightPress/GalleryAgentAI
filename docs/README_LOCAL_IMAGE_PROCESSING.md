
# Mochi Local Image Processing

This processes images you put in:

```text
artist_images/
```

It creates:
- local image catalog
- thumbnails
- contact sheets
- image statistics
- visual profile draft
- artist visual report

## Run while you shower

```powershell
python local_image_processor.py
python contact_sheet_builder.py
python visual_profile_draft_from_images.py
```

Then, after checking the draft:

```powershell
python apply_visual_profile_draft.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

## Outputs

```text
memory/artist_image_analysis/image_catalog.json
memory/artist_image_analysis/image_summary.json
memory/artist_visual_profile_draft.json
reports/contact_sheets/
reports/artist_visual_profile_draft.md
```

This is not full AI image understanding yet. It is the local processing pass that prepares the image set for visual profiling.
