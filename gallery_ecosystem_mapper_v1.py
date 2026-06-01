
import json
from pathlib import Path
from urllib.parse import urlparse

REFINED = Path("memory/gallery_candidates_refined.json")
RAW = Path("memory/gallery_candidates.json")
OUT_JSON = Path("memory/gallery_ecosystem.json")
OUT_REPORT = Path("reports/gallery_ecosystem.md")

DIRECT_OPP_TERMS = ["募集", "公募", "open call", "submission", "submit", "artist wanted", "recruiting", "application", "apply"]
EMERGING_TERMS = ["emerging", "若手", "新人", "登竜門", "new power", "grid next"]
LOCAL_HOODS = ["Koenji", "Nakano", "Kichijoji", "Shimokitazawa"]

def load(path, fallback):
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback

def get_candidates():
    refined = load(REFINED, None)
    if refined:
        return refined.get("candidates", [])
    return load(RAW, {"candidates": []}).get("candidates", [])

def clean_url(url):
    return str(url or "").strip()

def infer_submission(row):
    blob = f"{row.get('title','')} {row.get('url','')}".lower()
    return any(t.lower() in blob for t in DIRECT_OPP_TERMS) or row.get("has_direct_submission_signal", False)

def infer_artist_type(row):
    blob = f"{row.get('title','')} {row.get('url','')} {row.get('query','')}".lower()
    types = []
    if any(t.lower() in blob for t in EMERGING_TERMS):
        types.append("emerging artists")
    if "group" in blob or "グループ展" in blob:
        types.append("group exhibitions")
    if "contemporary" in blob or "現代" in blob:
        types.append("contemporary art")
    if "gallery cafe" in blob or "ギャラリーカフェ" in blob:
        types.append("gallery cafe")
    if not types:
        types.append("gallery / exhibition target")
    return types

def fit_notes(row):
    notes = []
    if infer_submission(row):
        notes.append("Has a direct submission/open-call signal.")
    if row.get("neighborhood") in LOCAL_HOODS:
        notes.append(f"Local-west Tokyo target: {row.get('neighborhood')}.")
    if "若手" in row.get("title", "") or "emerging" in row.get("title", "").lower():
        notes.append("Explicit emerging-artist signal.")
    if not notes:
        notes.append("Needs review of current/past artists before outreach.")
    return notes

def ecosystem_score(row):
    base = row.get("refined_score", row.get("score", 50))
    if infer_submission(row):
        base += 10
    if row.get("neighborhood") in LOCAL_HOODS:
        base += 5
    return max(0, min(100, round(base)))

def main():
    candidates = get_candidates()

    usable = []
    for r in candidates:
        bucket = r.get("refined_bucket", "")
        if bucket in {"reject_false_positive", "low_priority"}:
            continue
        if bucket == "reference_only" and r.get("refined_score", 0) < 70:
            continue

        item = {
            "name": r.get("title", ""),
            "url": clean_url(r.get("url", "")),
            "neighborhood": r.get("neighborhood", "Tokyo"),
            "submission_signal": infer_submission(r),
            "artist_type": infer_artist_type(r),
            "fit_notes": fit_notes(r),
            "score": ecosystem_score(r),
            "source_candidate_id": r.get("candidate_id"),
            "bucket": bucket or "raw_gallery_target",
            "status": "research_next",
        }
        usable.append(item)

    # De-dupe by name/url
    out = []
    seen = set()
    for item in sorted(usable, key=lambda x: x["score"], reverse=True):
        key = (item["name"].lower(), item["url"].lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(item)

    data = {
        "category": "galleries",
        "target_count": len(out),
        "direct_submission_count": len([x for x in out if x["submission_signal"]]),
        "local_target_count": len([x for x in out if x["neighborhood"] in LOCAL_HOODS]),
        "targets": out,
    }

    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Gallery Ecosystem",
        "",
        f"- Targets: {data['target_count']}",
        f"- Direct submission/open-call signals: {data['direct_submission_count']}",
        f"- Local-west Tokyo targets: {data['local_target_count']}",
        "",
    ]
    for item in out[:60]:
        lines.append(f"### {item['name']}")
        lines.append(f"- Score: {item['score']}")
        lines.append(f"- Neighborhood: {item['neighborhood']}")
        lines.append(f"- Submission signal: {item['submission_signal']}")
        lines.append(f"- Artist type: {', '.join(item['artist_type'])}")
        lines.append(f"- URL: {item['url']}")
        for n in item["fit_notes"]:
            lines.append(f"- Note: {n}")
        lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
