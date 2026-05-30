from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

old_tabs = '''with tabs[10]:
    st.header("Pipeline Status")
    st.markdown(load_text("pipeline_status.md", "No pipeline status generated yet."))
    

    with tabs[11]:
        st.header("Reusable Materials")
'''

new_tabs = '''with tabs[10]:
    st.header("Pipeline Status")

    if st.button("Run Full Council Pipeline"):
        import subprocess

        result = subprocess.run(
            ["python", "council_pipeline_agent.py"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            st.error("Pipeline failed.")
            st.code(result.stderr)
        else:
            st.success("Pipeline complete.")

    st.markdown(load_text("pipeline_status.md", "No pipeline status generated yet."))


with tabs[11]:
    st.header("Reusable Materials")
'''

text = text.replace(old_tabs, new_tabs)

path.write_text(text, encoding="utf-8")

print("Patched app.py pipeline/materials tabs.")