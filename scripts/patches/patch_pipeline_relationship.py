
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

text = path.read_text(encoding="utf-8")

insert = """
    "relationship_memory_engine.py",
    "momentum_scoring_engine.py",
"""

if "relationship_memory_engine.py" not in text:
    text = text.replace(
        '    "institution_profile_builder.py",',
        '    "institution_profile_builder.py",' + insert
    )

path.write_text(text, encoding="utf-8")

print("Patched pipeline.")
