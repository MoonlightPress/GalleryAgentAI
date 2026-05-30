
from pathlib import Path

path = Path(
    "run_full_mochi_pipeline.py"
)

text = path.read_text(
    encoding="utf-8"
)

entries = [
    '"institution_network_engine.py",',
    '"discovery_engine.py",',
    '"ecosystem_expansion_engine.py",',
]

anchor = '"fit_audit_engine.py",'

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
    "Patched network intelligence pipeline."
)
