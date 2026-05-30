
import json
import os
from pathlib import Path

import streamlit as st

from opportunity_status_engine import (
    load_json,
    save_json,
    key_for,
    mark_saved,
    mark_rejected,
    mark_contacted,
    mark_response_received,
    build_action_queue,
)


STATUS_PATH = "memory/opportunity_status.json"
ACTION_QUEUE_PATH = "memory/action_queue.json"
OPP_PATH = "deploy_data/compact_opportunities.json"


def title_of(opp):
    return opp.get("title") or opp.get("name") or "Unknown"


def find_opp_by_key(key):
    opps = load_json(OPP_PATH, [])
    for opp in opps:
        if key_for(opp) == key:
            return opp
    return None


def render_status_controls(opp, key_prefix="status"):
    key = key_for(opp)
    statuses = load_json(STATUS_PATH, {})
    status = statuses.get(key, {})

    st.caption(
        f"Status: {status.get('status', 'new')} · "
        f"Follow-up: {status.get('follow_up_date') or 'not set'}"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if st.button("Save", key=f"{key_prefix}_save_{key}"):
            mark_saved(key)
            build_action_queue()
            st.rerun()

    with c2:
        if st.button("Contacted", key=f"{key_prefix}_contacted_{key}"):
            mark_contacted(key)
            build_action_queue()
            st.rerun()

    with c3:
        if st.button("Response", key=f"{key_prefix}_response_{key}"):
            mark_response_received(key)
            build_action_queue()
            st.rerun()

    with c4:
        if st.button("Reject", key=f"{key_prefix}_reject_{key}"):
            mark_rejected(key, "Rejected from app UI.")
            build_action_queue()
            st.rerun()


def render_action_queue_panel():
    st.header("Action Queue")

    if st.button("Refresh action queue"):
        build_action_queue()
        st.rerun()

    queue = load_json(ACTION_QUEUE_PATH, [])

    if not queue:
        st.warning("No action queue yet. Run `python opportunity_status_engine.py`.")
        return

    high = [x for x in queue if x.get("priority") == "high"]
    medium = [x for x in queue if x.get("priority") == "medium"]
    low = [x for x in queue if x.get("priority") == "low"]

    c1, c2, c3 = st.columns(3)
    c1.metric("High", len(high))
    c2.metric("Medium", len(medium))
    c3.metric("Low", len(low))

    priority = st.selectbox("Priority", ["all", "high", "medium", "low"], key="action_priority_filter")

    visible = queue if priority == "all" else [x for x in queue if x.get("priority") == priority]

    for idx, item in enumerate(visible[:40]):
        title = item.get("title", "Unknown")
        score = item.get("score", "")
        priority = item.get("priority", "")
        status = item.get("status", "")

        with st.expander(f"{title} · {score}/10 · {priority} · {status}", expanded=idx < 4):
            st.write("**Recommended action:**", item.get("recommended_action"))
            st.write("**Missing:**", ", ".join(item.get("missing", [])) or "None")
            st.write("**Organization:**", item.get("organization") or "Not listed")

            opp = find_opp_by_key(item.get("key"))
            if opp:
                render_status_controls(opp, key_prefix=f"queue_{idx}")


def render_saved_opportunities_panel():
    st.header("Saved Opportunities")

    statuses = load_json(STATUS_PATH, {})
    opps = load_json(OPP_PATH, [])

    saved = []
    for opp in opps:
        status = statuses.get(key_for(opp), {})
        if status.get("saved") and not status.get("rejected"):
            saved.append((opp, status))

    if not saved:
        st.info("No saved opportunities yet.")
        return

    for idx, (opp, status) in enumerate(saved):
        with st.expander(f"{title_of(opp)} · {opp.get('overall_score', '?')}/10 · {status.get('status', 'saved')}", expanded=idx < 3):
            st.write("**Follow-up:**", status.get("follow_up_date") or "not set")
            st.write("**Notes:**", status.get("notes") or "")
            render_status_controls(opp, key_prefix=f"saved_{idx}")


def render_action_workspace():
    tabs = st.tabs(["Action Queue", "Saved"])

    with tabs[0]:
        render_action_queue_panel()

    with tabs[1]:
        render_saved_opportunities_panel()
