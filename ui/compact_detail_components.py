
import json
import os
from pathlib import Path

import streamlit as st


def clean_value(value, fallback="Not listed"):
    if value is None:
        return fallback
    text = str(value).strip()
    if not text or text.lower() in {"unknown", "none", "null", "n/a", "na"}:
        return fallback
    return text


def get_title(opp):
    return opp.get("title") or opp.get("name") or "Unknown"


def get_source(opp):
    return (
        opp.get("source_url")
        or opp.get("source_link")
        or opp.get("official_website")
        or opp.get("submission_page")
        or ""
    )


def score_num(value):
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def badge(text, kind="neutral"):
    colors = {
        "good": ("#eef7ee", "#315f3a"),
        "warn": ("#fff4dc", "#7a5520"),
        "bad": ("#fdeceb", "#8a382d"),
        "neutral": ("#f5efe5", "#5c4b3b"),
        "blue": ("#edf3fa", "#365a7c"),
    }
    bg, fg = colors.get(kind, colors["neutral"])

    return f"""
<span class="mini-badge" style="background:{bg};color:{fg};">
{text}
</span>
"""


def format_buckets(opp):
    buckets = opp.get("career_buckets", []) or []
    if not buckets:
        primary = opp.get("primary_bucket")
        buckets = [primary] if primary else []

    labels = {
        "career_changing": "Career-changing",
        "high_confidence": "High confidence",
        "publication_targets": "Publication",
        "book_zine_targets": "Book/Zine",
        "global_reach": "Global",
        "easy_wins": "Easy win",
        "relationship_builders": "Relationship",
        "needs_research": "Needs research",
        "low_priority": "Low priority",
    }

    rendered = []
    for b in buckets[:5]:
        label = labels.get(b, str(b).replace("_", " ").title())
        kind = "good"
        if b == "needs_research":
            kind = "warn"
        if b == "low_priority":
            kind = "bad"
        if b == "global_reach":
            kind = "blue"
        rendered.append(badge(label, kind))

    return " ".join(rendered)


def compact_metric(label, value):
    return f"""
<div class="compact-metric">
  <div class="compact-metric-label">{label}</div>
  <div class="compact-metric-value">{value}</div>
</div>
"""


def render_compact_detail(opp):
    title = get_title(opp)
    source = get_source(opp)

    score = clean_value(opp.get("overall_score"), "?")
    differentiated = clean_value(opp.get("differentiated_score"), score)
    visual = clean_value(opp.get("visual_fit_score"), "0")
    verification = clean_value(opp.get("verification_status"), "unverified")
    url_status = clean_value(opp.get("url_verification_status"), "unchecked")

    city = clean_value(opp.get("city"), "")
    country = clean_value(opp.get("country"), "")
    location = " ".join([city, country]).strip() or "Location not listed"

    deadline = clean_value(opp.get("deadline"))
    fees = clean_value(opp.get("fees"))
    submission = clean_value(opp.get("submission_page"))
    contact = clean_value(
        opp.get("contact")
        or opp.get("email")
        or opp.get("contact_email")
        or opp.get("contact_url")
    )

    one_sentence = clean_value(opp.get("one_sentence"), "")
    why = clean_value(opp.get("why_this_fits_short"), "")
    quick_action = clean_value(opp.get("quick_action"), "")
    strategy = clean_value(opp.get("submission_strategy"), "")
    tone = clean_value(opp.get("submission_tone"), "")

    visual_hits = opp.get("visual_fit_hits", []) or []
    bullets = opp.get("three_bullets", []) or []

    st.markdown(
        f"""
<div class="compact-detail-shell">

  <div class="compact-detail-header">
    <div>
      <div class="compact-detail-kicker">Selected Opportunity</div>
      <div class="compact-detail-title">{title}</div>
      <div class="compact-detail-location">{location}</div>
    </div>
    <div class="compact-detail-buckets">
      {format_buckets(opp)}
    </div>
  </div>

  <div class="compact-detail-metrics">
    {compact_metric("Score", score)}
    {compact_metric("Differentiated", differentiated)}
    {compact_metric("Visual Fit", visual)}
    {compact_metric("Verification", verification)}
    {compact_metric("URL", url_status)}
  </div>

</div>
""",
        unsafe_allow_html=True,
    )

    left, middle, right = st.columns([1, 1, 1])

    with left:
        st.markdown(
            f"""
<div class="compact-panel">
  <div class="compact-panel-title">Venue / Source</div>
  <p>{one_sentence}</p>
  <div class="compact-row"><b>Location:</b> {location}</div>
  <div class="compact-row"><b>Deadline:</b> {deadline}</div>
  <div class="compact-row"><b>Fees:</b> {fees}</div>
  <div class="compact-row"><b>Contact:</b> {contact}</div>
</div>
""",
            unsafe_allow_html=True,
        )

        if source:
            st.link_button("Open source", source, use_container_width=True)

    with middle:
        st.markdown(
            f"""
<div class="compact-panel">
  <div class="compact-panel-title">Submission / Action</div>
  <p>{quick_action}</p>
  <div class="compact-row"><b>Strategy:</b> {strategy}</div>
  <div class="compact-row"><b>Tone:</b> {tone}</div>
  <div class="compact-row"><b>Submission:</b> {submission}</div>
</div>
""",
            unsafe_allow_html=True,
        )

        draft = build_micro_draft(opp)
        with st.expander("Micro outreach draft", expanded=False):
            st.code(draft)

    with right:
        hit_html = ""
        for hit in visual_hits[:8]:
            hit_html += f"<span class='mini-badge'>{hit}</span> "

        bullet_html = ""
        for bullet in bullets[:4]:
            bullet_html += f"<li>{bullet}</li>"

        st.markdown(
            f"""
<div class="compact-panel">
  <div class="compact-panel-title">Why This Fits</div>
  <p>{why}</p>
  <div class="compact-row"><b>Visual signals:</b><br>{hit_html or "Not yet scored"}</div>
  <ul>{bullet_html}</ul>
</div>
""",
            unsafe_allow_html=True,
        )


def build_micro_draft(opp):
    org = opp.get("organization") or get_title(opp)

    return f"""Hello,

I am researching whether {org} is currently open to photography, photobook, artist-book, or zine-related submissions.

The work I am considering is a quiet photographic sequence about ordinary neighborhoods, human trace, memory, and lived-in spaces.

Could you let me know whether there is a current submission process, open call, or appropriate contact for this kind of work?

Thank you."""
