from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

start = text.index("with tabs[2]:")
end = text.index("\nwith tabs[3]:")

new_block = '''with tabs[2]:
    st.markdown("## 🐾 Opportunities")
    st.caption("Low-friction first. Click More to inspect, prepare, and act.")

    opportunities = load_json("memory/compact_opportunities.json", [])

    if not opportunities:
        st.info("No compact opportunities generated yet. Run compact_view_agent.py first.")

    else:
        section_map = {
            "Print / Zines / Bookstores": [
                "zine_print",
                "bookstore_gallery",
                "bookstore_event"
            ],
            "Cafe / Local Wall Spaces": [
                "cafe_gallery"
            ],
            "Markets / Popups / Booths": [
                "fair_popup",
                "market_event"
            ],
            "Artist Spaces / Community": [
                "artist_space",
                "event_space",
                "gallery_event"
            ],
            "Galleries": [
                "gallery"
            ],
            "Residencies / Institutional": [
                "residency",
                "institutional"
            ]
        }

        selected = st.session_state.get("selected_opportunity")
        selected_section = st.session_state.get("selected_section")

        def score_badge(score):
            try:
                score = float(score)
            except Exception:
                return "○"

            if score >= 7:
                return "●"
            if score >= 5:
                return "◐"
            return "○"

        def render_card(opp, key):
            title = opp.get("title", "Unknown")
            score = opp.get("overall_score", 0)
            difficulty = str(opp.get("difficulty", "unknown"))
            city = opp.get("city", "")
            sentence = opp.get("one_sentence", "")

            with st.container(border=True):
                st.markdown(f"**{score_badge(score)} {title}**")
                st.caption(f"{score} · {difficulty} · {city}")
                st.write(sentence[:135] + ("..." if len(sentence) > 135 else ""))

                if st.button("More", key=key):
                    st.session_state["selected_opportunity"] = opp
                    st.session_state["selected_section"] = st.session_state.get("current_section")
                    st.rerun()

        def render_detail(selected):
            st.markdown("---")

            left, right = st.columns([1, 1.4])

            with left:
                st.markdown(f"### {selected.get('title', 'Unknown')}")
                st.caption(
                    f"{selected.get('overall_score', 0)} · "
                    f"{selected.get('difficulty', 'unknown')} · "
                    f"{selected.get('city', '')}"
                )

                st.write("**Organization:**", selected.get("organization", ""))

                source_link = (
                    selected.get("source_link")
                    or selected.get("source_url")
                    or selected.get("official_website")
                )

                if source_link:
                    st.markdown(f"[Open Source Link]({source_link})")

                st.markdown("#### Immediate Next Step")
                st.info(selected.get("quick_action", "No action available."))

                st.markdown("#### Key Points")
                for bullet in selected.get("three_bullets", []):
                    st.write(f"- {bullet}")

                with st.expander("Logistics / Evidence"):
                    st.write("**Deadline:**", selected.get("deadline", "Unknown"))
                    st.write("**Fees:**", selected.get("fees", "Unknown"))
                    st.write("**Official Website:**", selected.get("official_website", ""))
                    st.write("**Submission Page:**", selected.get("submission_page", ""))
                    st.write("**Source URL:**", selected.get("source_url", ""))

            with right:
                st.markdown("#### Why This Might Fit")
                st.write(selected.get("why_this_fits_short", ""))

                st.markdown("#### Submission Starter")
                st.text_area(
                    "Draft email / inquiry starter",
                    value=f"""Hello,

I am writing to ask whether {selected.get("organization", selected.get("title", ""))} is currently accepting artist submissions, exhibition proposals, or artist book/zine proposals.

I am an artist working with atmospheric images of architecture, place, memory, and everyday spaces. I would be interested in learning whether my work might fit your programming.

Portfolio:
[portfolio link]

Thank you,
[artist name]""",
                    height=180,
                    key=f"email_{selected.get('title', 'unknown')}"
                )

                with st.expander("Council / Strategy Notes"):
                    st.write("This section should eventually pull the full council notes from the master record, not just compact output.")

                with st.expander("Raw Compact Record"):
                    st.json(selected)

        for section_name, categories in section_map.items():

            section_opps = [
                opp for opp in opportunities
                if opp.get("category") in categories
            ]

            if not section_opps:
                continue

            section_opps = sorted(
                section_opps,
                key=lambda x: -float(x.get("overall_score", 0) or 0)
            )

            st.session_state["current_section"] = section_name

            st.markdown(f"### {section_name}")

            cols = st.columns(4)

            for idx, opp in enumerate(section_opps[:4]):
                with cols[idx]:
                    render_card(
                        opp,
                        f"more_{section_name}_{idx}_{opp.get('title', 'unknown')}"
                    )

            if selected and selected_section == section_name:
                render_detail(selected)

            if len(section_opps) > 4:
                with st.expander(f"More {section_name}"):
                    more_cols = st.columns(4)
                    for idx, opp in enumerate(section_opps[4:8]):
                        with more_cols[idx]:
                            render_card(
                                opp,
                                f"more_extra_{section_name}_{idx}_{opp.get('title', 'unknown')}"
                            )

            st.markdown("---")
'''

text = text[:start] + new_block + text[end:]
path.write_text(text, encoding="utf-8")

print("Patched dense opportunity UI.")