
import base64
import json
import os
from collections import defaultdict
from report_ui_components import *
import streamlit as st
from report_ui_components import render_pretty_report
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


def clean_value(value, fallback="Not publicly listed"):
    if value is None:
        return fallback
    value = str(value).strip()
    if not value or value.lower() in {"unknown", "none", "null", "n/a"}:
        return fallback
    return value


def score_label(score):
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


def image_for_category(raw):
    category = str(raw or "").lower()
    if "book" in category or "zine" in category or "print" in category:
        return "static/assets/cards/stamp_bookstore.png"
    if "cafe" in category:
        return "static/assets/cards/stamp_cafe.png"
    if "market" in category or "popup" in category or "fair" in category:
        return "static/assets/cards/stamp_market.png"
    if "residency" in category:
        return "static/assets/cards/stamp_residency.png"
    return "static/assets/cards/stamp_gallery.png"


def image_data_uri(path):
    if not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lower().replace(".", "")
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{mime};base64,{data}"


def verification_badges(opp):
    source = get_source(opp)
    deadline = clean_value(opp.get("deadline"), "")
    fees = clean_value(opp.get("fees"), "")
    submission = clean_value(opp.get("submission_page"), "")

    badges = []
    badges.append(("verified", "Website") if source else ("missing", "No source"))
    badges.append(("verified", "Submission link") if submission else ("needs", "Submission unclear"))
    badges.append(("verified", "Deadline listed") if deadline else ("needs", "Deadline needed"))
    badges.append(("verified", "Fees listed") if fees else ("needs", "Fees needed"))
    return badges


def verification_summary(opp):
    badges = verification_badges(opp)
    missing = [label for status, label in badges if status in {"needs", "missing"}]
    if not missing:
        return "Core public details are present."
    return "Needs verification: " + ", ".join(missing[:3]) + ("." if len(missing) <= 3 else "…")


def report_markdown(opp):
    source = get_source(opp)
    bullets = opp.get("three_bullets", [])
    bullet_text = "\n".join([f"- {b}" for b in bullets]) if bullets else "- No bullet analysis available yet."

    return f"""
### {get_title(opp)}

**Snapshot**  
{score_label(opp.get("overall_score"))} · {opp.get("overall_score", "?")}/10 · {clean_value(opp.get("city"), "City not listed")} · {category_label(opp.get("category"))}

**Verified / missing information**  
{verification_summary(opp)}

**Known public facts**  
- Organization: {clean_value(opp.get("organization"))}
- Website/source: {source or "Not found"}
- Submission page: {clean_value(opp.get("submission_page"))}
- Deadline: {clean_value(opp.get("deadline"))}
- Fees: {clean_value(opp.get("fees"))}

**Fit analysis**  
{clean_value(opp.get("why_this_fits_short"), "No fit analysis available yet.")}

**Key points**  
{bullet_text}

**Risk / uncertainty**  
{clean_value(opp.get("dealbreaker"), "No specific dealbreaker listed. Manual verification still recommended.")}

**Recommended next step**  
{clean_value(opp.get("quick_action"), "Visit the source and verify current submission/contact details.")}
"""


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
    --leaf: #dfe8cf;
}

.stApp {
    background-color: var(--paper);
}

.block-container {
    max-width: 1440px;
    padding-top: 1.0rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: var(--ink);
    font-family: Georgia, "Times New Roman", serif;
}

p, li {
    color: var(--ink-soft);
}

.compact-card {
    position: relative;
    min-height: 190px;
    background: rgba(255, 250, 242, .96);
    border: 1px solid var(--line-soft);
    border-radius: 20px;
    padding: 14px 14px 12px 14px;
    margin-bottom: 6px;
    box-shadow: 0 5px 15px rgba(70, 44, 20, .06);
}

.card-topline {
    display: flex;
    gap: 12px;
    align-items: flex-start;
}

.card-stamp {
    width: 58px;
    height: 58px;
    object-fit: contain;
    opacity: .95;
    flex: 0 0 auto;
}

.card-main {
    min-width: 0;
}

