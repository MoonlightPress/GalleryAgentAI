
import json
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

SRC = Path("memory/gallery_candidates.json")
OUT_JSON = Path("memory/gallery_candidates_refined.json")
OUT_REPORT = Path("reports/gallery_candidates_refined.md")

SURNAME_FALSE_POSITIVES = [
    "daisuke nakano", "tomoya nakano", "akari nakano", "masataka nakano",
    "tomoko nakano", "kana nakano", "nakano studio", "nakano portfolio"
]

DIRECTORY_NOISE = [
    "time out", "tokyo art beat", "ocula", "1 cubic meter", "up magazine",
    "thestandardjapan", "artsy", "artnet", "tripadvisor", "guide"
]

STRONG_SIGNALS = [
    "募集", "公募", "open call", "submission", "submit", "recruiting",
    "artist wanted", "emerging", "若手", "参加アーティスト", "作家募集",
    "application", "apply"
]

GALLERY_SIGNALS = [
    "gallery", "ギャラリー", "artist-run", "contemporary", "exhibition",
    "showcase", "art space", "画廊"
]

def load(path, fallback):
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback

def unwrap(url):
    if not url:
        return ""
    if url.startswith("//"):
        url = "https:" + url
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    if "uddg" in qs and qs["uddg"]:
        return unquote(qs["uddg"][0])
    return url

def is_false_positive(row):
    blob = f"{row.get('title','')} {row.get('url','')} {row.get('query','')}".lower()
    if any(x in blob for x in SURNAME_FALSE_POSITIVES):
        return True
    # If query matched "Nakano gallery" but result is an artist named Nakano, reject.
    if "nakano gallery artist" in blob and any(x in blob for x in ["portfolio", "artist information", "home | tomoya"]):
        return True
    return False

def is_directory(row):
    blob = f"{row.get('title','')} {row.get('url','')}".lower()
    return any(x in blob for x in DIRECTORY_NOISE)

def refined_score(row):
    title = row.get("title", "")
    url = unwrap(row.get("url", ""))
    blob = f"{title} {url} {row.get('query','')}".lower()
    score = row.get("score", 40)

    if any(s.lower() in blob for s in STRONG_SIGNALS):
        score += 20
    if any(s.lower() in blob for s in GALLERY_SIGNALS):
        score += 10
    if is_directory(row):
        score -= 20
    if is_false_positive(row):
        score -= 60
    if any(x in blob for x in ["prtimes", "atpress", "press release"]):
        score -= 10

    return max(0, min(100, score))

def classify(row):
    score = refined_score(row)
    blob = f"{row.get('title','')} {unwrap(row.get('url',''))}".lower()

    if is_false_positive(row):
        bucket = "reject_false_positive"
    elif score >= 85 and any(s.lower() in blob for s in STRONG_SIGNALS):
        bucket = "direct_opportunity"
    elif score >= 65:
        bucket = "gallery_target"
    elif is_directory(row):
        bucket = "reference_only"
    else:
        bucket = "low_priority"

    out = dict(row)
    out["url"] = unwrap(row.get("url", ""))
    out["refined_score"] = score
    out["refined_bucket"] = bucket
    out["has_direct_submission_signal"] = any(s.lower() in blob for s in STRONG_SIGNALS)
    return out

def main():
    data = load(SRC, {"candidates": []})
    candidates = [classify(c) for c in data.get("candidates", [])]
    candidates.sort(key=lambda x: x["refined_score"], reverse=True)

    buckets = {}
    for c in candidates:
        buckets.setdefault(c["refined_bucket"], []).append(c)

    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    OUT_JSON.write_text(json.dumps({
        "source_count": len(candidates),
        "buckets": buckets,
        "candidates": candidates,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Gallery Candidates Refined", "", f"- Source candidates: {len(candidates)}", ""]
    for bucket in ["direct_opportunity", "gallery_target", "reference_only", "low_priority", "reject_false_positive"]:
        rows = buckets.get(bucket, [])
        lines += [f"## {bucket} ({len(rows)})", ""]
        for r in rows[:50]:
            lines.append(f"### {r.get('candidate_id')} — {r.get('title')}")
            lines.append(f"- Refined score: {r.get('refined_score')}")
            lines.append(f"- Neighborhood: {r.get('neighborhood')}")
            lines.append(f"- URL: {r.get('url')}")
            lines.append(f"- Direct signal: {r.get('has_direct_submission_signal')}")
            lines.append("")
        lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
