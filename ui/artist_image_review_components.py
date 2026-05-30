
import json
import os
from pathlib import Path

import streamlit as st

CATALOG_PATH = "memory/image_catalog.json"
CLUSTER_PATH = "portfolio_cluster_template.json"
PROFILE_DRAFT_PATH = "memory/artist_visual_profile_draft.json"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def render_image_catalog_grid(images):
    if not images:
        st.info("No images cataloged yet. Put images in artist_images/ and run image_catalog_builder.py.")
        return

    cols = st.columns(4)

    for idx, item in enumerate(images[:80]):
        path = item.get("path", "")

        with cols[idx % 4]:
            if os.path.exists(path):
                st.image(path, use_container_width=True)
            st.caption(item.get("filename", ""))
            st.caption(item.get("folder", ""))


def render_cluster_editor(catalog, clusters):
    st.subheader("Portfolio Clusters")

    filenames = [x.get("filename") for x in catalog]

    for idx, cluster in enumerate(clusters.get("clusters", [])):
        with st.expander(cluster.get("name", f"Cluster {idx+1}"), expanded=idx == 0):
            cluster["name"] = st.text_input(
                "Cluster name",
                cluster.get("name", ""),
                key=f"cluster_name_{idx}"
            )

            cluster["images"] = st.multiselect(
                "Assign images",
                filenames,
                default=cluster.get("images", []),
                key=f"cluster_images_{idx}"
            )

            cluster["notes"] = st.text_area(
                "Notes",
                cluster.get("notes", ""),
                height=120,
                key=f"cluster_notes_{idx}"
            )

    if st.button("Save cluster assignments"):
        save_json(CLUSTER_PATH, clusters)
        st.success("Saved portfolio clusters.")


def build_profile_draft(clusters):
    visual_language = []
    recurring_subjects = []
    emotional_tone = []
    best_formats = []

    cluster_names = [c.get("name", "") for c in clusters.get("clusters", [])]
    notes = " ".join(c.get("notes", "") for c in clusters.get("clusters", []))

    if any("architecture" in x.lower() or "place" in x.lower() for x in cluster_names) or "architecture" in notes.lower():
        visual_language.extend(["architecture", "place", "memory", "quiet urban atmosphere"])
        recurring_subjects.extend(["buildings", "streets", "interiors", "architectural fragments"])

    if "daily" in notes.lower() or any("daily" in x.lower() for x in cluster_names):
        visual_language.extend(["daily observation", "intimate documentary", "quiet attention"])
        recurring_subjects.extend(["domestic details", "ordinary spaces", "small moments"])

    if "book" in notes.lower() or "zine" in notes.lower():
        best_formats.extend(["photobook", "zine", "artist book", "printed matter"])

    emotional_tone.extend(["quiet", "restrained", "atmospheric", "observational"])

    profile = {
        "summary": "Draft visual profile generated from portfolio cluster notes. Review and rewrite before treating as final.",
        "dominant_subjects": list(dict.fromkeys(recurring_subjects)),
        "recurring_motifs": list(dict.fromkeys(recurring_subjects)),
        "composition_patterns": [],
        "color_palette": [],
        "emotional_tone": list(dict.fromkeys(emotional_tone)),
        "pace": "slow / observational",
        "scale": "intimate to medium",
        "best_formats": list(dict.fromkeys(best_formats or ["photobook", "zine", "small exhibition", "artist-run space"])),
        "bad_fit_contexts": ["corporate branding", "commercial expo", "loud trend-based open calls"],
        "artist_statement_phrases": [],
        "curatorial_keywords": list(dict.fromkeys(visual_language)),
        "portfolio_bodies_to_create": cluster_names,
    }

    return profile


def render_visual_profile_builder(clusters):
    st.subheader("Visual Profile Draft")

    if st.button("Generate visual profile draft from clusters"):
        profile = build_profile_draft(clusters)
        save_json(PROFILE_DRAFT_PATH, profile)
        st.success(f"Wrote {PROFILE_DRAFT_PATH}")

    draft = load_json(PROFILE_DRAFT_PATH, {})

    if draft:
        st.json(draft)
        st.caption("Copy this into memory/artist_master_profile.json under visual_profile when it looks right.")


def render_artist_image_review_panel():
    st.header("Artist Image Review")

    catalog = load_json(CATALOG_PATH, [])
    clusters = load_json(CLUSTER_PATH, {"clusters": []})

    c1, c2, c3 = st.columns(3)
    c1.metric("Cataloged images", len(catalog))
    c2.metric("Portfolio clusters", len(clusters.get("clusters", [])))
    c3.metric("Assigned images", sum(len(c.get("images", [])) for c in clusters.get("clusters", [])))

    tabs = st.tabs(["Image Catalog", "Clusters", "Visual Profile Draft"])

    with tabs[0]:
        render_image_catalog_grid(catalog)

    with tabs[1]:
        render_cluster_editor(catalog, clusters)

    with tabs[2]:
        render_visual_profile_builder(clusters)
