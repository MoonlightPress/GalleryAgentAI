
import json
import os
from pathlib import Path

import streamlit as st


QUEUE_PATH = "memory/research_queue.json"
REPORT_DIR = Path("memory/generated_analysis")
INQUIRY_DIR = Path("reports/inquiry_drafts")
VENUE_DIR = Path("memory/venues")


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def read_text(path, fallback=""):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return fallback


def slug_match(text):
    return (
        str(text or "")
        .lower()
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
        .replace(":", "")
        .replace("?", "")
        .replace("&", "and")
    )


def find_cached_report(title):
    if not REPORT_DIR.exists():
        return None

    target = slug_match(title)

    # First try loose title matching.
    for path in REPORT_DIR.glob("*.md"):
        if target[:30] and target[:30] in slug_match(path.name):
            return path

    # Fallback: return nothing.
    return None


def render_cached_report_for_opportunity(opp):
    title = opp.get("title") or opp.get("name") or "Unknown"
    path = find_cached_report(title)

    if not path:
        st.warning("No cached report found yet. Run `python analysis_cache_builder.py`.")
        return

    st.markdown(read_text(path))


def render_research_queue_panel():
    st.subheader("Research Queue")

    queue = load_json(QUEUE_PATH, [])

    if not queue:
        st.success("Research queue is empty.")
        return

    high = [x for x in queue if x.get("priority") == "high"]
    medium = [x for x in queue if x.get("priority") == "medium"]
    low = [x for x in queue if x.get("priority") == "low"]

    c1, c2, c3 = st.columns(3)
    c1.metric("High priority", len(high))
    c2.metric("Medium", len(medium))
    c3.metric("Low", len(low))

    priority_filter = st.selectbox(
        "Filter by priority",
        ["all", "high", "medium", "low"],
        key="research_priority_filter"
    )

    if priority_filter != "all":
        queue = [x for x in queue if x.get("priority") == priority_filter]

    for idx, item in enumerate(queue):
        title = item.get("title") or item.get("venue_name") or "Unknown"
        missing = item.get("missing", [])
        source = item.get("source", "")

        with st.expander(f"{title} · {item.get('priority', 'unknown')} · missing {len(missing)}", expanded=idx < 3):
            st.write("**Missing:**", ", ".join(missing) if missing else "Nothing listed")
            st.write("**Recommended action:**", item.get("recommended_action", "Research manually."))
            if item.get("organization"):
                st.write("**Organization:**", item.get("organization"))
            if item.get("score") is not None:
                st.write("**Score:**", item.get("score"))
            if source:
                st.link_button("Open source", source)


def render_inquiry_drafts_panel():
    st.subheader("Inquiry Drafts")

    if not INQUIRY_DIR.exists():
        st.warning("No inquiry drafts found. Run `python inquiry_draft_generator.py`.")
        return

    drafts = sorted(INQUIRY_DIR.glob("*.txt"))

    if not drafts:
        st.success("No inquiry drafts needed.")
        return

    draft_names = [p.name for p in drafts]

    selected = st.selectbox(
        "Choose inquiry draft",
        draft_names,
        key="inquiry_draft_picker"
    )

    path = INQUIRY_DIR / selected
    draft = read_text(path)

    st.text_area("Draft", draft, height=360)


def render_venue_memory_panel():
    st.subheader("Venue Memory")

    if not VENUE_DIR.exists():
        st.warning("No venue records found. Run `python venue_intelligence_builder.py`.")
        return

    venues = sorted(VENUE_DIR.glob("*.json"))

    if not venues:
        st.warning("No venue records found.")
        return

    selected = st.selectbox(
        "Choose venue",
        [p.name for p in venues],
        key="venue_memory_picker"
    )

    venue = load_json(VENUE_DIR / selected, {})

    st.markdown(f"### {venue.get('venue_name', 'Unknown venue')}")
    st.caption(f"{venue.get('venue_type', '')} · {venue.get('city', '')}")

    cols = st.columns(3)
    cols[0].metric("Sources", len(venue.get("source_links", [])))
    cols[1].metric("Missing fields", len(venue.get("missing_information", [])))
    cols[2].metric("Opportunities", len(venue.get("opportunity_titles", [])))

    if venue.get("website"):
        st.link_button("Open website", venue.get("website"))

    st.write("**Categories seen:**", ", ".join(venue.get("categories_seen", [])) or "None")
    st.write("**Missing information:**", ", ".join(venue.get("missing_information", [])) or "None")
    st.write("**Submission style:**", venue.get("submission_style", "unknown"))
    st.write("**Accepts unsolicited work:**", venue.get("accepts_unsolicited_work", "unknown"))

    with st.expander("Raw venue record"):
        st.json(venue)


def render_intelligence_workspace():
    st.header("Mochi Intelligence Workspace")

    tabs = st.tabs([
        "Research Queue",
        "Inquiry Drafts",
        "Venue Memory",
    ])

    with tabs[0]:
        render_research_queue_panel()

    with tabs[1]:
        render_inquiry_drafts_panel()

    with tabs[2]:
        render_venue_memory_panel()
