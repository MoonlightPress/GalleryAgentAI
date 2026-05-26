import json
import os
from collections import defaultdict

import streamlit as st

st.set_page_config(page_title="Mochi Atelier", layout="wide")


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return fallback


def load_text(path, fallback=""):
    if not os.path.exists(path):
        return fallback
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return fallback


def get_source(opp):
    return opp.get("source_link") or opp.get("source_url") or opp.get("official_website") or ""


def score_value(opp):
    try:
        return float(opp.get("overall_score", 0) or 0)
    except Exception:
        return 0.0


def effort_label(raw):
    d = str(raw or "").lower()
    if "low" in d or "easy" in d:
        return "Easy"
    if "medium" in d or "moderate" in d:
        return "Medium"
    if "high" in d or "demand" in d:
        return "Heavy"
    return "Check"


def card_meta(opp):
    score = opp.get("overall_score", 0)
    city = opp.get("city", "")
    category = str(opp.get("category", "")).replace("_", " ").title()
    effort = effort_label(opp.get("difficulty", ""))
    parts = [str(score), effort]
    if city:
        parts.append(city)
    if category:
        parts.append(category)
    return " · ".join(parts)


def select_opp(opp):
    st.session_state["selected_opp"] = opp


st.markdown(
    """
<style>
:root {
    --paper: #f7efe2;
    --card: #fffaf2;
    --ink: #3f3027;
    --muted: #7a6a58;
    --line: #e0c9a6;
    --soft: #f1dfc3;
    --accent: #b88768;
}

.stApp {
    background: var(--paper);
}

.block-container {
    max-width: 1320px;
    padding-top: 1.25rem;
    padding-bottom: 4rem;
}

h1, h2, h3, h4 {
    color: var(--ink);
    letter-spacing: -0.02em;
}

p, li {
    color: var(--ink);
}

[data-testid="stCaptionContainer"] p {
    color: var(--muted);
}

.hero-panel {
    border: 1px solid var(--line);
    border-radius: 28px;
    padding: 34px 42px;
    margin-bottom: 24px;
    background:
        radial-gradient(circle at 12% 30%, rgba(184,135,104,.18), transparent 22%),
        radial-gradient(circle at 88% 18%, rgba(143,167,125,.18), transparent 18%),
        linear-gradient(135deg, #fff9ed 0%, #f2dfc2 100%);
    box-shadow: 0 10px 30px rgba(70,45,20,.08);
}

.hero-title {
    font-family: Georgia, serif;
    font-size: 2.7rem;
    line-height: 1.05;
    color: var(--ink);
    margin: 0 0 8px 0;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: var(--muted);
    margin: 0;
}

.section-banner {
    margin-top: 34px;
    margin-bottom: 14px;
    padding: 18px 22px;
    border-radius: 22px;
    border: 1px solid var(--line);
    background: linear-gradient(135deg, #fffaf2 0%, #f1dfc3 100%);
    box-shadow: 0 6px 18px rgba(70,45,20,.06);
}

.section-title {
    font-family: Georgia, serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--ink);
}

.soft-note {
    background: #f4e7cf;
    border: 1px solid #dec5a0;
    border-radius: 14px;
    padding: 12px 14px;
    margin-top: 10px;
    color: #5a4737;
    font-size: .92rem;
    line-height: 1.5;
}

.metric-chip {
    display: inline-block;
    padding: 3px 9px;
    margin: 2px 4px 6px 0;
    border-radius: 999px;
    border: 1px solid #d7bea0;
    background: #f1e2ca;
    color: #594532;
    font-size: .78rem;
}

hr {
    border-color: #e6d6bf;
}
</style>
""",
    unsafe_allow_html=True,
)

opps = load_json("deploy_data/compact_opportunities.json", [])
# Optional local-only files. They may not exist on Streamlit Cloud yet.
daily = load_json("memory/daily_suggestions.json", {})
paths = load_json("memory/pathway_progress.json", {"pathways": []})
tasks = load_json("memory/mousehole_tasks.json", {"tasks": []})
artist_memory = load_json("memory/artist_memory.json", {})
artist_intel = load_json("memory/artist_intelligence.json", {})

st.markdown(
    """
<div class="hero-panel">
    <div class="hero-title">Mochi's Atelier</div>
    <p class="hero-subtitle">Gentle opportunities, source links, and ready-to-send drafts.</p>
</div>
""",
    unsafe_allow_html=True,
)

if not opps:
    st.error("No opportunity data found. Expected deploy_data/compact_opportunities.json.")


tabs = st.tabs(["Mochi Atelier", "Mousehole", "Observatory", "Archive"])

