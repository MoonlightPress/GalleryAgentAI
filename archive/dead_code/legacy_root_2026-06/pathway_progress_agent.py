import json
import os


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


materials = load_json(
    "memory/materials_memory.json",
    {}
)

accomplishments = load_json(
    "memory/accomplishments_memory.json",
    {
        "items": []
    }
)

model = load_json(
    "pathway_model_seed.json",
    {
        "pathways": []
    }
)


def has_material(req):
    mapping = {
        "artist_statement": materials.get("artist_statements"),
        "short_bio": materials.get("artist_bios"),
        "cv": materials.get("cv_versions"),
        "portfolio_set": materials.get("portfolio_sets"),
        "image_specs": materials.get("image_specs"),
        "simple_outreach_email": materials.get("translations"),
    }

    if req in mapping:
        return bool(mapping[req])

    text = json.dumps(
        accomplishments,
        ensure_ascii=False
    ).lower()

    return req.replace("_", " ") in text


progress = []

for pathway in model["pathways"]:

    total = 0
    done = 0
    levels_out = []

    for level in pathway["levels"]:

        reqs_out = []

        for req in level["requirements"]:
            ok = has_material(req)
            total += 1
            if ok:
                done += 1

            reqs_out.append({
                "requirement": req,
                "complete": ok
            })

        levels_out.append({
            "level": level["level"],
            "name": level["name"],
            "requirements": reqs_out
        })

    percent = round((done / total) * 100) if total else 0

    progress.append({
        "id": pathway["id"],
        "name": pathway["name"],
        "description": pathway["description"],
        "percent_complete": percent,
        "complete_requirements": done,
        "total_requirements": total,
        "levels": levels_out
    })

save_json(
    "memory/pathway_progress.json",
    {
        "pathways": progress
    }
)

print("Saved memory/pathway_progress.json")