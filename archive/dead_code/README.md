# Archived dead code (2026-06-25)

ORPHANED money-spending cluster: scheduler.py orchestrated weekly/monthly runs calling
deep_verification_agent.py (Claude) + rumor_mill (Tavily) WITHOUT PAID_STEPS gating.
Nothing fires them (no cron/bat/scheduled-task reference); cadence is monthly-by-hand.
Archived (not deleted) to neutralize the latent spend risk. Do NOT re-wire without gating.
