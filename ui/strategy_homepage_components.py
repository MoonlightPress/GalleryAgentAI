
import json
import os
from pathlib import Path
import base64
import streamlit as st
from opportunity_status_engine import mark_saved, mark_not_for_me, load_json as _load_statuses

STATUS_PATH = "memory/opportunity_status.json"

STRATEGY_PATH = "Memory/strategy_feed.json"

SECTION_COPY = {
    "featured": ("Best First Moves", "Strongest current options, balancing fit, confidence, and practical next steps.", "✦"),
    "easy_wins": ("Easy Wins", "Lower-friction opportunities that can build momentum without a major proposal burden.", "☕"),
    "career_changing": ("Career-Changing", "Higher-impact opportunities that may matter for reputation, network, or long-term positioning.", "◈"),
    "portfolio_builders": ("Portfolio Builders", "Good for publication history, artist-book credibility, and visible proof of activity.", "▤"),
    "community_builders": ("Community Builders", "Useful for local connection, peers, low-pressure visibility, and creative confidence.", "⌂"),
    "global_targets": ("Global Targets", "International opportunities that expand her reach beyond local Tokyo/Japan options.", "◎"),
    "publication_targets": ("Publication Targets", "Photobook, zine, artist-book, and magazine opportunities that build visible career evidence.", "▣"),
}

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def score_color(score):
    try:
        score = float(score or 0)
    except Exception:
        score = 0
    if score >= 8:
        return "#4f7a57"
    if score >= 6:
        return "#9b7b3d"
    return "#8a4d4d"

def card_image_for(item):
    bucket = item.get("bucket", "")
    category = str(item.get("category") or "").lower()
    if bucket == "career_changing":
        return "static/assets/cards/card_grant.png"
    if bucket == "easy_win":
        return "static/assets/cards/card_cafe.png"
    if bucket == "portfolio_builder":
        return "static/assets/cards/card_zine.png"
    if bucket == "community_builder":
        return "static/assets/cards/card_market.png"
    if "cafe" in category:
        return "static/assets/cards/card_cafe.png"
    if "zine" in category or "book" in category or "print" in category:
        return "static/assets/cards/card_zine.png"
    if "market" in category or "popup" in category:
        return "static/assets/cards/card_market.png"
    if "residenc" in category:
        return "static/assets/cards/card_residency.png"
    if "gallery" in category:
        return "static/assets/cards/card_gallery.png"
    return "static/assets/cards/card_featured.png"

def img_data(path):
    if not os.path.exists(path):
        return ""
    ext = Path(path).suffix.lower().replace(".", "")
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{mime};base64,{data}"

def render_strategy_css():
    st.markdown('''
<style>
.strategy-section { margin-top: 28px; margin-bottom: 30px; }
.strategy-header {
    display:flex; align-items:center; gap:14px; padding:18px 20px;
    border-radius:22px; background:linear-gradient(180deg, rgba(255,250,242,.98), rgba(244,233,215,.96));
    border:1px solid #e2cfb1; box-shadow:0 6px 18px rgba(70,44,20,.06); margin-bottom:16px;
}
.strategy-mark {
    width:44px; height:44px; border-radius:999px; background:#e8d5b5;
    display:flex; align-items:center; justify-content:center; font-size:23px; color:#4d3a2a; flex:0 0 auto;
}
.strategy-title { font-family:Georgia,"Times New Roman",serif; font-size:1.55rem; font-weight:700; color:#3f3027; line-height:1.1; }
.strategy-subtitle { font-size:.9rem; color:#6f5d4c; line-height:1.35; margin-top:4px; max-width:840px; }
.strategy-card {
    min-height:285px; border-radius:22px; overflow:hidden; background:rgba(255,250,242,.98);
    border:1px solid #e5d4bc; box-shadow:0 8px 20px rgba(70,44,20,.07); margin-bottom:12px;
}
.strategy-card-img { height:92px; background:#efe2cd; background-size:cover; background-position:center; border-bottom:1px solid #e5d4bc; }
.strategy-card-body { padding:14px; }
.strategy-card-title { font-family:Georgia,"Times New Roman",serif; font-size:1.05rem; font-weight:700; line-height:1.15; color:#3f3027; margin-bottom:8px; }
.strategy-card-meta { display:flex; gap:6px; flex-wrap:wrap; margin-bottom:8px; }
.strategy-pill { display:inline-block; padding:3px 8px; border-radius:999px; background:#efe1c8; color:#594636; font-size:.72rem; border:1px solid #dac09b; }
.strategy-card-reason { color:#6f5d4c; font-size:.86rem; line-height:1.35; }
.strategy-score { font-weight:700; }
.strategy-peek { height:34px; border-radius:0 0 18px 18px; background:linear-gradient(180deg, rgba(255,250,242,0), rgba(220,193,155,.28)); margin-top:-8px; margin-bottom:8px; }
</style>
''', unsafe_allow_html=True)

