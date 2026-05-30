
import streamlit as st

CATEGORY_ICONS = {
    "cafe": "☕",
    "gallery": "🖼️",
    "residency": "⌂",
    "publication": "📚",
    "photobook": "📷",
    "artist_book": "▣",
    "community": "✿",
    "fair": "◎",
    "open_call": "✦",
}

def icon_for(item):
    category = str(item.get("category", "")).lower()

    for key, icon in CATEGORY_ICONS.items():
        if key in category:
            return icon

    return "◌"

def render_visual_card(item):

    title = item.get("title", "Unknown")
    score = item.get("overall_score", "?")
    why = item.get("why_this_fits_short", "")
    city = item.get("city", "")
    country = item.get("country", "")
    icon = icon_for(item)

    st.markdown(
        f"""
<div class="mochi-visual-card">

<div class="visual-card-header">

<div class="visual-card-icon">
{icon}
</div>

<div class="visual-card-score">
{score}/10
</div>

</div>

<div class="visual-card-title">
{title}
</div>

<div class="visual-card-location">
{city} {country}
</div>

<div class="visual-card-why">
{why}
</div>

</div>
""",
        unsafe_allow_html=True,
    )
