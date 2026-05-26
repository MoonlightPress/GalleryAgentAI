from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

start = text.index("with tabs[2]:")
end = text.index("\nwith tabs[3]:")

new_block = '''with tabs[2]:
    st.header("Opportunities")

    opportunities = load_json("memory/compact_opportunities.json", [])

    if not opportunities:
        st.info("No compact opportunities generated yet. Run compact_view_agent.py first.")

    else:
        st.caption(f"{len(opportunities)} sourced opportunities loaded")

        section_map = {
            "Low-Friction Publishing / Zines": [
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

        def render_detail(selected):
            st.markdown("---")
            st.header(selected.get("title", "Unknown"))

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Score", selected.get("overall_score", 0))
            col2.metric("Difficulty", selected.get("difficulty", "unknown"))
            col3.metric("City", selected.get("city", ""))
            col4.metric("Category", selected.get("category", ""))

            st.write("**Organization:**", selected.get("organization", ""))

            source_link = (
                selected.get("source_link")
                or selected.get("source_url")
                or selected.get("official_website")
            )

            if source_link:
                st.markdown(f"[Open Source Link]({source_link})")

            st.markdown("### Immediate Next Step")
            st.info(selected.get("quick_action", "No action available."))

            st.markdown("### Why This Fits")
            st.write(selected.get("why_this_fits_short", ""))

            st.markdown("### Key Points")
            for bullet in selected.get("three_bullets", []):
                st.write(f"- {bullet}")

            st.markdown("### Submission Starter")

            st.text_area(
                "Draft email / inquiry starter",
                value=f"""Hello,

I am writing to ask whether {selected.get("organization", selected.get("title", ""))} is currently accepting artist submissions, exhibition proposals, or artist book/zine proposals.

I am an artist working with atmospheric images of architecture, place, memory, and disappearing everyday spaces. I would be interested in learning whether my work might fit your programming.

Portfolio:
[portfolio link]

Thank you,
[artist name]""",
                height=220,
                key=f"email_{selected.get('title', 'unknown')}"
            )

            with st.expander("Logistics / Evidence"):
                st.write("**Deadline:**", selected.get("deadline", "Unknown"))
                st.write("**Fees:**", selected.get("fees", "Unknown"))
                st.write("**Official Website:**", selected.get("official_website", ""))
                st.write("**Submission Page:**", selected.get("submission_page", ""))
                st.write("**Source URL:**", selected.get("source_url", ""))

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

            st.subheader(section_name)

            cols = st.columns(4)

            for idx, opp in enumerate(section_opps[:8]):

                col = cols[idx % 4]

                with col:
                    title = opp.get("title", "Unknown")
                    score = opp.get("overall_score", 0)
                    difficulty = opp.get("difficulty", "unknown")
                    city = opp.get("city", "")
                    sentence = opp.get("one_sentence", "")

                    st.markdown(
                        f"""
                        <div style="
                            border: 1px solid #ddd;
                            border-radius: 14px;
                            padding: 14px;
                            margin-bottom: 8px;
                            min-height: 230px;
                            background: #fafafa;
                        ">
                            <h4 style="margin-top: 0;">{title}</h4>
                            <p><b>Score:</b> {score}</p>
                            <p><b>Difficulty:</b> {difficulty}</p>
                            <p><b>City:</b> {city}</p>
                            <p style="font-size: 0.9em;">{sentence[:150]}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "More",
                        key=f"more_{section_name}_{idx}_{title}"
                    ):
                        st.session_state["selected_opportunity"] = opp
                        st.session_state["selected_section"] = section_name
                        st.rerun()

            if selected and selected_section == section_name:
                render_detail(selected)

            st.markdown("---")
'''

text = text[:start] + new_block + text[end:]

path.write_text(text, encoding="utf-8")

print("Patched Opportunities tab into section rows with inline detail panels.")