
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

anchor = '"visual_dna_extractor.py",'
if anchor not in text:
    anchor = '"artist_visual_profile_v1.py",'
if anchor not in text:
    anchor = '"pipeline_debug_summary.py",'

add_after(anchor, '"watercolor_artist_profile_engine.py",')
add_after('"watercolor_artist_profile_engine.py",', '"watercolor_source_expander.py",')
add_after('"watercolor_source_expander.py",', '"watercolor_opportunity_converter.py",')
add_after('"watercolor_opportunity_converter.py",', '"watercolor_project_rebuilder.py",')

if text != old:
    path.with_suffix(".py.before_watercolor_pipeline").write_text(old, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    print("Patched pipeline with watercolor intelligence layer.")
else:
    print("No pipeline changes made.")
