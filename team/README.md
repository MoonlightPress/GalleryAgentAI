# team/

This directory defines the agent team for Nin's career support system.

Inspired by the Arcadia/Moonlight Press org chart pattern — scaled to 4 agents with a manager-coordinator.

---

## Quick Reference

```
NIN (artist — final authority)
│
└── WREN (manager — routes work, daily briefings, task + decision queues)
    ├── MOCHI  🐱  action     — "what should Nin do today?"
    ├── PEPPERCORN  🐭  reflection  — "is the system understanding Nin correctly?"  [not yet built]
    └── SAFFRON  🐦  observatory — "what does the bigger picture look like?"  [not yet built]
```

## Files

| File | What it is |
|------|-----------|
| `TEAM_BIBLE.md` | Governance, mandates, rules — read this first |
| `agent_roster.md` | Full org chart with detail sheets for each agent |
| `ops/task_queue.md` | All pending work, owned by Wren |
| `ops/decision_queue.md` | Decisions only Nin can make, surfaced in morning briefing |
| `ops/SESSION_PROMPTS.md` | Copy-paste prompts to activate each agent |
| `ops/reports/` | Daily briefings + session reports from each agent |

## How to start a session

1. Open `ops/SESSION_PROMPTS.md`
2. Copy the prompt for the agent you want to run
3. Paste it at the start of a Claude Code conversation
4. The agent reads its required files and begins work
5. Session report goes in `ops/reports/`
6. Run Wren last to consolidate

## Current team status

| Agent | Status |
|-------|--------|
| Wren | Active — TASK-001 (first daily briefing) |
| Mochi | Active — TASK-002, TASK-003, TASK-004 |
| Peppercorn | Dormant — not yet built |
| Saffron | Dormant — not yet built |
