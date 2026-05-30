
from pathlib import Path

path = Path(
    "run_full_mochi_pipeline.py"
)

text = path.read_text(
    encoding="utf-8"
)

entries = [
    '"lineage_scoring_engine.py",',
    '"taste_cluster_report.py",',
]

anchor = '"deep_match_scoring_engine.py",'

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
    "Patched aesthetic intelligence pipeline."
)
