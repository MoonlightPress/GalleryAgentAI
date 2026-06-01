
"""
Optional helper patch.

You do NOT need this for zine opportunities to appear.
The converter adds zine opportunities directly to compact_opportunities.json.

Use this only if you want a quick sidebar filter default or button later.

Recommended app.py usage:

    zine_opps = [o for o in opps if o.get("career_category") == "zines"]

or:

    selected_category = st.selectbox(
        "Category",
        ["All"] + sorted(set(o.get("career_category", "other") for o in opps))
    )
"""

def is_zine_opportunity(opp):
    return (
        opp.get("career_category") == "zines"
        or opp.get("category") == "zine_print"
        or "zine" in str(opp.get("title", "")).lower()
    )
