
import base64
import json
import os
from datetime import datetime
from ui.strategy_homepage_components import render_strategy_homepage
from ui.zine_opportunity_section import render_zine_section
from ui.best_moves_streamlit_section import render_best_moves_section
from ui.category_context_streamlit_section import render_category_context_section
from ui.opportunity_review_sections import render_opportunity_review_sections
from ui.publishing_opportunity_section import render_publishing_section
from collections import defaultdict
from ui.report_ui_components import *
import streamlit as st
from ui.portfolio_match_ui_components import render_portfolio_match_panel
from ui.feedback_ui_components import render_feedback_learning_panel
from ui.relationship_ui_components import *
from visual_card_system import *
from report_layout_upgrade import *
from pathlib import Path
import json

APP_DIR = Path(__file__).resolve().parent
STRATEGY_FEED_PATH = APP_DIR / "Memory" / "strategy_feed.json"


def load_strategy_feed():
    if not STRATEGY_FEED_PATH.exists():
        return []
    with open(STRATEGY_FEED_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


from ui.report_ui_components import render_pretty_report

st.set_page_config(page_title="Mochi's Atelier", layout="wide")

with open("styles/generated_visual_upgrade.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


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


# ── Global base styles ───────────────────────────────────────────────────────

st.markdown("""
<style>
div[data-testid="stHeader"] { background: #0e1117 !important; }
header[data-testid="stHeader"] { background: #0e1117 !important; }
.stAppHeader { background: #0e1117 !important; }
h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #3f3027 !important; }

:root {
    --paper: #f7efe2;
    --paper-soft: #fffaf2;
    --ink: #3f3027;
    --ink-soft: #6f5d4c;
    --line: #dcc19b;
    --line-soft: #ead8bd;
    --leaf: #dfe8cf;
}

.stApp { background-color: var(--paper); }

.block-container {
    max-width: 1440px;
    padding-top: 1.0rem;
    padding-bottom: 3rem;
}

h1, h2, h3 { color: var(--ink); font-family: Georgia, "Times New Roman", serif; }
p, li { color: var(--ink-soft); }

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

.card-topline { display: flex; gap: 12px; align-items: flex-start; }
.card-stamp { width: 58px; height: 58px; object-fit: contain; opacity: .95; flex: 0 0 auto; }
.card-main { min-width: 0; }

.card-title {
    font-family: Georgia, "Times New Roman", serif;
    font-weight: 700;
    font-size: 1.08rem;
    color: var(--ink);
    line-height: 1.15;
    margin-bottom: 5px;
}

.card-meta { color: #7b6756; font-size: .78rem; margin-bottom: 7px; }
.card-summary { color: var(--ink-soft); font-size: .88rem; line-height: 1.35; margin-top: 8px; }

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

.chip-good { background: var(--leaf); border-color: #c6d1ad; }

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
""", unsafe_allow_html=True)


# ── Card / detail helpers (unchanged from app.py) ────────────────────────────

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

    st.markdown(f"""
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
""", unsafe_allow_html=True)

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


# ── New homepage section ─────────────────────────────────────────────────────

def _focus_display_name(raw):
    name = raw.split(" - ")[0].strip()
    if len(name) > 52:
        name = name[:50].rstrip() + "…"
    return name


def render_homepage_section():
    hour = datetime.now().hour
    if hour < 12:
        greeting, sub = "Good morning", "let's make something today."
    elif hour < 17:
        greeting, sub = "Good afternoon", "let's grow today."
    else:
        greeting, sub = "Good evening", "let's reflect and plan."

    best_moves_data = load_json("memory/best_moves.json", {})
    focus_raw = best_moves_data.get("global_best_moves", [])[:3]

    tier_meta = [
        ("🔍", "Quick Win", "5 min"),
        ("✉️", "High Impact", "30–60 min"),
        ("🌱", "Stretch Goal", "longer term"),
    ]

    focus_rows_html = ""
    for i, item in enumerate(focus_raw):
        icon, label, time_hint = tier_meta[i]
        name = _focus_display_name(item.get("name", ""))
        action = item.get("next_action", "")[:88].strip()
        deadline_raw = item.get("deadline", "").strip()
        dl_html = ""
        if deadline_raw and len(deadline_raw) < 70:
            dl_html = f'<span class="focus-dl">⏰ {deadline_raw[:55]}</span>'
        focus_rows_html += f"""
        <div class="focus-row">
          <div class="focus-ico">{icon}</div>
          <div class="focus-body">
            <div class="focus-tier">{label} <span class="focus-time">· {time_hint}</span></div>
            <div class="focus-name">{name}</div>
            <div class="focus-hint">{action}</div>
            {dl_html}
          </div>
        </div>"""

    hero_uri = image_data_uri("static/assets/headers/mochi_hero.png")
    hero_bg = (
        f'background-image: url("{hero_uri}"); background-size: cover; background-position: center 18%;'
        if hero_uri else
        "background: #f0e3cc;"
    )

    cat_html = ""
    svg_path = "static/assets/mochi/hero_cat.svg"
    if os.path.exists(svg_path):
        with open(svg_path, "r", encoding="utf-8") as f:
            cat_html = f'<div class="mochi-bar-portrait">{f.read()}</div>'

    st.markdown(f"""
<style>
/* ─── Hero ──────────────────────────────────────────────────── */
.hp-hero {{
  position: relative;
  width: 100%;
  min-height: 500px;
  border-radius: 28px;
  overflow: hidden;
  margin-bottom: 24px;
  border: 1px solid #dcc19b;
  box-shadow: 0 14px 40px rgba(70,44,20,.13);
  {hero_bg}
}}

.hp-panel {{
  position: absolute;
  top: 28px;
  left: 28px;
  width: 292px;
  background: rgba(255, 249, 237, 0.91);
  border: 1px solid rgba(220, 193, 155, 0.65);
  border-radius: 20px;
  padding: 20px 20px 16px 20px;
  box-shadow: 0 8px 28px rgba(70,44,20,.11);
}}

.hp-greeting {{
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.55rem;
  color: #3f3027;
  font-weight: bold;
  line-height: 1.05;
  margin-bottom: 2px;
}}

.hp-sub {{
  font-family: Georgia, "Times New Roman", serif;
  font-size: 0.88rem;
  color: #7a6352;
  font-style: italic;
  margin-bottom: 13px;
}}

.hp-focus-label {{
  font-size: 0.68rem;
  color: #9a8070;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: bold;
  margin-bottom: 10px;
  padding-bottom: 5px;
  border-bottom: 1px solid rgba(220,193,155,0.5);
}}

.focus-row {{
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 10px;
}}

.focus-ico {{
  font-size: 0.92rem;
  flex-shrink: 0;
  width: 18px;
  text-align: center;
  margin-top: 2px;
}}

.focus-body {{ flex: 1; min-width: 0; }}

.focus-tier {{
  font-size: 0.67rem;
  color: #9a8070;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1px;
}}

.focus-time {{
  font-weight: normal;
  text-transform: none;
  letter-spacing: 0;
}}

.focus-name {{
  font-size: 0.80rem;
  color: #3f3027;
  font-weight: 600;
  line-height: 1.25;
  margin-bottom: 1px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}}

.focus-hint {{
  font-size: 0.70rem;
  color: #7a6352;
  line-height: 1.3;
}}

.focus-dl {{
  display: inline-block;
  margin-top: 3px;
  font-size: 0.67rem;
  color: #8a5e3c;
  background: #fcecd8;
  border-radius: 6px;
  padding: 1px 6px;
}}

.focus-see-all {{
  display: block;
  margin-top: 10px;
  font-size: 0.73rem;
  color: #9a8070;
  font-style: italic;
  text-align: right;
}}

/* ─── Section Cards ──────────────────────────────────────────── */
.sc-row {{
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 14px;
  margin-bottom: 28px;
}}

.sc-card {{
  background: rgba(255, 250, 242, 0.96);
  border: 1px solid #e0ccaa;
  border-radius: 18px;
  padding: 18px 14px 14px 14px;
  box-shadow: 0 4px 14px rgba(70,44,20,.06);
  display: flex;
  flex-direction: column;
  min-height: 136px;
  transition: box-shadow 0.18s ease, transform 0.14s ease;
}}

.sc-card:hover {{
  box-shadow: 0 8px 24px rgba(70,44,20,.11);
  transform: translateY(-2px);
}}

.sc-icon {{ font-size: 1.5rem; margin-bottom: 6px; }}

.sc-title {{
  font-family: Georgia, "Times New Roman", serif;
  font-size: 0.88rem;
  color: #3f3027;
  font-weight: bold;
  margin-bottom: 5px;
}}

.sc-desc {{
  font-size: 0.71rem;
  color: #7a6352;
  line-height: 1.38;
  flex: 1;
}}

.sc-link {{
  display: block;
  font-size: 0.71rem;
  color: #9a7d5e;
  margin-top: 9px;
  font-style: italic;
}}

/* ─── Mochi Status Bar ───────────────────────────────────────── */
.mochi-bar {{
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(255, 249, 237, 0.95);
  border: 1px solid #dcc19b;
  border-radius: 18px;
  padding: 13px 20px;
  margin-bottom: 20px;
  box-shadow: 0 3px 12px rgba(70,44,20,.07);
}}

.mochi-bar-portrait {{
  width: 44px;
  height: 44px;
  flex-shrink: 0;
}}

.mochi-bar-portrait svg {{
  width: 44px;
  height: 44px;
}}

.mochi-bar-id {{ flex-shrink: 0; }}

.mochi-bar-name {{
  font-family: Georgia, "Times New Roman", serif;
  font-size: 0.95rem;
  color: #3f3027;
  font-weight: bold;
}}

.mochi-bar-status {{
  font-size: 0.70rem;
  color: #9a8070;
  margin-top: 2px;
}}

.mochi-bar-msg {{
  font-size: 0.82rem;
  color: #7a6352;
  font-style: italic;
  flex: 1;
  line-height: 1.4;
}}
</style>

<div class="hp-hero">
  <div class="hp-panel">
    <div class="hp-greeting">{greeting}</div>
    <div class="hp-sub">{sub}</div>
    <div class="hp-focus-label">Today's Focus</div>
    {focus_rows_html}
    <span class="focus-see-all">See all →</span>
  </div>
</div>

<div class="sc-row">
  <div class="sc-card">
    <div class="sc-icon">🏛️</div>
    <div class="sc-title">Opportunities</div>
    <div class="sc-desc">Galleries, open calls, residencies, zine shops, and more.</div>
    <span class="sc-link">View all →</span>
  </div>
  <div class="sc-card">
    <div class="sc-icon">🌿</div>
    <div class="sc-title">Suggested Peers</div>
    <div class="sc-desc">Artists to follow, connect with, and learn from.</div>
    <span class="sc-link">Explore →</span>
  </div>
  <div class="sc-card">
    <div class="sc-icon">✉️</div>
    <div class="sc-title">Outreach</div>
    <div class="sc-desc">Track conversations and manage your outreach.</div>
    <span class="sc-link">Open →</span>
  </div>
  <div class="sc-card">
    <div class="sc-icon">📋</div>
    <div class="sc-title">Quests</div>
    <div class="sc-desc">Daily and weekly goals to keep your practice moving.</div>
    <span class="sc-link">See quests →</span>
  </div>
  <div class="sc-card">
    <div class="sc-icon">📓</div>
    <div class="sc-title">Journal</div>
    <div class="sc-desc">Capture ideas, reflections, and inspiration.</div>
    <span class="sc-link">Open →</span>
  </div>
  <div class="sc-card">
    <div class="sc-icon">📊</div>
    <div class="sc-title">Analytics</div>
    <div class="sc-desc">See your progress and patterns over time.</div>
    <span class="sc-link">View →</span>
  </div>
</div>

<div class="mochi-bar">
  {cat_html}
  <div class="mochi-bar-id">
    <div class="mochi-bar-name">Mochi ♥</div>
    <div class="mochi-bar-status">Happy · Full · Content</div>
  </div>
  <div class="mochi-bar-msg">
    Mochi has been watching the light change all afternoon.<br>
    She found three things worth your attention today.
  </div>
</div>
""", unsafe_allow_html=True)


# ── Main app ─────────────────────────────────────────────────────────────────

opps = load_json(
    "deploy_data/compact_opportunities.json",
    load_json("memory/compact_opportunities.json", []),
)
relationship_memory = load_json("memory/relationship_memory.json", {})

render_homepage_section()

selected_title = st.session_state.get("selected_title")

if selected_title:
    selected = next(
        (o for o in opps if get_title(o) == selected_title),
        None,
    )
    if selected:
        memory = relationship_memory.get(get_title(selected), {})
        render_relationship_bar(memory)
        render_detail(selected)

tabs = st.tabs(["Mochi Atelier", "Feedback", "Mousehole", "Observatory", "Archive"])

with tabs[0]:
    render_best_moves_section()
    st.markdown("---")
    render_zine_section(render_compact_card)
    st.markdown("---")
    render_category_context_section()
    st.markdown("---")
    render_opportunity_review_sections()
    st.markdown("---")
    render_publishing_section(render_compact_card)
    st.markdown("---")
    render_strategy_homepage()

with tabs[1]:
    render_feedback_learning_panel()

with tabs[2]:
    st.header("Mousehole")
    st.write("Career pathways and task progress will go here next.")

with tabs[3]:
    st.header("Observatory")
    st.write("Reports, market positioning, and long-form analysis will go here next.")

with tabs[4]:
    st.header("Archive")
    st.write(f"Loaded {len(opps)} opportunities.")

st.markdown("---")
render_portfolio_match_panel()
