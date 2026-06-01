
from pathlib import Path

path=Path("run_full_mochi_pipeline.py")
if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found")

text=path.read_text(encoding="utf-8")
old=text

def add_after(anchor,entry):
    global text
    if entry not in text and anchor in text:
        text=text.replace(anchor, anchor+"\n    "+entry)

anchor='"source_purity_enforcer.py",'
if anchor not in text:
    anchor='"watercolor_source_expander.py",'
if anchor not in text:
    anchor='"pipeline_debug_summary.py",'

add_after(anchor,'"painting_discovery_engine.py",')
add_after('"painting_discovery_engine.py",','"painting_quality_gate.py",')
add_after('"painting_quality_gate.py",','"painting_action_report.py",')

if text!=old:
    path.with_suffix(".py.before_painting_discovery").write_text(old,encoding="utf-8")
    path.write_text(text,encoding="utf-8")
    print("Patched pipeline with painting discovery.")
else:
    print("No pipeline changes made.")