.card-title {
    font-family: Georgia, "Times New Roman", serif;
    font-weight: 700;
    font-size: 1.08rem;
    color: var(--ink);
    line-height: 1.15;
    margin-bottom: 5px;
}

.card-meta {
    color: #7b6756;
    font-size: .78rem;
    margin-bottom: 7px;
}

.card-summary {
    color: var(--ink-soft);
    font-size: .88rem;
    line-height: 1.35;
    margin-top: 8px;
}

.chip {
    display: inline-block;
    background: #efe1c8;
    border: 1px solid #dac09b;
    border-radius: 999px;
    padding: 2px 8px;
    margin: 0 4px 4px 0;
    color: #594636;
    font-size: .72rem;
    white-space: nowrap;
}

.chip-good {
    background: var(--leaf);
    border-color: #c6d1ad;
}

.badge-ok {
    display: inline-block;
    background: #e2ead5;
    color: #435134;
    border-radius: 999px;
    padding: 2px 7px;
    font-size: .70rem;
    margin: 0 4px 4px 0;
}

.badge-need {
    display: inline-block;
    background: #f4e3c7;
    color: #6a4e2f;
    border-radius: 999px;
    padding: 2px 7px;
    font-size: .70rem;
    margin: 0 4px 4px 0;
}

.detail-panel {
    background: rgba(255, 250, 242, .98);
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 20px;
    margin: 18px 0 26px 0;
    box-shadow: 0 12px 28px rgba(70, 44, 20, .10);
}

.report-box {
    background: #fffdf8;
    border: 1px solid #ead8bd;
    border-radius: 18px;
    padding: 18px;
    margin-top: 12px;
}

.soft-box {
    background: #f4e7cf;
    border: 1px solid #dec5a0;
    border-radius: 14px;
    padding: 12px;
    color: #594636;
    line-height: 1.45;
}

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

textarea {
    background: #fffdf8 !important;
    color: var(--ink) !important;
    border-radius: 14px !important;
}
</style>
""",
    unsafe_allow_html=True,
)


def render_compact_card(opp, key_prefix):
    title = get_title(opp)
    score = opp.get("overall_score", "?")
    city = clean_value(opp.get("city"), "City not listed")
    summary = opp.get("one_sentence", "") or opp.get("suggested_display_summary", "")
    category = category_label(opp.get("category"))
    stamp = image_data_uri(image_for_category(opp.get("category")))

    badge_html = ""
    for status, label in verification_badges(opp)[:3]:
        cls = "badge-ok" if status == "verified" else "badge-need"
        badge_html += f'<span class="{cls}">{label}</span>'

    img_html = f'<img class="card-stamp" src="{stamp}">' if stamp else ""

    st.markdown(
        f"""
<div class="compact-card">
  <div class="card-topline">
    {img_html}
    <div class="card-main">
      <div class="card-title">{title}</div>
      <div class="card-meta">{city} · {category} · {score}/10 · {score_label(score)} · {effort_label(opp.get("difficulty"))}</div>
      <div>{badge_html}</div>
      <div class="card-summary">{summary[:190]}</div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    b1, b2, b3 = st.columns([1, 1, 1.2])
    with b1:
        if st.button("Details", key=f"{key_prefix}_details"):
            st.session_state["selected_title"] = title
            st.session_state["selected_mode"] = "details"
            st.rerun()
    with b2:
        if st.button("Report", key=f"{key_prefix}_report"):
            st.session_state["selected_title"] = title
            st.session_state["selected_mode"] = "report"
            st.rerun()
    with b3:
        source = get_source(opp)
        if source:
            st.link_button("Source", source)


