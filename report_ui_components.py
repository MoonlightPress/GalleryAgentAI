import streamlit as st


def safe(value, fallback="Not listed"):
    if value is None:
        return fallback

    value = str(value).strip()

    if not value:
        return fallback

    return value


def score_color(score):
    try:
        score = float(score)
    except Exception:
        score = 0

    if score >= 8:
        return "#55705a"

    if score >= 6:
        return "#9c7a42"

    return "#8d5757"


def render_pretty_report(opp):
    title = opp.get("title") or opp.get("name") or "Unknown"

    category = (
        opp.get("category_label")
        or opp.get("category")
        or "Opportunity"
    )

    city = safe(opp.get("city"), "")

    score = safe(opp.get("overall_score"), "?")

    confidence = safe(
        opp.get("confidence_level"),
        "low"
    ).upper()

    st.markdown(
        f"""
<div style="
padding:28px;
border-radius:28px;
background:linear-gradient(
180deg,
rgba(247,243,236,.98),
rgba(241,233,220,.96)
);
border:1px solid #ddcfbc;
margin-bottom:22px;
">

<div style="
font-size:12px;
letter-spacing:.08em;
opacity:.65;
margin-bottom:10px;
">
{category}
</div>

<div style="
font-size:38px;
font-weight:700;
line-height:1.05;
margin-bottom:10px;
font-family:Georgia, serif;
color:#3f3027;
">
{title}
</div>

<div style="
font-size:15px;
opacity:.72;
color:#6f5d4c;
">
{city}
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div style="
padding:18px;
border-radius:18px;
background:#f8f3eb;
border:1px solid #dbcdb8;
margin-bottom:18px;
">

<div style="
font-size:13px;
letter-spacing:.08em;
opacity:.7;
margin-bottom:8px;
">
FIT ANALYSIS
</div>

<div style="
display:flex;
gap:16px;
align-items:center;
">

<div style="
font-size:42px;
font-weight:700;
color:{score_color(score)};
">
{score}/10
</div>

<div>

<div style="
display:inline-block;
padding:6px 12px;
border-radius:999px;
background:#6b5b4d;
color:white;
font-size:12px;
font-weight:600;
margin-bottom:8px;
">
{confidence} CONFIDENCE
</div>

<div style="
font-size:14px;
opacity:.75;
">
Curatorial compatibility estimate
</div>

</div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    tags = [
        opp.get("category_label"),
        opp.get("city"),
        opp.get("verification_status"),
        opp.get("research_priority"),
    ]

    tag_html = ""

    for tag in tags:
        if not tag:
            continue

        tag_html += f"""
<span style="
display:inline-block;
padding:7px 14px;
border-radius:999px;
background:#efe6d8;
margin-right:8px;
margin-bottom:8px;
font-size:12px;
">
{tag}
</span>
"""

    st.markdown(tag_html, unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("### Summary")

        st.write(
            opp.get("one_sentence")
            or opp.get("suggested_display_summary")
            or "No summary available."
        )

        st.markdown("### Verification")

        st.write(
            opp.get("verification_summary")
            or "Verification unknown."
        )

        st.markdown("### Logistics")

        st.write(
            f"Deadline: {safe(opp.get('deadline'))}"
        )

        st.write(
            f"Fees: {safe(opp.get('fees'))}"
        )

        st.write(
            f"Submission: {safe(opp.get('submission_page'))}"
        )

    with right:
        st.markdown("### Why this fits")

        st.write(
            opp.get("why_this_fits_short")
            or "No fit analysis available yet."
        )

        st.markdown("### Quick action")

        st.write(
            opp.get("quick_action")
            or "Review manually."
        )

        source = (
            opp.get("source_link")
            or opp.get("source_url")
            or opp.get("official_website")
            or opp.get("submission_page")
        )

        if source:
            st.link_button(
                "Open source",
                source
            )

    reasons = opp.get("three_bullets", [])

    if reasons:
        st.markdown("### Fit Signals")

        for reason in reasons[:8]:
            st.markdown(
                f"""
<div style="
padding:14px;
border-radius:14px;
background:#f8f4ee;
border:1px solid #e3d6c5;
margin-bottom:10px;
">
✓ {reason}
</div>
""",
                unsafe_allow_html=True,
            )

    if opp.get("dealbreaker"):
        st.markdown(
            f"""
<div style="
padding:16px;
border-radius:18px;
background:#fff4ef;
border:1px solid #e0b7a8;
margin-top:20px;
">
<div style="
font-size:12px;
letter-spacing:.08em;
font-weight:700;
opacity:.65;
margin-bottom:8px;
">
RISK / UNKNOWN
</div>

<div>
{opp.get("dealbreaker")}
</div>

</div>
""",
            unsafe_allow_html=True,
        )