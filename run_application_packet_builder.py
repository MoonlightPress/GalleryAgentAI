
import subprocess
import sys

for script in [
    "application_packet_builder.py",
    "artist_daily_tasks_builder.py",
    "dashboard_packet_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("APPLICATION PACKET BUILDER COMPLETE")
