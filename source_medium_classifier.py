
import json, os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
REPORT_PATH = "reports/source_medium_audit.md"

PAINTING_TERMS = [
    "watercolor", "watercolour", "painting", "works on paper", "drawing",
    "illustration", "small works", "open exhibition", "gallery open call",
    "artist-run gallery", "paper", "contemporary painting", "picture book",
    "illustration gallery", "hb gallery", "opa gallery", "pinpoint gallery",
    "gallery iyn", "mall galleries", "royal watercolour society", "jackson"
]

PHOTOGRAPHY_TERMS = [
    "photography", "photographer", "photographers", "photo", "photobook",
    "street photography", "lensculture", "photovogue", "aperture",
    "der greif", "camera", "photo contest", "photography award",
    "the photographers' gallery", "futures photography"
]

MIXED_TERMS = [
    "artist book", "zine", "printed matter", "book fair", "small press",
    "bookstore", "utrecht", "tokyo art book fair", "mount zine",
    "book and sons", "flotsam", "post", "nadiff", "self publish"
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

def raw_blob(opp):
    # Use original-ish source fields, not rewritten explanation fields where possible.
    parts = []
    for k in [
        "title", "name", "organization", "category", "category_label",
        "source_url", "official_website", "source_link", "submission_page",
        "source_type"
    ]:
        if opp.get(k):
            parts.append(str(opp[k]))

    # Use fit hits, but do not trust converted prose too much.
    for k in ["fit_keyword_hits", "tags"]:
        for x in opp.get(k, []) or []:
            parts.append(str(x))

    return " ".join(parts).lower()

def classify(opp):
    text = raw_blob(opp)

    painting_hits = [t for t in PAINTING_TERMS if t in text]
    photography_hits = [t for t in PHOTOGRAPHY_TERMS if t in text]
    mixed_hits = [t for t in MIXED_TERMS if t in text]

    # Explicit known source overrides.
    title = str(opp.get("title") or opp.get("name") or "").lower()
    org = str(opp.get("organization") or "").lower()
    source = " ".join([title, org, str(opp.get("source_url") or "")]).lower()

    if any(x in source for x in ["hb gallery", "opa gallery", "pinpoint", "gallery iyn", "royalwatercolour", "jacksonsart", "mallgalleries"]):
        native = "painting"
    elif any(x in source for x in ["aperture", "photovogue", "lensculture", "der greif", "photographers' gallery", "futures-photography"]):
        native = "photography"
    elif any(x in source for x in ["utrecht", "tokyo art book fair", "mount zine", "printed matter", "offprint", "book and sons", "flotsam", "post", "self publish"]):
        native = "mixed"
    elif painting_hits and len(painting_hits) >= len(photography_hits):
        native = "painting"
    elif photography_hits and not painting_hits:
        native = "photography"
    elif mixed_hits:
        native = "mixed"
    else:
        native = "unknown"

    opp["native_medium"] = native
    opp["native_medium_hits"] = {
        "painting": painting_hits[:10],
        "photography": photography_hits[:10],
        "mixed": mixed_hits[:10],
    }

    return native

def main():
    opps = load(OPP_PATH, [])
    counts = {}

    for opp in opps:
        native = classify(opp)
        counts[native] = counts.get(native, 0) + 1

    save(OPP_PATH, opps)

    lines = ["# Source Medium Audit", "", "## Counts", ""]
    for k, v in sorted(counts.items()):
        lines.append(f"- {k}: {v}")

    lines += ["", "## Classified Opportunities", ""]
    for opp in opps:
        title = opp.get("title") or opp.get("name") or "Unknown"
        native = opp.get("native_medium")
        hits = opp.get("native_medium_hits", {})
        lines.append(f"- **{title}** — {native}")
        h = []
        for key, vals in hits.items():
            if vals:
                h.append(f"{key}: {', '.join(vals[:4])}")
        if h:
            lines.append(f"  - hits: {' | '.join(h)}")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT_PATH}")

if __name__ == "__main__":
    main()
