
import json, os
from pathlib import Path

SOURCE_PATH = "source_targets.json"
REPORT_PATH = "reports/watercolor_source_expansion.md"

NEW_SOURCES = [
    {"name":"Jackson's Art Prize","url":"https://www.jacksonsart.com/paintingprize/","source_type":"painting_prize","region":"Global","priority":"high","fit_reason":"Works on paper and painting-friendly international open call."},
    {"name":"Royal Watercolour Society","url":"https://www.royalwatercoloursociety.co.uk/","source_type":"watercolor_society","region":"UK","priority":"medium","fit_reason":"Watercolor-specific institutional reference."},
    {"name":"Mall Galleries Open Exhibitions","url":"https://www.mallgalleries.org.uk/open-exhibitions","source_type":"open_exhibition","region":"UK","priority":"medium","fit_reason":"Traditional and contemporary painting/open exhibition path."},
    {"name":"ArtConnect Open Calls","url":"https://www.artconnect.com/opportunities","source_type":"open_call_index","region":"Global","priority":"high","fit_reason":"Broad open call index for painting, drawing, residency, and works on paper."},
    {"name":"CuratorSpace","url":"https://www.curatorspace.com/opportunities","source_type":"open_call_index","region":"Global","priority":"high","fit_reason":"Open calls across exhibitions, galleries, residencies, and publications."},
    {"name":"Tokyo Illustrators Society","url":"https://www.tis-home.com/","source_type":"illustration_society","region":"Japan","priority":"medium","fit_reason":"Useful if her watercolor practice overlaps with illustration/publishing."},
    {"name":"Gallery IYN","url":"https://www.gallery-iyn.com/","source_type":"japan_gallery_open_call","region":"Japan","priority":"medium","fit_reason":"Accessible Japanese gallery/open-call ecosystem for painting and illustration-adjacent work."},
    {"name":"Design Festa Gallery","url":"https://designfestagallery.com/","source_type":"accessible_gallery_space","region":"Japan","priority":"low","fit_reason":"Low-barrier display space. Useful only as a low-pressure first exhibition, not prestige."},
    {"name":"HB Gallery","url":"https://hbgallery.com/","source_type":"illustration_gallery","region":"Japan","priority":"high","fit_reason":"Tokyo illustration/gallery context; potentially strong for watercolor if image-led."},
    {"name":"OPA Gallery","url":"https://opagallery.net/","source_type":"illustration_gallery","region":"Japan","priority":"high","fit_reason":"Tokyo illustration and works-on-paper friendly gallery context."},
    {"name":"Pinpoint Gallery","url":"https://pinpointgallery.com/","source_type":"illustration_gallery","region":"Japan","priority":"high","fit_reason":"Picture book / illustration / works-on-paper context; potentially relevant for watercolor."}
]

def load(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    sources = load(SOURCE_PATH, {"seed_sources": [], "fit_keywords": [], "reject_keywords": []})
    existing = {s.get("url") for s in sources.get("seed_sources", [])}
    added = 0
    for src in NEW_SOURCES:
        if src["url"] not in existing:
            sources.setdefault("seed_sources", []).append(src)
            existing.add(src["url"])
            added += 1

    watercolor_keywords = ["watercolor","watercolour","works on paper","drawing","painting","small works","illustration","open exhibition","gallery open call","artist-run gallery","paper","residency for painters","contemporary painting"]
    sources["fit_keywords"] = list(dict.fromkeys(sources.get("fit_keywords", []) + watercolor_keywords))
    save(SOURCE_PATH, sources)

    lines = ["# Watercolor Source Expansion", "", f"Added sources: {added}", f"Total sources: {len(sources.get('seed_sources', []))}", "", "## Added Sources", ""]
    for src in NEW_SOURCES:
        lines.append(f"- **{src['name']}** — {src['source_type']} — {src['fit_reason']}")
    Path("reports").mkdir(exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")
    print(f"Added watercolor sources: {added}")
    print(f"Wrote {REPORT_PATH}")

if __name__ == "__main__":
    main()
