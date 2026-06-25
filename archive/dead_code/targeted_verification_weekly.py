"""
Weekly wrapper: runs targeted_verification_agent --all
Called by scheduler's WEEKLY_PIPELINE via smart_pipeline_runner.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Patch sys.argv so the agent runs in --all mode
sys.argv = [sys.argv[0], "--all"]

from engines.targeted_verification_agent import main
main()