def render_detail(opp):
    render_pretty_report(opp)
    mode = st.session_state.get("selected_mode", "details")

    st.markdown('<div class="detail-panel">', unsafe_allow_html=True)
    st.markdown(f"### {get_title(opp)}")
    st.caption(
        f"{score_label(opp.get('overall_score'))} · "
        f"{opp.get('overall_score', '?')}/10 · "
        f"{clean_value(opp.get('city'), 'City not listed')} · "
        f"{category_label(opp.get('category'))}"
    )

    if mode == "report":
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown(report_markdown(opp))
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        left, right = st.columns([1, 1.3])

        with left:
            st.write("**Organization:**", clean_value(opp.get("organization")))
            st.write("**Deadline:**", clean_value(opp.get("deadline")))
            st.write("**Fees:**", clean_value(opp.get("fees")))
            st.write("**Verification:**", verification_summary(opp))

            source = get_source(opp)
            if source:
                st.link_button("Open source", source)

            st.markdown("#### Immediate next step")
            st.markdown(
                f"""<div class="soft-box">{clean_value(opp.get('quick_action'), 'Verify current public submission/contact details.')}</div>""",
                unsafe_allow_html=True,
            )

        with right:
            st.markdown("#### Why this might fit")
            st.write(clean_value(opp.get("why_this_fits_short"), "No fit analysis available yet."))

            bullets = opp.get("three_bullets", [])
            if bullets:
                st.markdown("#### Key points")
                for bullet in bullets:
                    st.write("- " + str(bullet))

            st.markdown("#### Drafts")
            zh_tab, ja_tab, en_tab = st.tabs(["中文", "日本語", "English"])

            with zh_tab:
                st.text_area("Chinese draft", make_draft(opp, "zh"), height=190)
            with ja_tab:
                st.text_area("Japanese draft", make_draft(opp, "ja"), height=210)
            with en_tab:
                st.text_area("English draft", make_draft(opp, "en"), height=190)

    if st.button("Close"):
        st.session_state["selected_title"] = None
        st.session_state["selected_mode"] = "details"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_hero():
    hero_path = "static/assets/headers/mochi_hero.png"

    if os.path.exists(hero_path):
        with open(hero_path, "rb") as f:
            hero_b64 = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>
        .hero-box {{
            position: relative;
            height: 430px;
            margin-bottom: 24px;
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
            top: 130px;
            left: 58px;
            font-family: Georgia, "Times New Roman", serif;
            font-size: 3.2rem;
            color: #3f3027;
            line-height: 1;
        }}

        .hero-box .hero-subtitle {{
            position: absolute;
            top: 190px;
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


opps = load_json(
    "deploy_data/compact_opportunities.json",
    load_json("memory/compact_opportunities.json", []),
)

render_hero()

if not opps:
    st.error("No opportunity data found. Expected deploy_data/compact_opportunities.json.")
    st.stop()

tabs = st.tabs(["Mochi Atelier", "Mousehole", "Observatory", "Archive"])

with tabs[0]:
    st.subheader("Today's Suggestions")

    top = sorted(opps, key=lambda x: -score_num(x.get("overall_score")))[:6]
    cols = st.columns(3)
    for idx, opp in enumerate(top):
        with cols[idx % 3]:
            render_compact_card(opp, f"top_{idx}_{get_title(opp)}")

    selected_title = st.session_state.get("selected_title")
    if selected_title:
        selected = next((o for o in opps if get_title(o) == selected_title), None)
        if selected:
            render_detail(selected)

    st.markdown("---")
    st.subheader("Browse by Type")

    groups = defaultdict(list)
    for opp in opps:
        groups[category_label(opp.get("category"))].append(opp)

    for category in sorted(groups.keys()):
        with st.expander(f"{category} · {len(groups[category])}", expanded=True):
            sorted_items = sorted(groups[category], key=lambda x: -score_num(x.get("overall_score")))
            cols = st.columns(3)
            for idx, opp in enumerate(sorted_items[:9]):
                with cols[idx % 3]:
                    render_compact_card(opp, f"{category}_{idx}_{get_title(opp)}")

with tabs[1]:
    st.header("Mousehole")
    st.write("Career pathways and task progress will go here next.")

with tabs[2]:
    st.header("Observatory")
    st.write("Reports, market positioning, and long-form analysis will go here next.")

with tabs[3]:
    st.header("Archive")
    st.write(f"Loaded {len(opps)} opportunities.")
