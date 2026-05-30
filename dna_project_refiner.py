
import json
import os
from pathlib import Path

DNA_PATH = "memory/artist_dna.json"
PROJECT_PATH = "memory/next_projects.json"
OUT_PATH = "reports/dna_project_refinement.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    dna = load_json(DNA_PATH, {})
    projects = load_json(PROJECT_PATH, [])

    if not dna:
        print("No artist DNA found. Run visual_dna_extractor.py first.")
        return

    inferred = dna.get("inferred_artist_dna", {})
    core = inferred.get("core_subject_likelihoods", [])
    behavior = inferred.get("visual_behavior", [])
    anti = inferred.get("anti_patterns", [])

    lines = [
        "# DNA Project Refinement",
        "",
        "This report tightens project concepts using the extracted visual DNA.",
        "",
    ]

    for project in projects:
        project.setdefault("dna_refinement", {})
        project["dna_refinement"]["prioritize"] = core[:5] + behavior[:5]
        project["dna_refinement"]["avoid"] = anti[:5]
        project["dna_refinement"]["editing_rule"] = "Keep images that strengthen place, trace, sequence, and quiet observation. Remove images that only function as attractive single images."

        lines.append(f"## {project.get('title')}")
        lines.append("")
        lines.append("### Prioritize")
        for item in project["dna_refinement"]["prioritize"]:
            lines.append(f"- {item}")

        lines.append("")
        lines.append("### Avoid")
        for item in project["dna_refinement"]["avoid"]:
            lines.append(f"- {item}")

        lines.append("")
        lines.append("### Editing Rule")
        lines.append(project["dna_refinement"]["editing_rule"])
        lines.append("")

    save_json(PROJECT_PATH, projects)
    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
