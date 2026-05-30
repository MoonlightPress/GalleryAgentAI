
from pathlib import Path

path = Path(
    "run_full_mochi_pipeline.py"
)

text = path.read_text(
    encoding="utf-8"
)

entries = [
    '"visual_similarity_engine.py",',
    '"institution_reputation_graph.py",',
    '"opportunity_decay_engine.py",',
]

anchor = '"evidence_score_guard.py",'

for entry in reversed(entries):

    if entry not in text:
        text = text.replace(
            anchor,
            entry + "\n    " + anchor
        )

path.write_text(
    text,
    encoding="utf-8"
)

print(
    "Patched live refresh systems."
)
