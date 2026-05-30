
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")
if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found.")

text = path.read_text(encoding="utf-8")

if '"career_strategy_engine.py",' not in text and "'career_strategy_engine.py'," not in text:
    text = text.replace(
        '"opportunity_status_engine.py",',
        '"career_strategy_engine.py",\n    "opportunity_status_engine.py",'
    )

path.write_text(text, encoding="utf-8")
print("Patched run_full_mochi_pipeline.py")
