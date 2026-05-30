
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found.")

text = path.read_text(encoding="utf-8")

entries = [
    '"source_registry_merger.py",',
    '"source_type_weight_engine.py",',
    '"source_coverage_report.py",',
]

anchor = '"deep_crawl_engine.py",'

for entry in reversed(entries):
    if entry not in text:
        text = text.replace(anchor, entry + "\n    " + anchor)

path.write_text(text, encoding="utf-8")
print("Patched pipeline with source expansion.")

