
from pathlib import Path

path = Path("run_full_mochi_pipeline.py")

if not path.exists():
    raise SystemExit("run_full_mochi_pipeline.py not found.")

text = path.read_text(encoding="utf-8")

entries_before = [
    '"web_ingestion_engine.py",',
    '"scraped_candidate_extractor.py",',
    '"candidate_review_importer.py",',
    '"url_verification_engine.py",',
    '"score_sanity_engine.py",',
]

anchor = '"global_opportunity_expander.py",'

for entry in reversed(entries_before):
    if entry not in text:
        text = text.replace(anchor, entry + "\n    " + anchor)

if '"visual_profile_ingester.py",' not in text:
    text = text.replace(
        '"deep_match_scoring_engine.py",',
        '"visual_profile_ingester.py",\n    "deep_match_scoring_engine.py",'
    )

path.write_text(text, encoding="utf-8")

print("Patched pipeline with ingestion system.")
