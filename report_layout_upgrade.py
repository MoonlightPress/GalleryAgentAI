
import streamlit as st

def render_split_report(item):

    venue = item.get("one_sentence", "")
    process = item.get("quick_action", "")
    why = item.get("why_this_fits_short", "")

    bullets = item.get("three_bullets", [])

    st.markdown(
        """
<div class="mochi-detail-grid">
""",
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:

        st.markdown(
            f"""
<div class="mochi-detail-panel">

<div class="mochi-panel-title">
Venue
</div>

<div style="line-height:1.7;color:#5e4b3a;">
{venue}
</div>

<br>

<div class="mochi-panel-title">
Submission Strategy
</div>

<div style="line-height:1.7;color:#5e4b3a;">
{process}
</div>

</div>
""",
            unsafe_allow_html=True,
        )

    with right:

        bullet_html = ""

        for bullet in bullets:
            bullet_html += f"<li>{bullet}</li>"

        st.markdown(
            f"""
<div class="mochi-detail-panel">

<div class="mochi-panel-title">
Why This Works
</div>

<div style="line-height:1.7;color:#5e4b3a;">
{why}
</div>

<ul style="margin-top:14px;line-height:1.8;color:#5e4b3a;">
{bullet_html}
</ul>

</div>
""",
            unsafe_allow_html=True,
        )
