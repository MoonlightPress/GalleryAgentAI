
# Mochi Visual DNA Package

This package adds actual artist-specific image analysis.

## Use

Put images in one of these folders:

```text
images/
artist_images/
data/images/
uploads/images/
```

Then run:

```powershell
python patch_visual_dna_pipeline.py
python run_visual_dna_package.py
```

## Outputs

```text
analysis/image_features.json
memory/artist_dna.json
reports/artist_dna_report.md
reports/dna_recommendation_boost_report.md
reports/dna_project_refinement.md
```

## What it improves

- Extracts basic color, brightness, contrast, and orientation data.
- Builds `artist_dna.json`.
- Boosts recommendations using artist DNA.
- Refines next project concepts using artist DNA.

## Then run full pipeline

```powershell
python run_full_mochi_pipeline.py
```
