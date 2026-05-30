
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found.")

text = path.read_text(encoding="utf-8")

def add_before(anchor, entry):
    global text
    if entry not in text:
        text = text.replace(anchor, entry + "\n    " + anchor)

add_before('"opportunity_enrichment_pipeline.py",', '"global_opportunity_expander.py",')
add_before('"research_queue_report.py",', '"global_research_queue_builder.py",')
add_before('"opportunity_status_engine.py",', '"global_strategy_rebalance.py",')

path.write_text(text, encoding="utf-8")

print("Patched run_full_mochi_pipeline.py with global opportunity expansion.")
