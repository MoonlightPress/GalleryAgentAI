
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


def _first(value):
    """Normalise a field that may be a string, list, or None to a string."""
    if isinstance(value, list):
        value = value[0] if value else ""
    return (value or "").strip()


def get_actionable_url(opp):
    """The opportunity's own URL — official_website or submission_page only.

    Discovery-trail fields (source_url / source_link) are deliberately NOT used:
    they point at how the opportunity was *found* (a search result, directory,
    or social profile), not at the opportunity itself. Verifying them produced
    the contradiction where an opp with no real URL was still marked "ok".
    """
    return _first(opp.get("official_website")) or _first(opp.get("submission_page"))


def get_url(opp):
    # Back-compat shim; prefers the actionable URL, falls back to discovery
    # trail only for callers that still want *some* link to display.
    return (
        get_actionable_url(opp)
        or _first(opp.get("source_url"))
        or _first(opp.get("source_link"))
    )


def decide_url_status(opp):
    """Pure, network-free pre-check of url_verification_status.

    Returns "no_url" when the opportunity has neither an official_website nor a
    submission_page — you cannot verify a URL that does not exist, so such an
    entry must never be "ok". Returns "has_url" when a real, checkable URL is
    present (the live check then refines that to ok/bad/error).
    """
    return "has_url" if get_actionable_url(opp) else "no_url"


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

        # An opportunity with no official_website and no submission_page has no
        # URL to verify. Do NOT fall back to discovery-trail URLs (source_url /
        # source_link) and live-check those — that produced "ok" for opps that
        # have no real URL at all. Mark "no_url" and skip the network call.
        if decide_url_status(opp) == "no_url":
            url, status, code, final = "", "no_url", 0, ""
        else:
            url = get_actionable_url(opp)
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
