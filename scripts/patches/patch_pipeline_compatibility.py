
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found.")

old = path.read_text(encoding="utf-8")
path.with_suffix(".py.before_compatibility_fix").write_text(old, encoding="utf-8")

start = old.find("PIPELINE = [")
end = old.find("]", start)

if start == -1 or end == -1:
    raise SystemExit("Could not find PIPELINE list.")

pipeline_block = old[start:end + 1]

new_text = (
    "from safe_pipeline_runner import run_pipeline\n\n"
    + pipeline_block
    + "\n\nrun_pipeline(PIPELINE)\n"
)

path.write_text(new_text, encoding="utf-8")

print("Patched run_full_mochi_pipeline.py to use safe_pipeline_runner.")
print("Backup saved as run_full_mochi_pipeline.py.before_compatibility_fix")
