
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

text = path.read_text(encoding="utf-8")

entries = [
    '"curator_dossier_engine.py",',
    '"ecosystem_map_engine.py",',
    '"career_pathway_engine.py",',
]

anchor = '"priority_research_queue.py",'

for entry in reversed(entries):
    if entry not in text:
        text = text.replace(
            anchor,
            entry + "\n    " + anchor
        )

path.write_text(text,encoding="utf-8")

print("Patched curator intelligence.")
