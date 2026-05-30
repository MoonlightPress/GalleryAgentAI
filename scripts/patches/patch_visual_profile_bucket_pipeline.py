
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found.")

text = path.read_text(encoding="utf-8")
old = text

def add_before(anchor, entry):
    global text
    if entry not in text and anchor in text:
        text = text.replace(anchor, entry + "\n    " + anchor)

def add_after(anchor, entry):
    global text
    if entry not in text and anchor in text:
        text = text.replace(anchor, anchor + "\n    " + entry)

add_before('"visual_profile_ingester.py",', '"artist_visual_profile_v1.py",')
add_after('"global_strategy_rebalance.py",', '"opportunity_differentiation_engine.py",')
add_after('"opportunity_differentiation_engine.py",', '"career_bucket_report.py",')
add_after('"pipeline_debug_summary.py",', '"project_folder_audit.py",')

if text != old:
    path.with_suffix(".py.before_visual_profile_bucket_patch").write_text(old, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    print("Patched pipeline with visual profile and career buckets.")
else:
    print("No pipeline changes made.")

