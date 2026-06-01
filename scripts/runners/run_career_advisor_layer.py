
import subprocess, sys
for script in [
    "career_plan_generator.py",
    "opportunity_brief_generator.py",
    "dashboard_career_cards.py"
]:
    r = subprocess.run([sys.executable, script])
    if r.returncode != 0:
        raise SystemExit(script)
print("DONE")
