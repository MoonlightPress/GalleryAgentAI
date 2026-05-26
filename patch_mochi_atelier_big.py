from pathlib import Path

APP = Path("app.py")
ASSETS = Path("assets")
ASSETS.mkdir(exist_ok=True)

# ------------------------------------------------------------
# Create simple watercolor-style SVG assets
# ------------------------------------------------------------

svg_assets = {
    "cat_scene.svg": """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 260">
<rect width="1200" height="260" rx="34" fill="#fff6e8"/>
<circle cx="1030" cy="58" r="95" fill="#f8dfb4" opacity=".55"/>
<path d="M0 214 C190 170 310 245 480 200 S850 185 1200 220 V260 H0Z" fill="#e9f1df"/>
<path d="M60 205 C120 130 180 155 220 205" fill="none" stroke="#b8a27d" stroke-width="5" opacity=".45"/>
<rect x="170" y="92" width="170" height="95" rx="16" fill="#f2dcc1"/>
<rect x="190" y="112" width="35" height="60" rx="4" fill="#c98f78"/>
<rect x="235" y="105" width="28" height="67" rx="4" fill="#88a982"/>
<rect x="272" y="118" width="42" height="54" rx="4" fill="#d6b56d"/>
<path d="M830 160 q50 -80 100 0 v35 h-100z" fill="#3b342d"/>
<circle cx="875" cy="116" r="42" fill="#3b342d"/>
<path d="M846 84 l14 -28 l17 31" fill="#3b342d"/>
<path d="M896 84 l20 -27 l9 34" fill="#3b342d"/>
<circle cx="861" cy="112" r="4" fill="#fff7d5"/>
<circle cx="889" cy="112" r="4" fill="#fff7d5"/>
<path d="M870 132 q8 8 18 0" stroke="#fff7d5" stroke-width="3" fill="none"/>
<path d="M660 185 h260 q20 0 20 20 v15 h-300 v-15 q0-20 20-20z" fill="#b88f62" opacity=".65"/>
<path d="M430 82 C495 34 560 55 595 104 C550 95 505 112 460 128 C445 115 432 102 430 82Z" fill="#d9e7c7"/>
<circle cx="510" cy="94" r="18" fill="#c5dca9"/>
<text x="70" y="72" font-family="Georgia" font-size="38" fill="#5a4636">Mochi's Atelier</text>
<text x="72" y="112" font-family="Georgia" font-size="19" fill="#7b6a59">gentle opportunities, prepared messages, clear next steps</text>
</svg>
""",
    "books.svg": """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 120">
<rect width="260" height="120" rx="22" fill="#fff7ea"/>
<rect x="45" y="65" width="150" height="18" rx="4" fill="#c98f78"/>
<rect x="60" y="45" width="150" height="18" rx="4" fill="#88a982"/>
<rect x="75" y="25" width="145" height="18" rx="4" fill="#d6b56d"/>
<circle cx="40" cy="34" r="12" fill="#e6b7a0" opacity=".7"/>
<path d="M205 80 q28 -35 42 0" stroke="#b8a27d" stroke-width="4" fill="none"/>
</svg>
""",
    "matcha.svg": """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 120">
<rect width="260" height="120" rx="22" fill="#f7f3e8"/>
<ellipse cx="130" cy="68" rx="68" ry="28" fill="#d9c3a4"/>
<ellipse cx="130" cy="60" rx="55" ry="20" fill="#9ab586"/>
<path d="M183 63 q38 -2 32 25 q-7 28 -48 14" fill="none" stroke="#c29f7a" stroke-width="8"/>
<path d="M82 38 q-20 -18 0 -35" stroke="#c9b89a" stroke-width="4" fill="none" opacity=".55"/>
<path d="M132 36 q-20 -18 0 -35" stroke="#c9b89a" stroke-width="4" fill="none" opacity=".55"/>
</svg>
""",
    "booth.svg": """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 120">
<rect width="260" height="120" rx="22" fill="#fff5ea"/>
<path d="M45 38 h170 l-18 30 h-134z" fill="#c98f78"/>
<path d="M60 68 h140 v35 h-140z" fill="#ead8bd"/>
<path d="M73 75 h38 v28 h-38z" fill="#88a982" opacity=".75"/>
<path d="M145 77 h38 v26 h-38z" fill="#d6b56d" opacity=".85"/>
<path d="M50 38 q35 -30 70 0 q35 -30 70 0" fill="none" stroke="#b98268" stroke-width="5"/>
</svg>
""",
    "gallery.svg": """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 120">
<rect width="260" height="120" rx="22" fill="#f7f1e7"/>
<rect x="52" y="25" width="62" height="60" rx="4" fill="#fffdf7" stroke="#b8a27d" stroke-width="5"/>
<rect x="148" y="30" width="58" height="50" rx="4" fill="#fffdf7" stroke="#b8a27d" stroke-width="5"/>
<circle cx="83" cy="55" r="14" fill="#c98f78" opacity=".75"/>
<path d="M160 65 q20 -25 38 0" stroke="#88a982" stroke-width="5" fill="none"/>
<path d="M45 98 h170" stroke="#d8c5aa" stroke-width="4"/>
</svg>
""",
    "residency.svg": """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 120">
<rect width="260" height="120" rx="22" fill="#eef5ea"/>
<path d="M55 84 h150 l-25 -42 h-100z" fill="#d7b889"/>
<path d="M90 84 v-33 h80 v33" fill="#fff7ea"/>
<circle cx="130" cy="60" r="10" fill="#88a982"/>
<path d="M36 92 C82 62 112 110 160 78 S220 75 238 58" stroke="#9db18b" stroke-width="5" fill="none" opacity=".65"/>
<path d="M185 35 l18 -20 l8 28" fill="#6e5a45"/>
</svg>
"""
}

for name, svg in svg_assets.items():
    (ASSETS / name).write_text(svg.strip(), encoding="utf-8")

# ------------------------------------------------------------
# Replace Opportunities tab
# ------------------------------------------------------------

text = APP.read_text(encoding="utf-8")
start = text.index("with tabs[2]:")
end = text.index("\nwith tabs[3]:")

new_block = r'''with tabs[2]:
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
'''

text = text[:start] + new_block + text[end:]
APP.write_text(text, encoding="utf-8")

print("Patched Mochi visual MVP with assets, dense cards, readiness, and drill-down.")