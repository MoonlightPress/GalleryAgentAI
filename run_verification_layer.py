
import subprocess, sys

for script in [
"opportunity_verification_queue.py",
"verified_opportunity_schema_builder.py",
"gallery_verification_dashboard.py",
"top20_verification_pack_builder.py"
]:
    print("="*60)
    print("RUNNING:",script)
    print("="*60)
    r=subprocess.run([sys.executable,script])
    if r.returncode!=0:
        raise SystemExit(script)
