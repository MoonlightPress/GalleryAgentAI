
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

text = path.read_text(encoding="utf-8")

entries = [
    '"image_catalog_builder.py",',
    '"portfolio_cluster_report.py",',
    '"artist_dataset_score_engine.py",',
]

anchor = '"artist_profile_scoring_engine.py",'

for entry in reversed(entries):
    if entry not in text:
        text = text.replace(anchor, entry + "\n    " + anchor)

path.write_text(text,encoding="utf-8")

print("Patched artist dataset pipeline.")
