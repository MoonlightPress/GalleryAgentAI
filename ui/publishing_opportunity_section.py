
import json
from pathlib import Path
import streamlit as st

def load_json(path, fallback):
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return fallback

def publishing_items():
    data = load_json("deploy_data/compact_opportunities.json", [])
    return [
        o for o in data
        if o.get("career_category") == "publishing"
        or o.get("category") == "book_publishing"
        or o.get("import_source") == "publishing_category_import_v1"
    ]

def render_cards_grid(items, render_card=None, key_prefix="publishing"):
    rows = [items[i:i+3] for i in range(0, len(items), 3)]
    for row_index, row in enumerate(rows):
        cols = st.columns(3)
        for col_index, opp in enumerate(row):
            with cols[col_index]:
                if render_card:
                    render_card(opp, f"{key_prefix}_{row_index}_{col_index}_{opp.get('title', 'item')}")
                else:
                    st.write(opp.get("title"))

def render_publishing_section(render_card=None):
    items = publishing_items()

    if not items:
        st.warning("No publishing opportunities found yet. Run python run_publishing_into_existing_opportunities_v1.py first.")
        return

    summary = next(
        (o for o in items if o.get("opportunity_type") == "category_summary"),
        None
    )
    targets = [o for o in items if o.get("opportunity_type") != "category_summary"]
    targets = sorted(targets, key=lambda x: float(x.get("overall_score") or 0), reverse=True)

    st.markdown("## Publishing / Artist Books")

    if summary:
        st.caption(summary.get("one_sentence", ""))
        st.write(summary.get("quick_action", ""))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Targets", len(targets))
    c2.metric("High Priority", len([t for t in targets if t.get("tier") == 1]))
    c3.metric("Cost", "Very low")
    c4.metric("Timeline", "2–6 mo")

    visible = targets[:3]
    hidden = targets[3:]

    st.markdown("### Best Publishing Moves")
    render_cards_grid(visible, render_card=render_card, key_prefix="publishing_best")

    with st.expander("See more publishing targets", expanded=False):
        render_cards_grid(hidden, render_card=render_card, key_prefix="publishing_more")
