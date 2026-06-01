
import base64
import json
import os
import re
from datetime import datetime, date as _date
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

with open("styles/generated_visual_upgrade.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


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


# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
div[data-testid="stHeader"] { background: #f7efe2 !important; }
header[data-testid="stHeader"] { background: #f7efe2 !important; }
.stAppHeader { background: #f7efe2 !important; }

:root {
    --paper:      #f7efe2;
    --paper-soft: #fffaf2;
    --ink:        #3f3027;
    --ink-soft:   #6f5d4c;
    --line:       #dcc19b;
    --line-soft:  #ead8bd;
    --leaf:       #dfe8cf;
    --gold:       #c8960c;
}

.stApp { background-color: var(--paper); }

.block-container {
    max-width: 1360px;
    padding-top: .75rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--ink) !important;
    font-family: Georgia, "Times New Roman", serif !important;
}

p, li { color: var(--ink-soft); }

/* ── Warm tabs ──────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 3px;
    border-bottom: 1px solid var(--line) !important;
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,250,242,.7) !important;
    border: 1px solid var(--line) !important;
    border-bottom: none !important;
    border-radius: 10px 10px 0 0 !important;
    color: var(--ink-soft) !important;
    font-family: Georgia, serif !important;
    font-size: .88rem !important;
    padding: 6px 16px !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255,250,242,1) !important;
    color: var(--ink) !important;
}
.stTabs [aria-selected="true"] {
    background: var(--paper) !important;
    color: var(--ink) !important;
    font-weight: 700 !important;
    border-bottom: 1px solid var(--paper) !important;
}

/* ── Opportunity expanders ──────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid #e0c998 !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    margin-bottom: 8px !important;
    background: rgba(255,252,245,.97) !important;
    box-shadow: 0 2px 8px rgba(70,44,20,.05) !important;
}
[data-testid="stExpanderDetails"] {
    background: #fffdf8 !important;
    border-top: 1px solid #ead8bd !important;
    padding: 2px 4px 8px !important;
}
[data-testid="stExpanderToggleIcon"] {
    color: #a07840 !important;
}

/* ── Legacy card classes (used in archive) ──────────────── */
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
    font-weight: 700; font-size: 1.08rem; color: var(--ink);
    line-height: 1.15; margin-bottom: 5px;
}
.card-meta { color: #7b6756; font-size: .78rem; margin-bottom: 7px; }
.card-summary { color: var(--ink-soft); font-size: .88rem; line-height: 1.35; margin-top: 8px; }

.badge-ok {
    display: inline-block; background: #e2ead5; color: #435134;
    border-radius: 999px; padding: 2px 7px; font-size: .70rem; margin: 0 4px 4px 0;
}
.badge-need {
    display: inline-block; background: #f4e3c7; color: #6a4e2f;
    border-radius: 999px; padding: 2px 7px; font-size: .70rem; margin: 0 4px 4px 0;
}

.detail-panel {
    background: rgba(255, 250, 242, .98);
    border: 1px solid var(--line); border-radius: 24px;
    padding: 20px; margin: 18px 0 26px 0;
    box-shadow: 0 12px 28px rgba(70, 44, 20, .10);
}
.report-box {
    background: #fffdf8; border: 1px solid #ead8bd;
    border-radius: 18px; padding: 18px; margin-top: 12px;
}
.soft-box {
    background: #f4e7cf; border: 1px solid #dec5a0;
    border-radius: 14px; padding: 12px;
    color: #594636; line-height: 1.45;
}

/* ── Buttons ────────────────────────────────────────────── */
.stButton > button {
    background: #fffaf2 !important; color: #3f3027 !important;
    border: 1px solid #dcc19b !important; border-radius: 10px !important;
    box-shadow: none !important; font-weight: 600 !important;
}
.stButton > button:hover {
    background: #f3e3ca !important; color: #3f3027 !important;
    border-color: #caa978 !important;
}
.stLinkButton a {
    background: #fffaf2 !important; color: #3f3027 !important;
    border: 1px solid #dcc19b !important; border-radius: 10px !important;
    font-weight: 600 !important;
}

textarea {
    background: #fffdf8 !important; color: var(--ink) !important;
    border-radius: 14px !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ── Legacy card rendering (kept for Archive tab) ────────────────────────────
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
                f'<div class="soft-box">{clean_value(opp.get("quick_action"), "Verify current public submission/contact details.")}</div>',
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


# ── Deadline parser ──────────────────────────────────────────────────────────
def _parse_deadline_app(text):
    if not text:
        return None
    s = str(text).strip().lower()
    if s in {"unknown", "check source", "check current schedule", "n/a", "tbd", "varies", ""}:
        return None
    month_map = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
                 "jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}
    today = _date.today()
    candidates = []
    for m in re.finditer(
        r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\.?\s+(\d{1,2}),?\s+(20\d{2})",
        text, re.I,
    ):
        try:
            candidates.append(_date(int(m.group(3)), month_map[m.group(1).lower()[:3]], int(m.group(2))))
        except (ValueError, KeyError):
            pass
    for m in re.finditer(r"(20\d{2})-(\d{2})-(\d{2})", text):
        try:
            candidates.append(_date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            pass
    for m in re.finditer(
        r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\.?\s+(\d{1,2})\b(?!\s*,?\s*20\d{2})",
        text, re.I,
    ):
        try:
            month = month_map[m.group(1).lower()[:3]]
            d = _date(today.year, month, int(m.group(2)))
            if d < today:
                d = _date(today.year + 1, month, int(m.group(2)))
            candidates.append(d)
        except (ValueError, KeyError):
            pass
    if not candidates:
        return None
    future = [d for d in candidates if d >= today]
    return min(future) if future else None


# ── Tiered opportunity view ──────────────────────────────────────────────────

def _section_header(icon, title, subtitle=""):
    sub = f'<div style="font-size:.79rem;color:#7a6250;margin-top:3px;">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
<div style="margin:30px 0 14px;padding:12px 18px;
            background:rgba(255,248,236,.65);border-radius:12px;
            border-left:3px solid #dcc19b;">
  <span style="font-family:Georgia,serif;font-size:1.02rem;
               font-weight:700;color:#3f3027;">{icon}&nbsp; {title}</span>
  {sub}
</div>""",
        unsafe_allow_html=True,
    )


def _deadline_badge(delta):
    """Return (prefix_string, color) for the expander label."""
    if delta is None:
        return "", "#5e4d3d"
    if delta <= 7:
        return f"🔴 {delta}d — ", "#b03030"
    if delta <= 30:
        return f"🟡 {delta}d — ", "#8a6010"
    return f"🟢 {delta}d — ", "#4a7040"


def render_opportunity_card(entry, key_prefix, default_open=False):
    """Collapsible card for a single opportunity. entry is an enriched dict."""
    name     = entry["name"]
    detail   = entry["detail"]
    delta    = entry["delta"]
    dl_raw   = entry["dl_raw"]
    atype    = entry["atype"]
    why      = entry["why"] or detail.get("why_this_fits_short") or detail.get("one_sentence") or ""

    # Build expander label: badge + name + short hook
    if atype == "apply":
        prefix, _ = _deadline_badge(delta)
    elif atype == "submit_when_open":
        prefix = "◐  "
    else:
        prefix = "✉  "

    hook = why[:75].rstrip()
    if why and len(why) > 75:
        hook += "…"

    expander_label = f"{prefix}{name}"
    if hook:
        expander_label += f"  ·  {hook}"

    with st.expander(expander_label, expanded=default_open):

        col_l, col_r = st.columns([1, 1.4])

        with col_l:
            # Deadline
            if dl_raw and dl_raw.lower() not in {
                "unknown", "check source", "check current schedule", "n/a", "tbd", "varies", ""
            }:
                suffix = ""
                if delta is not None:
                    suffix = f"  *({delta} days)*" if delta > 0 else "  *⚠ check — may have passed*"
                st.markdown(f"**Deadline:** {dl_raw}{suffix}")

            # Fee
            fees = (detail.get("fees") or "").strip()
            if fees and fees.lower() not in {"unknown", "check source", ""}:
                st.markdown(f"**Fee:** {fees}")

            # Phone / address for café targets
            phone = detail.get("contact_phone") or ""
            address = detail.get("address") or ""
            if phone:
                st.markdown(f"**Phone:** {phone}")
            if address:
                st.markdown(f"**Address:** {address}")

            # Link
            link = (
                detail.get("submission_page")
                or detail.get("source_url")
                or entry.get("source")
                or ""
            )
            if link:
                st.link_button("Open →", link)

            # Next action box
            quick = (detail.get("quick_action") or "").strip()
            if quick:
                st.markdown(
                    f'<div class="soft-box" style="margin-top:10px;font-size:.81rem;">{quick}</div>',
                    unsafe_allow_html=True,
                )

        with col_r:
            # Why it fits
            if why:
                st.markdown(why)

            bullets = detail.get("three_bullets") or []
            for b in (bullets[:2] if bullets else []):
                st.markdown(f"— {str(b)[:130]}")

            # Outreach drafts for contact/propose items
            if atype in ("contact_and_propose",):
                st.markdown("")
                st.markdown("**Draft outreach**")
                draft_ja_prefab = entry.get("draft_ja") or ""
                draft_opp = detail if detail else {"name": name, "organization": name}
                ja_tab, en_tab = st.tabs(["日本語", "English"])
                with ja_tab:
                    content = draft_ja_prefab if draft_ja_prefab else make_draft(draft_opp, "ja")
                    st.text_area(
                        "ja", content, height=170,
                        key=f"{key_prefix}_ja",
                        label_visibility="collapsed",
                    )
                with en_tab:
                    st.text_area(
                        "en", make_draft(draft_opp, "en"), height=170,
                        key=f"{key_prefix}_en",
                        label_visibility="collapsed",
                    )


def render_tiered_opportunities():
    """Main opportunities tab: IBM → open calls → relationship targets → watch list."""
    buckets = load_json("memory/exclusive_strategy_buckets.json", {})
    deploy  = load_json("deploy_data/compact_opportunities.json", [])
    by_name = {
        (o.get("name") or o.get("title") or "").strip().lower(): o
        for o in deploy
    }
    today = _date.today()

    def enrich(e):
        name   = e.get("title") or e.get("name") or ""
        detail = by_name.get(name.lower(), {})
        dl_raw = detail.get("deadline") or ""
        dl_dt  = _parse_deadline_app(dl_raw)
        delta  = (dl_dt - today).days if dl_dt else None
        return {
            "name":     name,
            "detail":   detail,
            "dl_raw":   dl_raw,
            "delta":    delta,
            "atype":    e.get("action_type", "apply"),
            "why":      (e.get("why") or "").strip(),
            "source":   e.get("source") or "",
            "rel_note": e.get("relationship_note") or "",
            "draft_ja": e.get("draft_introduction_ja") or "",
            "score":    float(e.get("differentiated_score") or e.get("score") or 0),
        }

    ibm     = [enrich(e) for e in buckets.get("immediate_best_moves", [])]
    stretch = [enrich(e) for e in buckets.get("stretch_targets", [])]

    # Split and sort
    apply_items = sorted(
        [e for e in ibm if e["atype"] == "apply"],
        key=lambda x: (x["delta"] is None, x["delta"] if x["delta"] is not None else 9999),
    )
    submit_watch = [e for e in ibm if e["atype"] == "submit_when_open"]
    contact_items = sorted(
        [e for e in ibm if e["atype"] == "contact_and_propose"],
        key=lambda x: -x["score"],
    )

    urgent = [e for e in apply_items if e["delta"] is not None and e["delta"] <= 30]
    coming = [e for e in apply_items if e["delta"] is None or e["delta"] > 30]

    # ── Section 1: Immediate priorities ─────────────────────────────────────
    if urgent:
        plural = "s" if len(urgent) != 1 else ""
        _section_header(
            "🌿", "Act Now",
            f"{len(urgent)} open call{plural} closing within 30 days"
        )
        for i, entry in enumerate(urgent):
            render_opportunity_card(entry, f"urgent_{i}", default_open=(i == 0))

    # ── Section 2: Upcoming open calls ──────────────────────────────────────
    if coming or submit_watch:
        _section_header("📋", "Open Calls", "Applications open — no imminent deadline")
        for i, entry in enumerate(coming + submit_watch):
            render_opportunity_card(entry, f"coming_{i}")

    # ── Section 3: Contact & propose ────────────────────────────────────────
    if contact_items:
        _section_header(
            "✉️", "Contact & Propose",
            "Galleries, cafés, and spaces to approach directly — no application form"
        )
        for i, entry in enumerate(contact_items):
            render_opportunity_card(entry, f"contact_{i}")

    # ── Section 4: Watch list ────────────────────────────────────────────────
    if stretch:
        _section_header(
            "🔭", "Watch List",
            "Longer-term targets — build towards these, don't pursue now"
        )
        for i, entry in enumerate(stretch):
            name  = entry["name"]
            why   = entry["why"][:90] if entry["why"] else "Aspirational — revisit at a later career stage."
            link  = entry["detail"].get("source_url") or entry["source"] or ""
            label = f"◦  {name}  ·  {why}{'…' if entry['why'] and len(entry['why']) > 90 else ''}"
            with st.expander(label, expanded=False):
                st.markdown(entry["why"] if entry["why"] else "*No description available.*")
                if link:
                    st.link_button("Open →", link)

    # ── Empty state ──────────────────────────────────────────────────────────
    if not ibm and not stretch:
        st.markdown(
            """
<div style="padding:40px;text-align:center;color:#8b7360;font-family:Georgia,serif;">
  Mochi is still looking. Run the pipeline to surface new opportunities.
</div>""",
            unsafe_allow_html=True,
        )


# ── Section cards (hero footer) ──────────────────────────────────────────────
def _render_section_cards():
    sections = [
        ("static/assets/cards/stamp_gallery.png",  "🏛️", "Opportunities",  "Galleries, open calls, and residencies"),
        ("static/assets/cards/stamp_bookstore.png", "📖", "Zines & Print",  "Art book fairs, zine shops, self-publishing"),
        ("static/assets/cards/stamp_cafe.png",      "✉️", "Outreach",       "Conversations and ready-to-send drafts"),
        ("static/assets/cards/stamp_market.png",    "🐭", "Peppercorn",     "Goals, questlines, and your artist voice"),
        ("static/assets/cards/stamp_residency.png", "🐦", "Saffron",        "Market context and comparable artists"),
        ("",                                         "🗄️", "Archive",        "Complete history and all opportunities"),
    ]
    cols = st.columns(6, gap="small")
    for col, (stamp_path, fallback_icon, title, desc) in zip(cols, sections):
        with col:
            stamp_uri = image_data_uri(stamp_path) if stamp_path else ""
            icon_html = (
                f'<img src="{stamp_uri}" style="width:44px;height:44px;object-fit:contain;opacity:.9;">'
                if stamp_uri else
                f'<span style="font-size:1.8rem;line-height:1">{fallback_icon}</span>'
            )
            st.markdown(
                f"""
<div style="background:rgba(255,252,245,.95);border:1px solid #dcc19b;
            border-radius:18px;padding:16px 12px 14px;text-align:center;
            min-height:148px;box-shadow:0 4px 14px rgba(70,44,20,.07);
            display:flex;flex-direction:column;align-items:center;gap:7px;">
  {icon_html}
  <div style="font-family:Georgia,serif;font-size:.86rem;font-weight:700;
              color:#3f3027;line-height:1.2;margin-top:2px">{title}</div>
  <div style="font-size:.72rem;color:#7a6250;line-height:1.35">{desc}</div>
</div>""",
                unsafe_allow_html=True,
            )


# ── Mochi status bar ─────────────────────────────────────────────────────────
def render_mochi_statusbar():
    hour = datetime.now().hour
    if hour < 12:
        mood    = "☀️ Bright-eyed + Curious"
        message = "Mochi woke up early and checked for new opportunities."
    elif hour < 17:
        mood    = "🌿 Happy + Full + Content"
        message = "Mochi is happily napping in the sun. Come back later to feed and play!"
    else:
        mood    = "🕯 Cozy + Settled + Warm"
        message = "Mochi is dozing by the warm lamplight, dreaming of new shows."

    ibm_data  = load_json("memory/exclusive_strategy_buckets.json", {})
    ibm_count = len(ibm_data.get("immediate_best_moves", []))
    note = f"{ibm_count} things worth your attention today." if ibm_count else "You've got beautiful things to make."

    cat_uri  = image_data_uri("static/assets/header_cat.png")
    cat_html = (
        f'<img src="{cat_uri}" style="width:52px;height:52px;object-fit:cover;'
        f'border-radius:50%;border:2px solid #dcc19b;flex:0 0 auto;">'
        if cat_uri else '<span style="font-size:2.2rem">🐱</span>'
    )
    st.markdown(
        f"""
<div style="display:flex;align-items:center;gap:20px;
            background:#f7efe2;border:1px solid #dcc19b;border-radius:20px;
            padding:14px 24px;margin-top:28px;
            box-shadow:0 4px 14px rgba(70,44,20,.07);">
  {cat_html}
  <div style="flex:1;min-width:0;">
    <div style="font-family:Georgia,serif;font-size:.92rem;
                font-weight:700;color:#3f3027;">Mochi ♥</div>
    <div style="font-size:.76rem;color:#7a6250;margin-top:1px;">{mood}</div>
    <div style="font-size:.83rem;color:#5e4d3d;margin-top:3px;">{message}</div>
  </div>
  <div style="background:#fffdf4;border:1px solid #dcc19b;border-radius:14px;
              padding:10px 18px;font-size:.80rem;color:#5e4d3d;
              font-style:italic;flex:0 0 auto;max-width:220px;
              text-align:center;line-height:1.45;">
    {note}
  </div>
</div>""",
        unsafe_allow_html=True,
    )


# ── Homepage (hero + section cards) ─────────────────────────────────────────
def render_homepage():
    hour = datetime.now().hour
    if hour < 12:
        greeting, sub = "Good morning", "☕ a fresh start today."
    elif hour < 17:
        greeting, sub = "Good afternoon", "🌿 let's grow today."
    else:
        greeting, sub = "Good evening", "🕯 time for reflection."

    ibm_raw = load_json("memory/exclusive_strategy_buckets.json", {})
    deploy  = load_json("deploy_data/compact_opportunities.json", [])
    by_name = {(o.get("name") or o.get("title") or "").strip().lower(): o for o in deploy}
    ibm     = ibm_raw.get("immediate_best_moves", [])
    today   = _date.today()

    enriched = []
    for entry in ibm:
        name   = entry.get("title") or entry.get("name") or ""
        detail = by_name.get(name.lower(), {})
        dl_raw = detail.get("deadline") or ""
        dl_dt  = _parse_deadline_app(dl_raw)
        delta  = (dl_dt - today).days if dl_dt else None
        enriched.append({
            "name":  name,
            "dl_raw": dl_raw,
            "delta":  delta,
            "link":  (detail.get("submission_page") or detail.get("source_url")
                      or entry.get("source") or ""),
            "atype": entry.get("action_type", "apply"),
            "why":   (entry.get("why") or "")[:90],
        })

    apply_dl  = sorted([e for e in enriched if e["atype"] == "apply" and e["delta"] is not None],
                       key=lambda x: x["delta"])
    contact   = [e for e in enriched if e["atype"] in ("contact_and_propose", "submit_when_open")]
    apply_ndl = [e for e in enriched if e["atype"] == "apply" and e["delta"] is None]
    pool      = apply_dl + contact + apply_ndl

    slot_meta = [
        ("🌿", "Quick Win",        "5 min"),
        ("✉️", "High Impact Move", "30–60 min"),
        ("🔭", "Stretch Goal",     "longer term"),
    ]
    used, cards = set(), []
    for i, (icon, label, hint) in enumerate(slot_meta):
        candidates = (contact or pool) if i == 2 else pool
        chosen = next((e for e in candidates if e["name"] not in used), None)
        if chosen:
            used.add(chosen["name"])
            cards.append((icon, label, hint, chosen))

    focus_html = ""
    for icon, label, hint, item in cards:
        display = item["name"][:44] + ("…" if len(item["name"]) > 44 else "")
        if item["delta"] is not None:
            d   = item["delta"]
            clr = "#b03030" if d <= 7 else "#8a6010" if d <= 30 else "#4a7040"
            badge = f'<span style="font-size:.68rem;font-weight:700;color:{clr};"> — {d}d</span>'
        else:
            badge = ""
        focus_html += f"""
<div style="display:flex;align-items:flex-start;gap:8px;
            padding:6px 0;border-bottom:1px solid rgba(220,193,155,.45);">
  <span style="font-size:.95rem;flex:0 0 auto;margin-top:3px;">{icon}</span>
  <div style="min-width:0;">
    <div style="font-size:.66rem;color:#9a7d63;font-weight:700;
                text-transform:uppercase;letter-spacing:.05em;line-height:1.1;">
      {label} <span style="font-weight:400;text-transform:none;letter-spacing:0;">({hint})</span>
    </div>
    <div style="font-size:.83rem;color:#3f3027;line-height:1.25;margin-top:1px;
                word-break:break-word;">{display}{badge}</div>
  </div>
</div>"""

    hero_path = "static/assets/headers/mochi_hero.png"
    if os.path.exists(hero_path):
        with open(hero_path, "rb") as fh:
            hero_b64 = base64.b64encode(fh.read()).decode()
        bg = f"background-image:url('data:image/png;base64,{hero_b64}');background-size:cover;background-position:center 18%;"
    else:
        bg = "background:linear-gradient(135deg,#f0e6d0 0%,#d8c49a 100%);"

    st.markdown(
        f"""
<div style="position:relative;width:100%;height:460px;border-radius:28px;
            overflow:hidden;border:1px solid #dcc19b;
            box-shadow:0 14px 34px rgba(70,44,20,.13);
            margin-bottom:24px;{bg}">
  <div style="position:absolute;inset:0;
              background:linear-gradient(to right,
                rgba(247,239,226,.96) 0%,
                rgba(247,239,226,.90) 24%,
                rgba(247,239,226,.40) 50%,
                rgba(247,239,226,0)  66%);"></div>
  <div style="position:absolute;top:0;left:0;bottom:0;width:330px;
              padding:38px 30px 30px;display:flex;flex-direction:column;gap:18px;">
    <div>
      <div style="font-family:Georgia,'Times New Roman',serif;
                  font-size:2.0rem;font-weight:700;color:#3f3027;line-height:1.1;">
        {greeting}, Mochi</div>
      <div style="font-size:.98rem;color:#7a6250;margin-top:4px;">{sub}</div>
    </div>
    <div style="background:rgba(255,252,245,.88);border:1px solid rgba(220,193,155,.75);
                border-radius:18px;padding:13px 15px 11px;
                backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);">
      <div style="font-family:Georgia,serif;font-size:.86rem;font-weight:700;
                  color:#3f3027;letter-spacing:.03em;margin-bottom:9px;">
        Today's Focus</div>
      {focus_html}
      <div style="font-size:.72rem;color:#8b6914;font-weight:600;margin-top:8px;">
        See all quests →</div>
    </div>
  </div>
</div>""",
        unsafe_allow_html=True,
    )

    _render_section_cards()


# ── Module-level data ────────────────────────────────────────────────────────
opps = load_json(
    "deploy_data/compact_opportunities.json",
    load_json("memory/compact_opportunities.json", []),
)
relationship_memory = load_json("memory/relationship_memory.json", {})

render_homepage()

# Detail panel for selected opportunity (legacy flow used from archive)
selected_title = st.session_state.get("selected_title")
if selected_title:
    selected = next((o for o in opps if get_title(o) == selected_title), None)
    if selected:
        memory = relationship_memory.get(get_title(selected), {})
        render_relationship_bar(memory)
        render_detail(selected)


# ── Tabs ─────────────────────────────────────────────────────────────────────
tabs = st.tabs(["Mochi Atelier", "Feedback", "Mousehole", "Observatory", "Archive"])

with tabs[0]:
    render_tiered_opportunities()

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
    st.caption(f"{len(opps)} opportunities loaded.")
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

st.markdown("---")
render_portfolio_match_panel()
render_mochi_statusbar()
