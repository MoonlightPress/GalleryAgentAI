import streamlit as st
import json
import os
import base64


st.set_page_config(
    page_title="Mochi Atelier",
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


def img_data(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:image/svg+xml;base64,{encoded}"


st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(180deg, #fbf3e8 0%, #f6ecdc 100%);
}

.block-container {
    padding-top: 1.2rem;
    max-width: 1450px;
}

.portal-hero {
    background: #fff8ed;
    border: 1px solid #dfc9aa;
    border-radius: 28px;
    padding: 18px;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(92, 65, 37, .12);
}

.mode-card {
    background: rgba(255, 253, 247, .96);
    border: 1px solid #e1ceb2;
    border-radius: 22px;
    padding: 18px;
    min-height: 230px;
    box-shadow: 0 4px 14px rgba(92, 65, 37, .08);
}

.mode-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #4b3a2d;
}

.mode-note {
    color: #756653;
    font-size: .94rem;
    margin-bottom: 12px;
}

.path-card {
    background: #fffaf2;
    border: 1px solid #e2ceb1;
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 10px;
}

.small-chip {
    display: inline-block;
    background: #efe1c8;
    border: 1px solid #d9c09e;
    border-radius: 999px;
    padding: 3px 9px;
    margin: 2px;
    font-size: .78rem;
    color: #5e4c3b;
}
</style>
""",
    unsafe_allow_html=True
)


hero = img_data("assets/mochi/hero_cat.svg")

st.markdown('<div class="portal-hero">', unsafe_allow_html=True)

if hero:
    st.image(hero, use_container_width=True)
else:
    st.title("Mochi Atelier")

st.markdown("</div>", unsafe_allow_html=True)


opps = load_json("memory/compact_opportunities.json", [])
daily = load_json("memory/daily_suggestions.json", {})
paths = load_json("memory/pathway_progress.json", {"pathways": []})
tasks = load_json("memory/mousehole_tasks.json", {"tasks": []})
artist_memory = load_json("memory/artist_memory.json", {})
artist_intel = load_json("memory/artist_intelligence.json", {})

tabs = st.tabs(
    [
        "Mochi Atelier",
        "Mousehole",
        "Observatory",
        "Archive"
    ]
)


with tabs[0]:
    st.header("Mochi Atelier")
    st.caption("Browse today's openings. Pick something gentle. Copy the draft. Move forward.")

    featured = daily.get("featured_opportunities") or sorted(
        opps,
        key=lambda x: -float(x.get("overall_score", 0) or 0)
    )[:5]

    st.subheader("Today’s Suggestions")

    cols = st.columns(3)

    for idx, opp in enumerate(featured[:3]):
        with cols[idx]:
            with st.container(border=True):
                st.markdown(f"### {opp.get('title', 'Unknown')}")
                st.caption(
                    f"{opp.get('overall_score', 0)} · "
                    f"{opp.get('city', '')} · "
                    f"{opp.get('category', '')}"
                )
                st.write(opp.get("one_sentence", "")[:220])

                source = (
                    opp.get("source_link")
                    or opp.get("source_url")
                    or opp.get("official_website")
                )

                if source:
                    st.link_button("Open Source", source)

                st.info(opp.get("quick_action", "No action available."))

    st.subheader("Fast Browse")

    categories = {}

    for opp in opps:
        categories.setdefault(
            opp.get("category", "unknown"),
            []
        ).append(opp)

    for category, items in categories.items():
        with st.expander(f"{category} · {len(items)}"):
            cols = st.columns(4)
            for idx, opp in enumerate(items[:8]):
                with cols[idx % 4]:
                    st.write(f"**{opp.get('title', 'Unknown')}**")
                    st.caption(
                        f"{opp.get('overall_score', 0)} · {opp.get('city', '')}"
                    )


with tabs[1]:
    st.header("Mousehole")
    st.caption("Quest lines, readiness, materials, and career infrastructure.")

    st.subheader("Pathways")

    path_cols = st.columns(4)

    for idx, path in enumerate(paths.get("pathways", [])[:4]):
        with path_cols[idx]:
            st.markdown('<div class="path-card">', unsafe_allow_html=True)
            st.markdown(f"### {path.get('name', '')}")
            percent = path.get("percent_complete", 0)
            st.progress(percent / 100)
            st.write(f"{percent}% ready")
            st.caption(path.get("description", ""))
            st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("Best Tasks to Do Next")

    open_tasks = [
        t for t in tasks.get("tasks", [])
        if not t.get("complete")
    ]

    task_cols = st.columns(3)

    for idx, task in enumerate(open_tasks[:6]):
        with task_cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {task.get('title')}")
                st.write(task.get("description", ""))
                st.caption("Difficulty: " + task.get("difficulty", ""))
                st.markdown("Contributes to:")
                for path in task.get("contributes_to", []):
                    st.markdown(
                        f"<span class='small-chip'>{path}</span>",
                        unsafe_allow_html=True
                    )

    st.subheader("Add New Artist Memory")

    memory_type = st.selectbox(
        "Type",
        [
            "favorite_artists",
            "desired_peers",
            "publication_history",
            "sales_history",
            "career_goals",
            "avoid_preferences",
            "notes"
        ]
    )

    memory_text = st.text_area(
        "Plain text note",
        height=120
    )

    if st.button("Save to Artist Memory"):
        if memory_type not in artist_memory:
            artist_memory[memory_type] = []

        if memory_text.strip():
            artist_memory[memory_type].append(memory_text.strip())

            os.makedirs("memory", exist_ok=True)

            with open(
                "memory/artist_memory.json",
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    artist_memory,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

            st.success("Saved.")
            st.rerun()


with tabs[2]:
    st.header("Observatory")
    st.caption("Reports, positioning, intelligence, and deeper analysis.")

    left, right = st.columns([1, 1])

    with left:
        st.subheader("Artist Intelligence")

        if artist_intel:
            st.json(artist_intel)
        else:
            st.info("No artist intelligence generated yet.")

    with right:
        st.subheader("Market / Strategy Report")
        report = load_text(
            "final_gallery_report.md",
            "No market report found."
        )
        st.markdown(report[:6000])

    st.subheader("Artist Dossier")
    dossier = load_text(
        "artist_dossier.md",
        "No artist dossier found."
    )

    with st.expander("Open full dossier"):
        st.markdown(dossier)


with tabs[3]:
    st.header("Archive")
    st.caption("Stored source data, accomplishments, memory, and system status.")

    archive_tabs = st.tabs(
        [
            "Accomplishments",
            "Artist Memory",
            "Opportunity Status",
            "Raw Files"
        ]
    )

    with archive_tabs[0]:
        st.subheader("Accomplishments / Garden Log")

        accomplishments = load_json(
            "memory/accomplishments_memory.json",
            {"items": []}
        )

        new_accomplishment = st.text_area(
            "Add accomplishment",
            placeholder="Example: I showed five works at a Koenji cafe for three weeks and sold two prints.",
            height=120
        )

        if st.button("Save Accomplishment"):
            if new_accomplishment.strip():
                accomplishments["items"].append(
                    {
                        "raw_text": new_accomplishment.strip()
                    }
                )

                os.makedirs("memory", exist_ok=True)

                with open(
                    "memory/accomplishments_memory.json",
                    "w",
                    encoding="utf-8"
                ) as f:
                    json.dump(
                        accomplishments,
                        f,
                        indent=2,
                        ensure_ascii=False
                    )

                st.success("Saved.")
                st.rerun()

        for item in accomplishments.get("items", []):
            st.write("•", item.get("raw_text", item))

    with archive_tabs[1]:
        st.json(artist_memory)

    with archive_tabs[2]:
        st.markdown(
            load_text(
                "opportunity_database_status.md",
                "No database status found."
            )
        )

    with archive_tabs[3]:
        with st.expander("Compact opportunities"):
            st.json(opps[:10])

        with st.expander("Pathways"):
            st.json(paths)

        with st.expander("Tasks"):
            st.json(tasks)