from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

start = text.index("with tabs[2]:")
end = text.index("\nwith tabs[3]:")

new_block = '''with tabs[2]:
    st.markdown(
        """
        <style>
        .atelier-header {
            background: linear-gradient(135deg, #fff7ea 0%, #f7ead8 55%, #edf5e8 100%);
            border: 1px solid #ead8bd;
            border-radius: 22px;
            padding: 24px 28px;
            margin-bottom: 22px;
            box-shadow: 0 3px 12px rgba(120, 90, 55, 0.10);
        }

        .atelier-title {
            font-size: 2rem;
            font-weight: 650;
            margin-bottom: 4px;
        }

        .atelier-subtitle {
            color: #6d604f;
            font-size: 1rem;
        }

        .section-banner {
            background: linear-gradient(90deg, #fffaf0 0%, #f7efe2 65%, #eef6e9 100%);
            border: 1px solid #eadcc7;
            border-radius: 18px;
            padding: 14px 18px;
            margin-top: 24px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(120, 90, 55, 0.08);
        }

        .section-title {
            font-size: 1.25rem;
            font-weight: 650;
            margin-bottom: 2px;
        }

        .section-subtitle {
            color: #7a6b5a;
            font-size: 0.88rem;
        }

        .tiny-note {
            color: #776b5c;
            font-size: 0.84rem;
        }
        </style>

        <div class="atelier-header">
            <div class="atelier-title">🐾 Artist Opportunity Atelier</div>
            <div class="atelier-subtitle">
                Find gentle first steps, check the evidence, prepare the message, then send.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    opportunities = load_json("memory/compact_opportunities.json", [])

    if not opportunities:
        st.info("No compact opportunities generated yet. Run compact_view_agent.py first.")

    else:
        section_map = {
            "📚 Print / Zines / Bookstores": {
                "categories": ["zine_print", "bookstore_gallery", "bookstore_event"],
                "note": "Artist books, zines, print culture, quiet publishing paths."
            },
            "🍵 Cafe / Local Wall Spaces": {
                "categories": ["cafe_gallery"],
                "note": "Low-pressure local visibility and small walls."
            },
            "🎪 Markets / Popups / Booths": {
                "categories": ["fair_popup", "market_event"],
                "note": "Direct audience tests, sales experiments, booth energy."
            },
            "🏡 Artist Spaces / Community": {
                "categories": ["artist_space", "event_space", "gallery_event"],
                "note": "Local ecosystems, artist-run spaces, community contact."
            },
            "🖼️ Galleries": {
                "categories": ["gallery"],
                "note": "More formal exhibition contexts and gallery leads."
            },
            "🏯 Residencies / Institutional": {
                "categories": ["residency", "institutional"],
                "note": "Longer applications, stronger CV value, heavier preparation."
            }
        }

        selected = st.session_state.get("selected_opportunity")
        selected_section = st.session_state.get("selected_section")

        def score_badge(score):
            try:
                score = float(score)
            except Exception:
                return "○"

            if score >= 7:
                return "●"
            if score >= 5:
                return "◐"
            return "○"

        def short_effort_label(difficulty):
            d = str(difficulty).lower()

            if "low" in d or "easy" in d:
                return "Easy"
            if "medium" in d or "moderate" in d:
                return "Medium"
            if "high" in d or "demand" in d:
                return "Heavy"
            return "Check"

        def render_card(opp, key, section_name):
            title = opp.get("title", "Unknown")
            score = opp.get("overall_score", 0)
            difficulty = short_effort_label(opp.get("difficulty", "unknown"))
            city = opp.get("city", "")
            sentence = opp.get("one_sentence", "")

            current = st.session_state.get("selected_opportunity") or {}
            is_open = current.get("title") == title

            with st.container(border=True):
                st.markdown(f"**{score_badge(score)} {title}**")
                st.caption(f"{score} · {difficulty} · {city}")
                st.write(sentence[:150] + ("..." if len(sentence) > 150 else ""))

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
            st.markdown("---")

            left, right = st.columns([1, 1.25])

            with left:
                st.markdown(f"### {selected.get('title', 'Unknown')}")
                st.caption(
                    f"{selected.get('overall_score', 0)} · "
                    f"{short_effort_label(selected.get('difficulty', 'unknown'))} · "
                    f"{selected.get('city', '')}"
                )

                if st.button("Close Details"):
                    st.session_state["selected_opportunity"] = None
                    st.session_state["selected_section"] = None
                    st.rerun()

                st.write("**Organization:**", selected.get("organization", ""))

                source_link = (
                    selected.get("source_link")
                    or selected.get("source_url")
                    or selected.get("official_website")
                )

                if source_link:
                    st.markdown(f"[Open Source Link]({source_link})")

                st.markdown("#### Logistics / Evidence")
                st.write("**Deadline:**", selected.get("deadline", "Unknown"))
                st.write("**Fees:**", selected.get("fees", "Unknown"))
                st.write("**Official Website:**", selected.get("official_website", ""))
                st.write("**Submission Page:**", selected.get("submission_page", ""))

                st.markdown("#### Immediate Next Step")
                st.info(selected.get("quick_action", "No action available."))

            with right:
                st.markdown("#### Why This Might Fit")
                st.write(selected.get("why_this_fits_short", ""))

                st.markdown("#### Key Points")
                for bullet in selected.get("three_bullets", []):
                    st.write(f"- {bullet}")

                st.markdown("#### Submission Drafts")

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

                lang_tabs = st.tabs(["中文", "日本語", "English"])

                with lang_tabs[0]:
                    st.text_area(
                        "Chinese draft",
                        value=email_zh,
                        height=190,
                        key=f"email_zh_{selected.get('title', 'unknown')}"
                    )

                with lang_tabs[1]:
                    st.text_area(
                        "Japanese draft",
                        value=email_ja,
                        height=210,
                        key=f"email_ja_{selected.get('title', 'unknown')}"
                    )

                with lang_tabs[2]:
                    st.text_area(
                        "English draft",
                        value=email_en,
                        height=190,
                        key=f"email_en_{selected.get('title', 'unknown')}"
                    )

        for section_name, config in section_map.items():

            categories = config["categories"]

            section_opps = [
                opp for opp in opportunities
                if opp.get("category") in categories
            ]

            if not section_opps:
                continue

            section_opps = sorted(
                section_opps,
                key=lambda x: -float(x.get("overall_score", 0) or 0)
            )

            st.markdown(
                f"""
                <div class="section-banner">
                    <div class="section-title">{section_name}</div>
                    <div class="section-subtitle">{config["note"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            visible = section_opps[:4]
            extra = section_opps[4:8]

            cols = st.columns(4)

            for idx, opp in enumerate(visible):
                with cols[idx]:
                    render_card(
                        opp,
                        f"more_{section_name}_{idx}_{opp.get('title', 'unknown')}",
                        section_name
                    )

            if extra:
                with st.expander(f"More {section_name}"):
                    extra_cols = st.columns(4)

                    for idx, opp in enumerate(extra):
                        with extra_cols[idx]:
                            render_card(
                                opp,
                                f"more_extra_{section_name}_{idx}_{opp.get('title', 'unknown')}",
                                section_name
                            )

            if selected and selected_section == section_name:
                render_detail(selected)

            st.markdown("---")
'''

text = text[:start] + new_block + text[end:]
path.write_text(text, encoding="utf-8")

print("Patched atelier-style opportunities UI and fixed More button.")