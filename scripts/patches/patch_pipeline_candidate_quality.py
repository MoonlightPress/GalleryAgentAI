
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found.")

text = path.read_text(encoding="utf-8")

entries = [
    '"candidate_quality_gate.py",',
    '"approved_candidate_importer.py",',
    '"candidate_review_report.py",',
]

anchor = '"candidate_review_importer.py",'

for entry in reversed(entries):
    if entry not in text:
        text = text.replace(anchor, entry + "\n    " + anchor)

path.write_text(text, encoding="utf-8")

print("Patched pipeline with verified candidate importer v2.")

