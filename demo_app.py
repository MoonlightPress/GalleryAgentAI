import streamlit as st
import json
import os


st.set_page_config(
    page_title="Mochi's Atelier",
    layout="wide"
)


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_text(path, fallback=""):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


st.markdown("""
<style>
.stApp {
    background: #fbf4e8;
}
.block-container {
    max-width: 1300px;
    padding-top: 1.2rem;
}
.hero {
    background: linear-gradient(135deg, #fff8ea, #f2dfc2);
    border: 1px solid #d9bf96;
    border-radius: 28px;
    padding: 34px;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(80, 50, 25, .12);
}
.card {
    background: #fffdf8;
    border: 1px solid #d9bf96;
    border-radius: 20px;
    padding: 16px;
    min-height: 210px;
    box-shadow: 0 5px 16px rgba(80, 50, 25, .08);
}
.badge {
    display:inline-block;
    padding:3px 9px;
    border-radius:999px;
    background:#f0dfc4;
    margin-right:5px;
    font-size:.8rem;
}
</style>
""", unsafe_allow_html=True)


opps = load_json("memory/compact_opportunities.json", [])

st.markdown("""
<div class="hero">
<h1>Mochi's Atelier</h1>
<p>Gentle opportunities, source links, and ready-to-send drafts.</p>
</div>
""", unsafe_allow_html=True)

st.header("Today’s Suggestions")

top = sorted(
    opps,
    key=lambda x: -float(x.get("overall_score", 0) or 0)
)[:6]

cols = st.columns(3)

for i, opp in enumerate(top):
    with cols[i % 3]:
        with st.container(border=True):
            st.subheader(opp.get("title", "Unknown"))
            st.caption(
                f"{opp.get('overall_score', 0)} · "
                f"{opp.get('city', '')} · "
                f"{opp.get('category', '')}"
            )
            st.write(opp.get("one_sentence", ""))

            source = (
                opp.get("source_link")
                or opp.get("source_url")
                or opp.get("official_website")
            )

            if source:
                st.link_button("Open source", source)

            if st.button("Open details", key=f"open_{i}"):
                st.session_state["selected"] = opp


selected = st.session_state.get("selected")

if selected:
    st.markdown("---")
    left, right = st.columns([1, 1.2])

    with left:
        st.header(selected.get("title", "Unknown"))
        st.write("**Organization:**", selected.get("organization", ""))
        st.write("**Deadline:**", selected.get("deadline", "Check source"))
        st.write("**Fees:**", selected.get("fees", "Check source"))

        source = (
            selected.get("source_link")
            or selected.get("source_url")
            or selected.get("official_website")
        )

        if source:
            st.link_button("Open source", source)

        st.subheader("Next Step")
        st.info(selected.get("quick_action", "No action available."))

    with right:
        st.subheader("Why this might fit")
        st.write(selected.get("why_this_fits_short", ""))

        st.subheader("Key points")
        for bullet in selected.get("three_bullets", []):
            st.write("- " + str(bullet))

        org = selected.get("organization", selected.get("title", ""))

        zh = f"""您好，

我想询问一下，{org} 目前是否接受艺术家投稿、展览提案，或艺术书 / ZINE 相关的作品提案。

我的创作主要关注建筑、场所、记忆，以及日常空间中的安静氛围。如果我的作品有可能适合贵方的项目或空间，我会很高兴进一步了解。

作品集：
[portfolio link]

谢谢。

[artist name]"""

        en = f"""Hello,

I am writing to ask whether {org} is currently accepting artist submissions, exhibition proposals, or artist book/zine proposals.

I am an artist working with atmospheric images of architecture, place, memory, and everyday spaces. I would be interested in learning whether my work might fit your programming.

Portfolio:
[portfolio link]

Thank you,
[artist name]"""

        tabs = st.tabs(["中文", "English"])
        with tabs[0]:
            st.text_area("Chinese draft", zh, height=220)
        with tabs[1]:
            st.text_area("English draft", en, height=220)

    if st.button("Close"):
        st.session_state["selected"] = None
        st.rerun()