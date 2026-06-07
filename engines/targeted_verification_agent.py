"""
targeted_verification_agent.py

Fetches the top N IBM-eligible opportunities by score, performs a HEAD (then
GET fallback) request against official_website and submission_page, and writes
url_verification_status, deadline_verified, and last_verified back to
deploy_data/compact_opportunities.json.

Run standalone:
    python engines/targeted_verification_agent.py

Flags:
    --limit N   Number of opportunities to verify (default 50)
    --all       Verify all non-rejected opportunities
    --timeout N Request timeout in seconds (default 8)
"""
import sys
import json
import time
import hashlib
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

OPP_PATH    = Path("deploy_data/compact_opportunities.json")
REPORT_PATH = Path("reports/targeted_verification_report.md")

EXCLUDED_BUCKETS = {"reject", "low_priority"}

_DEADLINE_PLACEHOLDERS = frozenset({
    "", "unknown", "n/a", "tbd", "check current schedule",
    "varies", "check site", "see website", "none", "check source",
})

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
}


def _opp_id(opp: dict) -> str:
    raw = opp.get("id") or opp.get("title") or opp.get("name") or ""
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def _overall_score(opp: dict) -> float:
    return float(
        opp.get("overall_score")
        or opp.get("differentiated_score")
        or opp.get("watercolor_adjusted_score")
        or opp.get("dna_adjusted_score")
        or 0
    )


def _deadline_is_real(opp: dict) -> bool:
    d = str(opp.get("deadline", "")).strip().lower()
    return d not in _DEADLINE_PLACEHOLDERS and len(d) > 4


def check_url(url: str, timeout: int) -> tuple[str, int]:
    """Return (status, http_code). status: 'ok' | 'redirect' | 'error' | 'timeout' | 'skip'"""
    if not url or not url.startswith(("http://", "https://")):
        return "skip", 0

    req = urllib.request.Request(url, headers=HEADERS, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = resp.getcode()
            if 200 <= code < 300:
                return "ok", code
            if 300 <= code < 400:
                return "redirect", code
            return "error", code
    except urllib.error.HTTPError as e:
        # HEAD rejected — try GET (some servers refuse HEAD)
        if e.code in (405, 403):
            req2 = urllib.request.Request(url, headers=HEADERS)
            try:
                with urllib.request.urlopen(req2, timeout=timeout) as resp2:
                    code2 = resp2.getcode()
                    if 200 <= code2 < 300:
                        return "ok", code2
                    if 300 <= code2 < 400:
                        return "redirect", code2
                    return "error", code2
            except Exception:
                return "error", e.code
        return "error", e.code
    except urllib.error.URLError as e:
        if "timed out" in str(e).lower():
            return "timeout", 0
        return "error", 0
    except TimeoutError:
        return "timeout", 0
    except Exception:
        return "error", 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50, help="Max opportunities to verify")
    parser.add_argument("--all", action="store_true", help="Verify all non-rejected")
    parser.add_argument("--timeout", type=int, default=8, help="Request timeout seconds")
    args = parser.parse_args()

    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))

    candidates = [
        o for o in opps
        if o.get("exclusive_primary_bucket") not in EXCLUDED_BUCKETS
        and o.get("status") != "permanently_closed"
    ]
    candidates.sort(key=_overall_score, reverse=True)

    limit = len(candidates) if args.all else args.limit
    targets = candidates[:limit]
    by_id = {_opp_id(o): o for o in opps}

    print(f"Verifying {len(targets)} opportunities (timeout={args.timeout}s)…")
    print()

    now_ts = datetime.now(timezone.utc).isoformat()
    results = []

    for i, opp in enumerate(targets, 1):
        name = opp.get("name") or opp.get("title") or "?"
        site = opp.get("official_website", "")
        sub  = opp.get("submission_page", "")

        print(f"[{i:3d}/{len(targets)}] {name[:55]:<55}", end=" ", flush=True)

        # Check official website
        site_status, site_code = check_url(site, args.timeout)

        # Check submission page if distinct from site
        if sub and sub.rstrip("/") != site.rstrip("/"):
            sub_status, sub_code = check_url(sub, args.timeout)
        else:
            sub_status, sub_code = site_status, site_code

        # Derive url_verification_status
        if site_status == "ok" or sub_status == "ok":
            url_status = "ok"
        elif site_status == "skip" and sub_status == "skip":
            url_status = "no_url"
        elif "timeout" in (site_status, sub_status):
            url_status = "timeout"
        else:
            url_status = "error"

        # Deadline
        dl_verified = _deadline_is_real(opp)

        print(f"site={site_status}({site_code}) sub={sub_status}({sub_code})  url={url_status}  dl={'✓' if dl_verified else '✗'}")

        opp_id = _opp_id(opp)
        by_id[opp_id]["url_verification_status"]  = url_status
        by_id[opp_id]["site_http_code"]            = site_code
        by_id[opp_id]["deadline_verified"]         = dl_verified
        by_id[opp_id]["last_verified"]             = now_ts

        results.append({
            "name":        name,
            "url_status":  url_status,
            "site_code":   site_code,
            "sub_code":    sub_code,
            "dl_verified": dl_verified,
            "site":        site[:80],
        })

        # Polite crawl delay
        time.sleep(0.5)

    # Write back
    OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {OPP_PATH}")

    # Report
    ok      = sum(1 for r in results if r["url_status"] == "ok")
    errors  = sum(1 for r in results if r["url_status"] == "error")
    timeouts= sum(1 for r in results if r["url_status"] == "timeout")
    no_url  = sum(1 for r in results if r["url_status"] == "no_url")
    dl_ok   = sum(1 for r in results if r["dl_verified"])

    report_lines = [
        "# Targeted Verification Report",
        f"\nRun: {now_ts}  |  Checked: {len(results)}  |  Timeout: {args.timeout}s",
        "",
        "## Summary",
        "",
        f"| Status | Count |",
        f"|--------|-------|",
        f"| ✓ URL ok | {ok} |",
        f"| ✗ Error / unreachable | {errors} |",
        f"| ⏱ Timeout | {timeouts} |",
        f"| — No URL | {no_url} |",
        f"| 📅 Deadline confirmed | {dl_ok} / {len(results)} |",
        "",
        "## Results",
        "",
        "| # | Name | URL status | Code | Deadline |",
        "|---|------|-----------|------|----------|",
    ]
    for i, r in enumerate(results, 1):
        icon = {"ok": "✓", "error": "✗", "timeout": "⏱", "no_url": "—"}.get(r["url_status"], "?")
        dl   = "✓" if r["dl_verified"] else "✗"
        name = r["name"][:45].replace("|", "｜")
        report_lines.append(f"| {i} | {name} | {icon} {r['url_status']} | {r['site_code']} | {dl} |")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Report: {REPORT_PATH}")
    print(f"\nResults: {ok} ok · {errors} errors · {timeouts} timeouts · {no_url} no-url · {dl_ok} deadlines confirmed")


if __name__ == "__main__":
    main()
