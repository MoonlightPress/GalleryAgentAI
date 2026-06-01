from pathlib import Path
import streamlit as st

REPORTS = [
    {
        "title": "Ecosystem Summary",
        "path": "reports/ecosystem_summary_v2.md",
        "note": "High-level counts and current strongest categories.",
    },
    {
        "title": "Gallery Fit Analysis",
        "path": "reports/gallery_fit_analysis.md",
        "note": "Best gallery targets, fit score, risk score, and reason.",
    },
    {
        "title": "Gallery Tiers",
        "path": "reports/gallery_tiers.md",
        "note": "A/B/C sorting for gallery opportunities.",
    },
    {
        "title": "Gallery Profiles",
        "path": "reports/gallery_profiles.md",
        "note": "Raw profile details: emails, submission signals, and gallery type.",
    },
    {
        "title": "Verified Competitions",
        "path": "reports/verified_competitions.md",
        "note": "Competitions with extracted deadlines, fees, routes, and emails.",
    },
    {
        "title": "Competition Candidates",
        "path": "reports/competition_candidates.md",
        "note": "Raw competition discovery results.",
    },
    {
        "title": "Ecosystem Battle Plans",
        "path": "reports/ecosystem_battle_plans.md",
        "note": "Category-level practical action plans.",
    },
    {
        "title": "Opportunity Rankings",
        "path": "reports/opportunity_rankings.md",
        "note": "Highest actionability, local targets, prestige, and print/zine rankings.",
    },
    {
        "title": "Fair Ecosystem",
        "path": "reports/fair_ecosystem.md",
        "note": "Art fairs, creator markets, zine fairs, and event targets.",
    },
    {
        "title": "Open Call Verification",
        "path": "reports/open_call_verification.md",
        "note": "Verified open calls and application records.",
    },
]

def _read(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")

def _section_preview(md: str, max_chars: int = 4500) -> str:
    if len(md) <= max_chars:
        return md
    return md[:max_chars] + "\n\n---\n\n_Trimmed preview. Open the report file for the full version._"

def render_report_card(item, expanded=False):
    md = _read(item["path"])
    with st.expander(item["title"], expanded=expanded):
        st.caption(item["note"])
        st.code(item["path"], language="text")
        if not md:
            st.warning("Report not found yet. Run the relevant sprint first.")
            return
        st.markdown(_section_preview(md))

def render_opportunity_review_sections():
    st.markdown("## Review Intelligence")
    st.caption("Raw intelligence reports from the latest opportunity sprints. This is for review, not final UI.")

    existing = [r for r in REPORTS if Path(r["path"]).exists()]
    missing = [r for r in REPORTS if not Path(r["path"]).exists()]

    c1, c2, c3 = st.columns(3)
    c1.metric("Reports Found", len(existing))
    c2.metric("Reports Missing", len(missing))
    c3.metric("Mode", "Review")

    priority = [
        "Ecosystem Summary",
        "Gallery Fit Analysis",
        "Verified Competitions",
        "Opportunity Rankings",
        "Ecosystem Battle Plans",
    ]

    st.markdown("### Priority Review")
    for title in priority:
        item = next((r for r in REPORTS if r["title"] == title), None)
        if item:
            render_report_card(item, expanded=(title == "Ecosystem Summary"))

    with st.expander("More reports", expanded=False):
        for item in REPORTS:
            if item["title"] not in priority:
                render_report_card(item, expanded=False)
