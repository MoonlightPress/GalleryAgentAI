
from pathlib import Path

path = Path(
    "run_full_mochi_pipeline.py"
)

text = path.read_text(
    encoding="utf-8"
)

entries = [
    '"research_priority_engine.py",',
    '"email_draft_generator.py",',
    '"curator_intelligence_engine.py",',
    '"daily_quest_generator.py",',
]

anchor = '"strategy_explainer_generator.py",'

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
    "Patched autonomous research pipeline."
)
