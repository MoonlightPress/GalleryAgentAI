import json
import os
from datetime import date
from pathlib import Path

import streamlit as st

SUBMISSION_LOG_PATH = "memory/submission_log.json"
PROFILE_PATH = "memory/artist_master_profile.json"

OUTCOME_OPTIONS = [
    "pending",
    "accepted",
    "declined",
    "waitlisted",
    "no response",
    "withdrew",
]


def _load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def _save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def render_artist_statement():
    st.subheader("Artist Statement")
    st.caption("One or two sentences. Direct from you — this anchors every recommendation.")

    profile = _load_json(PROFILE_PATH, {})
    visual = profile.get("visual_profile", {})
    current = visual.get("artist_statement", "")

    new_statement = st.text_area(
        "Your statement",
        value=current,
        height=110,
        placeholder="e.g. I paint the quiet residue of daily life in Tokyo — windows, staircases, the light that collects in corners no one notices.",
        key="peppercorn_artist_statement",
    )

    if st.button("Save statement", key="peppercorn_save_statement"):
        if new_statement.strip():
            profile.setdefault("visual_profile", {})["artist_statement"] = new_statement.strip()
            _save_json(PROFILE_PATH, profile)
            st.success("Saved.")
        else:
            st.warning("Statement is empty — nothing saved.")


def render_submission_log():
    st.subheader("Submission Log")
    st.caption("A record of what you've submitted, where, and what happened. The pipeline reads this to track your history.")

    log = _load_json(SUBMISSION_LOG_PATH, [])

    # Display existing entries
    if log:
        for i, entry in enumerate(reversed(log)):
            outcome = entry.get("outcome", "pending")
            outcome_color = {
                "accepted": "🟢",
                "declined": "🔴",
                "pending": "🟡",
                "waitlisted": "🟠",
                "no response": "⚪",
                "withdrew": "⚫",
            }.get(outcome, "🟡")

            with st.expander(
                f"{outcome_color} {entry.get('venue', 'Unknown')} · {entry.get('date', '')} · {outcome}",
                expanded=i == 0,
            ):
                st.write("**What submitted:**", entry.get("what_submitted", "—"))
                if entry.get("notes"):
                    st.write("**Notes:**", entry["notes"])

                # Allow outcome update
                new_outcome = st.selectbox(
                    "Update outcome",
                    OUTCOME_OPTIONS,
                    index=OUTCOME_OPTIONS.index(outcome) if outcome in OUTCOME_OPTIONS else 0,
                    key=f"peppercorn_outcome_{i}",
                )
                if st.button("Update", key=f"peppercorn_update_{i}"):
                    actual_idx = len(log) - 1 - i
                    log[actual_idx]["outcome"] = new_outcome
                    _save_json(SUBMISSION_LOG_PATH, log)
                    st.rerun()
    else:
        st.info("No submissions logged yet. Add your first one below.")

    st.markdown("---")
    st.markdown("#### Log a submission")

    col1, col2 = st.columns(2)
    with col1:
        sub_date = st.date_input("Date submitted", value=date.today(), key="peppercorn_sub_date")
        venue = st.text_input("Venue / opportunity", placeholder="e.g. ZINE Fest Tokyo", key="peppercorn_venue")
    with col2:
        what = st.text_input("What you submitted", placeholder="e.g. Zine application, portfolio PDF", key="peppercorn_what")
        outcome = st.selectbox("Initial outcome", OUTCOME_OPTIONS, key="peppercorn_new_outcome")

    notes = st.text_input("Notes (optional)", placeholder="e.g. Applied via Google Form, confirmation email received", key="peppercorn_notes")

    if st.button("Add to log", key="peppercorn_add_log"):
        if venue.strip() and what.strip():
            entry = {
                "date": sub_date.isoformat(),
                "venue": venue.strip(),
                "what_submitted": what.strip(),
                "outcome": outcome,
                "notes": notes.strip(),
            }
            log.insert(0, entry)
            _save_json(SUBMISSION_LOG_PATH, log)
            st.success(f"Logged: {venue}")
            st.rerun()
        else:
            st.warning("Venue and 'what submitted' are required.")


def render_peppercorn_page():
    st.markdown(
        """
        <div style="margin-bottom:1.2rem;">
            <span style="font-size:2.2rem;">🐭</span>
            <span style="font-family:Georgia,serif;font-size:1.6rem;color:#3f3027;margin-left:0.5rem;">Peppercorn</span>
        </div>
        <p style="color:#7a6650;font-size:1rem;max-width:560px;margin-bottom:2rem;">
        This is where your voice enters the system. Peppercorn asks quiet questions and remembers the answers.
        Tell him what you've submitted. Tell him how you'd describe your work. He'll make sure Mochi understands you.
        </p>
        """,
        unsafe_allow_html=True,
    )

    render_artist_statement()
    st.markdown("---")
    render_submission_log()
