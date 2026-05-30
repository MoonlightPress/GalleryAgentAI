
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

anchor = '"opportunity_differentiation_engine.py",'
if anchor not in text:
    anchor = '"global_strategy_rebalance.py",'

add_after(anchor, '"artist_ecosystem_mapper.py",')
add_after('"artist_ecosystem_mapper.py",', '"peer_artist_engine.py",')
add_after('"peer_artist_engine.py",', '"publisher_match_engine.py",')
add_after('"publisher_match_engine.py",', '"ecosystem_opportunity_bridge.py",')
add_after('"ecosystem_opportunity_bridge.py",', '"ecosystem_report.py",')

if text != old:
    path.with_suffix(".py.before_artist_intelligence_v2").write_text(old, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    print("Patched pipeline with Artist Intelligence v2.")
else:
    print("No pipeline changes made.")
