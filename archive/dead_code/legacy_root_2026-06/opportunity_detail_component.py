import streamlit as st


def render_opportunity_detail(opp):

    st.markdown(f"# {opp.get('name', 'Unknown')}")

    st.markdown(
        f"""
**Organization:** {opp.get('organization', 'Unknown')}

**Category:** {opp.get('category', 'Unknown')}

**Location:** {opp.get('city', '')}, {opp.get('country', '')}

**Difficulty:** {opp.get('friction_level', 'Unknown')}

**Status:** {opp.get('status', 'Unknown')}
"""
    )

    source = opp.get("source_link", "")

    if source:
        st.markdown(f"[Open Source Link]({source})")

    compact = (
        opp.get("council_review", {})
        .get("compact_card", {})
    )

    st.markdown("---")

    st.markdown("## Overview")

    st.write(
        compact.get(
            "one_sentence",
            "No overview available."
        )
    )

    bullets = compact.get("three_bullets", [])

    if bullets:
        st.markdown("## Key Points")

        for bullet in bullets:
            st.markdown(f"- {bullet}")

    quick_action = compact.get("quick_action")

    if quick_action:
        st.markdown("## Immediate Next Step")
        st.info(quick_action)

    fit = compact.get("why_this_fits_short")

    if fit:
        st.markdown("## Why This Fits")
        st.write(fit)

    protective = (
        opp.get("council_review", {})
        .get("protective_voice", {})
    )

    st.markdown("---")

    st.markdown("## Emotional / Energy Considerations")

    emotional = protective.get(
        "likely_emotional_response"
    )

    if emotional:
        st.write(f"**Likely reaction:** {emotional}")

    friction = protective.get(
        "potential_friction",
        []
    )

    if friction:
        st.markdown("### Possible Friction")

        for item in friction:
            st.markdown(f"- {item}")

    softer = protective.get(
        "softer_summary"
    )

    if softer:
        st.markdown("### Guidance")
        st.write(softer)

    notes = (
        opp.get("council_review", {})
        .get("council_notes", {})
    )

    st.markdown("---")

    st.markdown("## Council Discussion")

    for role, text in notes.items():

        role_name = (
            role.replace("_", " ")
            .title()
        )

        with st.expander(role_name):
            st.write(text)