import streamlit as st
import json
import os

st.set_page_config(page_title="Mochi Atelier", layout="wide")


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


opps = load_json("memory/compact_opportunities.json", [])

st.title("Mochi's Atelier")
st.write("Gentle opportunities, source links, and ready-to-send drafts.")

tabs = st.tabs(["Mochi Atelier", "Mousehole", "Observatory", "Archive"])

with tabs[0]:
    st.header("Today's Suggestions")

    if not opps:
        st.error("No opportunities found. memory/compact_opportunities.json is missing or empty.")
    else:
        top = sorted(
            opps,
            key=lambda x: -float(x.get("overall_score", 0) or 0)
        )[:6]

        cols = st.columns(3)

        for i, opp in enumerate(top):
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(opp.get("title", "Unknown"))
                    st.caption(f"{opp.get('overall_score', 0)} · {opp.get('city', '')}")
                    st.write(opp.get("one_sentence", ""))

                    source = (
                        opp.get("source_link")
                        or opp.get("source_url")
                        or opp.get("official_website")
                    )

                    if source:
                        st.link_button("Open source", source)

                    if st.button("Open details", key=f"open_{i}"):
                        st.session_state["selected"] = opp

        selected = st.session_state.get("selected")

        if selected:
            st.divider()
            st.header(selected.get("title", "Unknown"))

            left, right = st.columns([1, 1.3])

            with left:
                st.write("**Organization:**", selected.get("organization", ""))
                st.write("**Deadline:**", selected.get("deadline", "Check source"))
                st.write("**Fees:**", selected.get("fees", "Check source"))

                source = (
                    selected.get("source_link")
                    or selected.get("source_url")
                    or selected.get("official_website")
                )

                if source:
                    st.link_button("Open source", source)

                st.subheader("Immediate Next Step")
                st.info(selected.get("quick_action", "No action available."))

                if st.button("Close details"):
                    st.session_state["selected"] = None
                    st.rerun()

            with right:
                st.subheader("Why this might fit")
                st.write(selected.get("why_this_fits_short", ""))

                st.subheader("Key points")
                for bullet in selected.get("three_bullets", []):
                    st.write("- " + str(bullet))

                org = selected.get("organization", selected.get("title", ""))

                st.subheader("Draft email")

                draft = f"""Hello,

I am writing to ask whether {org} is currently accepting artist submissions, exhibition proposals, or artist book/zine proposals.

I am an artist working with atmospheric images of architecture, place, memory, and everyday spaces. I would be interested in learning whether my work might fit your programming.

Portfolio:
[portfolio link]

Thank you,
[artist name]"""

                st.text_area("English draft", draft, height=220)

with tabs[1]:
    st.header("Mousehole")
    st.write("Career pathways and task progress will go here.")

with tabs[2]:
    st.header("Observatory")
    st.write("Reports and deeper analysis will go here.")

with tabs[3]:
    st.header("Archive")
    st.write("Memory, accomplishments, and raw records will go here.")