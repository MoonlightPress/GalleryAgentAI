from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

text = text.replace(
'''                    if (
                        st.session_state.get("selected_opportunity", {}).get("title")
                        == title
                    ):''',
'''                    current_selected = st.session_state.get("selected_opportunity") or {}

                    if (
                        current_selected.get("title")
                        == title
                    ):'''
)

text = text.replace(
'''            if selected and selected_section == section_name:
                render_detail(selected)

            if len(section_opps) > 4:
                with st.expander(f"More {section_name}"):''',
'''            if len(section_opps) > 4:
                with st.expander(f"More {section_name}"):'''
)

text = text.replace(
'''            st.markdown("---")
''',
'''            if selected and selected_section == section_name:
                render_detail(selected)

            st.markdown("---")
''',
1
)

path.write_text(text, encoding="utf-8")

print("Fixed close crash and moved detail below full section.")