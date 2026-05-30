
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")
text = path.read_text(encoding="utf-8")

entries = [
    '"artist_profile_scoring_engine.py",',
    '"artist_gap_analysis.py",',
    '"priority_research_queue.py",',
]

anchor = '"visual_similarity_engine.py",'

for entry in reversed(entries):
    if entry not in text:
        text = text.replace(anchor, entry + "\n    " + anchor)

path.write_text(text, encoding="utf-8")
print("Patched artist intelligence.")
