
import subprocess, sys
for script in ["candidate_cleanup_v1.py","ingest_clean_business_decisions.py","clean_candidate_summary.py","clean_candidate_dashboard_export.py"]:
    print("="*70); print("RUNNING:",script); print("="*70)
    r=subprocess.run([sys.executable,script])
    if r.returncode!=0: raise SystemExit(f"FAILED: {script}")
print("CANDIDATE CLEANUP V1 COMPLETE")
