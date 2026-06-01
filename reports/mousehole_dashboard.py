import streamlit as st
import json
import os


st.set_page_config(
    page_title="Mousehole",
    layout="wide"
)


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


st.title("Mousehole")
st.caption("Career paths, readiness, uploaded materials, and compounding progress.")

tasks = load_json("memory/mousehole_tasks.json", {"tasks": []})["tasks"]
paths = load_json("memory/pathway_progress.json", {"pathways": []})["pathways"]
artist_memory = load_json("memory/artist_memory.json", {})

st.header("Pathways")

cols = st.columns(4)

for idx, path in enumerate(paths[:4]):
    with cols[idx]:
        with st.container(border=True):
            st.subheader(path["name"])
            st.progress(path.get("percent_complete", 0) / 100)
            st.write(f"{path.get('percent_complete', 0)}% complete")
            st.caption(path.get("description", ""))

st.header("Open Tasks")

open_tasks = [t for t in tasks if not t.get("complete")]
done_tasks = [t for t in tasks if t.get("complete")]

task_cols = st.columns(3)

for idx, task in enumerate(open_tasks):
    with task_cols[idx % 3]:
        with st.container(border=True):
            st.subheader(task["title"])
            st.write(task["description"])
            st.caption("Contributes to: " + ", ".join(task.get("contributes_to", [])))
            st.caption("Difficulty: " + task.get("difficulty", ""))

st.header("Completed Infrastructure")
for task in done_tasks:
    st.write("✅", task["title"])

st.header("Add Artist Memory")

memory_type = st.selectbox(
    "Memory Type",
    [
        "favorite_artists",
        "desired_peers",
        "publication_history",
        "sales_history",
        "career_goals",
        "avoid_preferences",
        "notes"
    ]
)

memory_text = st.text_area("Add one item or note")

if st.button("Save Memory"):
    if memory_type not in artist_memory:
        artist_memory[memory_type] = []

    if memory_text.strip():
        artist_memory[memory_type].append(memory_text.strip())
        save_json("memory/artist_memory.json", artist_memory)
        st.success("Saved.")
        st.rerun()

st.header("Current Artist Memory")
st.json(artist_memory)