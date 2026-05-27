import json
import os
from collections import defaultdict

import streamlit as st

st.set_page_config(page_title="Mochi's Atelier", layout="wide")


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def score_num(value):
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def get_title(opp):
    return opp.get("title") or opp.get("name") or "Unknown"


def get_source(opp):
    return (
        opp.get("source_link")
        or opp.get("source_url")
        or opp.get("official_website")
        or opp.get("submission_page")
        or ""
    )


def fit_label(score):
    score = score_num(score)
    if score >= 7.5:
        return "Strong fit"
    if score >= 5.5:
        return "Promising"
    if score >= 4:
        return "Possible"
    return "Low priority"


def effort_label(raw):
    text = str(raw or "").lower()
    if "low" in text or "easy" in text:
        return "Easy"
    if "medium" in text or "moderate" in text:
        return "Medium"
    if "high" in text or "heavy" in text or "demand" in text:
        return "Heavy"
    return "Check"


def category_label(raw):
    labels = {
        "zine_print": "Print / Zines / Bookstores",
        "bookstore_gallery": "Print / Zines / Bookstores",
        "bookstore_event": "Print / Zines / Bookstores",
        "cafe_gallery": "Cafe / Local Wall Spaces",
        "fair_popup": "Markets / Popups / Booths",
        "market_event": "Markets / Popups / Booths",
        "artist_space": "Artist Spaces",
        "event_space": "Artist Spaces",
        "gallery_event": "Galleries / Exhibition Calls",
        "gallery": "Galleries / Exhibition Calls",
        "residency": "Residencies / Longer Projects",
        "institutional": "Institutional / Grants",
    }
    return labels.get(raw, str(raw or "Other").replace("_", " ").title())


def section_class(category):
    if "Print" in category or "Book" in category or "Zine" in category:
        return "section-zines"
    if "Cafe" in category:
        return "section-cafes"
    if "Market" in category or "Popup" in category or "Booth" in category:
        return "section-markets"
    if "Residenc" in category:
        return "section-residencies"
    return "section-galleries"


def card_class(opp):
    category = str(opp.get("category", "")).lower()
    if "book" in category or "zine" in category or "print" in category:
        return "card-bookstore"
    if "cafe" in category:
        return "card-cafe"
    if "market" in category or "popup" in category or "fair" in category:
        return "card-market"
    if "residency" in category:
        return "card-residency"
    return "card-gallery"


def make_draft(opp, lang):
    org = opp.get("organization") or get_title(opp)
    if lang == "zh":
        return f"""您好，

我想询问一下，{org} 目前是否接受艺术家投稿、展览提案，或艺术书 / ZINE 相关的作品提案。

我的创作主要关注建筑、场所、记忆，以及日常空间中的安静氛围。如果我的作品有可能适合贵方的项目或空间，我会很高兴进一步了解。

作品集：
[portfolio link]

谢谢。

[artist name]"""
    if lang == "ja":
        return f"""こんにちは。

突然のご連絡失礼いたします。

現在、{org}様でアーティストの応募、展示企画、またはアーティストブック・ZINEの提案を受け付けていらっしゃるかお伺いしたく、ご連絡いたしました。

私は建築、場所、記憶、日常の風景をテーマに、静かな雰囲気の作品を制作しているアーティストです。私の作品が貴施設の企画に合う可能性があるか、ご確認いただけましたら幸いです。

ポートフォリオ：
[portfolio link]

どうぞよろしくお願いいたします。

[artist name]"""
    return f"""Hello,

I am writing to ask whether {org} is currently accepting artist submissions, exhibition proposals, or artist book/zine proposals.

I am an artist working with atmospheric images of architecture, place, memory, and everyday spaces. I would be interested in learning whether my work might fit your programming.

Portfolio:
[portfolio link]

Thank you,
[artist name]"""


