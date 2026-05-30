from pathlib import Path

files = [
    "opportunity_validator.py",
    "opportunity_discovery_agent.py",
    "opportunity_resolution_agent.py",
    "artist_profile_agent.py",
    "opportunity_ranking_agent.py",
    "opportunity_filter_agent.py",
    "submission_packet_agent.py",
    "council_agent.py",
    "compact_view_agent.py",
    "materials_memory_agent.py",
    "pipeline_status_agent.py",
    "council_pipeline_agent.py",
    "council_pipeline_cached.py",
]

header = """import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

"""

for file in files:
    path = Path(file)

    if not path.exists():
        print(f"SKIP missing: {file}")
        continue

    text = path.read_text(encoding="utf-8")

    if "sys.stdout.reconfigure" in text:
        print(f"OK already patched: {file}")
        continue

    path.write_text(header + text, encoding="utf-8")
    print(f"PATCHED: {file}")