
from pathlib import Path

path = Path(
    "run_full_mochi_pipeline.py"
)

text = path.read_text(
    encoding="utf-8"
)

entries = [
    '"submission_strategy_engine.py",',
    '"smart_cover_letter_engine.py",',
    '"submission_timeline_engine.py",',
]

anchor = '"portfolio_match_engine.py",'

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
    "Patched submission strategy pipeline."
)
