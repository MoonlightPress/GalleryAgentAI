
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

anchor = '"visual_profile_ingester.py",'
if anchor not in text:
    anchor = '"artist_visual_profile_v1.py",'
if anchor not in text:
    anchor = '"pipeline_debug_summary.py",'

add_after(anchor, '"visual_dna_extractor.py",')
add_after('"visual_dna_extractor.py",', '"dna_recommendation_booster.py",')
add_after('"next_project_engine.py",', '"dna_project_refiner.py",')

if text != old:
    path.with_suffix(".py.before_visual_dna").write_text(old, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    print("Patched pipeline with visual DNA engines.")
else:
    print("No pipeline changes made.")
