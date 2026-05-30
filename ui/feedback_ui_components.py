
import json
import os
from pathlib import Path

import streamlit as st

PREF_PATH = "memory/learned_artist_preferences.json"
REPORT_PATH = "reports/feedback_learning_report.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def read_text(path, fallback=""):
    if os.path.exists(path):
        return Path(path).read_text(encoding="utf-8")
    return fallback


def render_feedback_learning_panel():
    st.header("Feedback Learning")

    learned = load_json(PREF_PATH, {})

    if not learned:
        st.warning("No learned preferences yet. Mark opportunities as interested, rejected, submitted, etc., then run the pipeline.")
        return

    positive = learned.get("positive_signals", [])
    negative = learned.get("negative_signals", [])

    c1, c2, c3 = st.columns(3)
    c1.metric("Positive examples", len(learned.get("positive_titles", [])))
    c2.metric("Negative examples", len(learned.get("negative_titles", [])))
    c3.metric("Learned weights", len(learned.get("preference_weights", {})))

    left, right = st.columns(2)

    with left:
        st.subheader("Positive Signals")
        for token, count in positive[:20]:
            st.write(f"**{token}** · {count}")

    with right:
        st.subheader("Negative Signals")
        for token, count in negative[:20]:
            st.write(f"**{token}** · {count}")

    with st.expander("Full feedback report"):
        st.markdown(read_text(REPORT_PATH, "No report found."))
