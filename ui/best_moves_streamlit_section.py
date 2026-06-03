import json
import re
from datetime import date, datetime
from pathlib import Path
import streamlit as st

def load_json(path, fallback):
    p = Path(path)
    if not p.exists():
        return fallback
    return json.loads(p.read_text(encoding="utf-8"))

_MONTHS = {
    "january":1,"february":2,"march":3,"april":4,"may":5,"june":6,
    "july":7,"august":8,"september":9,"october":10,"november":11,"december":12,
    "jan":1,"feb":2,"mar":3,"apr":4,"jun":6,"jul":7,"aug":8,
    "sep":9,"oct":10,"nov":11,"dec":12,
}

def days_until_deadline(deadline_str):
    """Return the smallest non-negative days until any date found in deadline_str, or None."""
    if not deadline_str:
        return None
    today = date.today()
    found = []
    # ISO format: 2026-06-05
    for m in re.finditer(r"(\d{4})-(\d{2})-(\d{2})", deadline_str):
        try:
            found.append(date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            pass
    # "June 6, 2026" / "June 7th (Sun), 2026" / "6 June 2026"
    for m in re.finditer(
        r"([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?(?:\s*\([^)]*\))?,?\s+(\d{4})",
        deadline_str,
    ):
        try:
            if m.group(1).lower() in _MONTHS:
                found.append(date(int(m.group(3)), _MONTHS[m.group(1).lower()], int(m.group(2))))
        except (ValueError, TypeError):
            pass
    candidates = [(d - today).days for d in found if (d - today).days >= 0]
    return min(candidates) if candidates else None

def deadline_badge_html(deadline_str):
    days = days_until_deadline(deadline_str)
    if days is None:
        return ""
    if days == 0:
        return '<span style="background:#c0392b;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.78em;font-weight:700;margin-left:6px;">CLOSES TODAY</span>'
    if days == 1:
        return '<span style="background:#c0392b;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.78em;font-weight:700;margin-left:6px;">1 DAY LEFT</span>'
    if days <= 7:
        return f'<span style="background:#e67e22;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.78em;font-weight:700;margin-left:6px;">{days} DAYS LEFT</span>'
    if days <= 30:
        return f'<span style="background:#7d6b4f;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.78em;font-weight:600;margin-left:6px;">{days}d</span>'
    return ""

def render_move_card(move, key=None):
    deadline_str = move.get("deadline", "")
    badge = deadline_badge_html(deadline_str)
    with st.container(border=True):
        st.markdown(f"### {move.get('name', 'Untitled')}{badge}", unsafe_allow_html=True)
        st.caption(f"{move.get('category', '')} · Score {move.get('score', '-')} · Confidence {move.get('confidence', '-')}")
        if move.get("reason"):
            st.write(move["reason"])
        if move.get("next_action"):
            st.info(move["next_action"])
        meta = []
        if deadline_str:
            meta.append(f"**Deadline:** {deadline_str}")
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
