
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found.")

text = path.read_text(encoding="utf-8")
old = text

def add_after(anchor, entry):
    global text
    if entry not in text and anchor in text:
        text = text.replace(anchor, anchor + "\n    " + entry)

anchor = '"ecosystem_report.py",'
if anchor not in text:
    anchor = '"strategic_action_report.py",'
if anchor not in text:
    anchor = '"pipeline_debug_summary.py",'

add_after(anchor, '"artist_project_builder.py",')
add_after('"artist_project_builder.py",', '"project_submission_mapper.py",')

if text != old:
    path.with_suffix(".py.before_project_builder_v1").write_text(old, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    print("Patched pipeline with project builder.")
else:
    print("No pipeline changes made.")
