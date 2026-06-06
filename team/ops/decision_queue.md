# Decision Queue — Nin's Career Team

*Maintained by: Wren | Max items: 10 | Current count: 3*

> Decisions that only Nin can make. Agents do not proceed past a decision — they work on something else and wait. Wren surfaces these in the daily briefing.

---

## Open Decisions

---

### DECISION-001
**Status:** OPEN  
**Raised by:** Wren (system initialization)  
**Raised on:** 2026-06-06  
**Question:** The pipeline currently runs as a scheduled background task. Should it continue running on its own schedule, or would you prefer Wren to explicitly flag when it's about to run and report when it's done?  
**Options:**
- A) Keep running silently; Wren just reads the output and reports findings
- B) Wren flags before each run so Nin is aware; reports output afterward
- C) Pipeline runs only when Nin explicitly asks for it

**Blocking:** Nothing critical, but Wren's morning briefing format depends on this.  
**Nin's answer:** *(pending)*

---

### DECISION-002
**Status:** OPEN  
**Raised by:** Wren (planning Peppercorn)  
**Raised on:** 2026-06-06  
**Question:** Peppercorn's job is to capture your voice — preferences, feedback on recommendations, career goals. Before designing his page, what would you most want to be able to tell the system that you currently can't?  
**Options:**
- A) I want to flag specific opportunities as "definitely not" so they stop appearing
- B) I want to set a monthly focus (e.g., "this month I'm only interested in zine fairs")
- C) I want to update my artist statement and have the system adjust recommendations accordingly
- D) Something else — I'll tell you in free text

**Blocking:** TASK-010 (Peppercorn page design)  
**Nin's answer:** *(pending)*

---

### DECISION-003
**Status:** OPEN  
**Raised by:** Wren (career phase planning)  
**Raised on:** 2026-06-06  
**Question:** The system currently treats Tier 3 opportunities (TOKAS, BankART, Youkobo, Shoto Museum) as "not yet" — they're tracked but not actively recommended. Do you want to start receiving awareness of Tier 3 deadlines even if they're not in Today's Focus? This would be Saffron's role: "heads up, TOKAS open call is in 4 months — no action needed yet but worth noting."  
**Options:**
- A) Yes — I want early awareness of Tier 3 timing, even if not actionable yet
- B) No — keep Tier 3 fully out of view until I'm ready to move up
- C) Only for specific venues I name (e.g., just TOKAS)

**Blocking:** Saffron's long-range tracking scope (TASK-007 partial)  
**Nin's answer:** *(pending)*

---

## Resolved Decisions

*(None yet — queue opened 2026-06-06)*

---

## Queue Rules

- Maximum 10 open items. If the queue reaches 10, Wren flags CAUTION in the daily briefing and asks Nin to prioritize clearing decisions before new work begins.
- Wren adds items; agents can request Wren add an item via their session report.
- Once Nin answers, Wren removes the item and updates the relevant task.
- Decisions are never left open indefinitely — if a decision has been open 14+ days without an answer, Wren re-surfaces it with a note about what's blocked.
