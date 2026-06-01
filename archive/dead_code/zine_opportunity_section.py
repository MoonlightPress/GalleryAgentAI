
import json
from pathlib import Path
import streamlit as st

def load_json(path, fallback):
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return fallback

def zine_items():
    data = load_json("deploy_data/compact_opportunities.json", [])
    return [
        o for o in data
        if o.get("career_category") == "zines"
        or o.get("category") == "zine_print"
        or o.get("import_source") == "zine_category_import_v1"
    ]

def render_simple_zine_card(opp):
    title = opp.get("title") or opp.get("name") or "Untitled"
    city = opp.get("city") or "Tokyo"
    score = opp.get("overall_score", "?")
    summary = opp.get("one_sentence") or opp.get("suggested_display_summary") or ""
    action = opp.get("quick_action") or ""
    source = opp.get("source_url") or opp.get("source_link") or opp.get("official_website") or ""

    with st.container(border=True):
        st.markdown(f"### {title}")
        st.caption(f"{city} · {score}/10")
        if summary:
            st.write(summary)
        if action:
            st.info(action)
        if source:
            st.link_button("Source", source)

def render_cards_grid(items, render_card=None, key_prefix="zine"):
    rows = [items[i:i+3] for i in range(0, len(items), 3)]
    for row_index, row in enumerate(rows):
        cols = st.columns(3)
        for col_index, opp in enumerate(row):
            with cols[col_index]:
                if render_card:
                    render_card(opp, f"{key_prefix}_{row_index}_{col_index}_{opp.get('title', 'item')}")
                else:
                    render_simple_zine_card(opp)

def render_zine_section(render_card=None):
    items = zine_items()

    if not items:
        st.warning("No zine opportunities found yet. Run python run_zines_into_existing_opportunities_v1.py first.")
        return

    summary = next(
        (o for o in items if o.get("opportunity_type") == "category_summary"),
        None
    )
    targets = [
        o for o in items
        if o.get("opportunity_type") != "category_summary"
    ]

    targets = sorted(
        targets,
        key=lambda x: float(x.get("overall_score") or 0),
        reverse=True
    )

    st.markdown("## Zines / Artist Books")

    if summary:
        st.caption(summary.get("one_sentence", ""))
        st.write(summary.get("quick_action", ""))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Targets", len(targets))
    c2.metric("High Priority", len([t for t in targets if t.get("tier") == 1]))
    c3.metric("Koenji + Nakano", len([t for t in targets if t.get("neighborhood") in {"Koenji", "Nakano"}]))
    c4.metric("Est. Cost", "¥10k–¥25k")

    phase_names = {
        "Tacoche",
        "LOCAL Gallery・Books",
        "Dig A Hole Zines",
        "本店・本屋の実験室",
        "そぞろ書房",
    }

    phase1 = [t for t in targets if (t.get("title") or t.get("name")) in phase_names]
    other = [t for t in targets if (t.get("title") or t.get("name")) not in phase_names]

    visible = phase1[:3]
    hidden_phase1 = phase1[3:]

    st.markdown("### Best Zine Moves")
    render_cards_grid(visible, render_card=render_card, key_prefix="zine_best")

    with st.expander("See more zine opportunities", expanded=False):
        if hidden_phase1:
            st.markdown("#### More Phase 1")
            render_cards_grid(hidden_phase1, render_card=render_card, key_prefix="zine_phase1_more")

        if other:
            st.markdown("#### Additional Targets")
            render_cards_grid(other, render_card=render_card, key_prefix="zine_more")
