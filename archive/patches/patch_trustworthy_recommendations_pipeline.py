
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

anchor = '"final_score_guard.py",'
add_after(anchor, '"recommendation_trust_cleaner.py",')
add_after('"recommendation_trust_cleaner.py",', '"exclusive_strategy_bucket_engine.py",')
add_after('"exclusive_strategy_bucket_engine.py",', '"strategic_action_report.py",')

if text != old:
    path.with_suffix(".py.before_trustworthy_recommendations").write_text(old, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    print("Patched pipeline with trustworthy recommendation reports.")
else:
    print("No pipeline changes made.")
