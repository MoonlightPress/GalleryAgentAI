
from pathlib import Path

path = Path(
    "run_full_mochi_pipeline.py"
)

text = path.read_text(
    encoding="utf-8"
)

entries = [
    '"curator_personality_engine.py",',
    '"career_path_engine.py",',
    '"serendipity_engine.py",',
]

anchor = '"institution_network_engine.py",'

for entry in reversed(entries):

    if entry not in text:
        text = text.replace(
            anchor,
            anchor + "\n    " + entry
        )

path.write_text(
    text,
    encoding="utf-8"
)

print(
    "Patched curator brain pipeline."
)
