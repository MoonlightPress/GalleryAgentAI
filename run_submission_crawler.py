
import subprocess,sys

for s in [
 'submission_link_hunter.py',
 'requirement_extractor.py',
 'opportunity_action_builder.py'
]:
    print('='*60)
    print('RUNNING:',s)
    print('='*60)
    r=subprocess.run([sys.executable,s])
    if r.returncode!=0:
        raise SystemExit(s)

print('SUBMISSION CRAWLER COMPLETE')
