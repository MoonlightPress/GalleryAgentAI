
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found.")

text = path.read_text(encoding="utf-8")

entries = [
    '"publication_frequency_engine.py",',
    '"deadline_extraction_engine.py",',
    '"verified_detail_merger.py",',
    '"detail_confidence_engine.py",',
]

anchor = '"evidence_extraction_engine.py",'

for entry in reversed(entries):
    if entry not in text:
        text = text.replace(anchor, entry + "\n    " + anchor)

path.write_text(text, encoding="utf-8")

print("Patched pipeline with publication/deadline intelligence.")
