import subprocess, sys
for script in ["gallery_profile_builder_v1.py","gallery_tiering_engine_v1.py","gallery_fit_analysis_v1.py","competition_expansion_v1.py","competition_verifier_v1.py","ecosystem_summary_refresh_v1.py"]:
    print("="*70); print("RUNNING:", script); print("="*70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")
print("GALLERY INTELLIGENCE SPRINT V1 COMPLETE")
