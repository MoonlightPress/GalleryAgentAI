
import subprocess
import sys

# Correct order:
# 1. Verify pages and save relevant_links.
# 2. Hunt submission links from relevant_links.
# 3. Extract placeholder requirements.
# 4. Rank links.
# 5. Crawl application pages.
# 6. Classify opportunity type WITHOUT discarding fields.
# 7. Render final reports.

PIPELINE = [
    "run_real_verification.py",
    "run_submission_link_precision_patch.py",
    "submission_link_ranker.py",
    "application_page_crawler.py",
    "opportunity_type_classifier.py",
    "application_action_report.py",
]

for script in PIPELINE:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("FIXED APPLICATION PIPELINE COMPLETE")
