
import json
import os
from collections import defaultdict

import streamlit as st

st.set_page_config(page_title="Mochi's Atelier", layout="wide")


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


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
    if "high" in text or "demand" in text:
        return "Heavy"
    return "Check"


def category_label(raw):
    labels = {
        "zine_print": "Print / Zines",
        "bookstore_gallery": "Bookstores",
        "bookstore_event": "Bookstores",
        "cafe_gallery": "Cafe Walls",
        "fair_popup": "Markets / Popups",
        "market_event": "Markets / Popups",
        "artist_space": "Artist Spaces",
        "event_space": "Artist Spaces",
        "gallery_event": "Artist Spaces",
        "gallery": "Galleries",
        "residency": "Residencies",
        "institutional": "Institutional",
    }
    return labels.get(raw, str(raw or "Other").replace("_", " ").title())


def draft_email(opp, lang):
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


def render_card(opp, key):
    title = get_title(opp)
    score = opp.get("overall_score", 0)
    city = opp.get("city", "")
    summary = opp.get("one_sentence", "")

    st.markdown(
        f"""
<div class="card">
  <div class="card-title">{title}</div>
  <span class="chip chip-good">{fit_label(score)}</span>
  <span class="chip">{score}/10</span>
  <span class="chip">{effort_label(opp.get("difficulty"))}</span>
  <span class="chip">{city}</span>
  <div class="summary">{summary[:190]}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.button("Open details", key=key):
        st.session_state["selected_opp"] = opp
        st.rerun()


def render_detail(opp):
    st.markdown('<div class="detail">', unsafe_allow_html=True)

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
            f"""<div class="soft-box">{opp.get("quick_action", "No action available.")}</div>""",
            unsafe_allow_html=True,
        )

        if st.button("Close details"):
            st.session_state["selected_opp"] = None
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
            st.text_area("Chinese draft", draft_email(opp, "zh"), height=220)
        with ja_tab:
            st.text_area("Japanese draft", draft_email(opp, "ja"), height=240)
        with en_tab:
            st.text_area("English draft", draft_email(opp, "en"), height=220)

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    """
<style>
.stApp { background: #f7efe2; }
.block-container { max-width: 1400px; padding-top: 1.25rem; }

.hero {
    background:
        radial-gradient(circle at 8% 20%, rgba(191,137,105,.18), transparent 22%),
        radial-gradient(circle at 92% 15%, rgba(135,160,115,.18), transparent 22%),
        linear-gradient(135deg, #fffaf0 0%, #f1dfc4 100%);
    border: 1px solid #d8bd93;
    border-radius: 30px;
    padding: 32px 36px;
    margin-bottom: 24px;
    box-shadow: 0 10px 26px rgba(70,44,20,.10);
}
.hero h1 {
    margin: 0;
    color: #443226;
    font-family: Georgia, serif;
    font-size: 2.4rem;
}
.hero p {
    margin-top: 8px;
    color: #725f4d;
    font-size: 1.05rem;
}

.card {
    background: #fffaf2;
    border: 1px solid #dfc7a3;
    border-radius: 22px;
    padding: 16px;
    min-height: 220px;
    box-shadow: 0 5px 14px rgba(70,44,20,.07);
    margin-bottom: 10px;
}
.card-title {
    font-family: Georgia, serif;
    color: #443226;
    font-weight: 700;
    font-size: 1.05rem;
    line-height: 1.22;
    margin-bottom: 8px;
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
}
.chip-good {
    background: #e8efd9;
    border-color: #c3d0aa;
}
.summary {
    color: #635242;
    font-size: .92rem;
    line-height: 1.45;
}
.detail {
    background: #fffaf2;
    border: 1px solid #d7bc91;
    border-radius: 26px;
    padding: 24px;
    margin: 22px 0 28px 0;
    box-shadow: 0 10px 28px rgba(70,44,20,.10);
}
.soft-box {
    background: #f4e7cf;
    border: 1px solid #dec5a0;
    border-radius: 16px;
    padding: 14px;
    color: #594636;
    line-height: 1.5;
}
.section-title {
    margin-top: 32px;
    margin-bottom: 10px;
    font-family: Georgia, serif;
    color: #443226;
    font-size: 1.55rem;
    font-weight: 700;
}
</style>
""",
    unsafe_allow_html=True,
)

opps = load_json(
    "deploy_data/compact_opportunities.json",
    load_json("memory/compact_opportunities.json", []),
)
st.write(opps[:2])
st.markdown(
    """
<div class="hero">
  <h1>Mochi's Atelier</h1>
  <p>Gentle opportunity browsing, source links, and ready-to-edit outreach drafts.</p>
</div>
""",
    unsafe_allow_html=True,
)

if not opps:
    st.error("No opportunity data found. Expected deploy_data/compact_opportunities.json.")
    st.stop()

tabs = st.tabs(["Mochi Atelier", "Mousehole", "Observatory", "Archive"])

with tabs[0]:
    st.subheader("Today's Suggestions")

    top = sorted(opps, key=lambda x: -score_num(x.get("overall_score")))[:6]

    cols = st.columns(3)
    for i, opp in enumerate(top):
        with cols[i % 3]:
            render_card(opp, f"top_{i}")

    selected = st.session_state.get("selected_opp")
    if selected:
        render_detail(selected)

    st.markdown("---")
    st.subheader("Browse by Category")

    groups = defaultdict(list)
    for opp in opps:
        groups[category_label(opp.get("category"))].append(opp)

    for category, items in groups.items():
        st.markdown(f'<div class="section-title">{category}</div>', unsafe_allow_html=True)
        sorted_items = sorted(items, key=lambda x: -score_num(x.get("overall_score")))

        cols = st.columns(4)
        for idx, opp in enumerate(sorted_items[:8]):
            with cols[idx % 4]:
                render_card(opp, f"{category}_{idx}")

with tabs[1]:
    st.header("Mousehole")
    st.write("Career pathways and task progress will go here next.")
    st.markdown(
        """
- Upload artist statement
- Upload bio
- Select portfolio set
- Log publications
- Log shows and sales
- Use those materials to improve opportunity ranking
"""
    )

with tabs[2]:
    st.header("Observatory")
    st.write("Reports, market positioning, and long-form analysis will go here next.")

with tabs[3]:
    st.header("Archive")
    st.write("Raw deploy data preview.")
    with st.expander("First 5 opportunities"):
        st.json(opps[:5])
