
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

anchor = '"watercolor_opportunity_converter.py",'
if anchor not in text:
    anchor = '"final_score_guard.py",'
if anchor not in text:
    anchor = '"pipeline_debug_summary.py",'

add_after(anchor, '"opportunity_truth_checker.py",')
add_after('"opportunity_truth_checker.py",', '"score_explanation_alignment.py",')
add_after('"score_explanation_alignment.py",', '"career_path_ranker.py",')

if text != old:
    path.with_suffix(".py.before_truth_alignment").write_text(old, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    print("Patched pipeline with truth alignment.")
else:
    print("No pipeline changes made.")
