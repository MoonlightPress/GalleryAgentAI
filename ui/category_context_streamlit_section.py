
import json
from pathlib import Path
import streamlit as st

def load_json(path, fallback):
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return fallback

def render_context_metric_row(ctx):
    cols = st.columns(5)
    cols[0].metric("Actionability", ctx.get("actionability_score", "-"))
    cols[1].metric("Found", ctx.get("opportunities_found", 0))
    cols[2].metric("High", ctx.get("high_priority", 0))
    cols[3].metric("Medium", ctx.get("medium_priority", 0))
    cols[4].metric("Deadlines", ctx.get("items_with_deadlines", 0))

def render_context_best_move(move):
    with st.container(border=True):
        st.markdown(f"### {move.get('title', 'Untitled')}")
        st.caption(f"Score {move.get('score', '-')}")
        if move.get("quick_action"):
            st.write(move["quick_action"])
        if move.get("url"):
            st.link_button("Open source", move["url"])

def render_category_context_section():
    data = load_json("deploy_data/category_context.json", {"categories": []})
    categories = data.get("categories", [])

    if not categories:
        st.warning("No category context found. Run python run_category_context_v1.py first.")
        return

    st.markdown("## Opportunity Context")
    st.caption("What is worth acting on next, based on the latest crawl.")

    for ctx in categories:
        with st.expander(f"{ctx['title']} — Actionability {ctx['actionability_score']}", expanded=ctx == categories[0]):
            render_context_metric_row(ctx)

            st.markdown("#### Why this matters")
            st.write(ctx.get("why_this_matters", ""))

            st.markdown("#### Recommendation")
            st.info(ctx.get("recommendation", ""))

            st.markdown("#### Best first move")
            render_context_best_move(ctx.get("best_first_move", {}))

            st.markdown("#### Battle plan")
            for step in ctx.get("battle_plan", []):
                st.write(f"- {step}")

            st.markdown("#### Best moves")
            moves = ctx.get("best_moves", [])
            visible = moves[:3]
            hidden = moves[3:]

            cols = st.columns(3)
            for i, move in enumerate(visible):
                with cols[i]:
                    render_context_best_move(move)

            if hidden:
                with st.expander("See more"):
                    for move in hidden:
                        render_context_best_move(move)
