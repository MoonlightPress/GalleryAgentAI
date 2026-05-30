
import json, os
from pathlib import Path

PACK_PATH = "painting_source_pack.json"
OPP_PATH = "deploy_data/compact_opportunities.json"
REPORT_PATH = "reports/painting_discovery_report.md"

def load(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def key(item):
    return (str(item.get("title") or item.get("name") or "").lower().strip(), str(item.get("official_website") or item.get("source_url") or "").lower().strip())

def score_source(src):
    base = 7.0
    if src.get("priority") == "high":
        base += 1.2
    elif src.get("priority") == "medium":
        base += 0.5
    elif src.get("priority") == "low":
        base -= 0.8

    st = src.get("source_type", "")
    if "watercolor" in st or "open_exhibition" in st or "painting_prize" in st:
        base += 0.8
    if "illustration_gallery" in st:
        base += 0.7
    if "rental" in st or "low_barrier" in st:
        base -= 0.7
    return round(max(0, min(9.4, base)), 2)

def make_opp(src):
    name = src["name"]
    st = src.get("source_type", "")
    region = src.get("region", "")

    if "illustration_gallery" in st:
        why = "Native works-on-paper / illustration gallery context. Stronger medium fit than photography or photobook-only opportunities."
    elif "watercolor" in st:
        why = "Native watercolor context. Strong medium fit if requirements and dates are current."
    elif "open_exhibition" in st:
        why = "Open exhibition context for painting, drawing, or works on paper. Good candidate for direct verification."
    elif "painting_prize" in st:
        why = "Painting prize / works-on-paper friendly opportunity. Useful for credibility if submission terms fit."
    elif "open_call_index" in st:
        why = "Discovery source for painting, drawing, residency, and works-on-paper opportunities. Use as a recurring research feed."
    else:
        why = "Potential native painting or works-on-paper venue. Needs verification before recommendation."

    return {
        "title": name,
        "organization": name,
        "official_website": src.get("url", ""),
        "source_url": src.get("url", ""),
        "source_type": st,
        "region": region,
        "country": region,
        "native_medium": "painting",
        "translation_candidate": false if False else False,
        "overall_score": score_source(src),
        "differentiated_score": score_source(src),
        "watercolor_adjusted_score": score_source(src),
        "truth_aligned_score": score_source(src),
        "source_purity_score": score_source(src),
        "verification_bucket": "research_needed",
        "verification_status": "partial",
        "recommendation_visibility": "show",
        "watercolor_fit_hits": ["painting", "works on paper"],
        "why_this_fits_short": why,
        "one_sentence": f"{name} is a {st.replace('_',' ')} source in {region} for watercolor / works on paper research.",
        "quick_action": "Verify current submission, exhibition, or contact details before recommending.",
        "manual_review_needed": True,
        "import_status": "painting_discovery_seed"
    }

def main():
    pack = load(PACK_PATH, {"painting_sources": []})
    opps = load(OPP_PATH, [])

    existing = {key(o) for o in opps}
    added = []
    skipped = 0

    for src in pack.get("painting_sources", []):
        opp = make_opp(src)
        if key(opp) in existing:
            skipped += 1
            continue
        opps.append(opp)
        existing.add(key(opp))
        added.append(opp)

    opps.sort(key=lambda x: float(x.get("source_purity_score", x.get("watercolor_adjusted_score", x.get("overall_score", 0))) or 0), reverse=True)
    save(OPP_PATH, opps)

    lines = ["# Painting Discovery Report", "", f"Added native painting sources: {len(added)}", f"Skipped existing: {skipped}", f"Total opportunities: {len(opps)}", "", "## Added", ""]
    for opp in added:
        lines.append(f"- **{opp['title']}** — {opp['source_purity_score']} — {opp['why_this_fits_short']}")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")
    print(f"Added painting opportunities: {len(added)}")
    print(f"Total opportunities: {len(opps)}")
    print(f"Wrote {REPORT_PATH}")

if __name__ == "__main__":
    main()
