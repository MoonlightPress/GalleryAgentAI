
import json
import os
from pathlib import Path

import streamlit as st

MATCH_PATH = "memory/portfolio_matches.json"
PITCH_DIR = Path("reports/portfolio_pitches")


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def read_text(path, fallback=""):
    if os.path.exists(path):
        return Path(path).read_text(encoding="utf-8")
    return fallback


def render_portfolio_match_panel():
    st.header("Portfolio Matching")

    matches = load_json(MATCH_PATH, {})

    if not matches:
        st.warning("No portfolio matches yet. Run the pipeline.")
        return

    titles = sorted(matches.keys())

    selected = st.selectbox(
        "Choose opportunity",
        titles,
        key="portfolio_match_picker",
    )

    st.subheader(selected)

    for match in matches.get(selected, []):
        with st.expander(f"{match.get('title')} · score {match.get('score')}", expanded=True):
            st.write(match.get("description", ""))
            st.write("**Hits:**", ", ".join(match.get("hits", [])) or "None")
            st.write("**Best formats:**", ", ".join(match.get("best_formats", [])) or "None")

    if PITCH_DIR.exists():
        possible = list(PITCH_DIR.glob("*.md"))
        selected_slug = selected.replace("/", "_").replace("\\", "_").replace(":", "").replace("?", "")[:40].lower()

        for path in possible:
            if selected_slug[:20] in path.name.lower():
                with st.expander("Generated portfolio pitch"):
                    st.markdown(read_text(path))
                break
