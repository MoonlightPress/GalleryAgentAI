
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found.")

text = path.read_text(encoding="utf-8")

entries = [
    '"evidence_extraction_engine.py",',
    '"claim_validation_engine.py",',
    '"evidence_score_guard.py",',
    '"source_dossier_generator.py",',
]

anchor = '"fit_audit_engine.py",'

for entry in reversed(entries):
    if entry not in text:
        text = text.replace(anchor, entry + "\n    " + anchor)

path.write_text(text, encoding="utf-8")

print("Patched pipeline with evidence system.")
