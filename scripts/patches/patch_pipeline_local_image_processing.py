
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found.")

text = path.read_text(encoding="utf-8")

entries = [
    '"local_image_processor.py",',
    '"contact_sheet_builder.py",',
    '"visual_profile_draft_from_images.py",',
]

anchor = '"artist_visual_language_engine.py",'

for entry in reversed(entries):
    if entry not in text:
        text = text.replace(anchor, entry + "\n    " + anchor)

path.write_text(text, encoding="utf-8")
print("Patched pipeline with local image processing.")