def render_section_header(key):
    title, subtitle, mark = SECTION_COPY.get(key, SECTION_COPY["featured"])
    st.markdown(f'''
<div class="strategy-header">
  <div class="strategy-mark">{mark}</div>
  <div>
    <div class="strategy-title">{title}</div>
    <div class="strategy-subtitle">{subtitle}</div>
  </div>
</div>
''', unsafe_allow_html=True)

def render_strategy_card(item, key):
    title = item.get("title") or "Unknown"
    score = item.get("score", "?")
    confidence = item.get("confidence") or "unknown"
    city = item.get("city") or ""
    category = item.get("category") or ""
    reason = item.get("reason") or "Potentially useful depending on current goals."
    image = img_data(card_image_for(item))
    image_style = f'background-image:url("{image}");' if image else ""
    st.markdown(f'''
<div class="strategy-card">
  <div class="strategy-card-img" style='{image_style}'></div>
  <div class="strategy-card-body">
    <div class="strategy-card-title">{title}</div>
    <div class="strategy-card-meta">
      <span class="strategy-pill strategy-score" style="color:{score_color(score)};">{score}/10</span>
      <span class="strategy-pill">{confidence}</span>
      <span class="strategy-pill">{city}</span>
      <span class="strategy-pill">{category}</span>
    </div>
    <div class="strategy-card-reason">{reason}</div>
  </div>
</div>
''', unsafe_allow_html=True)
    title_key = title.strip().lower()
    statuses = _load_statuses(STATUS_PATH, {})
    opp_key = next((k for k in statuses if k.startswith(title_key + "::")), title_key + "::")
    status = statuses.get(opp_key, {})
    is_saved = status.get("saved", False)
    is_dismissed = status.get("rejected", False)

    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
    with c1:
        if st.button("Details", key=f"{key}_details"):
            st.session_state["selected_title"] = title
            st.session_state["selected_mode"] = "details"
            st.rerun()
    with c2:
        if st.button("Report", key=f"{key}_report"):
            st.session_state["selected_title"] = title
            st.session_state["selected_mode"] = "report"
            st.rerun()
    with c3:
        if is_saved:
            st.button("Saved ✓", key=f"{key}_save", disabled=True)
        elif not is_dismissed:
            if st.button("Save", key=f"{key}_save"):
                mark_saved(opp_key)
                st.rerun()
    with c4:
        if is_dismissed:
            st.button("Dismissed", key=f"{key}_nfm", disabled=True)
        elif not is_saved:
            if st.button("Not for me", key=f"{key}_nfm"):
                mark_not_for_me(opp_key, "Dismissed from strategy card")
                st.rerun()

def render_strategy_section(feed, key):
    items = feed.get(key, [])
    if not items:
        return
    st.markdown('<div class="strategy-section">', unsafe_allow_html=True)
    render_section_header(key)
    cols = st.columns(3)
    for idx, item in enumerate(items[:3]):
        with cols[idx % 3]:
            render_strategy_card(item, f"{key}_top_{idx}")
    if len(items) > 3:
        st.markdown('<div class="strategy-peek"></div>', unsafe_allow_html=True)
        with st.expander(f"Show more · {len(items) - 3} more", expanded=False):
            page_key = f"{key}_page"
            if page_key not in st.session_state:
                st.session_state[page_key] = 0
            remaining = items[3:]
            page_size = 6
            max_page = max((len(remaining) - 1) // page_size, 0)
            st.session_state[page_key] = min(st.session_state[page_key], max_page)
            start = st.session_state[page_key] * page_size
            page_items = remaining[start:start + page_size]
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav1:
                if st.button("‹ Back", key=f"{key}_back", disabled=st.session_state[page_key] <= 0):
                    st.session_state[page_key] -= 1
                    st.rerun()
            with nav2:
                st.caption(f"Page {st.session_state[page_key] + 1} of {max_page + 1}")
            with nav3:
                if st.button("Next ›", key=f"{key}_next", disabled=st.session_state[page_key] >= max_page):
                    st.session_state[page_key] += 1
                    st.rerun()
            cols = st.columns(3)
            for idx, item in enumerate(page_items):
                with cols[idx % 3]:
                    render_strategy_card(item, f"{key}_page_{st.session_state[page_key]}_{idx}")
    st.markdown('</div>', unsafe_allow_html=True)

def render_strategy_homepage():
    render_strategy_css()
    feed = load_json(STRATEGY_PATH, {})
    if not feed:
        st.warning("No strategy feed found. Run python career_strategy_engine.py or python run_full_mochi_pipeline.py.")
        return
    st.markdown('''
<div style="margin-bottom:20px;">
  <div style="font-family:Georgia,serif;font-size:1.9rem;font-weight:700;color:#3f3027;">Curated Career Strategy</div>
  <div style="color:#6f5d4c;font-size:.95rem;max-width:760px;line-height:1.45;">
    Opportunities grouped by strategic purpose: first moves, easy wins, career-changing prospects, portfolio builders, and community builders.
  </div>
</div>
''', unsafe_allow_html=True)
    for key in ["featured", "easy_wins", "global_targets", "publication_targets", "career_changing", "portfolio_builders", "community_builders"]:
        render_strategy_section(feed, key)
