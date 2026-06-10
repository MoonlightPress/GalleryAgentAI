import streamlit as st
import json
import os
import base64


st.set_page_config(
    page_title="Mochi's Atelier",
    layout="wide"
)


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def img64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def asset(path):
    b64 = img64(path)
    if not b64:
        return ""
    return f"data:image/svg+xml;base64,{b64}"


opps = load_json("memory/compact_opportunities.json", [])
materials = load_json("memory/materials_memory.json", {})

st.markdown("""
<style>
:root {
    --paper: #fbf4e8;
    --ink: #49382c;
    --muted: #7c6a55;
    --gold: #c9a96b;
    --leaf: #8fa77d;
    --rose: #c98370;
}

.stApp {
    background: #fbf5ea;
}
.block-container {
    padding-top: 1.4rem;
    max-width: 1400px;
}
.mochi-card {
    background:
        linear-gradient(#fffdf8, #fff9ef),
        radial-gradient(circle at top left, rgba(190,130,98,.12), transparent 30%);
    border: 1px solid #d9c19a;
    border-radius: 22px;
    padding: 16px;
    min-height: 220px;
    box-shadow:
        0 8px 20px rgba(84, 57, 29, .10),
        inset 0 0 0 1px rgba(255,255,255,.65);
    position: relative;
}
.mochi-card-title {
    font-family: Georgia, serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #4a372b;
    line-height: 1.22;
}
.mochi-meta {
    color: #7d6d5d;
    font-size: .82rem;
}
.mochi-chip {
    display: inline-block;
    background: #efe2cb;
    border: 1px solid #dfc7a7;
    border-radius: 999px;
    padding: 2px 8px;
    margin-right: 5px;
    font-size: .78rem;
    color: #5f4e3f;
}
.section-img {
    width: 100%;
    border-radius: 20px;
    border: 1px solid #e2ceb0;
    margin: 20px 0 10px 0;
}
.detail-box {
    background:
        linear-gradient(180deg, #fffdf8 0%, #fff7ea 100%);
    border: 1px solid #d6bb91;
    border-radius: 28px;
    padding: 24px;
    margin-top: 18px;
    box-shadow: 0 12px 32px rgba(84, 57, 29, .13);
}
</style>
""", unsafe_allow_html=True)

hero = asset("assets/mochi/hero_cat.svg")
if hero:
    st.image(hero, use_container_width=True)

st.markdown("## Today's Suggestions")

top = sorted(
    opps,
    key=lambda x: -float(x.get("overall_score", 0) or 0)
)[:3]

top_cols = st.columns(3)
for col, opp in zip(top_cols, top):
    with col:
        with st.container(border=True):
            st.markdown(f"**{opp.get('title', 'Unknown')}**")
            st.caption(f"{opp.get('overall_score', 0)} · {opp.get('city', '')}")
            st.write(opp.get("one_sentence", "")[:160])
            if st.button("Open", key=f"today_{opp.get('title')}"):
                st.session_state["selected"] = opp

st.markdown("---")


SECTION_MAP = {
    "Print / Zines / Bookstores": {
        "categories": ["zine_print", "bookstore_gallery", "bookstore_event"],
        "image": "assets/mochi/zines.svg",
    },
    "Cafe / Local Wall Spaces": {
        "categories": ["cafe_gallery"],
        "image": "assets/mochi/cafe.svg",
    },
    "Markets / Popups / Booths": {
        "categories": ["fair_popup", "market_event"],
        "image": "assets/mochi/market.svg",
    },
    "Galleries": {
        "categories": ["gallery", "artist_space", "event_space", "gallery_event"],
        "image": "assets/mochi/gallery.svg",
    },
    "Residencies / Institutional": {
        "categories": ["residency", "institutional"],
        "image": "assets/mochi/residency.svg",
    },
}


def score_dot(score):
    try:
        score = float(score)
    except Exception:
        return "○"
    if score >= 7:
        return "●"
    if score >= 5:
        return "◐"
    return "○"


def effort_label(raw):
    d = str(raw).lower()
    if "low" in d or "easy" in d:
        return "Easy"
    if "medium" in d or "moderate" in d:
        return "Medium"
    if "high" in d or "demand" in d:
        return "Heavy"
    return "Check"


def readiness():
    rows = [
        ("Artist Statement", materials.get("artist_statements")),
        ("Short Bio", materials.get("artist_bios")),
        ("CV", materials.get("cv_versions")),
        ("Portfolio Set", materials.get("portfolio_sets")),
        ("Image Specs", materials.get("image_specs")),
        ("Translations", materials.get("translations")),
    ]
    ready = sum(1 for _, v in rows if v)
    return ready, len(rows), rows


def email_drafts(organization):
    zh = f"""您好，

我想询问一下，{organization} 目前是否接受艺术家投稿、展览提案，或艺术书 / ZINE 相关的作品提案。

我的创作主要关注建筑、场所、记忆，以及日常空间中的安静氛围。如果我的作品有可能适合贵方的项目或空间，我会很高兴进一步了解。

作品集：
[portfolio link]

谢谢。

[artist name]"""

    en = f"""Hello,

I am writing to ask whether {organization} is currently accepting artist submissions, exhibition proposals, or artist book/zine proposals.

I am an artist working with atmospheric images of architecture, place, memory, and everyday spaces. I would be interested in learning whether my work might fit your programming.

Portfolio:
[portfolio link]

Thank you,
[artist name]"""

    return zh, en


