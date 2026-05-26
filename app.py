import streamlit as st
import json
import os


st.set_page_config(
    page_title="Artist Career Dashboard",
    layout="wide"
)


def load_text(path, fallback=""):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


st.title("Artist Career Dashboard")

tabs = st.tabs([
    "Artist Dossier",
    "Market Report",
    "Opportunities",
    "Add Opportunity",
    "CRM",
    "Add Contact",
    "Email Drafts",
    "Quests",
    "Chinese Summary",
    "Japanese Outreach",
    "Pipeline Status",
    "Materials",

])


with tabs[0]:
    st.header("Artist Dossier")
    st.markdown(load_text("artist_dossier.md", "No artist dossier found."))


with tabs[1]:
    st.header("Market / Strategy Report")
    st.markdown(load_text("final_gallery_report.md", "No market report found."))

with tabs[2]:
    st.markdown(
        """
        <style>
        .stApp {
            background: #fbf4e8;
        }

        div[data-testid="stTabs"] button {
            font-size: 0.88rem;
        }

        .mochi-hero {
            border-radius: 28px;
            overflow: hidden;
            border: 1px solid #e4d2b8;
            margin-bottom: 18px;
            box-shadow: 0 6px 20px rgba(112, 82, 48, 0.14);
            background: #fff7ea;
        }

        .section-shell {
            background: rgba(255, 250, 241, 0.78);
            border: 1px solid #e5d5bf;
            border-radius: 24px;
            padding: 16px 18px 18px 18px;
            margin: 22px 0;
            box-shadow: 0 4px 16px rgba(112, 82, 48, 0.08);
        }

        .section-head {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 12px;
        }

        .section-art {
            width: 120px;
            height: 56px;
            object-fit: cover;
            border-radius: 16px;
            border: 1px solid #e0cfb7;
            background: #fff;
        }

        .section-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #4d3c2f;
            margin-bottom: 2px;
        }

        .section-note {
            color: #7a6b5a;
            font-size: 0.9rem;
        }

        .dense-card {
            background: #fffdf7;
            border: 1px solid #e2d4bf;
            border-radius: 18px;
            padding: 12px 13px 11px 13px;
            min-height: 205px;
            box-shadow: 0 2px 8px rgba(112, 82, 48, 0.08);
        }

        .dense-card-title {
            color: #4b3b2d;
            font-weight: 700;
            font-size: 0.98rem;
            line-height: 1.18;
            margin-bottom: 6px;
        }

        .badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-bottom: 8px;
        }

        .badge {
            display: inline-block;
            padding: 2px 7px;
            border-radius: 999px;
            font-size: 0.72rem;
            border: 1px solid #decbb1;
            background: #f8eddd;
            color: #5e4b3a;
        }

        .badge-good {
            background: #edf6df;
            border-color: #c9dcb3;
        }

        .badge-source {
            background: #e8f2f4;
            border-color: #bdd6dc;
        }

        .card-summary {
            font-size: 0.84rem;
            color: #594a3c;
            line-height: 1.35;
        }

        .detail-shell {
            background: #fffdf8;
            border: 1px solid #dfceb5;
            border-radius: 24px;
            padding: 18px;
            margin-top: 16px;
            box-shadow: 0 8px 22px rgba(112, 82, 48, 0.12);
        }

        .info-box {
            background: #fbf4e8;
            border: 1px solid #e4d1b8;
            border-radius: 16px;
            padding: 11px 13px;
            margin-bottom: 10px;
        }

        .tiny-label {
            color: #7d6d5c;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: .04em;
            margin-bottom: 2px;
        }

        .readiness-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 7px 0;
            border-bottom: 1px dashed #e4d4be;
            font-size: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="mochi-hero">', unsafe_allow_html=True)
    st.image("assets/cat_scene.svg", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    opportunities = load_json("memory/compact_opportunities.json", [])
    materials = load_json(
        "memory/materials_memory.json",
        {
            "artist_bios": [],
            "artist_statements": [],
            "cv_versions": [],
            "portfolio_sets": [],
            "image_specs": [],
            "translations": []
        }
    )

    if not opportunities:
        st.info("No compact opportunities generated yet. Run compact_view_agent.py first.")

    else:
        section_map = {
            "Print / Zines / Bookstores": {
                "categories": ["zine_print", "bookstore_gallery", "bookstore_event"],
                "note": "Artist books, zines, small press, quiet publishing paths.",
                "image": "assets/books.svg"
            },
            "Cafe / Local Wall Spaces": {
                "categories": ["cafe_gallery"],
                "note": "Low-pressure local visibility and small approachable walls.",
                "image": "assets/matcha.svg"
            },
            "Markets / Popups / Booths": {
                "categories": ["fair_popup", "market_event"],
                "note": "Direct audience tests, booth experiments, product feedback.",
                "image": "assets/booth.svg"
            },
            "Artist Spaces / Community": {
                "categories": ["artist_space", "event_space", "gallery_event"],
                "note": "Artist-run spaces, local ecosystems, peer discovery.",
                "image": "assets/gallery.svg"
            },
            "Galleries": {
                "categories": ["gallery"],
                "note": "More formal exhibition contexts and gallery leads.",
                "image": "assets/gallery.svg"
            },
            "Residencies / Institutional": {
                "categories": ["residency", "institutional"],
                "note": "Longer applications, stronger CV value, heavier prep.",
                "image": "assets/residency.svg"
            }
        }

        selected = st.session_state.get("selected_opportunity")
        selected_section = st.session_state.get("selected_section")

        def effort_label(difficulty):
            d = str(difficulty).lower()
            if "low" in d or "easy" in d:
                return "Easy"
            if "medium" in d or "moderate" in d:
                return "Medium"
            if "high" in d or "demand" in d or "very" in d:
                return "Heavy"
            return "Check"

        def fit_label(score):
            try:
                score = float(score)
            except Exception:
                return "Check"
            if score >= 7.5:
                return "Strong"
            if score >= 5.5:
                return "Promising"
            if score >= 4:
                return "Maybe"
            return "Low"

        def status_check(items):
            return bool(items and len(items) > 0)

        def render_readiness():
            checks = [
                ("Artist bio", status_check(materials.get("artist_bios", []))),
                ("Artist statement", status_check(materials.get("artist_statements", []))),
                ("CV / resume", status_check(materials.get("cv_versions", []))),
                ("Portfolio set", status_check(materials.get("portfolio_sets", []))),
                ("Image specs", status_check(materials.get("image_specs", []))),
                ("Translations", status_check(materials.get("translations", []))),
            ]

            ready = sum(1 for _, ok in checks if ok)

            st.markdown(f"#### Submission Readiness · {ready}/{len(checks)}")

            for label, ok in checks:
                icon = "✓" if ok else "＋"
                action = "ready" if ok else "add"
                st.markdown(
                    f"""
                    <div class="readiness-row">
                        <span>{icon} {label}</span>
                        <span style="color:#7d6d5c;">{action}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        def render_card(opp, key, section_name):
            title = opp.get("title", "Unknown")
            score = opp.get("overall_score", 0)
            effort = effort_label(opp.get("difficulty", "unknown"))
            city = opp.get("city", "")
            source = (
                opp.get("source_link")
                or opp.get("source_url")
                or opp.get("official_website")
            )
            sentence = opp.get("one_sentence", "")

            current = st.session_state.get("selected_opportunity") or {}
            is_open = current.get("title") == title

            st.markdown(
                f"""
                <div class="dense-card">
                    <div class="dense-card-title">{title}</div>
                    <div class="badge-row">
                        <span class="badge badge-good">{fit_label(score)}</span>
                        <span class="badge">{score}/10</span>
                        <span class="badge">{effort}</span>
                        <span class="badge">{city}</span>
                        <span class="badge badge-source">Source {'✓' if source else '?'}</span>
                    </div>
                    <div class="card-summary">{sentence[:175]}{"..." if len(sentence) > 175 else ""}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            label = "Close" if is_open else "More"
            if st.button(label, key=key):
                if is_open:
                    st.session_state["selected_opportunity"] = None
                    st.session_state["selected_section"] = None
                else:
                    st.session_state["selected_opportunity"] = opp
                    st.session_state["selected_section"] = section_name
                st.rerun()

        def render_detail(selected):
            st.markdown('<div class="detail-shell">', unsafe_allow_html=True)

            left, right = st.columns([1, 1.25])

            with left:
                st.markdown(f"### {selected.get('title', 'Unknown')}")
                st.caption(
                    f"{fit_label(selected.get('overall_score', 0))} · "
                    f"{selected.get('overall_score', 0)}/10 · "
                    f"{effort_label(selected.get('difficulty', 'unknown'))} · "
                    f"{selected.get('city', '')}"
                )

                if st.button("Close Details"):
                    st.session_state["selected_opportunity"] = None
                    st.session_state["selected_section"] = None
                    st.rerun()

                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown('<div class="tiny-label">Evidence</div>', unsafe_allow_html=True)
                st.write("**Organization:**", selected.get("organization", ""))

                source_link = (
                    selected.get("source_link")
                    or selected.get("source_url")
                    or selected.get("official_website")
                )
                if source_link:
                    st.markdown(f"[Open Source Link]({source_link})")

                st.write("**Deadline:**", selected.get("deadline", "Unknown"))
                st.write("**Fees:**", selected.get("fees", "Unknown"))
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown('<div class="tiny-label">Next Step</div>', unsafe_allow_html=True)
                st.write(selected.get("quick_action", "No action available."))
                st.markdown('</div>', unsafe_allow_html=True)

                render_readiness()

            with right:
                st.markdown("#### Why This Might Fit")
                st.write(selected.get("why_this_fits_short", ""))

                st.markdown("#### Key Points")
                for bullet in selected.get("three_bullets", []):
                    st.write(f"- {bullet}")

                organization = selected.get("organization", selected.get("title", ""))

                email_zh = f"""您好，

我想询问一下，{organization} 目前是否接受艺术家投稿、展览提案，或艺术书 / ZINE 相关的作品提案。

我的创作主要关注建筑、场所、记忆，以及日常空间中的安静氛围。如果我的作品有可能适合贵方的项目或空间，我会很高兴进一步了解。

作品集：
[portfolio link]

谢谢。

[artist name]"""

                email_ja = f"""こんにちは。

突然のご連絡失礼いたします。

現在、{organization}様でアーティストの応募、展示企画、またはアーティストブック・ZINEの提案を受け付けていらっしゃるかお伺いしたく、ご連絡いたしました。

私は建築、場所、記憶、日常の風景をテーマに、静かな雰囲気の作品を制作しているアーティストです。私の作品が貴施設の企画に合う可能性があるか、ご確認いただけましたら幸いです。

ポートフォリオ：
[portfolio link]

どうぞよろしくお願いいたします。

[artist name]"""

                email_en = f"""Hello,

I am writing to ask whether {organization} is currently accepting artist submissions, exhibition proposals, or artist book/zine proposals.

I am an artist working with atmospheric images of architecture, place, memory, and everyday spaces. I would be interested in learning whether my work might fit your programming.

Portfolio:
[portfolio link]

Thank you,
[artist name]"""

                st.markdown("#### Submission Drafts")
                lang_tabs = st.tabs(["中文", "日本語", "English"])

                with lang_tabs[0]:
                    st.text_area(
                        "Chinese draft",
                        value=email_zh,
                        height=180,
                        key=f"email_zh_{selected.get('title', 'unknown')}"
                    )

                with lang_tabs[1]:
                    st.text_area(
                        "Japanese draft",
                        value=email_ja,
                        height=205,
                        key=f"email_ja_{selected.get('title', 'unknown')}"
                    )

                with lang_tabs[2]:
                    st.text_area(
                        "English draft",
                        value=email_en,
                        height=180,
                        key=f"email_en_{selected.get('title', 'unknown')}"
                    )

                with st.expander("Full Report / Deeper Reasoning"):
                    st.write(
                        "This should pull the long council report from opportunities_master.json next. "
                        "For now this panel reserves the drill-down layer."
                    )

            st.markdown('</div>', unsafe_allow_html=True)

        for section_name, config in section_map.items():

            section_opps = [
                opp for opp in opportunities
                if opp.get("category") in config["categories"]
            ]

            if not section_opps:
                continue

            section_opps = sorted(
                section_opps,
                key=lambda x: -float(x.get("overall_score", 0) or 0)
            )

            st.markdown('<div class="section-shell">', unsafe_allow_html=True)

            head_left, head_right = st.columns([0.16, 0.84])

            with head_left:
                st.image(config["image"], use_container_width=True)

            with head_right:
                st.markdown(
                    f"""
                    <div class="section-title">{section_name}</div>
                    <div class="section-note">{config["note"]}</div>
                    """,
                    unsafe_allow_html=True
                )

            cols = st.columns(4)
            for idx, opp in enumerate(section_opps[:4]):
                with cols[idx]:
                    render_card(
                        opp,
                        f"more_{section_name}_{idx}_{opp.get('title', 'unknown')}",
                        section_name
                    )

            if len(section_opps) > 4:
                with st.expander(f"More {section_name}"):
                    extra_cols = st.columns(4)
                    for idx, opp in enumerate(section_opps[4:8]):
                        with extra_cols[idx]:
                            render_card(
                                opp,
                                f"more_extra_{section_name}_{idx}_{opp.get('title', 'unknown')}",
                                section_name
                            )

            if selected and selected_section == section_name:
                render_detail(selected)

            st.markdown('</div>', unsafe_allow_html=True)

with tabs[3]:

    st.header("Add Opportunity")

    new_name = st.text_input("Name")
    new_type = st.text_input("Type")
    new_city = st.text_input("City")
    new_country = st.text_input("Country")
    new_website = st.text_input(
    "Official Website",
    key="opportunity_official_website"
)
    new_contact = st.text_input(
    "Contact Email",
    key="opportunity_contact_email"
)
  

    new_fit = st.text_area(
        "Why This Fits",
        height=120
    )

    new_action = st.text_area(
        "Next Action",
        height=120
    )

    new_risks = st.text_area(
        "Risk Notes",
        height=120
    )

    fit_score = st.slider(
        "Fit Score",
        1,
        10,
        5
    )

    urgency_score = st.slider(
        "Urgency Score",
        1,
        10,
        5
    )

    effort_score = st.slider(
        "Effort Required",
        1,
        10,
        5
    )

    strategic_score = st.slider(
        "Strategic Value",
        1,
        10,
        5
    )

    emotional_resistance = st.slider(
        "Emotional Resistance",
        1,
        10,
        5
    )
    

    if st.button("Save Opportunity"):

        opportunities = load_json(
            "memory/compact_opportunities.json",
            []
        )
        weighted_score = (
            fit_score * 2
            + urgency_score
            + strategic_score * 2
            - effort_score
            - emotional_resistance
        )

        if weighted_score >= 25:
            calculated_priority = "A"
        elif weighted_score >= 15:
            calculated_priority = "B"
        else:
            calculated_priority = "C"
        new_opportunity = {
            "fit_score": fit_score,
            "urgency_score": urgency_score,
            "effort_score": effort_score,
            "strategic_score": strategic_score,
            "emotional_resistance": emotional_resistance,
     
            "name": new_name,
            "type": new_type,
            "city": new_city,
            "country": new_country,
            "official_website": new_website,
            "contact_email": new_contact,
            "status": "research_needed",
            "priority": calculated_priority,
            "why_fit": new_fit,
            "next_action": new_action,
            "risk_notes": new_risks
        }

        opportunities.append(new_opportunity)

        with open(
            "memory/opportunities.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                opportunities,
                f,
                indent=2,
                ensure_ascii=False
            )

        st.success("Opportunity saved.")

with tabs[4]:
    st.header("CRM / Contacts")
    contacts = load_json("memory/contact_memory.json", {"contacts": []}).get("contacts", [])

    if not contacts:
        st.info("No contacts yet.")
    else:
        for contact in contacts:
            analysis = contact.get("crm_analysis", {})
            with st.expander(contact.get("name", "Unnamed contact")):
                st.write("**Type:**", contact.get("type", ""))
                st.write("**City:**", contact.get("city", ""))
                st.write("**Country:**", contact.get("country", ""))
                st.write("**Status:**", contact.get("status", ""))
                st.write("**Priority:**", analysis.get("priority", ""))
                st.write("**Next action:**", analysis.get("next_action", ""))
                st.write("**Follow-up timing:**", analysis.get("follow_up_timing", ""))
                st.write("**Risk notes:**", analysis.get("risk_notes", ""))
                web = contact.get("web_verification", {})
                st.write("**Official website:**", contact.get("official_website", ""))
                st.write("**Contact page:**", contact.get("contact_page", ""))
                st.write("**Submission page:**", contact.get("submission_page", ""))
                st.write("**Contact email:**", contact.get("contact_email", ""))
                st.write("**Instagram:**", web.get("instagram", ""))
                st.write("**Verification status:**", web.get("verification_status", ""))
                st.write("**Last verified:**", web.get("last_verified", ""))

with tabs[5]:

    st.header("Add Contact")

    contact_name = st.text_input("Contact Name")
    contact_type = st.text_input("Contact Type")
    contact_city = st.text_input("Contact City")
    contact_country = st.text_input("Contact Country")
    contact_email = st.text_input(
    "Contact Email",
    key="contact_contact_email"
)
    contact_website = st.text_input(
    "Official Website",
    key="contact_official_website"
)
    contact_page = st.text_input("Contact Page")

    contact_notes = st.text_area(
        "Contact Notes",
        height=120
    )

    if st.button("Save Contact"):

        contact_memory = load_json(
            "memory/contact_memory.json",
            {"contacts": []}
        )

        new_contact = {
            "name": contact_name,
            "type": contact_type,
            "city": contact_city,
            "country": contact_country,
            "contact_email": contact_email,
            "official_website": contact_website,
            "contact_page": contact_page,
            "status": "not_contacted",
            "response_received": False,
            "notes": contact_notes
        }

        contact_memory["contacts"].append(new_contact)

        with open(
            "memory/contact_memory.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                contact_memory,
                f,
                indent=2,
                ensure_ascii=False
            )

        st.success("Contact saved.")

with tabs[6]:
    st.header("Email Drafts")
    st.markdown(load_text("email_drafts.md", "No email drafts found."))


with tabs[7]:
    st.header("Quest Report")
    st.markdown(load_text("quest_report.md", "No quest report found."))


with tabs[8]:
    st.header("Chinese Summary")
    st.info("Placeholder: Chinese artist-facing summary will go here.")


with tabs[9]:
    st.header("Japanese Outreach")
    st.info("Placeholder: Japanese gallery outreach support will go here.")

with tabs[10]:
    st.header("Pipeline Status")
    st.markdown(load_text("pipeline_status.md", "No pipeline status generated yet."))
    

    with tabs[11]:
        st.header("Reusable Materials")

        materials = load_json(
            "memory/materials_memory.json",
            {
                "artist_bios": [],
                "artist_statements": [],
                "cv_versions": [],
                "portfolio_sets": [],
                "image_specs": [],
                "translations": [],
                "last_updated": ""
            }
        )

        st.write("**Last updated:**", materials.get("last_updated", ""))

    st.subheader("Artist Bios")

    for idx, item in enumerate(
        materials.get("artist_bios", [])
    ):

        col1, col2 = st.columns([10, 1])

        col1.write(item)

        if col2.button(
            "X",
            key=f"delete_bio_{idx}"
        ):

            materials["artist_bios"].pop(idx)

            save_json(
                "memory/materials_memory.json",
                materials
            )

            st.rerun()

        st.subheader("Artist Statements")
        for item in materials.get("artist_statements", []):
            st.write("- " + str(item))

        st.subheader("CV Versions")
        for item in materials.get("cv_versions", []):
            st.write("- " + str(item))

        st.subheader("Portfolio Sets")
        for item in materials.get("portfolio_sets", []):
            st.write("- " + str(item))

        st.subheader("Image Specs")
        for item in materials.get("image_specs", []):
            st.write("- " + str(item))

        st.subheader("Translations")
        for item in materials.get("translations", []):
            st.write("- " + str(item))
               
    st.markdown("---")
    st.subheader("Add Reusable Material")

    material_type = st.selectbox(
        "Material Type",
        [
            "artist_bios",
            "artist_statements",
            "cv_versions",
            "portfolio_sets",
            "image_specs",
            "translations"
        ]
    )

    material_text = st.text_area(
        "Material Content",
        height=150
    )

    if st.button("Save Material"):

        if material_text.strip():

            materials[material_type].append(
                material_text.strip()
            )

            save_json(
                "memory/materials_memory.json",
                materials
            )

            st.success("Material saved.")
            st.rerun()