st.markdown(
    """
<style>
:root {
    --paper: #f7efe2;
    --paper-soft: #fffaf2;
    --ink: #3f3027;
    --ink-soft: #6f5d4c;
    --line: #dcc19b;
    --line-soft: #ead8bd;
    --button: #4c321f;
    --button-hover: #6a472c;
    --leaf: #dfe8cf;
}

.stApp {
    background-color: var(--paper);
    background-image:url("/app/static/assets/backgrounds/app_bg.png");
    background-size: cover;
    background-attachment: fixed;
    background-position: center top;
}

.block-container {
    max-width: 1440px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    color: var(--ink);
    font-family: Georgia, "Times New Roman", serif;
}

p, li {
    color: var(--ink-soft);
}

.section-banner {
    min-height: 150px;
    border-radius: 24px;
    border: 1px solid var(--line);
    background-size: cover;
    background-position: center center;
    box-shadow: 0 8px 22px rgba(70, 44, 20, .08);
    margin: 34px 0 18px 0;
    padding: 26px 30px;
    display: flex;
    align-items: center;
}

.section-banner h2 {
    margin: 0;
    font-size: 1.65rem;
}

.section-banner p {
    margin: 6px 0 0 0;
    max-width: 520px;
}

.section-zines {
    background-image: linear-gradient(90deg, rgba(255,250,242,.92), rgba(255,250,242,.58)), url("app/static/assets/headers/section_zines.png");
}

.section-cafes {
    background-image: linear-gradient(90deg, rgba(255,250,242,.92), rgba(255,250,242,.58)),url("app/static/assets/headers/section_cafes.png");
}

.section-markets {
    background-image: linear-gradient(90deg, rgba(255,250,242,.92), rgba(255,250,242,.58)),url("app/static/assets/headers/section_markets.png");
}

.section-galleries {
    background-image: linear-gradient(90deg, rgba(255,250,242,.92), rgba(255,250,242,.58)),url("/app/static/assets/headers/section_galleries.png");
}

.section-residencies {
    background-image: linear-gradient(90deg, rgba(255,250,242,.92), rgba(255,250,242,.58)), url("/app/static/assets/headers/section_residencies.png");
}

.opportunity-card {
    position: relative;
    min-height: 235px;
    background: rgba(255, 250, 242, .92);
    border: 1px solid var(--line-soft);
    border-radius: 22px;
    padding: 18px;
    margin-bottom: 12px;
    box-shadow: 0 6px 18px rgba(70, 44, 20, .07);
    overflow: hidden;
}

.opportunity-card:after {
    content: "";
    position: absolute;
    right: 12px;
    bottom: 10px;
    width: 74px;
    height: 74px;
    opacity: .18;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
}

.card-bookstore:after { background-image: url("/app/static/assets/cards/stamp_bookstore.png"); }
.card-cafe:after { background-image: url("/app/static/assets/cards/stamp_cafe.png"); }
.card-market:after { background-image: url("/app/static/assets/cards/stamp_market.png"); }
.card-gallery:after { background-image: url("/app/static/assets/cards/stamp_gallery.png"); }
.card-residency:after { background-image:url("/app/static/assets/cards/stamp_residency.png"); }

.opportunity-title {
    font-family: Georgia, "Times New Roman", serif;
    font-weight: 700;
    font-size: 1.15rem;
    color: var(--ink);
    line-height: 1.22;
    margin-bottom: 10px;
    padding-right: 60px;
}

.opportunity-summary {
    color: var(--ink-soft);
    font-size: .94rem;
    line-height: 1.48;
    margin-top: 8px;
}

.chip {
    display: inline-block;
    background: #efe1c8;
    border: 1px solid #dac09b;
    border-radius: 999px;
    padding: 3px 9px;
    margin: 0 4px 6px 0;
    color: #594636;
    font-size: .78rem;
    white-space: nowrap;
}

.chip-good {
    background: var(--leaf);
    border-color: #c6d1ad;
}

.detail-panel {
    background: rgba(255, 250, 242, .96);
    border: 1px solid var(--line);
    border-radius: 28px;
    padding: 26px;
    margin: 26px 0 34px 0;
    box-shadow: 0 14px 34px rgba(70, 44, 20, .12);
}

.soft-box {
    background: #f4e7cf;
    border: 1px solid #dec5a0;
    border-radius: 16px;
    padding: 14px;
    color: #594636;
    line-height: 1.5;
}



textarea {
    background: #fffdf8 !important;
    color: var(--ink) !important;
    border-radius: 14px !important;
}
/* Safe Streamlit button reset: readable, not black-on-black */
.stButton > button {
    background: #fffaf2 !important;
    color: #3f3027 !important;
    border: 1px solid #dcc19b !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background: #f3e3ca !important;
    color: #3f3027 !important;
    border-color: #caa978 !important;
}

.stLinkButton a {
    background: #fffaf2 !important;
    color: #3f3027 !important;
    border: 1px solid #dcc19b !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

</style>
""",
    unsafe_allow_html=True,
)

