import json
from pathlib import Path
import streamlit as st

def load_json(path, fallback):
    p = Path(path)
    if not p.exists():
        return fallback
    return json.loads(p.read_text(encoding="utf-8"))

def render_move_card(move, key=None):
    with st.container(border=True):
        st.markdown(f"### {move.get('name', 'Untitled')}")
        st.caption(f"{move.get('category', '')} · Score {move.get('score', '-')} · Confidence {move.get('confidence', '-')}")
        if move.get("reason"):
            st.write(move["reason"])
        if move.get("next_action"):
            st.info(move["next_action"])
        meta = []
        if move.get("deadline"):
            meta.append(f"**Deadline:** {move['deadline']}")
        if move.get("fee"):
            meta.append(f"**Fee:** {move['fee']}")
        if meta:
            st.markdown(" · ".join(meta))
        if move.get("url"):
            st.link_button("Open source", move["url"])

def render_best_moves_section():
    data = load_json("deploy_data/best_moves.json", None)
    if not data:
        st.warning("Best moves not found yet. Run python run_best_moves_sprint_v1.py first.")
        return

    st.markdown("## Best Next Moves")
    st.caption(data.get("summary", ""))

    st.markdown("### Overall")
    cols = st.columns(3)
    for i, move in enumerate(data.get("global_best_moves", [])[:3]):
        with cols[i % 3]:
            render_move_card(move, key=f"global_{i}")

    with st.expander("More overall moves", expanded=False):
        for i, move in enumerate(data.get("global_best_moves", [])[3:]):
            render_move_card(move, key=f"global_more_{i}")

    st.markdown("### By Category")
    for cat in data.get("categories", []):
        with st.expander(cat.get("title", "Category"), expanded=False):
            st.write(cat.get("summary", ""))
            moves = cat.get("best_moves", [])
            cols = st.columns(3)
            for i, move in enumerate(moves[:3]):
                with cols[i % 3]:
                    render_move_card(move, key=f"{cat.get('title','cat')}_{i}")
