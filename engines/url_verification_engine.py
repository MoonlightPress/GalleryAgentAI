
import json
import os
from pathlib import Path

import requests


OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/url_verification_report.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def get_url(opp):
    return (
        opp.get("source_url")
        or opp.get("source_link")
        or opp.get("official_website")
        or opp.get("submission_page")
        or ""
    )


def check(url):
    if not url:
        return "missing", 0, ""

    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0 MochiVerifier/0.1"})
        return "ok" if r.status_code < 400 else "bad", r.status_code, r.url
    except Exception as e:
        return "error", 0, str(e)[:160]


def main():
    opps = load_json(OPP_PATH, [])

    lines = [
        "# URL Verification Report",
        "",
    ]

    for opp in opps:
        title = opp.get("title") or opp.get("name") or "Unknown"
        url = get_url(opp)
        status, code, final = check(url)

        opp["url_verification_status"] = status
        opp["url_status_code"] = code
        opp["url_final"] = final

        if status != "ok":
            lines.append(f"## {title}")
            lines.append(f"- URL: {url or 'missing'}")
            lines.append(f"- Status: {status}")
            lines.append(f"- Code: {code}")
            lines.append(f"- Detail: {final}")
            lines.append("")

    with open(OPP_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, indent=2, ensure_ascii=False)

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