def chunked(items, size):
    items = list(items)
    for start in range(0, len(items), size):
        yield items[start:start + size]

def render_card(opp, key):
    title = get_title(opp)
    score = opp.get("overall_score", 0)
    city = opp.get("city", "")
    summary = opp.get("one_sentence", "") or opp.get("suggested_display_summary", "")

    st.markdown(
        f"""
<div class="opportunity-card {card_class(opp)}">
  <div class="opportunity-title">{title}</div>
  <span class="chip chip-good">{fit_label(score)}</span>
  <span class="chip">{score}/10</span>
  <span class="chip">{effort_label(opp.get("difficulty"))}</span>
  <span class="chip">{city}</span>
  <div class="opportunity-summary">{summary[:220]}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.button("Open details", key=key):
        st.session_state["selected_title"] = title
        st.rerun()

def render_detail(opp):
    st.markdown('<div class="detail-panel">', unsafe_allow_html=True)

    left, right = st.columns([1, 1.25])

    with left:
        st.markdown(f"### {get_title(opp)}")
        st.caption(
            f"{fit_label(opp.get('overall_score'))} · "
            f"{opp.get('overall_score', 0)}/10 · "
            f"{effort_label(opp.get('difficulty'))} · "
            f"{opp.get('city', '')}"
        )

        st.write("**Organization:**", opp.get("organization", ""))
        st.write("**Deadline:**", opp.get("deadline", "Check source"))
        st.write("**Fees:**", opp.get("fees", "Check source"))

        source = get_source(opp)
        if source:
            st.link_button("Open source", source)

        st.markdown("#### Immediate next step")
        st.markdown(
            f"""<div class="soft-box">{opp.get('quick_action', 'No action available.')}</div>""",
            unsafe_allow_html=True,
        )

        if st.button("Close details"):
            st.session_state["selected_title"] = None
            st.rerun()

    with right:
        st.markdown("#### Why this might fit")
        st.write(opp.get("why_this_fits_short", ""))

        st.markdown("#### Key points")
        for bullet in opp.get("three_bullets", []):
            st.write("- " + str(bullet))

        st.markdown("#### Drafts")
        zh_tab, ja_tab, en_tab = st.tabs(["中文", "日本語", "English"])

        with zh_tab:
            st.text_area("Chinese draft", make_draft(opp, "zh"), height=220)
        with ja_tab:
            st.text_area("Japanese draft", make_draft(opp, "ja"), height=240)
        with en_tab:
            st.text_area("English draft", make_draft(opp, "en"), height=220)

    st.markdown("</div>", unsafe_allow_html=True)


def render_section_banner(category):
    st.markdown(
        f"""
<div class="section-banner {section_class(category)}">
  <div>
    <h2>{category}</h2>
    <p>Curated opportunities, source links, and ready-to-send drafts.</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


opps = load_json(
    "deploy_data/compact_opportunities.json",
    load_json("memory/compact_opportunities.json", []),
)

# =========================
# HERO
# =========================

hero_path = "static/assets/headers/mochi_hero.png"

if os.path.exists(hero_path):
    import base64

    with open(hero_path, "rb") as f:
        hero_b64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .hero-box {{
        position: relative;
        height: 430px;
        margin-bottom: 28px;
        border-radius: 28px;
        overflow: hidden;
        border: 1px solid #dcc19b;
        box-shadow: 0 14px 34px rgba(70,44,20,.12);
        background-image: url("data:image/png;base64,{hero_b64}");
        background-size: cover;
        background-position: center center;
    }}

    .hero-box .hero-title {{
        position: absolute;
        top: 64px;
        left: 58px;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 3.2rem;
        color: #3f3027;
        line-height: 1;
    }}

    .hero-box .hero-subtitle {{
        position: absolute;
        top: 138px;
        left: 58px;
        max-width: 470px;
        font-size: 1.12rem;
        line-height: 1.45;
        color: #5e4d3d;
        background: rgba(255,248,240,.72);
        padding: 12px 16px;
        border-radius: 14px;
    }}
    </style>

    <div class="hero-box">
        <div class="hero-title">Mochi's Atelier</div>
        <div class="hero-subtitle">
            Gentle opportunity browsing, source links,
            and ready-to-edit outreach drafts.
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error(f"Hero image not found: {hero_path}")

if not opps:
    st.error("No opportunity data found. Expected deploy_data/compact_opportunities.json.")
    st.stop()

tabs = st.tabs(["Mochi Atelier", "Mousehole", "Observatory", "Archive"])

with tabs[0]:
    st.subheader("Today's Suggestions")

    top = sorted(opps, key=lambda x: -score_num(x.get("overall_score")))[:12]

    if "suggestion_page" not in st.session_state:
        st.session_state["suggestion_page"] = 0

    pages = list(chunked(top, 3))
    max_page = max(len(pages) - 1, 0)
    st.session_state["suggestion_page"] = min(st.session_state["suggestion_page"], max_page)

    nav_left, nav_mid, nav_right = st.columns([1, 3, 1])
    with nav_left:
        if st.button("‹ Previous", key="suggestions_prev", disabled=st.session_state["suggestion_page"] <= 0):
            st.session_state["suggestion_page"] -= 1
            st.rerun()
    with nav_mid:
        st.caption(f"Set {st.session_state['suggestion_page'] + 1} of {len(pages)}")
    with nav_right:
        if st.button("Next ›", key="suggestions_next", disabled=st.session_state["suggestion_page"] >= max_page):
            st.session_state["suggestion_page"] += 1
            st.rerun()

    visible = pages[st.session_state["suggestion_page"]] if pages else []
    cols = st.columns(3)
    for i, opp in enumerate(visible):
        with cols[i]:
            render_card(opp, f"top_{st.session_state['suggestion_page']}_{i}_{get_title(opp)}")

selected_title = st.session_state.get("selected_title")

if selected_title:
    selected = next(
        (o for o in opps if get_title(o) == selected_title),
        None
    )

    if selected:
        render_detail(selected)

    st.markdown("---")
    st.subheader("Browse by Category")

    groups = defaultdict(list)
    for opp in opps:
        groups[category_label(opp.get("category"))].append(opp)

    for category, items in groups.items():
        render_section_banner(category)
        sorted_items = sorted(items, key=lambda x: -score_num(x.get("overall_score")))

        cols = st.columns(4)
        for idx, opp in enumerate(sorted_items[:8]):
            with cols[idx % 4]:
                render_card(opp, f"{category}_{idx}_{get_title(opp)}")

with tabs[1]:
    st.header("Mousehole")
    st.write("Career pathways and task progress will go here next.")

with tabs[2]:
    st.header("Observatory")
    st.write("Reports, market positioning, and long-form analysis will go here next.")

with tabs[3]:
    st.header("Archive")
    st.write(f"Loaded {len(opps)} opportunities.")
