
import streamlit as st

STATE_COLORS = {
    "unseen": "#b8b1a3",
    "researching": "#b89c5a",
    "interested": "#d89c52",
    "submitted": "#7a9e6e",
    "waiting": "#9b87c8",
    "follow_up": "#d07a7a",
    "conversation_started": "#5c9bb8",
    "soft_relationship": "#6d8e5d",
    "strong_relationship": "#3e6d4c",
    "rejected": "#8c6c6c",
    "archived": "#7c7c7c",
}

def render_relationship_bar(memory):

    state = memory.get(
        "state",
        "unseen",
    )

    color = STATE_COLORS.get(
        state,
        "#b8b1a3",
    )

    interest = memory.get(
        "interest_level",
        0,
    )

    relationship = memory.get(
        "relationship_strength",
        0,
    )

    st.markdown(
        f"""
<div style="
padding:14px 16px;
border-radius:18px;
background:rgba(255,250,242,.95);
border:1px solid #e2cfb1;
margin-bottom:16px;
">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:10px;
">

<div style="
font-weight:700;
color:{color};
">
{state.replace("_", " ").title()}
</div>

<div style="
font-size:.85rem;
color:#7b6b58;
">
Momentum Active
</div>

</div>

<div style="
font-size:.85rem;
color:#6f5d4c;
margin-bottom:6px;
">
Interest Level: {interest}/10
</div>

<div style="
font-size:.85rem;
color:#6f5d4c;
">
Relationship Strength: {relationship}/10
</div>

</div>
""",
        unsafe_allow_html=True,
    )
