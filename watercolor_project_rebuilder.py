
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_JSON = "memory/watercolor_projects.json"
OUT_REPORT = "reports/watercolor_projects.md"

def load(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def blob(opp):
    parts = []
    for k in ["title", "name", "organization", "category", "one_sentence", "why_this_fits_short"]:
        if opp.get(k):
            parts.append(str(opp[k]))
    for k in ["watercolor_fit_hits", "visual_fit_hits", "fit_keyword_hits"]:
        for x in opp.get(k, []) or []:
            parts.append(str(x))
    return " ".join(parts).lower()

def find_targets(opps, terms, limit=8):
    matches = []
    for opp in opps:
        text = blob(opp)
        hits = [t for t in terms if t.lower() in text]
        if hits:
            matches.append({
                "title": opp.get("title") or opp.get("name") or "Unknown",
                "score": opp.get("watercolor_adjusted_score", opp.get("overall_score")),
                "hits": hits,
                "why": opp.get("why_this_fits_short") or opp.get("one_sentence") or "",
            })
    matches.sort(key=lambda x: float(x.get("score", 0) or 0), reverse=True)
    return matches[:limit]

def build_projects():
    return [
        {"title":"Quiet Neighborhood Watercolors","format":"12–18 watercolor paintings","description":"A coherent series of small watercolors based on ordinary neighborhoods, plants, shopfronts, windows, stairs, fences, and lived-in architectural details.","portfolio_use":"Best for works-on-paper open calls, bookstore/gallery spaces, and small gallery submissions.","terms":["watercolor","works on paper","painting","gallery","small works","bookstore","artist-run gallery"],"first_action":"Choose 12 finished or nearly finished watercolors. Group them by place, plant life, architecture, and human trace."},
        {"title":"Human Trace / Works on Paper","format":"focused works-on-paper proposal","description":"A tighter project about indirect human presence: domestic edges, plants, walls, windows, shop signs, objects, and architectural traces.","portfolio_use":"Best for group shows, open exhibitions, and residencies where the work needs a clearer conceptual statement.","terms":["works on paper","drawing","painting","residency","open exhibition","architecture","memory"],"first_action":"Write a 90-word statement and select 8–12 works that all show indirect human presence."},
        {"title":"Small Places","format":"small works exhibition","description":"A soft, accessible series of small watercolor paintings about small local places: cafés, shops, streets, corners, and plants.","portfolio_use":"Best for local galleries, cafes, bookstores, and low-pressure first exhibitions.","terms":["small works","cafe","bookstore","gallery","local","watercolor","painting"],"first_action":"Prepare a compact PDF: title, 10 images, dimensions, prices if available, and a 3-line artist note."},
        {"title":"Watercolor Artist Book","format":"zine / artist book from watercolor works","description":"A printed sequence of watercolor works, using photobook logic but keeping painting as the primary medium.","portfolio_use":"Best for TOKYO ART BOOK FAIR, UTRECHT, MOUNT ZINE, flotsam books, and artist-book ecosystems.","terms":["artist book","zine","book fair","printed matter","small press","illustration","watercolor"],"first_action":"Make a 16-page PDF mockup using existing watercolor images. Do not overexplain it."}
    ]

def main():
    opps = load(OPP_PATH, [])
    projects = build_projects()
    for project in projects:
        project["opportunity_targets"] = find_targets(opps, project["terms"], limit=8)
    save(OUT_JSON, projects)

    lines = ["# Watercolor Project Plan", "", "This replaces the photography-first project logic with watercolor-first project logic.", ""]
    for project in projects:
        lines += [f"## {project['title']}", "", f"**Format:** {project['format']}", "", project["description"], "", f"**Portfolio use:** {project['portfolio_use']}", "", "### Best Targets"]
        targets = project.get("opportunity_targets", [])
        if not targets:
            lines.append("_No targets yet._")
        else:
            for t in targets:
                lines.append(f"- **{t['title']}** — watercolor score {t.get('score')}. {t.get('why')}")
        lines += ["", "### First Action", project["first_action"], ""]
    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_REPORT}")

if __name__ == "__main__":
    main()
