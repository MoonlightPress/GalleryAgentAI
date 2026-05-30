from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

start = text.index("with tabs[2]:")
end = text.index("\nwith tabs[3]:")

new_block = '''with tabs[2]:
    st.markdown("## 🐾 Opportunities")
    st.caption("Start with low-friction options. Open one card, check the evidence, copy the draft, send.")

    opportunities = load_json("memory/compact_opportunities.json", [])

    if not opportunities:
        st.info("No compact opportunities generated yet. Run compact_view_agent.py first.")

    else:
        section_map = {
            "📚 Print / Zines / Bookstores": [
                "zine_print",
                "bookstore_gallery",
                "bookstore_event"
            ],
            "🍵 Cafe / Local Wall Spaces": [
                "cafe_gallery"
            ],
            "🎪 Markets / Popups / Booths": [
                "fair_popup",
                "market_event"
            ],
            "🏡 Artist Spaces / Community": [
                "artist_space",
                "event_space",
                "gallery_event"
            ],
            "🖼️ Galleries": [
                "gallery"
            ],
            "🏯 Residencies / Institutional": [
                "residency",
                "institutional"
            ]
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

        def render_card(opp, key, section_name):
            title = opp.get("title", "Unknown")
            score = opp.get("overall_score", 0)
            difficulty = str(opp.get("difficulty", "unknown"))
            city = opp.get("city", "")
            sentence = opp.get("one_sentence", "")

            with st.container(border=True):
                st.markdown(f"**{score_badge(score)} {title}**")
                st.caption(f"{score} · {difficulty} · {city}")
                st.write(sentence[:120] + ("..." if len(sentence) > 120 else ""))

                if st.button("More", key=key):
                    if (
                        st.session_state.get("selected_opportunity", {}).get("title")
                        == title
                    ):
                        st.session_state["selected_opportunity"] = None
                        st.session_state["selected_section"] = None
                    else:
                        st.session_state["selected_opportunity"] = opp
                        st.session_state["selected_section"] = section_name
                    st.rerun()

        def render_detail(selected):
            st.markdown("---")

            top_left, top_right = st.columns([1, 1.2])

            with top_left:
                st.markdown(f"### {selected.get('title', 'Unknown')}")
                st.caption(
                    f"{selected.get('overall_score', 0)} · "
                    f"{selected.get('difficulty', 'unknown')} · "
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

            with top_right:
                st.markdown("#### Why This Might Fit")
                st.write(selected.get("why_this_fits_short", ""))

                st.markdown("#### Key Points")
                for bullet in selected.get("three_bullets", []):
                    st.write(f"- {bullet}")

                with st.expander("Deeper reasoning"):
                    st.write("Later this should pull the full mentor/council notes from opportunities_master.json.")

            st.markdown("#### Submission Drafts")

            organization = selected.get("organization", selected.get("title", ""))

            email_en = f"""Hello,

I am writing to ask whether {organization} is currently accepting artist submissions, exhibition proposals, or artist book/zine proposals.

I am an artist working with atmospheric images of architecture, place, memory, and everyday spaces. I would be interested in learning whether my work might fit your programming.

Portfolio:
[portfolio link]

Thank you,
[artist name]"""

            email_ja = f"""こんにちは。

突然のご連絡失礼いたします。

現在、{organization}様でアーティストの応募、展示企画、またはアーティストブック・ZINEの提案を受け付けていらっしゃるかお伺いしたく、ご連絡いたしました。

私は建築、場所、記憶、日常の風景をテーマに、静かな雰囲気の作品を制作しているアーティストです。私の作品が貴施設の企画に合う可能性があるか、ご確認いただけましたら幸いです。

ポートフォリオ：
[portfolio link]

どうぞよろしくお願いいたします。

[artist name]"""

            email_zh = f"""您好，

我想询问一下，{organization} 目前是否接受艺术家投稿、展览提案，或艺术书 / ZINE 相关的作品提案。

我的创作主要关注建筑、场所、记忆，以及日常空间中的安静氛围。如果我的作品有可能适合贵方的项目或空间，我会很高兴进一步了解。

作品集：
[portfolio link]

谢谢。

[artist name]"""

            lang_tabs = st.tabs(["中文", "日本語", "English"])

            with lang_tabs[0]:
                st.text_area(
                    "Chinese draft",
                    value=email_zh,
                    height=210,
                    key=f"email_zh_{selected.get('title', 'unknown')}"
                )

            with lang_tabs[1]:
                st.text_area(
                    "Japanese draft",
                    value=email_ja,
                    height=230,
                    key=f"email_ja_{selected.get('title', 'unknown')}"
                )

            with lang_tabs[2]:
                st.text_area(
                    "English draft",
                    value=email_en,
                    height=210,
                    key=f"email_en_{selected.get('title', 'unknown')}"
                )

        for section_name, categories in section_map.items():

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

            st.markdown(f"### {section_name}")

            visible = section_opps[:4]

            cols = st.columns(4)

            for idx, opp in enumerate(visible):
                with cols[idx]:
                    render_card(
                        opp,
                        f"more_{section_name}_{idx}_{opp.get('title', 'unknown')}",
                        section_name
                    )

            if selected and selected_section == section_name:
                render_detail(selected)

            if len(section_opps) > 4:
                with st.expander(f"More {section_name}"):
                    more_cols = st.columns(4)
                    for idx, opp in enumerate(section_opps[4:8]):
                        with more_cols[idx]:
                            render_card(
                                opp,
                                f"more_extra_{section_name}_{idx}_{opp.get('title', 'unknown')}",
                                section_name
                            )

            st.markdown("---")
'''

text = text[:start] + new_block + text[end:]
path.write_text(text, encoding="utf-8")

print("Patched polished opportunity UI.")