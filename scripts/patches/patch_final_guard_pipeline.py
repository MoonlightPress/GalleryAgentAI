
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found.")

text = path.read_text(encoding="utf-8")

if '"final_score_guard.py",' not in text:
    # Put final_score_guard near the very end, immediately before debug summary.
    text = text.replace(
        '"pipeline_debug_summary.py",',
        '"final_score_guard.py",\n    "pipeline_debug_summary.py",'
    )

# Ensure candidate_quality_gate runs after candidate extraction.
if text.find('"candidate_quality_gate.py",') < text.find('"scraped_candidate_extractor.py",'):
    text = text.replace('    "candidate_quality_gate.py",\n', '')
    text = text.replace(
        '"scraped_candidate_extractor.py",',
        '"scraped_candidate_extractor.py",\n    "candidate_quality_gate.py",'
    )

path.write_text(text, encoding="utf-8")

print("Patched pipeline with final score guard.")
