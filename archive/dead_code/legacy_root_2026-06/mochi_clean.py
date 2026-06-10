import base64
import html as _html
import json
import os
from datetime import datetime
from pathlib import Path
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# Page config — must be first Streamlit call
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Mochi's Atelier", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
# Data helpers
# ─────────────────────────────────────────────────────────────────────────────
_OPP_CACHE = None


def load_json(path, default):
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def _opps():
    global _OPP_CACHE
    if _OPP_CACHE is None:
        _OPP_CACHE = load_json("deploy_data/compact_opportunities.json", [])
    return _OPP_CACHE


def image_data_uri(path):
    if not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    with open(path, "rb") as f:
        return f"data:image/{mime};base64,{base64.b64encode(f.read()).decode()}"


def get_title(opp):
    return opp.get("title") or opp.get("name") or "Untitled"


def get_source(opp):
    return (
        opp.get("source_url")
        or opp.get("official_website")
        or opp.get("submission_page")
        or ""
    )


def best_score(opp):
    for field in ("watercolor_adjusted_score", "truth_aligned_score", "overall_score"):
        v = opp.get(field)
        if v is not None:
            try:
                return min(float(v), 10.0)
            except Exception:
                continue
    return 0.0


def clean_val(v, fallback="—"):
    if not v:
        return fallback
    s = str(v).strip()
    return fallback if s.lower() in ("unknown", "none", "null", "n/a", "not publicly listed", "") else s


def _has_real_deadline(opp):
    return clean_val(opp.get("deadline")) != "—"


# ─────────────────────────────────────────────────────────────────────────────
# Email drafts
# ─────────────────────────────────────────────────────────────────────────────
def email_draft_ja(opp):
    if opp.get("draft_introduction_ja"):
        return opp["draft_introduction_ja"]
    org = clean_val(opp.get("organization"), get_title(opp))
    return (
        "件名：水彩画作品についてのご相談\n\n"
        "はじめまして。東京在住の水彩画家、GEGYjijiと申します。\n"
        "都市の風景、建築、記憶といった日常の静けさをテーマに水彩画を制作しております。\n\n"
        f"{org}様のお取り組みに関心を持ち、作品のご紹介や展示・販売について\n"
        "ご相談できればと思い、ご連絡いたしました。\n\n"
        "ポートフォリオ：[portfolio link]\n\n"
        "どうぞよろしくお願いいたします。\n"
        "GEGYjiji"
    )


