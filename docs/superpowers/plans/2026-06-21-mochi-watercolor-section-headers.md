# Mochi Watercolor Section Headers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Mochi's emoji-only browse headings with compact, section-specific watercolor scenes containing live localized titles.

**Architecture:** Store generated raster assets under `frontend/public/section-art/`. Map existing section IDs to CSS
background images, using the existing `.opp-section-title-row` as the decorative image surface. Add a matching
title-art wrapper to Today's Focus because its heading currently has no row container.

**Tech Stack:** React 19, component CSS, generated PNG watercolor assets, Playwright visual verification.

## Global Constraints

- Work only in canonical `frontend/`; do not touch `frontend2/` or retired Streamlit.
- Do not change recommendation behavior, copy, API contracts, or generated JSON.
- Header art is 72px desktop and 56px mobile.
- Titles and counts remain live localized HTML, never bitmap text.
- Decorative images must not create horizontal overflow.

---

### Task 1: Create The Watercolor Asset Set

**Files:**
- Create: `frontend/public/section-art/*.png`

- [ ] Generate each scene from the approved watercolor style and section mapping.
- [ ] Inspect every output for unwanted words, people, logos, or digital-vector styling.
- [ ] Copy selected assets into `frontend/public/section-art/` without deleting the generated originals.
- [ ] Confirm every file opens and has sufficient pale negative space for title placement.

### Task 2: Integrate Browse Headers

**Files:**
- Modify: `frontend/src/components/OpportunitiesSection.css`
- Modify: `frontend/src/components/RelationshipTargets.css` only if its existing shared header needs an override.

- [ ] Remove the previous synthetic brush-swash title treatment.
- [ ] Map each existing section ID to its image using CSS custom properties.
- [ ] Turn `.opp-section-title-row` into a 72px decorative background surface with title/count nested in negative space.
- [ ] Hide `.opp-section-icon` only for illustrated headings.
- [ ] Add the 56px mobile crop and wrapping rules.

### Task 3: Integrate Today's Focus Header

**Files:**
- Modify: `frontend/src/components/TodaysFocus.jsx`
- Modify: `frontend/src/components/TodaysFocus.css`

- [ ] Wrap each Today's Focus title in the same `tf-title-art` container.
- [ ] Apply its scene as a 72px/56px decorative background.
- [ ] Keep loading, empty, and populated states structurally consistent.

### Task 4: Verify And Document

**Files:**
- Modify: `CURRENT_STATE.md`

- [ ] Run `npm.cmd test`; expect all frontend tests to pass.
- [ ] Run `npm.cmd run lint`; record any pre-existing warnings separately.
- [ ] Run `npm.cmd run build`; expect exit code 0.
- [ ] Capture desktop and 390px mobile screenshots from `http://localhost:5177/`.
- [ ] Confirm title readability, 72px/56px art height, and no new horizontal overflow.
- [ ] Move the scope note to Recent completed work with implementation commit hashes.
- [ ] Commit only files belonging to this pass and push `main`.
