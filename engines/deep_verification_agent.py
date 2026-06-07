"""
deep_verification_agent.py

For opportunities that have url_ok but are missing contact_verified,
fees_verified, or submission_process_known — fetches the venue page and
uses Claude API to extract the missing details.

Targets "partial" (score 3-4) and "research_needed" (score <3) opps.
After running, re-run verification_report_engine.py to recompute statuses.

Usage:
    python engines/deep_verification_agent.py
    python engines/deep_verification_agent.py --limit 50
    python engines/deep_verification_agent.py --all
"""
import sys
import json
import os
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

OPP_PATH = Path("deploy_data/compact_opportunities.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
}

MAX_BODY = 6000   # chars of page body to send to Claude


def fetch_page(url: str, timeout: int = 10) -> str:
    """Fetch page body, strip CSS/JS/HTML tags, return truncated readable text."""
    if not url or not url.startswith(("http://", "https://")):
        return ""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            # Detect charset from response headers or meta tag
            charset = "utf-8"
            ct = resp.headers.get("Content-Type", "")
            if "charset=" in ct.lower():
                charset = ct.lower().split("charset=")[-1].split(";")[0].strip()
            # Try detected charset first, fall back to utf-8 then latin-1
            for enc in (charset, "utf-8", "shift_jis", "latin-1"):
                try:
                    text = raw.decode(enc)
                    break
                except (UnicodeDecodeError, LookupError):
                    continue
            else:
                text = raw.decode("utf-8", errors="replace")
            import re
            # Remove script and style blocks first (they dominate stripped output)
            text = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
            # Remove remaining HTML tags
            text = re.sub(r"<[^>]+>", " ", text)
            # Decode HTML entities
            text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#39;", "'").replace("&nbsp;", " ")
            text = re.sub(r"\s{3,}", "\n", text)
            return text.strip()[:MAX_BODY]
    except Exception:
        return ""


def ask_claude(client, page_text: str, opp_name: str, category: str) -> dict:
    """Use Claude to extract contact/fees/process from page text."""
    prompt = f"""You are reviewing a venue page for a Tokyo-based artist researching exhibition/consignment opportunities.

Venue: {opp_name}
Category: {category}

Page content (truncated):
---
{page_text or "(page not fetchable)"}
---

Answer ONLY with a JSON object containing these fields:
{{
  "contact_email": "<email address found, or null>",
  "has_contact_info": true/false,
  "fees_described": true/false,
  "fees_notes": "<brief description of any fees/commission, or null>",
  "submission_process_described": true/false,
  "process_notes": "<brief description of how to submit/apply/consign, or null>",
  "confidence": "high" | "medium" | "low"
}}

Rules:
- has_contact_info = true if any email, phone, or contact form is present
- fees_described = true if the page mentions any entry fee, commission rate, or explicitly says 'no fee'
- submission_process_described = true if the page describes how to submit work, apply, or inquire about consignment
- Be conservative: only mark true if the page actually contains this information

Output JSON only, no commentary.
"""
    import anthropic
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    text = msg.content[0].text.strip()
    # Parse JSON
    import re
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        return json.loads(m.group(0))
    return {}


def needs_deep_check(opp: dict) -> bool:
    """True if the opp has url_ok but is missing at least one key verification field."""
    if opp.get("url_verification_status") != "ok":
        return False
    missing = (
        not opp.get("contact_verified")
        or not opp.get("fees_verified")
        or not opp.get("submission_process_known")
    )
    return missing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    # Load API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        except ImportError:
            pass
    if not api_key:
        env_path = Path(".env")
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))

    # Target: partial or research_needed, url_ok, missing at least one field
    targets = [o for o in opps if needs_deep_check(o)]
    # Prioritize "partial" over "research_needed" — more likely to have usable pages
    targets.sort(key=lambda o: (
        0 if o.get("verification_status") == "partial" else 1,
        -float(o.get("overall_score") or 0),
    ))

    limit = len(targets) if args.all else args.limit
    targets = targets[:limit]

    print(f"Deep verification: {len(targets)} opportunities with url_ok but missing contact/fees/process")

    changed = 0
    errors = 0

    for i, opp in enumerate(targets, 1):
        name = opp.get("name") or opp.get("title") or "?"
        site = str(opp.get("official_website") or opp.get("submission_page") or "")
        if isinstance(site, list):
            site = site[0] if site else ""

        print(f"[{i:3d}/{len(targets)}] {name[:55]:<55}", end=" ", flush=True)

        page = fetch_page(site)
        if not page:
            print("no_page")
            errors += 1
            time.sleep(0.3)
            continue

        try:
            result = ask_claude(client, page, name, opp.get("category", ""))
        except Exception as e:
            print(f"claude_error: {e}")
            errors += 1
            time.sleep(0.5)
            continue

        updated = False

        if result.get("has_contact_info") and not opp.get("contact_verified"):
            opp["contact_verified"] = True
            if result.get("contact_email"):
                opp["contact_email_verified"] = result["contact_email"]
            updated = True

        if result.get("fees_described") and not opp.get("fees_verified"):
            opp["fees_verified"] = True
            if result.get("fees_notes"):
                opp["fees_notes"] = result["fees_notes"]
            updated = True

        if result.get("submission_process_described") and not opp.get("submission_process_known"):
            opp["submission_process_known"] = True
            if result.get("process_notes"):
                opp["submission_process_notes"] = result["process_notes"]
            updated = True

        if updated:
            changed += 1

        flags = []
        if result.get("has_contact_info"): flags.append("contact")
        if result.get("fees_described"): flags.append("fees")
        if result.get("submission_process_described"): flags.append("process")
        conf = result.get("confidence", "?")
        print(f"{'ok' if flags else 'nothing'} [{','.join(flags) or 'none'}] conf={conf}")

        time.sleep(0.4)

    # Write back
    OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDeep verification complete: {changed}/{len(targets)} updated, {errors} errors/no-page")
    print("Run verification_report_engine.py to recompute verification_status fields.")


if __name__ == "__main__":
    main()
