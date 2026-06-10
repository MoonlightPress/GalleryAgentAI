import subprocess

pipeline = [
    "artist_intelligence_pipeline.py",
    "career_intelligence_pipeline.py",
    "living_career_pipeline.py",
    "opportunity_verification_agent.py",
    "portfolio_fit_agent.py",
    "opportunity_decay_agent.py",
    "energy_strategy_agent.py",
    "career_sequence_agent.py",
    "mochi_mouse_pipeline.py"
]

for script in pipeline:

    print()
    print("=" * 60)
    print("RUNNING:", script)
    print("=" * 60)

    result = subprocess.run(
        ["python", script]
    )

    if result.returncode != 0:
        raise SystemExit(
            f"FAILED: {script}"
        )

print()
print("FINAL MEGA PIPELINE COMPLETE")