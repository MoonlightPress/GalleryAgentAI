
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found.")

text = path.read_text(encoding="utf-8")

entry = '"fit_audit_engine.py",'
anchor = '"strategy_explainer_generator.py",'

if entry not in text:
    text = text.replace(anchor, entry + "\n    " + anchor)

path.write_text(text, encoding="utf-8")
print("Patched pipeline with fit audit.")
