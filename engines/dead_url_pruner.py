"""
dead_url_pruner.py

Pipeline step: marks entries with confirmed dead URLs (HTTP 404, url_verification_status=bad)
as recommendation_visibility=hidden so they don't surface in the UI.

Replaces the previous pattern of manually setting recommendation_visibility on individual entries.
Idempotent — safe to run repeatedly.
"""
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT     = Path(__file__).parent.parent
OPP_PATH = ROOT / "deploy_data" / "compact_opportunities.json"

DEAD_STATUS_CODES  = {404, 410}
DEAD_URL_STATUSES  = {"bad"}


def main():
    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))

    hidden = 0
    restored = 0

    for opp in opps:
        status_code = opp.get("url_status_code")
        url_status  = opp.get("url_verification_status", "")
        current_vis = opp.get("recommendation_visibility", "show")

        try:
            code = int(status_code) if status_code is not None else None
        except (ValueError, TypeError):
            code = None

        is_dead = (code in DEAD_STATUS_CODES) or (url_status in DEAD_URL_STATUSES)

        if is_dead and current_vis != "hidden":
            opp["recommendation_visibility"] = "hidden"
            name = opp.get("name") or opp.get("title") or "?"
            print(f"  HIDDEN: {name[:60]} (code={code}, status={url_status})")
            hidden += 1
        elif not is_dead and current_vis == "hidden" and opp.get("url_verification_status") == "ok":
            # Restore entries that were hidden for URL issues but now verified ok
            opp["recommendation_visibility"] = "show"
            name = opp.get("name") or opp.get("title") or "?"
            print(f"  RESTORED: {name[:60]}")
            restored += 1

    OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDone. {hidden} entries hidden, {restored} restored.")


if __name__ == "__main__":
    main()
