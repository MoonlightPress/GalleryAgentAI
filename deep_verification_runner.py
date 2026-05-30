
import subprocess,sys

for script in [
    "contact_page_crawler.py",
    "open_call_link_follower.py",
    "deadline_relevance_filter.py",
    "verification_score_builder.py"
]:
    print("="*60)
    print("RUNNING:",script)
    print("="*60)

    r=subprocess.run([sys.executable,script])
    if r.returncode!=0:
        raise SystemExit(script)

print("DEEP VERIFICATION COMPLETE")
