
import subprocess
import sys

for script in [
    "artist_biography_parser_v2.py",
    "artist_career_graph.py",
    "artist_career_relevance_summary.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("ARTIST BIOGRAPHY PARSER V2 COMPLETE")
