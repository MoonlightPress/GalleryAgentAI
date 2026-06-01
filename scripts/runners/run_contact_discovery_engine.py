
import subprocess,sys

for script in [
    "contact_discovery_engine.py",
    "outreach_queue_builder.py"
]:
    r=subprocess.run([sys.executable,script])
    if r.returncode:
        raise SystemExit(script)

print("CONTACT DISCOVERY COMPLETE")
