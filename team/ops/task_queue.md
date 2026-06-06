# Task Queue — Nin's Career Team

*Last updated: 2026-06-06 | Maintained by: Wren*

---

## Queue Health

| Metric | Value |
|--------|-------|
| Open tasks | 10 |
| Blocked tasks | 1 |
| Decision queue items | 3 |
| Completed this week | 0 (team newly initialized) |

---

## CRITICAL

---

### TASK-001
**Title:** Produce first Wren daily briefing from current pipeline state  
**Owner:** Wren  
**Status:** NOT STARTED  
**Depends on:** Nothing — start here  
**Estimate:** 1 session  
**Notes:** Read `memory/daily_digest_snapshot.json`, `memory/opportunity_rankings.json`, and `memory/opportunity_status.json`. Produce `team/ops/reports/daily_briefing_2026-06-06.md` with exactly 3 actions for Nin. This is Wren's inaugural run.

---

### TASK-002
**Title:** Audit Today's Focus output — confirm Tier 4 filter and 3-item discipline  
**Owner:** Mochi  
**Status:** NOT STARTED  
**Depends on:** TASK-001 (Wren must run first to establish baseline)  
**Estimate:** 1 session  
**Notes:** Pull the current `memory/daily_digest_snapshot.json`. Verify: (1) exactly 3 items in Today's Focus, (2) no Tier 4 opportunities appearing in Immediate Best Moves, (3) all items have verification status. Flag any violations.

---

### TASK-003
**Title:** Verification gap audit — map which opportunities have confirmed open status  
**Owner:** Mochi  
**Status:** NOT STARTED  
**Depends on:** Nothing  
**Estimate:** 1–2 sessions  
**Notes:** Verification is the weakest layer (30% mature). Audit `memory/verified/` against `memory/opportunities.json`. What percentage of high-ranked opportunities have confirmed live URLs and confirmed open submission windows? Produce summary report. This directly determines how reliable Mochi's recommendations are.

---

## HIGH

---

### TASK-004
**Title:** Deadline scan — identify all opportunities closing within 30 days  
**Owner:** Mochi  
**Status:** NOT STARTED  
**Depends on:** Nothing  
**Estimate:** 1 session  
**Notes:** Scan all opportunities for deadline fields. Surface anything closing before 2026-07-06. Flag items where deadline is present but verification status is unconfirmed. This is immediately actionable for Nin.

---

### TASK-005
**Title:** Submission queue — identify opportunities ready to submit vs. needing prep  
**Owner:** Mochi  
**Status:** NOT STARTED  
**Depends on:** TASK-004 (deadline context needed)  
**Estimate:** 1 session  
**Notes:** Of the near-deadline opportunities: which ones have everything needed (artist statement, portfolio images, application form location)? Which are missing something? Produce two lists: "ready to go" and "needs X before submitting."

---

### TASK-006
**Title:** Design Peppercorn's question queue  
**Owner:** Peppercorn (planning phase — can be done by Wren as proxy)  
**Status:** NOT STARTED  
**Depends on:** Nothing  
**Estimate:** 1 session  
**Notes:** What are the 10 most important things the system doesn't yet know about Nin's preferences that would change its recommendations? Read `memory/artist_master_profile.json` and `memory/learned_artist_preferences.json` to identify gaps. Output: a prioritized question list that Peppercorn will ask Nin one at a time, in order.

---

### TASK-007
**Title:** First Saffron observatory report — landscape from above  
**Owner:** Saffron (planning phase — can be done by Wren as proxy)  
**Status:** NOT STARTED  
**Depends on:** Nothing  
**Estimate:** 1–2 sessions  
**Notes:** Read `memory/ecosystem_patterns.json`, `memory/career_overview.json`, `memory/peer_artists.json`, `memory/fit_audit.json`. Produce `team/ops/reports/session_2026-06-06_saffron.md`: what does the opportunity landscape look like from altitude? What patterns is Mochi probably missing from ground level? What are the long-range targets Nin should begin preparing for even if they're not actionable yet?

---

### TASK-008
**Title:** CRM baseline — who has Nin already contacted or connected with?  
**Owner:** Wren (route to Mochi for execution)  
**Status:** NOT STARTED  
**Depends on:** Nothing  
**Estimate:** 1 session  
**Notes:** Read `memory/contact_memory.json` and `memory/relationship_memory.json`. Produce a human-readable summary: who are the key relationships, what is the current status of each, what is the next logical contact for each? CRM is 5% mature — this is the foundational audit before building further.

---

## NORMAL

---

### TASK-009
**Title:** Score inflation audit — check if high-ranked opportunities are earning their scores  
**Owner:** Saffron (planning phase — Wren as proxy)  
**Status:** NOT STARTED  
**Depends on:** TASK-007 (needs landscape context)  
**Estimate:** 1 session  
**Notes:** Compare `memory/opportunity_rankings.json` against `memory/opportunity_evidence.json`. Are high scores backed by strong evidence, or are they artifacts of the scoring algorithm's optimism? Flag any opportunity scoring 80+ without strong evidence. This is the Truth Alignment layer check.

---

### TASK-010
**Title:** Peppercorn page design brief  
**Owner:** Wren  
**Status:** BLOCKED on DECISION-002  
**Depends on:** DECISION-002 (Nin's input on what she wants from the reflection page)  
**Estimate:** 1 session after decision  
**Notes:** Before designing the Peppercorn UI page, Nin should weigh in on what she actually wants to be asked about. See DECISION-002.

---

## LOW

---

*(No low-priority tasks yet — keeping the queue clean while the team initializes)*

---

## Completed

*(None yet — team initialized 2026-06-06)*

---

## Task Status Definitions

| Status | Meaning |
|--------|---------|
| **NOT STARTED** | Task is defined and ready to begin |
| **IN PROGRESS** | Agent is actively working on this |
| **AWAITING NIN** | Task needs a decision or input from Nin before proceeding |
| **BLOCKED** | Cannot proceed — see notes for blocker |
| **DONE** | Complete; output produced and logged |