def render_detail(opp):
    st.markdown('<div class="detail-box">', unsafe_allow_html=True)

    left, right = st.columns([1, 1.25])

    with left:
        st.markdown(f"### {opp.get('title', 'Unknown')}")
        st.markdown(
            f"""
<span class="mochi-chip">Fit {opp.get('overall_score', 0)}</span>
<span class="mochi-chip">{effort_label(opp.get('difficulty', ''))}</span>
<span class="mochi-chip">{opp.get('city', '')}</span>
""",
            unsafe_allow_html=True
        )

        source = (
            opp.get("source_link")
            or opp.get("source_url")
            or opp.get("official_website")
        )

        if source:
            st.link_button("Open source", source)

        st.markdown("#### Evidence")
        st.write("**Deadline:**", opp.get("deadline", "Check source"))
        st.write("**Fees:**", opp.get("fees", "Check source"))
        st.write("**Organization:**", opp.get("organization", ""))

        ready, total, rows = readiness()
        st.markdown(f"#### Submission Readiness: {ready}/{total}")
        for label, value in rows:
            mark = "✅" if value else "⬜"
            st.write(f"{mark} {label}")

        st.markdown("#### Immediate Next Step")
        st.info(opp.get("quick_action", "No action available."))

    with right:
        st.markdown("#### Why this might fit")
        st.write(opp.get("why_this_fits_short", ""))

        st.markdown("#### Key points")
        for bullet in opp.get("three_bullets", []):
            st.write(f"- {bullet}")

        st.markdown("#### Drafts")
        organization = opp.get("organization", opp.get("title", ""))
        zh, en = email_drafts(organization)

        tabs = st.tabs(["中文", "English", "Deep report"])
        with tabs[0]:
            st.text_area("Chinese draft", zh, height=210, key=f"zh_{opp.get('title')}")
        with tabs[1]:
            st.text_area("English draft", en, height=210, key=f"en_{opp.get('title')}")
        with tabs[2]:
            st.write("Deep report should load full council notes from opportunities_master.json in the next pass.")
            st.json(opp)

    if st.button("Close detail"):
        st.session_state["selected"] = None
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


for section, config in SECTION_MAP.items():
    st.markdown(
        f"""
        <div style="
            margin-top: 28px;
            margin-bottom: 14px;
            padding: 18px 22px;
            border-radius: 24px;
            border: 1px solid #d9bf96;
            background:
                radial-gradient(circle at 8% 18%, rgba(190,130,98,.20), transparent 18%),
                radial-gradient(circle at 92% 24%, rgba(130,160,115,.20), transparent 16%),
                linear-gradient(135deg, #fffaf0 0%, #f3e4ce 100%);
            box-shadow: 0 8px 24px rgba(78, 55, 30, .10);
            position: relative;
        ">
            <div style="
                font-family: Georgia, serif;
                font-size: 1.45rem;
                font-weight: 700;
                color: #4f3c2f;
                letter-spacing: .01em;
            ">{section}</div>
            <div style="
                margin-top: 4px;
                color: #7b6a55;
                font-size: .94rem;
            ">Curated opportunities, source links, and ready-to-send drafts.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    section_opps = [
        o for o in opps
        if o.get("category") in config["categories"]
    ]

    section_opps = sorted(
        section_opps,
        key=lambda x: -float(x.get("overall_score", 0) or 0)
    )

    if not section_opps:
        continue

    cols = st.columns(4)

    for idx, opp in enumerate(section_opps[:4]):
        with cols[idx]:
            st.markdown('<div class="mochi-card">', unsafe_allow_html=True)
            st.markdown(
                f"<div class='mochi-card-title'>{score_dot(opp.get('overall_score'))} {opp.get('title', 'Unknown')}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div class='mochi-meta'>{opp.get('overall_score', 0)} · {effort_label(opp.get('difficulty'))} · {opp.get('city', '')}</div>",
                unsafe_allow_html=True
            )
            st.write(opp.get("one_sentence", "")[:150])
            if st.button("More", key=f"more_{section}_{idx}_{opp.get('title')}"):
                st.session_state["selected"] = opp
                st.session_state["selected_section"] = section
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("selected") and st.session_state.get("selected_section") == section:
        render_detail(st.session_state["selected"])

    with st.expander(f"More {section}"):
        extra_cols = st.columns(4)
        for idx, opp in enumerate(section_opps[4:8]):
            with extra_cols[idx]:
                st.write(f"**{opp.get('title')}**")
                st.caption(f"{opp.get('overall_score')} · {effort_label(opp.get('difficulty'))}")
                if st.button("Open", key=f"extra_{section}_{idx}_{opp.get('title')}"):
                    st.session_state["selected"] = opp
                    st.session_state["selected_section"] = section
                    st.rerun()