def email_draft_en(opp):
    if opp.get("draft_introduction_en"):
        return opp["draft_introduction_en"]
    org = clean_val(opp.get("organization"), get_title(opp))
    return (
        "Subject: Inquiry from watercolor artist GEGYjiji\n\n"
        "Hello,\n\n"
        "My name is GEGYjiji, a watercolor painter based in Tokyo.\n"
        "I work with themes of urban landscapes, architecture, memory, and quiet everyday spaces.\n\n"
        f"I am writing to enquire whether {org} might be open to discussing\n"
        "exhibitions, consignment, or submissions.\n\n"
        "Portfolio: [portfolio link]\n\n"
        "Thank you,\n"
        "GEGYjiji"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Section data getters
# ─────────────────────────────────────────────────────────────────────────────
def get_immediate_best_moves():
    items = [o for o in _opps() if o.get("exclusive_primary_bucket") == "immediate_best_moves"]
    items.sort(key=best_score, reverse=True)
    return items[:5]


def get_open_calls():
    items = [
        o for o in _opps()
        if _has_real_deadline(o)
        and o.get("exclusive_primary_bucket") not in ("reject", "stretch_targets", "low_priority")
    ]
    items.sort(key=best_score, reverse=True)
    return items[:5]


def get_zines_and_print():
    zine_cats = {
        "zine_print", "bookstore_gallery", "bookstore_event",
        "zine_shop_consignment", "zine_fair_booth",
    }
    items = [
        o for o in _opps()
        if (
            o.get("exclusive_primary_bucket") == "publication_targets"
            or o.get("category") in zine_cats
        )
        and o.get("exclusive_primary_bucket") != "reject"
    ]
    items.sort(key=best_score, reverse=True)
    return items[:5]


def get_relationship_targets():
    items = [o for o in _opps() if o.get("exclusive_primary_bucket") == "relationship_builders"]
    items.sort(key=best_score, reverse=True)
    return items[:5]


def get_watch_list():
    items = [o for o in _opps() if o.get("exclusive_primary_bucket") == "stretch_targets"]
    items.sort(key=best_score, reverse=True)
    return items[:5]


# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
def inject_css():
    # Hero background isolated — the 1.9 MB PNG becomes a 2.6 MB base64 blob.
    # Keeping it in its own st.markdown() call prevents it from corrupting the
    # HTML renderer when combined with other content.
    hero_uri = image_data_uri("static/assets/headers/mochi_hero.png")
    if hero_uri:
        st.markdown(
            f'<style>.hp-hero {{ background-image: url("{hero_uri}"); '
            f'background-size: cover; background-position: center 18%; }}</style>',
            unsafe_allow_html=True,
        )

    st.markdown("""
<style>
/* ─ Page base ─────────────────────────────────────────────── */
:root {
  --paper:      #f7efe2;
  --paper-soft: #fffaf2;
  --ink:        #3f3027;
  --ink-soft:   #6f5d4c;
  --line:       #dcc19b;
  --line-soft:  #ead8bd;
  --gold:       #b87d3a;
}

.stApp { background-color: var(--paper); }
.block-container { max-width: 1400px; padding-top: 1rem; padding-bottom: 3rem; }
div[data-testid="stHeader"] { background: #0e1117 !important; }

h1, h2, h3, h4, h5, h6 { color: var(--ink); font-family: Georgia, "Times New Roman", serif; }
p, li { color: var(--ink-soft); }

/* ─ Hero ───────────────────────────────────────────────────── */
.hp-hero {
  position: relative;
  width: 100%;
  min-height: 500px;
  border-radius: 28px;
  overflow: hidden;
  margin-bottom: 24px;
  border: 1px solid var(--line);
  box-shadow: 0 14px 40px rgba(70,44,20,.13);
  background: #f0e3cc;
}

.hp-panel {
  position: absolute;
  top: 28px; left: 28px;
  width: 292px;
  background: rgba(255, 249, 237, 0.91);
  border: 1px solid rgba(220, 193, 155, 0.65);
  border-radius: 20px;
  padding: 20px 20px 16px 20px;
  box-shadow: 0 8px 28px rgba(70,44,20,.11);
}

.hp-greeting {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.55rem; color: var(--ink);
  font-weight: bold; line-height: 1.05; margin-bottom: 2px;
}
.hp-sub {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 0.88rem; color: #7a6352;
  font-style: italic; margin-bottom: 13px;
}
.hp-focus-label {
  font-size: 0.68rem; color: #9a8070;
  text-transform: uppercase; letter-spacing: 0.08em;
  font-weight: bold; margin-bottom: 10px;
  padding-bottom: 5px;
  border-bottom: 1px solid rgba(220,193,155,0.5);
}
.focus-row { display: flex; align-items: flex-start; gap: 8px; margin-bottom: 10px; }
.focus-ico { font-size: 0.92rem; flex-shrink: 0; width: 18px; text-align: center; margin-top: 2px; }
.focus-body { flex: 1; min-width: 0; }
.focus-tier {
  font-size: 0.67rem; color: #9a8070; font-weight: bold;
  text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1px;
}
.focus-time { font-weight: normal; text-transform: none; letter-spacing: 0; }
.focus-name {
  font-size: 0.80rem; color: var(--ink); font-weight: 600;
  line-height: 1.25; margin-bottom: 1px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.focus-hint { font-size: 0.70rem; color: #7a6352; line-height: 1.3; }
.focus-dl {
  display: inline-block; margin-top: 3px;
  font-size: 0.67rem; color: #8a5e3c;
  background: #fcecd8; border-radius: 6px; padding: 1px 6px;
}
.focus-see-all {
  display: block; margin-top: 10px;
  font-size: 0.73rem; color: #9a8070; font-style: italic; text-align: right;
}

/* ─ Section headers ─────────────────────────────────────────── */
.sec-header {
  border-left: 4px solid var(--gold);
  padding-left: 14px;
  margin: 36px 0 10px 0;
}
.sec-header-title {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.1rem; color: var(--ink);
  font-weight: bold; margin: 0 0 3px 0;
}
.sec-header-desc {
  font-size: 0.81rem; color: var(--ink-soft);
  font-style: italic; margin: 0;
}

/* ─ Opportunity cards ───────────────────────────────────────── */
.opp-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 14px;
  background: var(--paper-soft);
  border: 1px solid var(--line-soft);
  border-radius: 14px;
  margin-bottom: 2px;
  box-shadow: 0 2px 8px rgba(70,44,20,.05);
}
.opp-title {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 0.95rem; color: var(--ink);
  font-weight: bold; line-height: 1.2; margin-bottom: 3px;
}
.opp-oneliner { font-size: 0.77rem; color: var(--ink-soft); line-height: 1.35; }
.opp-meta { font-size: 0.69rem; color: #9a8070; margin-top: 4px; }
.score-pill {
  font-size: 0.76rem; font-weight: bold;
  border-radius: 8px; padding: 3px 9px;
  white-space: nowrap; flex-shrink: 0;
  margin-top: 2px;
}

.detail-label {
  font-size: 0.70rem; text-transform: uppercase;
  letter-spacing: 0.07em; color: #9a8070;
  font-weight: bold; margin: 12px 0 4px 0;
  border-bottom: 1px solid var(--line-soft);
  padding-bottom: 3px;
}

/* ─ Section nav cards ───────────────────────────────────────── */
.sc-row {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 14px;
  margin: 36px 0 20px 0;
}
.sc-card {
  background: var(--paper-soft);
  border: 1px solid #e0ccaa; border-radius: 18px;
  padding: 18px 14px 14px 14px;
  box-shadow: 0 4px 14px rgba(70,44,20,.06);
  display: flex; flex-direction: column; min-height: 136px;
  transition: box-shadow 0.18s ease, transform 0.14s ease;
}
.sc-card:hover { box-shadow: 0 8px 24px rgba(70,44,20,.11); transform: translateY(-2px); }
.sc-icon { font-size: 1.5rem; margin-bottom: 6px; }
.sc-title {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 0.88rem; color: var(--ink); font-weight: bold; margin-bottom: 5px;
}
.sc-desc { font-size: 0.71rem; color: #7a6352; line-height: 1.38; flex: 1; }
.sc-link { display: block; font-size: 0.71rem; color: #9a7d5e; margin-top: 9px; font-style: italic; }

/* ─ Mochi status bar ────────────────────────────────────────── */
.mochi-bar {
  display: flex; align-items: center; gap: 14px;
  background: rgba(255, 249, 237, 0.95);
  border: 1px solid var(--line); border-radius: 18px;
  padding: 13px 20px; margin: 28px 0 20px 0;
  box-shadow: 0 3px 12px rgba(70,44,20,.07);
}
.mochi-bar-portrait { width: 44px; height: 44px; flex-shrink: 0; }
.mochi-bar-portrait svg { width: 44px; height: 44px; }
.mochi-bar-id { flex-shrink: 0; }
.mochi-bar-name {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 0.95rem; color: var(--ink); font-weight: bold;
}
.mochi-bar-status { font-size: 0.70rem; color: #9a8070; margin-top: 2px; }
.mochi-bar-msg { font-size: 0.82rem; color: #7a6352; font-style: italic; flex: 1; line-height: 1.4; }

/* ─ Streamlit element overrides ─────────────────────────────── */
.stButton > button {
  background: var(--paper-soft) !important; color: var(--ink) !important;
  border: 1px solid var(--line) !important; border-radius: 10px !important;
  box-shadow: none !important; font-weight: 600 !important;
}
.stButton > button:hover { background: #f3e3ca !important; border-color: #caa978 !important; }
.stLinkButton a {
  background: var(--paper-soft) !important; color: var(--ink) !important;
  border: 1px solid var(--line) !important; border-radius: 10px !important; font-weight: 600 !important;
}
textarea { background: #fffdf8 !important; color: var(--ink) !important; border-radius: 14px !important; }
[data-testid="stExpander"] { background: var(--paper-soft) !important; border-color: var(--line-soft) !important; border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Hero + Today's Focus
# ─────────────────────────────────────────────────────────────────────────────
def _focus_display_name(raw):
    name = raw.split(" - ")[0].strip()
    return (name[:50].rstrip() + "…") if len(name) > 52 else name


def render_homepage_section():
    hour = datetime.now().hour
    if hour < 12:
        greeting, sub = "Good morning", "let's make something today."
    elif hour < 17:
        greeting, sub = "Good afternoon", "let's grow today."
    else:
        greeting, sub = "Good evening", "let's reflect and plan."

    focus_raw = load_json("memory/best_moves.json", {}).get("global_best_moves", [])[:3]
    tier_meta = [
        ("🔍", "Quick Win", "5 min"),
        ("✉️", "High Impact", "30–60 min"),
        ("🌱", "Stretch Goal", "longer term"),
    ]

    rows_html = ""
    for i, item in enumerate(focus_raw):
        icon, label, hint = tier_meta[i]
        name = _html.escape(_focus_display_name(item.get("name", "")))
        action = _html.escape(item.get("next_action", "")[:88].strip())
        dl_raw = item.get("deadline", "").strip()
        dl_html = (
            f'<span class="focus-dl">&#x23F0; {_html.escape(dl_raw[:55])}</span>'
            if dl_raw and len(dl_raw) < 70 else ""
        )
        rows_html += (
            f'<div class="focus-row">'
            f'<div class="focus-ico">{icon}</div>'
            f'<div class="focus-body">'
            f'<div class="focus-tier">{label} <span class="focus-time">&middot; {hint}</span></div>'
            f'<div class="focus-name">{name}</div>'
            f'<div class="focus-hint">{action}</div>'
            f'{dl_html}'
            f'</div></div>'
        )

    st.markdown(
        f'<div class="hp-hero"><div class="hp-panel">'
        f'<div class="hp-greeting">{_html.escape(greeting)}</div>'
        f'<div class="hp-sub">{_html.escape(sub)}</div>'
        f'<div class="hp-focus-label">Today\'s Focus</div>'
        f'{rows_html}'
        f'<span class="focus-see-all">See all &rarr;</span>'
        f'</div></div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Opportunity card
# ─────────────────────────────────────────────────────────────────────────────
def render_card(opp, key_prefix):
    title = get_title(opp)
    score = best_score(opp)
    city = clean_val(opp.get("city"), "")
    deadline = clean_val(opp.get("deadline"))
    one_liner = clean_val(opp.get("one_sentence"), clean_val(opp.get("why_this_fits_short"), ""))

    # Score pill colour
    pill_color = "#4a7c3a" if score >= 9 else ("#a07030" if score >= 7 else "#8a7060")

    meta_parts = [city] if city else []
    if deadline != "—":
        meta_parts.append(f"DL: {deadline[:50]}")
    meta_html = (
        f'<div class="opp-meta">{_html.escape(" · ".join(meta_parts))}</div>'
        if meta_parts else ""
    )
    oneliner_html = (
        f'<div class="opp-oneliner">{_html.escape(one_liner[:115])}</div>'
        if one_liner else ""
    )

    # Always-visible header
    st.markdown(
        f'<div class="opp-header">'
        f'<div style="flex:1;min-width:0;">'
        f'<div class="opp-title">{_html.escape(title)}</div>'
        f'{oneliner_html}'
        f'{meta_html}'
        f'</div>'
        f'<span class="score-pill" style="background:{pill_color};color:#fff;">{score:.1f}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Expandable details
    with st.expander("Details + email draft", expanded=False):
        # Venue overview
        venue = clean_val(opp.get("one_sentence"), clean_val(opp.get("relationship_note"), ""))
        if venue:
            st.markdown('<div class="detail-label">Venue</div>', unsafe_allow_html=True)
            st.write(venue)

        # Why it fits
        fit = clean_val(opp.get("why_this_fits_short"), "")
        if fit:
            st.markdown('<div class="detail-label">Why it fits</div>', unsafe_allow_html=True)
            st.write(fit)

        # What they're looking for
        bullets = [b for b in (opp.get("three_bullets") or []) if b]
        if bullets:
            st.markdown('<div class="detail-label">What they\'re looking for</div>', unsafe_allow_html=True)
            for b in bullets:
                st.markdown(f"- {b}")

        # How to apply
        st.markdown('<div class="detail-label">How to apply</div>', unsafe_allow_html=True)
        col_dl, col_fee = st.columns(2)
        col_dl.markdown(f"**Deadline:** {deadline}")
        col_fee.markdown(f"**Fee:** {clean_val(opp.get('fees'))}")

        action = clean_val(opp.get("quick_action"), "")
        if action:
            st.info(action)

        url = opp.get("submission_page") or get_source(opp)
        if url:
            st.link_button("Visit →", url)

        # Email drafts
        st.markdown('<div class="detail-label">Sample email</div>', unsafe_allow_html=True)
        tab_ja, tab_en = st.tabs(["日本語", "English"])
        with tab_ja:
            st.text_area(
                "ja",
                email_draft_ja(opp),
                height=200,
                key=f"{key_prefix}_ja",
                label_visibility="collapsed",
            )
        with tab_en:
            st.text_area(
                "en",
                email_draft_en(opp),
                height=200,
                key=f"{key_prefix}_en",
                label_visibility="collapsed",
            )


# ─────────────────────────────────────────────────────────────────────────────
# Opportunity sections
# ─────────────────────────────────────────────────────────────────────────────
def render_section(title, description, items, key_prefix):
    st.markdown(
        f'<div class="sec-header">'
        f'<div class="sec-header-title">{_html.escape(title)}</div>'
        f'<div class="sec-header-desc">{_html.escape(description)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if not items:
        st.caption("Nothing in this category yet.")
        return
    for i, opp in enumerate(items):
        render_card(opp, f"{key_prefix}_{i}")


SECTIONS = [
    (
        "Immediate Best Moves",
        "Mochi ranked these first. High confidence, right career phase, and something actionable today.",
        get_immediate_best_moves,
        "imm",
    ),
    (
        "Open Calls — by Deadline",
        "Time-sensitive. These have known deadlines. A closed call with a perfect score is worthless.",
        get_open_calls,
        "open",
    ),
    (
        "Zines and Print",
        "Bookstores, zine shops, and publications. The most friction-free path to getting work into circulation.",
        get_zines_and_print,
        "zine",
    ),
    (
        "Relationship Targets",
        "Cafes, galleries, and spaces that suit a quiet personal introduction. No deadline pressure — just the right moment.",
        get_relationship_targets,
        "rel",
    ),
    (
        "Watch List",
        "Tier 3–4 targets — institutional, prestigious, not yet appropriate. Track them now. Do not apply yet.",
        get_watch_list,
        "watch",
    ),
]


def render_opportunity_sections():
    for title, description, getter, key_prefix in SECTIONS:
        render_section(title, description, getter(), key_prefix)


# ─────────────────────────────────────────────────────────────────────────────
# Section nav cards
# ─────────────────────────────────────────────────────────────────────────────
def render_section_cards():
    st.markdown("""
<div class="sc-row">
  <div class="sc-card">
    <div class="sc-icon">&#x1F3DB;</div>
    <div class="sc-title">Opportunities</div>
    <div class="sc-desc">All galleries, open calls, residencies, and more.</div>
    <span class="sc-link">View all &rarr;</span>
  </div>
  <div class="sc-card">
    <div class="sc-icon">&#x1F33F;</div>
    <div class="sc-title">Suggested Peers</div>
    <div class="sc-desc">Artists to follow, connect with, and learn from.</div>
    <span class="sc-link">Explore &rarr;</span>
  </div>
  <div class="sc-card">
    <div class="sc-icon">&#x2709;&#xFE0F;</div>
    <div class="sc-title">Outreach</div>
    <div class="sc-desc">Track conversations and manage your outreach.</div>
    <span class="sc-link">Open &rarr;</span>
  </div>
  <div class="sc-card">
    <div class="sc-icon">&#x1F4CB;</div>
    <div class="sc-title">Quests</div>
    <div class="sc-desc">Daily and weekly goals to keep your practice moving.</div>
    <span class="sc-link">See quests &rarr;</span>
  </div>
  <div class="sc-card">
    <div class="sc-icon">&#x1F4D3;</div>
    <div class="sc-title">Journal</div>
    <div class="sc-desc">Capture ideas, reflections, and inspiration.</div>
    <span class="sc-link">Open &rarr;</span>
  </div>
  <div class="sc-card">
    <div class="sc-icon">&#x1F4CA;</div>
    <div class="sc-title">Analytics</div>
    <div class="sc-desc">See your progress and patterns over time.</div>
    <span class="sc-link">View &rarr;</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Mochi status bar
# ─────────────────────────────────────────────────────────────────────────────
def render_mochi_status_bar():
    cat_html = ""
    svg_path = "static/assets/mochi/hero_cat.svg"
    if os.path.exists(svg_path):
        with open(svg_path, "r", encoding="utf-8") as f:
            cat_html = f'<div class="mochi-bar-portrait">{f.read()}</div>'

    st.markdown(
        f'<div class="mochi-bar">'
        f'{cat_html}'
        f'<div class="mochi-bar-id">'
        f'<div class="mochi-bar-name">Mochi &#x2665;</div>'
        f'<div class="mochi-bar-status">Happy &middot; Full &middot; Content</div>'
        f'</div>'
        f'<div class="mochi-bar-msg">'
        f'Mochi has been watching the light change all afternoon.<br>'
        f'She found five things worth your attention today.'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
inject_css()
render_homepage_section()
render_opportunity_sections()
render_section_cards()
render_mochi_status_bar()
