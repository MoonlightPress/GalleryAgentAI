
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

anchor = '"strategic_action_report.py",'
if anchor not in text:
    anchor = '"ecosystem_report.py",'
if anchor not in text:
    anchor = '"pipeline_debug_summary.py",'

add_after(anchor, '"next_project_engine.py",')
add_after('"next_project_engine.py",', '"next_email_engine.py",')
add_after('"next_email_engine.py",', '"next_exhibition_engine.py",')

if text != old:
    path.with_suffix(".py.before_next_moves").write_text(old, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    print("Patched pipeline with next moves engines.")
else:
    print("No pipeline changes made.")
