# GalleryAgentAI — Project State & Architecture

## Project Purpose

GalleryAgentAI is an AI-assisted artist career support system.

The core idea is:

- reduce emotional and cognitive friction for artists
- surface meaningful opportunities
- help with outreach and follow-up
- provide ecosystem awareness
- make career development feel gentle, actionable, and emotionally sustainable

The system is NOT intended to:

- automate spam outreach
- impersonate the artist
- replace human judgment
- optimize purely for prestige or growth metrics

The system SHOULD:

- act like a thoughtful assistant
- surface opportunities and peers
- explain why recommendations matter
- help organize the artist’s life and momentum
- provide emotionally lightweight guidance

Current primary artist target:

- young painter / illustrator
- Chinese-speaking
- Japan-based ecosystem
- illustration-adjacent contemporary art
- emotionally sensitive to institutional pressure
- values aesthetics, atmosphere, and artistic life

The system architecture should remain adaptable for:

- other artists
- creative professionals
- eventually the user’s own game/project ecosystem

---

# Current Technology Stack

## Frontend

- Streamlit
- Single-page dashboard architecture
- Current UI is transitional / developer-heavy

## Backend / Logic

- Python
- JSON-based memory/state
- Agent-oriented architecture

## Current Data Storage

Primary memory files:

```text
memory/opportunities.json
memory/contact_memory.json
```

Other generated files:

```text
artist_dossier.md
final_gallery_report.md
email_drafts.md
quest_report.md
```

---

# Current Repo Philosophy

The system is transitioning from:

```text
prototype dashboard
```

into:

```text
adaptive artist-career intelligence system
```

The repo is now large enough that:

- architecture documentation matters
- modularization matters
- repo-aware agents are preferable to conversational patch editing

Future architecture should likely include:

```text
/agents
/ui
/themes
/memory
/reports
/assets
/docs
```

---

# Current Product Philosophy

The product should NOT feel like:

- CRM software
- admin tooling
- corporate productivity software
- growth-hacking infrastructure

The product SHOULD feel like:

- a gentle knowledge system
- a companion workspace
- a Primer-style discovery interface
- a curated ecosystem
- a soft artistic operating system

Key metaphors:

- cards
- discoveries
- atelier
- desk space
- companion creature
- opportunities as “doors”
- quests instead of tasks

The emotional target is:

```text
"I feel supported, not managed."
```

---

# Product Direction

## Current State

The current system already includes:

- opportunity storage
- CRM
- multilingual outreach generation
- scoring
- status workflow
- notes
- dashboard metrics
- daily quest generation
- Chinese summaries
- outreach support

The current bottleneck is NOT feature count.

The bottlenecks are:

- data quality
- opportunity discovery
- verification
- UX clarity
- emotional usability
- architectural organization

---

# Corrected Development Phases

## Phase 1 — Functional Opportunity Pipeline

Goal:

```text
artist profile
→ discover opportunities
→ verify opportunities
→ score/filter
→ generate outreach
→ track workflow
```

This phase is NOT fully complete yet.

What already exists:

- UI scaffold
- memory system
- workflow system
- outreach generation
- CRM
- scoring

What is still incomplete:

- true autonomous discovery
- robust verification
- source grounding
- automatic ingestion

Primary remaining work:

- opportunity_discovery_agent.py
- verification refinement
- automatic ingestion pipeline

---

## Phase 2 — Adaptive Intelligence Layer

Goal:

Improve judgment quality and system reasoning.

This phase includes:

- missing information detection
- confidence scoring
- uncertainty awareness
- adaptive questioning
- recommendation refinement
- learning from artist feedback
- emotional friction awareness
- ecosystem understanding
- aesthetic compatibility reasoning

Important:

This phase is what transforms the product from:

```text
useful software
```

into:

```text
intelligent creative companion
```

Key planned agent:

```text
missing_info_agent.py
```

Purpose:

- identify gaps in artist understanding
- ask targeted questions
- improve downstream recommendation quality

Example:

```json
{
  "field": "medium",
  "importance": "high",
  "question": "What mediums does the artist primarily work in?"
}
```

---

## Phase 3 — Productization / UX Layer

Goal:

Make the system emotionally compelling and artist-facing.

Includes:

- visual redesign
- Primer-style interaction model
- card-based UI
- cleaner navigation
- mobile responsiveness
- theming system
- mascot integration
- deployment
- accounts/auth
- multi-user support

Important:

Phase 3 should happen AFTER the intelligence layer stabilizes.

Do not polish unstable cognition.

---

# UI Direction

## Current UI Problem

Current UI is:

- tab-heavy
- developer-oriented
- too much raw information
- too CRUD-oriented

The artist-facing version should instead feel:

- gentle
- curated
- lightweight
- exploratory
- emotionally low-pressure

---

# Desired UI Structure

## Top Section

A large Primer-style hero/header.

Concept:

- atelier desk
- companion cat
- soft atmosphere
- hand-painted card feeling
- emotional warmth

Important:

Do NOT overcomplicate with full animation initially.

Static is acceptable.

---

## Main Interaction Philosophy

NOT:

```text
forms and giant dashboards
```

BUT:

```text
actionable cards
```

Examples:

- Opportunity Card
- Peer Card
- Gallery Card
- Quest Card
- Insight Card
- Ecosystem Card

Card shows:

- synopsis
- fit
- urgency
- why it matters

Clicking expands into:

- full analysis
- outreach
- risks
- examples
- notes
- next actions

---

# Theme System

Planned theme architecture:

```text
/themes
  primer_minimal.json
  primer_atelier.json
  primer_admin.json
```

Theme controls:

- colors
- fonts
- card styles
- mascot styling
- background texture
- UI density

---

# Mascot Philosophy

The cat mascot is NOT merely decorative.

It should function as:

- emotional continuity
- soft companionship
- a non-demanding presence
- symbolic studio life

Avoid:

- gamified manipulation
- aggressive productivity pressure
- guilt mechanics

Future possibilities:

- reacts to completed tasks
- sleeps/rests
- gentle ambient behaviors
- seasonal changes

But initially:

- static companion is sufficient

---

# Opportunity Philosophy

The system should NOT focus only on:

- prestigious galleries
- elite institutions
- formal submissions

It SHOULD also surface:

- handmade markets
- local fairs
- artist cafés
- peer ecosystems
- small exhibitions
- zines
- temporary popups
- station markets
- emotionally low-pressure opportunities

The system should understand:

```text
creative ecosystems
```

not just:

```text
institutions
```

---

# Current Important Files

## Main UI

```text
app.py
```

## Agent Files

Current or planned:

```text
crm_summary_agent.py
web_verification_agent.py
outreach_email_agent.py
opportunity_discovery_agent.py
missing_info_agent.py
```

## Memory Files

```text
memory/opportunities.json
memory/contact_memory.json
```

---

# Current Technical Reality

The project has become too large for pure conversational editing.

Current pain points:

- interdependent files
- long patch-edit loops
- fragile copy/paste editing
- chat-memory limitations

Long-term solution:

- repo-aware coding agents
- direct repository editing
- automated validation/testing
- architecture documentation

---

# Current Strategic Priorities

In order:

1. stabilize repo structure
2. improve discovery/verification
3. improve recommendation quality
4. simplify UX
5. improve presentation
6. adaptive intelligence layer
7. visual polish

Avoid:

- feature sludge
- premature polish
- unnecessary UI complexity

---

# Current Core Insight

The project is no longer primarily:

```text
"build more features"
```

It is now:

```text
"improve fidelity, judgment, and emotional usability"
```

That is the current stage of the project.

