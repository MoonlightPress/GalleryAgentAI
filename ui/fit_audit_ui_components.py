
import json
import os
from pathlib import Path

import streamlit as st

AUDIT_PATH = "memory/fit_audit.json"
REPORT_PATH = "reports/fit_audit_report.md"


GRADE_COLORS = {
    "solid": "#4f7a57",
    "needs review": "#9b7b3d",
    "possibly inflated": "#9b5a4a",
    "possibly underrated": "#5d6f9b",
    "normal": "#7a6b5d",
}


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def read_text(path, fallback=""):
    if os.path.exists(path):
        return Path(path).read_text(encoding="utf-8")
    return fallback


def grade_badge(grade):
    color = GRADE_COLORS.get(grade, "#7a6b5d")
    return f"""
<span style="
display:inline-block;
padding:4px 10px;
border-radius:999px;
background:{color};
color:white;
font-size:.75rem;
font-weight:700;
">
{grade}
</span>
"""


def render_fit_audit_panel():
    st.header("Fit Audit")

    audit = load_json(AUDIT_PATH, [])

    if not audit:
        st.warning("No fit audit found. Run `python fit_audit_engine.py` or `python run_full_mochi_pipeline.py`.")
        return

    solid = [x for x in audit if x.get("confidence_grade") == "solid"]
    review = [x for x in audit if x.get("confidence_grade") == "needs review"]
    inflated = [x for x in audit if x.get("confidence_grade") == "possibly inflated"]
    underrated = [x for x in audit if x.get("confidence_grade") == "possibly underrated"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Solid", len(solid))
    c2.metric("Needs review", len(review))
    c3.metric("Inflated?", len(inflated))
    c4.metric("Underrated?", len(underrated))

    grade = st.selectbox(
        "Filter",
        ["all", "solid", "needs review", "possibly inflated", "possibly underrated", "normal"],
        key="fit_audit_grade_filter",
    )

    visible = audit if grade == "all" else [x for x in audit if x.get("confidence_grade") == grade]

    for idx, item in enumerate(visible[:60]):
        title = item.get("title", "Unknown")
        score = item.get("score", "?")
        g = item.get("confidence_grade", "normal")

        with st.expander(f"{title} · {score}/10 · {g}", expanded=idx < 5):
            st.markdown(grade_badge(g), unsafe_allow_html=True)

            st.write("**Category:**", item.get("category") or "")
            st.write("**Location:**", " ".join([str(item.get("city") or ""), str(item.get("country") or "")]).strip())

            if item.get("positive_reasons"):
                st.write("**Positive reasons:**")
                for reason in item["positive_reasons"]:
                    st.write("- " + reason)

            if item.get("risks"):
                st.write("**Risks:**")
                for risk in item["risks"]:
                    st.write("- " + risk)

            if item.get("missing_fields"):
                st.write("**Missing fields:**", ", ".join(item["missing_fields"]))

    with st.expander("Full markdown audit report"):
        st.markdown(read_text(REPORT_PATH, "No report found."))
