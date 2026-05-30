
from pathlib import Path

path = Path(
    "run_full_mochi_pipeline.py"
)

text = path.read_text(
    encoding="utf-8"
)

entries = [
    '"reputation_engine.py",',
    '"momentum_wave_engine.py",',
    '"social_proof_engine.py",',
]

anchor = '"submission_strategy_engine.py",'

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
    "Patched reputation pipeline."
)
