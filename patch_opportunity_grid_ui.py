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

        priorities = {
            "low": 0,
            "Low": 0,
            "Low-Medium": 1,
            "medium": 2,
            "medium-high": 3,
            "high": 4,
            "Very High": 5,
            "extremely_high": 6
        }

        opportunities = sorted(
            opportunities,
            key=lambda x: (
                priorities.get(str(x.get("difficulty", "")), 3),
                -float(x.get("overall_score", 0) or 0)
            )
        )

        for row_start in range(0, len(opportunities), 4):
            cols = st.columns(4)

            for col, opp in zip(cols, opportunities[row_start:row_start + 4]):
                with col:
                    title = opp.get("title", "Unknown")
                    score = opp.get("overall_score", 0)
                    difficulty = opp.get("difficulty", "unknown")
                    city = opp.get("city", "")
                    sentence = opp.get("one_sentence", "")
                    quick_action = opp.get("quick_action", "")
                    source = (
                        opp.get("source_link")
                        or opp.get("source_url")
                        or opp.get("official_website")
                        or ""
                    )

                    st.markdown(
                        f"""
                        <div style="
                            border: 1px solid #ddd;
                            border-radius: 14px;
                            padding: 14px;
                            margin-bottom: 12px;
                            min-height: 260px;
                            background: #fafafa;
                        ">
                            <h4 style="margin-top: 0;">{title}</h4>
                            <p><b>Score:</b> {score}</p>
                            <p><b>Difficulty:</b> {difficulty}</p>
                            <p><b>City:</b> {city}</p>
                            <p style="font-size: 0.9em;">{sentence[:180]}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "Open",
                        key=f"open_{row_start}_{title}"
                    ):
                        st.session_state["selected_opportunity"] = opp

        selected = st.session_state.get("selected_opportunity")

        if selected:
            st.markdown("---")

            st.header(selected.get("title", "Unknown"))

            score = selected.get("overall_score", 0)
            difficulty = selected.get("difficulty", "unknown")
            city = selected.get("city", "")
            category = selected.get("category", "")
            org = selected.get("organization", "")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Score", score)
            col2.metric("Difficulty", difficulty)
            col3.metric("City", city)
            col4.metric("Category", category)

            st.write(f"**Organization:** {org}")

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

            st.markdown("### Workflow Status")

            current_status = selected.get("workflow_status", "DISCOVERED")
            st.write(f"Current Status: **{current_status}**")

            s1, s2, s3, s4, s5 = st.columns(5)

            if s1.button("Interested"):
                selected["workflow_status"] = "INTERESTED"

            if s2.button("Researching"):
                selected["workflow_status"] = "RESEARCHING"

            if s3.button("Preparing"):
                selected["workflow_status"] = "PREPARING"

            if s4.button("Submitted"):
                selected["workflow_status"] = "SUBMITTED"

            if s5.button("Archive"):
                selected["workflow_status"] = "ARCHIVED"

            st.markdown("### Submission Starter")

            st.text_area(
                "Draft email / inquiry starter",
                value=f"""Hello,

I am writing to ask whether {selected.get("organization", selected.get("title", ""))} is currently accepting artist submissions or exhibition proposals.

I am an artist working with atmospheric images of architecture, place, memory, and disappearing everyday spaces. I would be interested in learning whether my work might fit your programming.

Portfolio:
[portfolio link]

Thank you,
[artist name]""",
                height=220
            )

            st.markdown("### Expand More")

            with st.expander("Logistics / Evidence"):
                st.write("**Deadline:**", selected.get("deadline", "Unknown"))
                st.write("**Fees:**", selected.get("fees", "Unknown"))
                st.write("**Official Website:**", selected.get("official_website", ""))
                st.write("**Submission Page:**", selected.get("submission_page", ""))
                st.write("**Source URL:**", selected.get("source_url", ""))

            with st.expander("Raw Compact Record"):
                st.json(selected)
'''

text = text[:start] + new_block + text[end:]

path.write_text(text, encoding="utf-8")

print("Patched Opportunities tab into 4-column grid with detail panel.")