with tabs[0]:
    st.header("Mochi Atelier")
    st.caption("Browse today's openings. Pick something gentle. Copy the draft. Move forward.")

    featured = daily.get("featured_opportunities") or sorted(opps, key=score_value, reverse=True)[:5]

    st.subheader("Today’s Suggestions")
    cols = st.columns(3)

    for idx, opp in enumerate(featured[:3]):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {opp.get('title', 'Unknown')}")
                st.caption(card_meta(opp))
                st.write(str(opp.get("one_sentence", ""))[:240])

                source = get_source(opp)
                if source:
                    st.link_button("Open Source", source)

                if st.button("Open Details", key=f"featured_details_{idx}_{opp.get('title', 'unknown')}"):
                    select_opp(opp)
                    st.rerun()

                quick = opp.get("quick_action", "No action available.")
                st.markdown(f'<div class="soft-note">{quick}</div>', unsafe_allow_html=True)

    selected = st.session_state.get("selected_opp")
    if selected:
        st.divider()
        st.subheader(selected.get("title", "Unknown"))
        left, right = st.columns([1, 1.25])

        with left:
            st.caption(card_meta(selected))
            st.write("**Organization:**", selected.get("organization", ""))
            st.write("**Deadline:**", selected.get("deadline", "Check source"))
            st.write("**Fees:**", selected.get("fees", "Check source"))
            source = get_source(selected)
            if source:
                st.link_button("Open Source", source)
            st.markdown('<div class="soft-note">' + selected.get("quick_action", "No action available.") + '</div>', unsafe_allow_html=True)
            if st.button("Close Details"):
                st.session_state["selected_opp"] = None
                st.rerun()

        with right:
            st.markdown("#### Why this might fit")
            st.write(selected.get("why_this_fits_short", ""))
            bullets = selected.get("three_bullets", []) or []
            if bullets:
                st.markdown("#### Key points")
                for bullet in bullets:
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
            draft_tabs = st.tabs(["中文", "English"])
            with draft_tabs[0]:
                st.text_area("Chinese draft", zh, height=220)
            with draft_tabs[1]:
                st.text_area("English draft", en, height=220)

    st.markdown('<div class="section-banner"><div class="section-title">Fast Browse</div></div>', unsafe_allow_html=True)

    categories = defaultdict(list)
    for opp in opps:
        categories[opp.get("category", "unknown")].append(opp)

    for category, items in sorted(categories.items()):
        st.markdown(f"### {category.replace('_', ' ').title()} · {len(items)}")
        browse_cols = st.columns(4)
        for idx, opp in enumerate(sorted(items, key=score_value, reverse=True)[:8]):
            with browse_cols[idx % 4]:
                with st.container(border=True):
                    st.markdown(f"**{opp.get('title', 'Unknown')}**")
                    st.caption(card_meta(opp))
                    if st.button("Details", key=f"browse_details_{category}_{idx}_{opp.get('title', 'unknown')}"):
                        select_opp(opp)
                        st.rerun()

with tabs[1]:
    st.header("Mousehole")
    st.caption("Quest lines, readiness, materials, and career infrastructure.")

    if not paths.get("pathways"):
        st.info("No pathway data deployed yet. This tab is ready, but memory/pathway_progress.json is not online.")
    else:
        path_cols = st.columns(4)
        for idx, path in enumerate(paths.get("pathways", [])[:4]):
            with path_cols[idx % 4]:
                with st.container(border=True):
                    st.subheader(path.get("name", ""))
                    percent = path.get("percent_complete", 0)
                    st.progress(percent / 100)
                    st.write(f"{percent}% ready")
                    st.caption(path.get("description", ""))

    st.subheader("Best Tasks to Do Next")
    open_tasks = [t for t in tasks.get("tasks", []) if not t.get("complete")]
    if not open_tasks:
        st.write("No task data deployed yet.")
    else:
        task_cols = st.columns(3)
        for idx, task in enumerate(open_tasks[:6]):
            with task_cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"### {task.get('title')}")
                    st.write(task.get("description", ""))
                    st.caption("Difficulty: " + task.get("difficulty", ""))

with tabs[2]:
    st.header("Observatory")
    st.caption("Reports, positioning, intelligence, and deeper analysis.")
    if artist_intel:
        st.subheader("Artist Intelligence")
        st.json(artist_intel)
    else:
        st.info("No artist intelligence deployed yet.")

    report = load_text("final_gallery_report.md", "")
    if report:
        with st.expander("Market / Strategy Report"):
            st.markdown(report[:6000])

with tabs[3]:
    st.header("Archive")
    st.caption("Stored source data and raw records.")
    with st.expander("Compact opportunities"):
        st.json(opps[:10])
    with st.expander("Pathways"):
        st.json(paths)
    with st.expander("Tasks"):
        st.json(tasks)
