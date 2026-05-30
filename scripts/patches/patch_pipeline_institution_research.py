
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")
text = path.read_text(encoding="utf-8")

entries = [
    '"institution_profile_engine.py",',
    '"institution_fit_engine.py",',
    '"research_priority_matrix.py",',
]

anchor = '"curator_dossier_engine.py",'

for entry in reversed(entries):
    if entry not in text:
        text = text.replace(
            anchor,
            entry + "\n    " + anchor
        )

path.write_text(text,encoding="utf-8")

print("Patched institution research layer.")
