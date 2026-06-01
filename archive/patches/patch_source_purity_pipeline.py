
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

anchor = '"opportunity_truth_checker.py",'
if anchor not in text:
    anchor = '"watercolor_opportunity_converter.py",'
if anchor not in text:
    anchor = '"final_score_guard.py",'

add_after(anchor, '"source_medium_classifier.py",')
add_after('"source_medium_classifier.py",', '"translation_candidate_detector.py",')
add_after('"translation_candidate_detector.py",', '"source_purity_enforcer.py",')
add_after('"source_purity_enforcer.py",', '"native_medium_ranker.py",')

if text != old:
    path.with_suffix(".py.before_source_purity").write_text(old, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    print("Patched pipeline with source purity layer.")
else:
    print("No pipeline changes made.")
